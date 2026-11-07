# -*- coding: utf-8 -*-
"""
TOEIC Remote Agent Coach (`remote_agent_coach.py`)
--------------------------------------------------
Provides interactive AI-driven weakness tracking and on-demand custom HTML drill generation
via Telegram (@Toeic_practice_bot):
1. Listens for user messages in Telegram:
   - Wrong question reports: e.g. `錯題回報 Day04 morning: 3, 8, 15` or `錯題 3, 8, 15`
   - Custom topic drills: e.g. `加練 分詞構句`, `加練 假設語氣`, `加練 介系詞`, `加練 詞性`
   - Weakness summary / diagnostic drill: e.g. `弱點` or `診斷`
2. Updates persistent `user_weakness_profile.json` so daily Afternoon Practice automatically
   incorporates targeted review of the user's morning mistakes.
3. Generates standalone mobile-optimized interactive HTML drill files (`sendDocument` only,
   zero plain text messages) and dispatches them immediately to Telegram.
"""

import argparse
import datetime
import html
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from dotenv import load_dotenv

from html_generator import INTERACTIVE_SCRIPT, _render_option_details_html
from master_curriculum import DAYS_DATA
from telegram_sender import send_telegram_document as send_html_report

PROJECT_DIR = Path(__file__).resolve().parent
PROFILE_PATH = PROJECT_DIR / "user_weakness_profile.json"
OUTPUT_DIR = PROJECT_DIR / "output"
SPRINT_START_DATE = datetime.date(2026, 11, 4)


def get_taipei_today() -> datetime.date:
    tz_taipei = datetime.timezone(datetime.timedelta(hours=8))
    return datetime.datetime.now(tz_taipei).date()


def get_current_sprint_day() -> int:
    delta = (get_taipei_today() - SPRINT_START_DATE).days + 1
    return max(1, min(25, delta))


def load_weakness_profile() -> dict:
    if PROFILE_PATH.exists():
        try:
            return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "last_update_id": 0,
        "history": [],
        "weak_words": {},
        "weak_categories": {},
    }


def save_weakness_profile(profile: dict) -> None:
    PROFILE_PATH.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def classify_question_category(q: dict) -> str:
    text = (q.get("analysis", "") + " " + q.get("trap_point", "")).lower()
    if any(k in text for k in ["假設", "倒裝", "should", "had ", "were "]):
        return "假設語氣與倒裝結構"
    if any(k in text for k in ["分詞", "減化", "v-ing", "v-ed", "主動", "被動"]):
        return "分詞構句與減化子句"
    if any(k in text for k in ["連接詞", "介系詞", "owing to", "despite", "although", "whereas", "prior to"]):
        return "連接詞 vs. 介系詞辨析"
    if any(k in text for k in ["副詞", "形容詞", "名詞", "詞性", "夾心"]):
        return "高頻詞性槽位秒殺"
    return "高階商務字彙與固定搭配"


def get_session_questions(day_num: int, session: str) -> List[dict]:
    day_data = DAYS_DATA.get(day_num, DAYS_DATA[1])
    if session.lower().startswith("m"):
        return day_data["morning"]["part5"]
    traps = day_data["afternoon"]["spaced_traps"]
    p7_passages = day_data["afternoon"]["part7"].get("passages", [])
    p7_qs = [q for p in p7_passages for q in p.get("questions", [])]
    return traps + p7_qs


def find_similar_remedial_questions(
    missed_qs: List[dict],
    exclude_stems: set,
    target_count: int = 12,
) -> List[dict]:
    """Select complex multi-clause Part 5 / Trap questions targeting the same word families or grammar categories."""
    target_words = set()
    target_categories = set()
    for mq in missed_qs:
        for w in mq.get("options", {}).values():
            target_words.add(w.lower())
            # Also match 5-char root prefix for word families
            if len(w) >= 5:
                target_words.add(w[:5].lower())
        target_categories.add(classify_question_category(mq))

    scored_candidates = []
    seen_stems = set(exclude_stems)

    for d in range(1, 26):
        day_obj = DAYS_DATA[d]
        for q in day_obj["morning"]["part5"] + day_obj["afternoon"]["spaced_traps"]:
            stem = q["question"].strip()
            if stem in seen_stems:
                continue
            opts_lower = [v.lower() for v in q["options"].values()]
            score = 0
            # Check exact or root overlap
            for ow in opts_lower:
                if ow in target_words or (len(ow) >= 5 and ow[:5] in target_words):
                    score += 5
            if classify_question_category(q) in target_categories:
                score += 2
            if score > 0:
                scored_candidates.append((score, d, q))
                seen_stems.add(stem)

    scored_candidates.sort(key=lambda x: x[0], reverse=True)
    selected = [item[2] for item in scored_candidates[:target_count]]

    # If fewer than target_count, fill with high-difficulty traps
    if len(selected) < target_count:
        for d in range(1, 26):
            for q in DAYS_DATA[d]["afternoon"]["spaced_traps"]:
                stem = q["question"].strip()
                if stem not in seen_stems:
                    selected.append(q)
                    seen_stems.add(stem)
                    if len(selected) >= target_count:
                        break
            if len(selected) >= target_count:
                break

    return selected


def search_topic_questions(topic_query: str, target_count: int = 15) -> List[dict]:
    """Search across all 850 Part 5 / Trap questions for a user-requested grammar or vocabulary topic."""
    keywords = [k.strip().lower() for k in re.split(r"[\s,，、/]+", topic_query) if k.strip()]
    # Expand common topic aliases
    expanded = list(keywords)
    for kw in keywords:
        if "分詞" in kw or "減化" in kw:
            expanded.extend(["分詞", "減化", "v-ing", "v-ed", "while"])
        elif "假設" in kw or "倒裝" in kw or "條件" in kw:
            expanded.extend(["假設", "倒裝", "條件", "should", "provided", "unless", "had"])
        elif "介系詞" in kw or "連接詞" in kw or "連介" in kw:
            expanded.extend(["介系詞", "連接詞", "owing to", "despite", "although", "prior to", "whereas"])
        elif "詞性" in kw or "副詞" in kw or "形容詞" in kw:
            expanded.extend(["副詞", "形容詞", "夾心", "名詞", "詞性"])
        elif "代名詞" in kw:
            expanded.extend(["代名詞", "another", "other", "others", "each other"])

    scored = []
    seen_stems = set()
    for d in range(1, 26):
        day_obj = DAYS_DATA[d]
        topic_str = day_obj.get("topic", "").lower()
        for q in day_obj["morning"]["part5"] + day_obj["afternoon"]["spaced_traps"]:
            stem = q["question"].strip()
            if stem in seen_stems:
                continue
            haystack = " ".join([
                topic_str,
                stem.lower(),
                q.get("analysis", "").lower(),
                q.get("trap_point", "").lower(),
                q.get("translation", "").lower(),
                " ".join(q.get("options", {}).values()).lower(),
            ])
            score = sum(3 if kw in haystack else 0 for kw in expanded)
            if score > 0:
                scored.append((score, q))
                seen_stems.add(stem)

    scored.sort(key=lambda x: x[0], reverse=True)
    result = [item[1] for item in scored[:target_count]]
    if not result:
        # Fallback to Day 24-25 comprehensive review questions
        for d in (24, 25):
            for q in DAYS_DATA[d]["morning"]["part5"]:
                if len(result) < target_count:
                    result.append(q)
    return result


def render_agent_custom_html(
    title: str,
    subtitle: str,
    diagnostic_notes: List[dict],
    questions: List[dict],
    day_num: int,
) -> str:
    """Render a standalone mobile-optimized interactive HTML file for Remote Agent remedial/topic drills."""
    diag_html = ""
    if diagnostic_notes:
        cards = ""
        for idx, note in enumerate(diagnostic_notes, 1):
            cards += f"""
            <div class="chunk-card" style="border-left: 4px solid #dc2626;">
                <div class="chunk-header">
                    <span class="chunk-num" style="background:#fee2e2;color:#b91c1c;">錯題 #{note['orig_id']}</span>
                    <span class="chunk-title">{html.escape(note['category'])}</span>
                </div>
                <div class="chunk-scenario" style="margin-top:6px;">📌 <b>原題正解：({html.escape(note['answer'])}) {html.escape(note['correct_word'])}</b></div>
                <div class="chunk-para" style="margin-top:4px;">💡 <b>弱點診斷：</b>{html.escape(note['summary'])}</div>
            </div>
            """
        diag_html = f"""
        <section class="section-container">
            <div class="section-title">🩺 遠端 Agent 錯題基因診斷報告（共 {len(diagnostic_notes)} 題）</div>
            {cards}
        </section>
        """

    q_html = ""
    total_q = len(questions)
    for idx, q in enumerate(questions, 1):
        opts = q.get("options", {})
        ans = q.get("answer", "A")
        opt_bd_html = _render_option_details_html(q)
        cat_label = classify_question_category(q)
        q_html += f"""
        <div class="question-block" id="q-block-{idx}">
            <div class="q-header">
                <span class="q-tag">第 {idx} 題 / 共 {total_q} 題 ({html.escape(cat_label)})</span>
                <span class="q-time timer-badge" onclick="startTimer(this, 15)" title="點擊啟動倒數">⏱️ 限時 15 秒 ▶</span>
            </div>
            <div class="q-text">{html.escape(q['question'])}</div>
            <div class="options-grid" data-answer="{ans}">
                <button type="button" class="opt-btn" data-opt="A"><span class="opt-letter">A</span> <span class="opt-txt">{html.escape(opts.get('A', ''))}</span></button>
                <button type="button" class="opt-btn" data-opt="B"><span class="opt-letter">B</span> <span class="opt-txt">{html.escape(opts.get('B', ''))}</span></button>
                <button type="button" class="opt-btn" data-opt="C"><span class="opt-letter">C</span> <span class="opt-txt">{html.escape(opts.get('C', ''))}</span></button>
                <button type="button" class="opt-btn" data-opt="D"><span class="opt-letter">D</span> <span class="opt-txt">{html.escape(opts.get('D', ''))}</span></button>
            </div>
            <details class="spoiler-card">
                <summary class="spoiler-summary">
                    <span>🔓 點擊查看第 {idx} 題答案與選項詳解</span>
                    <span class="tap-hint">防雷展開</span>
                </summary>
                <div class="spoiler-body">
                    <div class="ans-badge"><b>正解：({ans}) {html.escape(opts.get(ans, ''))}</b></div>
                    <div class="ans-analysis">💡 <b>秒殺解析：</b>{html.escape(q.get('analysis', ''))}</div>
                    {opt_bd_html}
                    <div class="ans-trans">🇹🇼 <b>全句中譯：</b>{html.escape(q.get('translation', ''))}</div>
                </div>
            </details>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        :root {{
            --primary: #0f766e;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-sub: #334155;
            --border-color: #cbd5e1;
            --accent-green: #059669;
            --accent-red: #dc2626;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-color: #0b1120;
                --card-bg: #1e293b;
                --text-main: #f8fafc;
                --text-sub: #cbd5e1;
                --border-color: #475569;
            }}
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            font-size: 16px;
            line-height: 1.65;
            padding: 16px 14px 48px 14px;
            max-width: 540px;
            margin: 0 auto;
        }}
        .hero-banner {{
            background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
            color: #ffffff;
            padding: 22px 20px;
            border-radius: 18px;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.35);
        }}
        .hero-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        .hero-title {{ font-size: 22px; font-weight: 800; line-height: 1.35; margin-bottom: 6px; }}
        .hero-sub {{ font-size: 14px; opacity: 0.92; }}
        .section-container {{ margin-bottom: 24px; }}
        .section-title {{
            font-size: 18px; font-weight: 800; margin-bottom: 12px;
            padding-left: 10px; border-left: 4px solid var(--primary);
        }}
        .chunk-card, .question-block {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 14px;
        }}
        .chunk-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }}
        .chunk-num {{ padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: 800; }}
        .chunk-title {{ font-size: 16px; font-weight: 800; }}
        .sticky-control-bar {{
            position: sticky; top: 8px; z-index: 100;
            background: var(--card-bg); border: 2px solid var(--primary);
            border-radius: 14px; padding: 10px 12px; margin-bottom: 18px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }}
        .bar-top-row {{ display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px; }}
        .score-stats {{ font-size: 14px; display: flex; align-items: center; gap: 8px; }}
        .score-pct-badge {{ background: #ccfbf1; color: #115e59; padding: 2px 8px; border-radius: 99px; font-weight: 700; font-size: 13px; }}
        .bar-actions {{ display: flex; gap: 6px; }}
        .action-btn-sm {{
            border: 1px solid var(--border-color); background: var(--bg-color); color: var(--text-main);
            padding: 4px 8px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;
        }}
        .progress-track {{ height: 6px; background: #e2e8f0; border-radius: 99px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: var(--primary); transition: width 0.25s ease; }}
        .q-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .q-tag {{ font-size: 13px; font-weight: 700; color: var(--primary); }}
        .timer-badge {{
            background: #f1f5f9; color: #334155; padding: 4px 10px; border-radius: 99px;
            font-size: 12px; font-weight: 700; cursor: pointer; user-select: none;
        }}
        .q-text {{ font-size: 17px; font-weight: 600; margin-bottom: 14px; line-height: 1.55; }}
        .options-grid {{ display: grid; grid-template-columns: 1fr; gap: 8px; margin-bottom: 12px; }}
        .opt-btn {{
            display: flex; align-items: center; gap: 10px; width: 100%; text-align: left;
            padding: 11px 14px; border-radius: 10px; border: 1.5px solid var(--border-color);
            background: var(--bg-color); color: var(--text-main); font-size: 15px; font-weight: 600; cursor: pointer;
        }}
        .opt-letter {{
            display: inline-flex; align-items: center; justify-content: center;
            width: 26px; height: 26px; border-radius: 50%; background: var(--card-bg);
            border: 1px solid var(--border-color); font-weight: 800; font-size: 13px; flex-shrink: 0;
        }}
        .opt-btn.opt-correct {{ background: #ecfdf5 !important; border-color: #059669 !important; color: #065f46 !important; }}
        .opt-btn.opt-wrong {{ background: #fef2f2 !important; border-color: #dc2626 !important; color: #991b1b !important; }}
        details.spoiler-card {{ border-top: 1px dashed var(--border-color); padding-top: 10px; }}
        summary.spoiler-summary {{
            list-style: none; display: flex; justify-content: space-between; align-items: center;
            font-size: 14px; font-weight: 700; color: var(--primary); cursor: pointer;
        }}
        .spoiler-body {{ margin-top: 10px; font-size: 14.5px; display: flex; flex-direction: column; gap: 8px; }}
        .ans-badge {{ color: var(--accent-green); font-size: 15px; }}
        .opt-breakdown-box {{
            margin-top: 4px; padding: 10px 12px; border-radius: 10px;
            background: rgba(15, 23, 42, 0.03); border: 1px solid var(--border-color);
        }}
        .opt-breakdown-title {{ font-size: 13.5px; font-weight: 800; margin-bottom: 6px; }}
        .opt-bd-row {{ padding: 6px 8px; border-radius: 8px; margin-bottom: 5px; font-size: 13.5px; }}
        .opt-bd-correct {{ background: rgba(5, 150, 105, 0.08); border-left: 3px solid #059669; }}
        .opt-bd-wrong {{ background: rgba(220, 38, 38, 0.05); border-left: 3px solid #dc2626; }}
        .opt-bd-head {{ font-weight: 800; margin-bottom: 2px; }}
    </style>
</head>
<body data-day="{day_num}" data-session="agent">
    <div class="hero-banner">
        <div class="hero-badge">🤖 Antigravity 遠端 Agent 客製化特訓</div>
        <h1 class="hero-title">{html.escape(title)}</h1>
        <div class="hero-sub">{html.escape(subtitle)}</div>
    </div>

    {diag_html}

    <div class="sticky-control-bar" id="live-score-bar">
        <div class="bar-top-row">
            <div class="score-stats">
                <span>🎯 客製特訓進度: <b id="score-progress">0 / {total_q}</b></span>
                <span class="score-pct-badge" id="score-pct">0% 正確</span>
            </div>
            <div class="bar-actions">
                <button type="button" class="action-btn-sm" onclick="toggleAllSpoilers(true)">👁️ 全開</button>
                <button type="button" class="action-btn-sm" onclick="toggleAllSpoilers(false)">🙈 全收</button>
                <button type="button" class="action-btn-sm" id="wrong-filter-btn" onclick="toggleWrongOnly()">❌ 錯題</button>
                <button type="button" class="action-btn-sm" onclick="resetQuiz()">🔄 重置</button>
            </div>
        </div>
        <div class="progress-track">
            <div class="progress-fill" id="score-progress-fill" style="width: 0%;"></div>
        </div>
    </div>

    <section class="section-container">
        <div class="section-title">⚡ 遠端 Agent 靶向實戰題 (共 {total_q} 題)</div>
        {q_html}
    </section>

    <div id="final-summary-card" class="chunk-card" style="display: none; text-align: center; border: 2px solid var(--primary);">
        <h3 style="margin-bottom: 6px;">🎉 遠端 Agent 客製特訓完成！</h3>
        <div>最終成績：<b id="final-score-text">0 / {total_q} (0%)</b></div>
    </div>

    {INTERACTIVE_SCRIPT}
</body>
</html>"""


def parse_and_handle_message(
    text: str,
    profile: dict,
    bot_token: str,
    chat_id: str,
    send_remedial_file: bool = True,
) -> Optional[Path]:
    """
    Parse an incoming user message from Telegram and either:
    - Record wrong questions + send a custom Remedial HTML file
    - Generate & send a custom Topic Drill HTML file
    """
    clean_text = text.strip()
    if not clean_text:
        return None

    default_day = get_current_sprint_day()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Pattern 1: Wrong question report, e.g.:
    # "錯題回報 Day04 morning: 3, 8, 15" or "錯題 3, 8, 15" or "Day4 M 2, 5"
    day_match = re.search(r"day\s*0*(\d+)", clean_text, re.IGNORECASE)
    day_num = int(day_match.group(1)) if day_match else default_day
    day_num = max(1, min(25, day_num))

    session = "morning"
    if any(k in clean_text.lower() for k in ["afternoon", "下午", "陷阱"]):
        session = "afternoon"

    # Extract question numbers if message is reporting wrong questions
    is_wrong_report = any(k in clean_text.lower() for k in ["錯題", "wrong", "答錯", "mistake"]) or bool(
        re.fullmatch(r"[\d\s,，、]+", clean_text)
    )

    if is_wrong_report:
        # Remove "Day04" before extracting question IDs
        text_without_day = re.sub(r"day\s*0*\d+", "", clean_text, flags=re.IGNORECASE)
        q_nums = [int(n) for n in re.findall(r"\b(\d{1,2})\b", text_without_day) if 1 <= int(n) <= 20]
        if q_nums:
            session_qs = get_session_questions(day_num, session)
            missed_qs = []
            diag_notes = []
            exclude_stems = set()

            for qn in sorted(set(q_nums)):
                if 1 <= qn <= len(session_qs):
                    mq = session_qs[qn - 1]
                    missed_qs.append(mq)
                    exclude_stems.add(mq["question"].strip())
                    ans = mq["answer"]
                    c_word = mq["options"].get(ans, "")
                    cat = classify_question_category(mq)
                    diag_notes.append({
                        "orig_id": qn,
                        "category": cat,
                        "answer": ans,
                        "correct_word": c_word,
                        "summary": mq.get("trap_point") or mq.get("analysis", "")[:110],
                    })
                    # Record into persistent profile
                    profile["weak_words"][c_word] = profile["weak_words"].get(c_word, 0) + 1
                    profile["weak_categories"][cat] = profile["weak_categories"].get(cat, 0) + 1

            profile["history"].append({
                "date": str(get_taipei_today()),
                "day": day_num,
                "session": session,
                "wrong_ids": sorted(set(q_nums)),
                "categories": [d["category"] for d in diag_notes],
            })
            save_weakness_profile(profile)

            if send_remedial_file and missed_qs:
                remedial_qs = find_similar_remedial_questions(missed_qs, exclude_stems, target_count=12)
                sess_zh = "上午練習" if session == "morning" else "下午練習"
                title = f"Day {day_num:02d} {sess_zh} — 錯題靶向加練卷"
                subtitle = f"針對您回報的第 {', '.join(map(str, sorted(set(q_nums))))} 題弱點，由遠端 Agent 動態生成 {len(remedial_qs)} 道同觀念變形長句實戰題"
                html_str = render_agent_custom_html(title, subtitle, diag_notes, remedial_qs, day_num)
                out_path = OUTPUT_DIR / f"TOEIC_Day{day_num:02d}_Agent_Remedial.html"
                out_path.write_text(html_str, encoding="utf-8")
                send_html_report(bot_token, chat_id, str(out_path))
                return out_path

    # Pattern 2: Topic drill or Weakness diagnostic request
    topic_query = re.sub(r"^(加練|特訓|練習|弱點|診斷|drill|practice)\s*[:：]?\s*", "", clean_text, flags=re.IGNORECASE).strip()
    if not topic_query or clean_text in ("弱點", "診斷", "狀態"):
        # Build from accumulated weak categories/words
        top_cats = sorted(profile.get("weak_categories", {}).items(), key=lambda x: x[1], reverse=True)
        topic_query = " ".join(c[0] for c in top_cats[:2]) if top_cats else "分詞 假設語氣 介系詞"

    if send_remedial_file:
        drill_qs = search_topic_questions(topic_query, target_count=15)
        title = f"遠端 Agent 隨選主題特訓：{topic_query[:18]}"
        subtitle = f"依據您的指令「{clean_text[:28]}」從金色證書題庫精選 {len(drill_qs)} 道高複雜度多子句實戰題"
        html_str = render_agent_custom_html(title, subtitle, [], drill_qs, default_day)
        out_path = OUTPUT_DIR / f"TOEIC_Agent_Custom_Drill.html"
        out_path.write_text(html_str, encoding="utf-8")
        send_html_report(bot_token, chat_id, str(out_path))
        return out_path

    return None


def process_pending_telegram_updates(send_remedial_file: bool = True, poll_timeout: int = 0) -> int:
    """Fetch new Telegram messages sent to @Toeic_practice_bot and process them."""
    load_dotenv(PROJECT_DIR / ".env")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not bot_token or not chat_id:
        return 0

    profile = load_weakness_profile()
    offset = profile.get("last_update_id", 0) + 1
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    try:
        resp = requests.get(
            url,
            params={"offset": offset, "timeout": poll_timeout, "allowed_updates": json.dumps(["message"])},
            timeout=poll_timeout + 10,
        )
        data = resp.json()
        if not data.get("ok"):
            return 0
    except Exception:
        return 0

    processed = 0
    for upd in data.get("result", []):
        upd_id = upd.get("update_id", 0)
        if upd_id > profile.get("last_update_id", 0):
            profile["last_update_id"] = upd_id
            save_weakness_profile(profile)

        msg = upd.get("message", {})
        sender_chat_id = str(msg.get("chat", {}).get("id", ""))
        if sender_chat_id != str(chat_id):
            continue

        text = msg.get("text", "").strip()
        if not text or text.startswith("/start") and len(text) <= 7:
            continue
        if text.startswith("/start "):
            text = text[7:].strip()

        parse_and_handle_message(text, profile, bot_token, chat_id, send_remedial_file=send_remedial_file)
        processed += 1

    return processed


def main():
    parser = argparse.ArgumentParser(description="TOEIC Remote Agent Coach")
    parser.add_argument("--once", action="store_true", help="Process pending Telegram messages once and exit")
    parser.add_argument("--daemon", action="store_true", help="Run continuous long-polling daemon for instant replies")
    parser.add_argument("--simulate", type=str, help="Simulate a user command string and dispatch HTML to Telegram")
    args = parser.parse_args()

    load_dotenv(PROJECT_DIR / ".env")
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if args.simulate:
        profile = load_weakness_profile()
        out = parse_and_handle_message(args.simulate, profile, bot_token, chat_id, send_remedial_file=True)
        print(f"Dispatched simulated Remote Agent drill: {out}")
        return 0

    if args.daemon:
        print("Starting TOEIC Remote Agent Coach daemon (long-polling @Toeic_practice_bot)...")
        while True:
            try:
                process_pending_telegram_updates(send_remedial_file=True, poll_timeout=20)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Daemon error: {e}", file=sys.stderr)
                time.sleep(5)
        return 0

    count = process_pending_telegram_updates(send_remedial_file=True, poll_timeout=0)
    print(f"Processed {count} Telegram updates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
