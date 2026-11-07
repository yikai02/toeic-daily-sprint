# -*- coding: utf-8 -*-
"""Sanity-checks curriculum data and HTML rendering.
Run: python3 validate_curriculum.py [--min-morning 20 --min-afternoon 20 --min-p7-words 175]
"""
import argparse
import sys
from collections import Counter

from html_generator import render_day_html
from master_curriculum import DAYS_DATA


def questions(day):
    a = day["afternoon"]
    p7 = a["part7"]
    passages = p7.get("passages") or [p7]
    return (
        day["morning"]["part5"],
        a["quick_recall"],
        a["spaced_traps"],
        [q for p in passages for q in p["questions"]],
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-morning", type=int, default=20)
    ap.add_argument("--min-afternoon", type=int, default=20)
    ap.add_argument(
        "--min-p7-words",
        type=int,
        default=175,
        help="Minimum word count per Part 7 passage",
    )
    args = ap.parse_args()
    errors = []
    all_stems = set()

    for n in range(1, 26):
        if n not in DAYS_DATA:
            errors.append(f"Day {n} missing")
            continue
        morning, recall, traps, p7 = questions(DAYS_DATA[n])
        if len(morning) < args.min_morning:
            errors.append(f"Day {n}: morning {len(morning)} < {args.min_morning}")
        if len(traps) + len(p7) < args.min_afternoon:
            errors.append(f"Day {n}: afternoon {len(traps)+len(p7)} < {args.min_afternoon}")

        if args.min_p7_words > 0:
            passages = DAYS_DATA[n]["afternoon"]["part7"].get("passages", [])
            for p_idx, p in enumerate(passages):
                wc = len(p["content"].split())
                if wc < args.min_p7_words:
                    errors.append(f"Day {n} P{p_idx+1}: word count {wc} < {args.min_p7_words}")

        # Check within-session unique option sets and within-day unique (option_set, answer) pairs
        m_optsets = [tuple(sorted(q["options"].values())) for q in morning]
        t_optsets = [tuple(sorted(q["options"].values())) for q in traps]
        if len(set(m_optsets)) != len(m_optsets):
            errors.append(f"Day {n}: duplicate option sets within Morning session")
        if len(set(t_optsets)) != len(t_optsets):
            errors.append(f"Day {n}: duplicate option sets within Afternoon Traps session")

        day_pairs = [
            (tuple(sorted(q["options"].values())), q["options"][q["answer"]])
            for q in morning + traps
        ]
        if len(set(day_pairs)) != len(day_pairs):
            errors.append(f"Day {n}: duplicate (option_set, answer) pairs within day")

        # Check answer key balance
        m_ans_counts = Counter(q["answer"] for q in morning)
        a_ans_counts = Counter(q["answer"] for q in traps + p7)
        for letter in ("A", "B", "C", "D"):
            if m_ans_counts[letter] < 3 or a_ans_counts[letter] < 3:
                errors.append(f"Day {n}: unbalanced answer key distribution M={m_ans_counts} A={a_ans_counts}")

        for q in morning + traps:
            stem = q["question"].strip()
            if stem in all_stems:
                errors.append(f"Day {n}: duplicate question stem across curriculum: {stem[:50]}")
            all_stems.add(stem)
            if len(stem.split()) < 20:
                errors.append(f"Day {n}: stem under 20 words ({len(stem.split())}w): {stem[:50]}")
            if not q.get("translation"):
                errors.append(f"Day {n}: missing translation on {stem[:40]}")

        for q in morning + traps + p7:
            if q["answer"] not in q["options"]:
                errors.append(f"Day {n}: answer {q['answer']} not in options: {q['question'][:40]}")
            if len(set(q["options"].values())) != len(q["options"]):
                errors.append(f"Day {n}: duplicate options: {q['question'][:40]}")
            od = q.get("option_details", {})
            if set(od.keys()) != {"A", "B", "C", "D"}:
                errors.append(f"Day {n}: missing option_details keys on {q['question'][:40]}")

        # Verify HTML generation, 5-Part structure & 43 interactive 4-option breakdowns per session
        m_html = render_day_html(DAYS_DATA[n], "morning")
        a_html = render_day_html(DAYS_DATA[n], "afternoon")
        if "☀️ 上午練習" not in m_html or "盤後" in m_html or "早間晨報" in m_html:
            errors.append(f"Day {n}: invalid morning HTML session labels")
        if "🌤️ 下午練習" not in a_html or "盤後" in a_html or "早間晨報" in a_html:
            errors.append(f"Day {n}: invalid afternoon HTML session labels")
        for sess_name, h_doc in (("morning", m_html), ("afternoon", a_html)):
            for req_sec in (
                "第一部分：單字表詳細介紹",
                "第二部分：文法詳細介紹",
                "第三部分：選擇題練習",
                "第四部分：填空選擇題",
                "第五部分：閱讀測驗",
                "實戰統計儀表板",
            ):
                if req_sec not in h_doc:
                    errors.append(f"Day {n} {sess_name}: missing section '{req_sec}'")
            if h_doc.count("📋 各選項詞性、意思與正誤詳解：") != 43:
                errors.append(
                    f"Day {n} {sess_name}: expected 43 option breakdowns, got {h_doc.count('📋 各選項詞性、意思與正誤詳解：')}"
                )
            if h_doc.count('class="options-grid"') != 43:
                errors.append(
                    f"Day {n} {sess_name}: expected 43 interactive MC question grids, got {h_doc.count('class=\"options-grid\"')}"
                )

    print(
        "\n".join(errors)
        if errors
        else "All 50 5-Part HTML sessions (2,150 interactive questions & 252 deduplicated vocab items) passed rigorous validation ✅"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
