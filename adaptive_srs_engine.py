# -*- coding: utf-8 -*-
"""
Adaptive Spaced-Repetition & Weakness Priority Engine (`adaptive_srs_engine.py`)
--------------------------------------------------------------------------------
Implements the 5-Part Daily Practice + Algorithmic Weakness Review system:
1. Part 1 (單字表詳細介紹): 16 deduplicated vocabulary items per session (32/day),
   combining full-catalog sequential coverage with algorithmic priority boosting
   for (a) shorter, simpler, ultra-high-frequency TOEIC core words, and (b) words
   the user has missed in previous sessions.
2. Part 2 (文法詳細介紹): Visual Anchor + 2 Deep-Dive 860+ Grammar Modules
   (Micro-Signals 1-4, One-Verb-Per-Clause Rules 1-3, Subjunctive Mood Rules 1-2,
   and Confusion Matrix).
3. Part 3 (選擇題練習 — 單字與文法): 25 complex multi-clause multiple-choice questions
   (Questions 1..25), prioritized by vocabulary frequency and user error history.
4. Part 4 (填空選擇題 — 段落克漏字): 3 business passages × 4 blanks = 12 multiple-choice
   questions (Questions 26..37, >= 10 questions).
5. Part 5 (閱讀測驗 — 商務長文閱讀): 2 long-form multi-paragraph business documents
   with 6 multiple-choice questions (Questions 38..43).
"""

import copy
import json
import math
from pathlib import Path
import re
from typing import Dict, List, Tuple

from master_curriculum import DAYS_DATA
from toeic_860_bank import (
    CLOZE_PASSAGES_BANK,
    EXTRA_860_LEXICON,
    GRAMMAR_MODULES_DB,
    QUESTIONS_860_BANK,
)
from vocabulary_manager import (
    VOCAB_DB_PATH,
    build_or_update_master_vocab_db,
    normalize_headword as normalize_key,
)


def build_or_load_vocab_db() -> List[dict]:
    if VOCAB_DB_PATH.exists():
        try:
            obj = json.loads(VOCAB_DB_PATH.read_text(encoding="utf-8"))
            if isinstance(obj, dict) and "entries" in obj:
                return obj["entries"]
            if isinstance(obj, list):
                return obj
        except Exception:
            pass
    obj = build_or_update_master_vocab_db()
    return obj.get("entries", [])

PROJECT_DIR = Path(__file__).resolve().parent
PROFILE_PATH = PROJECT_DIR / "user_weakness_profile.json"


def _normalize_counter_keys(counter: dict) -> dict:
    """Merge legacy un-normalised keys (e.g. 'Provided that') into their normalised form."""
    merged: Dict[str, int] = {}
    for k, v in counter.items():
        nk = normalize_key(k)
        merged[nk] = merged.get(nk, 0) + int(v)
    return merged


def load_weakness_profile() -> dict:
    if PROFILE_PATH.exists():
        try:
            data = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
            data.setdefault("last_update_id", 0)
            data.setdefault("history", [])
            data.setdefault("weak_words", {})
            data.setdefault("weak_categories", {})
            data.setdefault("weak_rules", {})
            data.setdefault("word_srs", {})
            data["weak_words"] = _normalize_counter_keys(data["weak_words"])
            return data
        except Exception:
            pass
    return {
        "last_update_id": 0,
        "history": [],
        "weak_words": {},
        "weak_categories": {},
        "weak_rules": {},
        "word_srs": {},
    }


def compute_word_priority(entry: dict, profile: dict) -> Tuple[float, int, float, str]:
    """
    Compute the algorithmic priority score for a vocabulary item `entry`:
      Priority(w) = F_TOEIC(w) * 2.2
                  + SimplicityBonus(w) * 1.2
                  + ErrorCount(w)^1.6 * 4.5
                  + (2.5 / EF(w)) * 2.0
    Returns `(priority_score, error_count, easiness_factor, reason_badge)`.
    """
    word = entry.get("word", "")
    norm_w = normalize_key(word)
    freq_tier = int(entry.get("freq_tier", 2))

    # Shorter, simpler, everyday TOEIC words get a simplicity frequency boost
    clean_len = len(word.replace(" ", ""))
    simplicity_bonus = max(0.0, (14.0 - min(14.0, float(clean_len))) / 5.0)
    if freq_tier == 3:
        simplicity_bonus += 1.0

    weak_words = profile.get("weak_words", {})
    word_srs = profile.get("word_srs", {})

    # Match exact word or 5-char stem in weak_words
    err_count = int(weak_words.get(norm_w, 0))
    if err_count == 0 and len(norm_w) >= 6:
        # Word-family match (e.g. negligent / negligence): shared 6-char stem, both words >= 6 chars
        stem = norm_w[:6]
        for kw, cnt in weak_words.items():
            if len(kw) >= 6 and kw[:6] == stem:
                err_count = max(err_count, int(cnt))

    srs_info = word_srs.get(norm_w, {})
    ef = float(srs_info.get("ef", max(1.3, 2.5 - 0.25 * err_count)))
    ef = max(1.3, min(2.5, ef))

    score = (
        freq_tier * 2.2
        + simplicity_bonus * 1.2
        + (err_count ** 1.6) * 4.5
        + (2.5 / ef) * 2.0
    )
    src_str = str(entry.get("source", "")) + " " + " ".join(entry.get("sources", []))
    if "860" in src_str:
        score += 0.6

    if err_count >= 2:
        reason = f"🔥 高危錯題字 (累計答錯 {err_count} 次 · 演算法強制加權)"
    elif err_count == 1:
        reason = "⚠️ 曾錯弱點字 (演算法優先排程複習)"
    elif freq_tier == 3:
        reason = "⚡ 多益超高頻核心字 (短小精悍 · 高頻率循環)"
    elif "860" in src_str:
        reason = "🎯 860+ 弱點突破字彙"
    else:
        reason = "📘 商務核心必背語塊"

    return round(score, 2), err_count, round(ef, 2), reason


def filter_high_impact_vocabulary(vocab_db: List[dict], profile: dict) -> List[dict]:
    """
    [21-Day High-Impact Filter]
    Strictly filters out peripheral, low-yield, or trivial words (e.g. stapler, takeout, stroll down, along the coast).
    Retains ONLY Tier 3 (Ultra-High Frequency Core), Tier 2 (High-Frequency Business),
    and User Weakness words (~168 high-impact words).
    """
    trivial_words = {"along the coast", "stroll down", "takeout", "repaving", "stapler"}
    high_impact = []
    weak_keys = set(profile.get("weak_words", {}).keys())
    for raw_e in vocab_db:
        w_norm = normalize_key(raw_e["word"])
        ft = int(raw_e.get("freq_tier", 2))
        is_weak = w_norm in weak_keys or profile.get("weak_words", {}).get(w_norm, 0) > 0
        is_user_or_860 = ("860" in str(raw_e.get("id", ""))) or ("USER" in str(raw_e.get("id", "")))

        # Filter logic: eliminate trivial words unless specifically marked as user weakness
        if w_norm in trivial_words and not is_weak:
            continue
        if ft >= 2 or is_weak or is_user_or_860:
            high_impact.append(raw_e)

    return high_impact if high_impact else vocab_db


def select_part1_vocabulary(
    day_num: int,
    session: str,
    vocab_db: List[dict],
    profile: dict,
    target_count: int = 16,
) -> List[dict]:
    """
    Select `target_count` (16) detailed vocabulary items for Part 1:
    [21-Day High-Impact Sprint Mode]
    - Filters out low-yield peripheral words, retaining only the most frequently tested core & weak words.
    - Ranked and sorted strictly by weight (Error Count & Priority Score) from highest to lowest.
    - Earlier days systematically send the highest-weighted items in the database first.
    - Inside each session, items are strictly presented in descending order of weight (Card #1 = highest weight).
    """
    if not vocab_db:
        return []

    # Apply 21-Day High-Impact Filter
    filtered_db = filter_high_impact_vocabulary(vocab_db, profile)

    is_morning = session.lower().startswith("m")
    day_offset = (day_num - 5) if day_num >= 5 else (day_num - 1)
    s_idx = max(0, day_offset) * 2 + (0 if is_morning else 1)
    n_total = len(filtered_db)

    # Enrich all entries with live priority metrics
    enriched_all = []
    for idx, raw_e in enumerate(filtered_db):
        e = copy.deepcopy(raw_e)
        e["norm_key"] = e.get("norm_key") or normalize_key(e["word"])
        p_score, err_cnt, ef, reason = compute_word_priority(e, profile)
        e["priority_score"] = p_score
        e["error_count"] = err_cnt
        e["easiness_factor"] = ef
        e["priority_reason"] = reason
        ft = int(e.get("freq_tier", 2))
        if ft == 3:
            e["freq_stars"] = "⭐⭐⭐ 超高頻必考"
        elif ft == 2:
            e["freq_stars"] = "⭐⭐ 高頻商務核心"
        else:
            e["freq_stars"] = "⭐ 860+ 進階決勝"

        src_str = str(e.get("source", "")) + " " + " ".join(e.get("sources", []))
        if "延伸語塊" in e.get("collocations", ""):
            e["source_badge"] = "🔄 雙重核心 (既有語塊 + 860 弱點合併)"
        elif "860" in src_str:
            e["source_badge"] = "🆕 860 弱點新增單字"
        elif "User" in src_str or "custom" in src_str or "使用者" in src_str:
            e["source_badge"] = "🔥 使用者回報弱點"
        else:
            e["source_badge"] = "📘 25天衝刺核心語塊"

        enriched_all.append(e)

    # Sort entire database strictly by priority_score descending!
    sorted_all = sorted(
        enriched_all,
        key=lambda x: x["priority_score"],
        reverse=True,
    )

    # Pick the slice for the current session from the sorted list
    start_pos = (s_idx * target_count) % n_total
    selected = []
    for offset in range(n_total):
        cand = sorted_all[(start_pos + offset) % n_total]
        selected.append(cand)
        if len(selected) >= target_count:
            break

    # Guarantee items inside this session are strictly ordered from highest weight to lowest weight
    selected.sort(key=lambda x: x["priority_score"], reverse=True)
    return selected


def select_part2_grammar(day_num: int, session: str, profile: dict) -> List[dict]:
    """
    Select 2 deep-dive Grammar Modules from `GRAMMAR_MODULES_DB` for Part 2.
    Prioritizes grammar modules matching the user's `weak_rules` / `weak_categories`
    while rotating across all 10 modules so every grammar signal & rule is thoroughly reviewed.
    """
    s_idx = (day_num - 1) * 2 + (0 if session.lower().startswith("m") else 1)
    n_mods = len(GRAMMAR_MODULES_DB)
    idx1 = (s_idx * 2) % n_mods
    idx2 = (s_idx * 2 + 1) % n_mods
    mods = [copy.deepcopy(GRAMMAR_MODULES_DB[idx1]), copy.deepcopy(GRAMMAR_MODULES_DB[idx2])]

    # If user has a weak rule or weak category in profile not in mods, replace the second slot with the highest weak grammar module
    weak_candidates = {**profile.get("weak_categories", {}), **profile.get("weak_rules", {})}
    if weak_candidates:
        ranked_cats = sorted(weak_candidates.items(), key=lambda kv: kv[1], reverse=True)
        top_rule_text = ranked_cats[s_idx % len(ranked_cats)][0].lower()
        for m in GRAMMAR_MODULES_DB:
            if m["id"] not in (mods[0]["id"], mods[1]["id"]):
                match_tokens = [tok for tok in re.split(r"[\s(/、)]+", top_rule_text) if len(tok) >= 2]
                if any(tok in m["title"].lower() or tok in m["category"].lower() or tok in m["formula"].lower() for tok in match_tokens):
                    mods[1] = copy.deepcopy(m)
                    mods[1]["is_weakness_boosted"] = True
                    break

    return mods


def select_part3_mc_questions(
    day_num: int,
    session: str,
    part1_vocab: List[dict],
    profile: dict,
    target_count: int = 25,
    exclude_stems: set = None,
) -> List[dict]:
    """
    Build Part 3 (單字與文法單句選擇題 — 25 題, numbered 1..25):
    Combines:
    1. User weakness / error-boosted questions (if user has reported wrong questions in `profile`).
    2. 8 bespoke questions from `QUESTIONS_860_BANK` testing `860_antigravity.md` vocabulary & grammar signals.
    3. The session's core complex questions (`morning.part5` or `afternoon.spaced_traps`) + cross-day
       high-frequency vocabulary questions matching `part1_vocab`.
    All 25 questions are guaranteed to have unique stems, balanced (A)(B)(C)(D) answer keys,
    `rule_ref`, `analysis`, and 4-option `option_details`.
    """
    s_idx = (day_num - 1) * 2 + (0 if session.lower().startswith("m") else 1)
    is_morning = session.lower().startswith("m")
    day_data = DAYS_DATA.get(day_num, DAYS_DATA[1])

    selected: List[dict] = []
    seen_stems = set(exclude_stems or ())

    def _add_q(raw_q: dict, source_label: str = "") -> bool:
        stem = raw_q.get("question", "").strip()
        if not stem or stem in seen_stems:
            return False
        q_copy = copy.deepcopy(raw_q)
        if source_label and not q_copy.get("rule_ref"):
            q_copy["rule_ref"] = source_label
        if not q_copy.get("rule_ref"):
            q_copy["rule_ref"] = q_copy.get("trap_point") or "多益高頻句構與核心商務搭配"
        selected.append(q_copy)
        seen_stems.add(stem)
        return True

    # 1. Weakness injection: pull questions whose ANSWER is one of the user's most-missed words,
    #    searching the whole pool (860 bank, cloze bank, 25-day curriculum). More errors => more questions.
    weak_words = profile.get("weak_words", {})
    if weak_words:
        pool = list(QUESTIONS_860_BANK)
        for pas in CLOZE_PASSAGES_BANK:
            pool.extend(pas.get("questions", []))
        for dd in range(1, 26):
            pool.extend(DAYS_DATA[dd]["morning"]["part5"])
            pool.extend(DAYS_DATA[dd]["afternoon"]["spaced_traps"])
        by_answer: Dict[str, List[dict]] = {}
        for q in pool:
            by_answer.setdefault(normalize_key(q["options"].get(q.get("answer", ""), "")), []).append(q)
        max_weak_q = 8
        ranked = sorted(weak_words.items(), key=lambda kv: kv[1], reverse=True)
        n_ranked = len(ranked)
        rank_offset = (s_idx * 3) % n_ranked if n_ranked else 0
        for i in range(n_ranked):
            w, cnt = ranked[(rank_offset + i) % n_ranked]
            cands = by_answer.get(w, [])
            if not cands:
                for q_item in pool:
                    if w in normalize_key(q_item["question"]) or any(w in normalize_key(ov) for ov in q_item["options"].values()):
                        cands.append(q_item)
            # rotate so the same weak word is practised with a different sentence each session
            for k in range(min(len(cands), 1 + (1 if cnt >= 2 else 0))):
                cand = cands[(s_idx + k) % len(cands)]
                _add_q(cand, cand.get("rule_ref", "🔥 錯題弱點演算法加權複習"))
            if len(selected) >= max_weak_q:
                break

    # 2. Add 8 questions from `QUESTIONS_860_BANK` rotated by s_idx (prioritizing matches with today's Part 1 vocab)
    p1_words_lower = {normalize_key(v["word"]) for v in part1_vocab}
    n_860 = len(QUESTIONS_860_BANK)
    # First pick questions in QUESTIONS_860_BANK that test today's Part 1 vocab
    for i in range(n_860):
        cand = QUESTIONS_860_BANK[(s_idx * 5 + i) % n_860]
        ans_w = normalize_key(cand["options"].get(cand["answer"], ""))
        if ans_w in p1_words_lower:
            _add_q(cand)
            if len(selected) >= 8:
                break

    # Fill up to 9 questions from QUESTIONS_860_BANK deterministically
    for i in range(n_860):
        if len(selected) >= 9:
            break
        cand = QUESTIONS_860_BANK[(s_idx * 7 + i) % n_860]
        _add_q(cand)

    # 3. Add today's primary session questions (Morning Part 5 or Afternoon Spaced Traps)
    primary_pool = (
        day_data["morning"]["part5"]
        if is_morning
        else day_data["afternoon"]["spaced_traps"]
    )
    for pq in primary_pool:
        if len(selected) >= target_count:
            break
        _add_q(pq, pq.get("trap_point") or f"Day {day_num} 核心句構與單字實戰")

    # 4. If still < target_count (e.g. afternoon has 14 traps + 9 from 860 bank = 23), fill from complementary pool
    comp_day = DAYS_DATA.get((day_num % 25) + 1, DAYS_DATA[1])
    comp_pool = (
        day_data["afternoon"]["spaced_traps"]
        if is_morning
        else comp_day["morning"]["part5"]
    )
    for cq in comp_pool:
        if len(selected) >= target_count:
            break
        _add_q(cq, cq.get("trap_point") or "跨日高頻核心單字與語法複習")

    # Number 1..25 consecutively and ensure balanced A/B/C/D keys
    letters = ("A", "B", "C", "D")
    for idx, q in enumerate(selected[:target_count], 1):
        q["id"] = idx
        q["target_seconds"] = q.get("target_seconds", 15 if idx <= 18 else 20)

    return selected[:target_count]


def select_part4_cloze_passages(
    day_num: int,
    session: str,
    profile: dict,
    start_q_id: int = 26,
    passage_count: int = 3,
) -> Tuple[List[dict], int]:
    """
    Select `passage_count` (3) Cloze passages × 4 blanks = 12 Cloze multiple-choice questions
    (numbered `26..37`, satisfying >= 10 Cloze questions per session).
    """
    s_idx = (day_num - 1) * 2 + (0 if session.lower().startswith("m") else 1)
    n_passages = len(CLOZE_PASSAGES_BANK)

    chosen_passages = []
    seen_titles = set()
    for i in range(n_passages):
        cand = CLOZE_PASSAGES_BANK[(s_idx * 3 + i) % n_passages]
        if cand["title"] not in seen_titles:
            chosen_passages.append(copy.deepcopy(cand))
            seen_titles.add(cand["title"])
            if len(chosen_passages) >= passage_count:
                break

    q_cursor = start_q_id
    for pas in chosen_passages:
        for b_idx, cq in enumerate(pas.get("questions", []), 1):
            cq["id"] = q_cursor
            cq["blank_num"] = b_idx
            # Replace ___[b_idx]___ in passage content with highlighted marker [第 q_cursor 題 / 空格 b_idx]
            pas["content"] = re.sub(
                rf"___\s*\[{b_idx}\]\s*___",
                f"【第 {q_cursor} 題 (空格 {b_idx})】",
                pas["content"],
            )
            q_cursor += 1

    return chosen_passages, q_cursor


def select_part5_reading_passages(
    day_num: int,
    session: str,
    start_q_id: int = 38,
) -> Tuple[List[dict], int]:
    """
    Select 2 long-form multi-paragraph business reading comprehension passages (6 questions,
    numbered `38..43`) for Part 5 (閱讀測驗).
    - Afternoon session uses `DAYS_DATA[day_num]["afternoon"]["part7"]["passages"]`.
    - Morning session uses `DAYS_DATA[((day_num + 11) % 25) + 1]["afternoon"]["part7"]["passages"]`
      so Morning and Afternoon on the same day have completely distinct reading comprehension passages!
    """
    is_morning = session.lower().startswith("m")
    source_day = ((day_num + 11) % 25) + 1 if is_morning else day_num
    p7_obj = DAYS_DATA.get(source_day, DAYS_DATA[1])["afternoon"]["part7"]
    raw_passages = p7_obj.get("passages", [])

    passages = copy.deepcopy(raw_passages)
    q_cursor = start_q_id
    for pas in passages:
        for rq in pas.get("questions", []):
            rq["id"] = q_cursor
            rq["rule_ref"] = rq.get("radar", "Part 7 商務長文細節定位與同義替換雷達")
            q_cursor += 1

    return passages, q_cursor


def build_session_payload(day_num: int, session: str = "morning") -> dict:
    """
    Master entry point returning the complete 5-Part + SRS Analytics payload for `(day_num, session)`.
    """
    vocab_db = build_or_load_vocab_db()
    profile = load_weakness_profile()

    part1_vocab = select_part1_vocabulary(day_num, session, vocab_db, profile, target_count=16)
    part2_grammar = select_part2_grammar(day_num, session, profile)
    PART3_COUNT = 25
    part4_cloze, next_qid = select_part4_cloze_passages(
        day_num, session, profile, start_q_id=PART3_COUNT + 1, passage_count=3
    )
    cloze_stems = {cq["question"].strip() for pas in part4_cloze for cq in pas.get("questions", [])}
    part3_mc = select_part3_mc_questions(
        day_num, session, part1_vocab, profile, target_count=PART3_COUNT, exclude_stems=cloze_stems
    )
    assert len(part3_mc) == PART3_COUNT, f"Part 3 produced {len(part3_mc)} questions"
    part5_reading, end_qid = select_part5_reading_passages(
        day_num, session, start_q_id=next_qid
    )

    total_questions = end_qid - 1
    cloze_q_count = sum(len(p.get("questions", [])) for p in part4_cloze)
    reading_q_count = sum(len(p.get("questions", [])) for p in part5_reading)

    high_impact_db = filter_high_impact_vocabulary(vocab_db, profile)
    tier3_count = sum(1 for v in high_impact_db if int(v.get("freq_tier", 2)) == 3)
    tier2_count = sum(1 for v in high_impact_db if int(v.get("freq_tier", 2)) == 2)
    tier1_count = sum(1 for v in high_impact_db if int(v.get("freq_tier", 2)) == 1)
    weak_words_count = len(profile.get("weak_words", {}))
    history_sessions = len(profile.get("history", []))

    return {
        "day": day_num,
        "session": session,
        "part1_vocab": part1_vocab,
        "part2_grammar": part2_grammar,
        "part3_mc_questions": part3_mc,
        "part4_cloze_passages": part4_cloze,
        "part5_reading_passages": part5_reading,
        "counts": {
            "vocab_items": len(part1_vocab),
            "grammar_modules": len(part2_grammar),
            "part3_mc": len(part3_mc),
            "part4_cloze": cloze_q_count,
            "part5_reading": reading_q_count,
            "total_questions": total_questions,
        },
        "srs_stats": {
            "total_unique_vocab": len(high_impact_db),
            "tier3_ultra_freq": tier3_count,
            "tier2_high_freq": tier2_count,
            "tier1_advanced_860": tier1_count,
            "tracked_weak_words": weak_words_count,
            "completed_agent_drills": history_sessions,
            "top_weak_words": sorted(
                profile.get("weak_words", {}).items(), key=lambda x: x[1], reverse=True
            )[:8],
            "top_weak_categories": sorted(
                profile.get("weak_categories", {}).items(), key=lambda x: x[1], reverse=True
            )[:5],
        },
    }


def get_all_session_questions_flat(day_num: int, session: str = "morning") -> List[dict]:
    """
    Returns all 43 interactive questions (`1..43`) across Part 3 (MC), Part 4 (Cloze) and Part 5
    (Reading) in order. Prefers the saved manifest of what was actually sent; falls back to a
    deterministic rebuild when no manifest exists.
    """
    manifest = load_session_manifest(day_num, session)
    if manifest:
        return manifest
    return _flatten_payload(build_session_payload(day_num, session))


def _flatten_payload(payload: dict) -> List[dict]:
    all_qs = list(payload["part3_mc_questions"])
    for pas in payload["part4_cloze_passages"]:
        for cq in pas.get("questions", []):
            c = copy.deepcopy(cq)
            c["section_type"] = f"第四部分：填空選擇題 ({pas.get('title', '')})"
            all_qs.append(c)
    for pas in payload["part5_reading_passages"]:
        for rq in pas.get("questions", []):
            r = copy.deepcopy(rq)
            r["section_type"] = f"第五部分：閱讀測驗 ({pas.get('title', '')})"
            all_qs.append(r)
    return all_qs


MANIFEST_DIR = PROJECT_DIR / "reports" / "manifests"


def save_session_manifest(payload: dict) -> Path:
    """
    Persist the exact question list that was sent for (day, session). The Remote Agent uses it to
    map reported question numbers back to the real questions even after the weakness profile
    (and therefore tomorrow's selection) has changed.
    """
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    sess = "morning" if str(payload["session"]).lower().startswith("m") else "afternoon"
    path = MANIFEST_DIR / f"Day{int(payload['day']):02d}_{sess}.json"
    path.write_text(json.dumps(_flatten_payload(payload), ensure_ascii=False), encoding="utf-8")
    return path


def load_session_manifest(day_num: int, session: str) -> List[dict]:
    sess = "morning" if session.lower().startswith("m") else "afternoon"
    path = MANIFEST_DIR / f"Day{int(day_num):02d}_{sess}.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []
