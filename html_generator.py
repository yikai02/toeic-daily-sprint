# -*- coding: utf-8 -*-
"""
Mobile-Optimized HTML Generator for TOEIC 25-Day Sprint.
Produces standalone, responsive HTML files engineered specifically for smartphone screens.
Features:
- Extra-large readable typography for mobile screens (16px base, 17-19px headings)
- Per-Question Anti-Spoiler Accordions: Instant answer & explanation button right below each question
- Clean iOS/Material hybrid card aesthetics
- High visual hierarchy (short blocks, bold keywords, chip tags)
- Light/Dark mode support
"""

import html

def render_day_html(day_data: dict, session: str = "morning") -> str:
    """
    Renders a single day's session ('morning' or 'afternoon') into a responsive HTML document.
    """
    day = day_data["day"]
    date_str = day_data.get("date", "")
    phase = day_data.get("phase", 1)
    phase_name = day_data.get("phase_name", "")
    topic = day_data.get("topic", "")

    is_morning = (session.lower() == "morning")
    session_title = "☀️ 早間晨報 (Morning Boost)" if is_morning else "🌙 盤後特訓 (Afternoon Review & Drill)"
    badge_color = "#2563eb" if is_morning else "#7c3aed"

    # Content generation
    if is_morning:
        m_data = day_data.get("morning", {})
        chunks = m_data.get("chunks", [])
        anchor = m_data.get("visual_anchor", {})
        part5 = m_data.get("part5", [])

        # Build Chunks HTML
        chunks_html = ""
        for idx, c in enumerate(chunks, 1):
            alert_html = f'<div class="alert-box">⚠️ {html.escape(c["alert"])}</div>' if c.get("alert") else ""
            chunks_html += f"""
            <div class="chunk-card">
                <div class="chunk-header">
                    <span class="chunk-num">#{idx}</span>
                    <span class="chunk-title">{html.escape(c['chunk'])}</span>
                </div>
                <div class="chunk-meaning">{html.escape(c['meaning'])}</div>
                <div class="chunk-scenario">💼 <b>商務微情境：</b>{html.escape(c['scenario'])}</div>
                <div class="chunk-para">🔄 <b>必考替換：</b><code>{html.escape(c['paraphrase'])}</code></div>
                {alert_html}
            </div>
            """

        # Build Anchor HTML
        anchor_html = f"""
        <div class="anchor-card">
            <div class="anchor-badge">⚡ 無公式視覺錨點</div>
            <h3 class="anchor-title">{html.escape(anchor.get('title', ''))}</h3>
            <p class="anchor-rule">{html.escape(anchor.get('rule_1', ''))}</p>
            <p class="anchor-rule">{html.escape(anchor.get('rule_2', ''))}</p>
            <div class="golden-banner">{html.escape(anchor.get('golden_rule', ''))}</div>
        </div>
        """

        # Build Part 5 Questions (With dedicated per-question spoiler button right below each!)
        p5_questions_html = ""
        for q in part5:
            qid = q["id"]
            sec = q.get("target_seconds", 15)
            opts = q.get("options", {})
            p5_questions_html += f"""
            <div class="question-block">
                <div class="q-header">
                    <span class="q-tag">Question {qid}</span>
                    <span class="q-time">⏱️ 限時 {sec} 秒</span>
                </div>
                <div class="q-text">{html.escape(q['question'])}</div>
                <div class="options-grid">
                    <div class="opt-btn"><b>(A)</b> {html.escape(opts.get('A', ''))}</div>
                    <div class="opt-btn"><b>(B)</b> {html.escape(opts.get('B', ''))}</div>
                    <div class="opt-btn"><b>(C)</b> {html.escape(opts.get('C', ''))}</div>
                    <div class="opt-btn"><b>(D)</b> {html.escape(opts.get('D', ''))}</div>
                </div>

                <!-- 專屬單題防雷按鈕 -->
                <details class="spoiler-card">
                    <summary class="spoiler-summary">
                        <span>🛡️ 點擊查看 Q{qid} 答案與解析</span>
                        <span class="tap-hint">防雷揭曉</span>
                    </summary>
                    <div class="spoiler-body">
                        <div class="ans-badge"><b>正解：({q['answer']})</b></div>
                        <div class="ans-analysis">💡 <b>視覺秒殺詳解：</b>{html.escape(q['analysis'])}</div>
                        <div class="ans-trans">🇹🇼 <b>全句中譯：</b>{html.escape(q.get('translation', ''))}</div>
                    </div>
                </details>
            </div>
            """

        body_content = f"""
        <section class="section-container">
            <div class="section-title">📦 今日核心語塊 (3-Word Chunks)</div>
            {chunks_html}
        </section>

        <section class="section-container">
            <div class="section-title">🎯 視覺秒殺錨點</div>
            {anchor_html}
        </section>

        <section class="section-container">
            <div class="section-title">⚡ Part 5 實戰校正題 (共 {len(part5)} 題)</div>
            {p5_questions_html}
        </section>
        """

    else:
        # Afternoon Session
        a_data = day_data.get("afternoon", {})
        recall = a_data.get("quick_recall", [])
        traps = a_data.get("spaced_traps", [])
        p7 = a_data.get("part7", {})

        # Quick Recall (Each with sleek fold)
        recall_html = ""
        for idx, r in enumerate(recall, 1):
            recall_html += f"""
            <div class="recall-item">
                <div class="recall-prompt"><b>{idx}.</b> {html.escape(r['prompt'])}</div>
                <div class="recall-clue">💡 線索：{html.escape(r['clue'])}</div>
                <details class="spoiler-card" style="margin-top: 10px;">
                    <summary class="spoiler-summary" style="padding: 10px 14px; font-size: 15px;">
                        <span>🛡️ 點擊查看第 {idx} 題正解</span>
                        <span class="tap-hint">揭曉</span>
                    </summary>
                    <div class="spoiler-body" style="padding: 12px 14px;">
                        <div class="ans-badge" style="margin-bottom: 0;">👉 正解：<b>{html.escape(r['answer'])}</b></div>
                    </div>
                </details>
            </div>
            """

        # Spaced Traps (Each with dedicated per-question spoiler button right below!)
        traps_q_html = ""
        for t in traps:
            tid = t.get("id", 1)
            opts = t.get("options", {})
            traps_q_html += f"""
            <div class="question-block">
                <div class="q-header">
                    <span class="q-tag">陷阱題 {tid}</span>
                    <span class="q-time">🔥 易錯陷阱</span>
                </div>
                <div class="q-text">{html.escape(t['question'])}</div>
                <div class="options-grid">
                    <div class="opt-btn"><b>(A)</b> {html.escape(opts.get('A', ''))}</div>
                    <div class="opt-btn"><b>(B)</b> {html.escape(opts.get('B', ''))}</div>
                    <div class="opt-btn"><b>(C)</b> {html.escape(opts.get('C', ''))}</div>
                    <div class="opt-btn"><b>(D)</b> {html.escape(opts.get('D', ''))}</div>
                </div>

                <!-- 專屬陷阱題防雷按鈕 -->
                <details class="spoiler-card">
                    <summary class="spoiler-summary">
                        <span>🛡️ 點擊查看陷阱題 {tid} 答案與解析</span>
                        <span class="tap-hint">防雷揭曉</span>
                    </summary>
                    <div class="spoiler-body">
                        <div class="ans-badge"><b>正解：({t['answer']})</b></div>
                        <div class="trap-point">⚠️ <b>命題陷阱點：</b>{html.escape(t.get('trap_point', ''))}</div>
                        <div class="ans-analysis">💡 <b>解析：</b>{html.escape(t['analysis'])}</div>
                    </div>
                </details>
            </div>
            """

        # Part 7 Micro-Reading (Support single passage or multiple passages)
        passages = p7.get("passages")
        if not passages:
            passages = [{
                "text_type": p7.get("text_type", "Business Document"),
                "title": p7.get("title", ""),
                "content": p7.get("content", ""),
                "questions": p7.get("questions", [])
            }]

        p7_sections_html = ""
        total_p7_q = 0
        global_q_idx = 1
        for p_idx, pas in enumerate(passages, 1):
            p_body = html.escape(pas.get("content", "")).replace("\n", "<br>")
            p7_doc_label = f" (文本 {p_idx})" if len(passages) > 1 else ""
            p7_sections_html += f"""
            <div class="p7-doc">
                <div class="p7-doc-type">📄 {html.escape(pas.get('text_type', 'Business Document'))}{p7_doc_label}</div>
                <div class="p7-doc-title">{html.escape(pas.get('title', ''))}</div>
                <div class="p7-doc-body">{p_body}</div>
            </div>
            """
            for pq in pas.get("questions", []):
                total_p7_q += 1
                opts = pq.get("options", {})
                p7_sections_html += f"""
                <div class="question-block">
                    <div class="q-header">
                        <span class="q-tag">Part 7 題 {global_q_idx}</span>
                    </div>
                    <div class="q-text">{html.escape(pq['question'])}</div>
                    <div class="options-grid">
                        <div class="opt-btn"><b>(A)</b> {html.escape(opts.get('A', ''))}</div>
                        <div class="opt-btn"><b>(B)</b> {html.escape(opts.get('B', ''))}</div>
                        <div class="opt-btn"><b>(C)</b> {html.escape(opts.get('C', ''))}</div>
                        <div class="opt-btn"><b>(D)</b> {html.escape(opts.get('D', ''))}</div>
                    </div>

                    <!-- 專屬 Part 7 防漏看雷達按鈕 -->
                    <details class="spoiler-card">
                        <summary class="spoiler-summary">
                            <span>🔍 點擊查看題 {global_q_idx} 答案與防漏看雷達</span>
                            <span class="tap-hint">防雷揭曉</span>
                        </summary>
                        <div class="spoiler-body">
                            <div class="ans-badge"><b>正解：({pq['answer']})</b></div>
                            <div class="radar-box">{html.escape(pq.get('radar', ''))}</div>
                            <div class="ans-analysis">💡 <b>詳解：</b>{html.escape(pq['analysis'])}</div>
                        </div>
                    </details>
                </div>
                """
                global_q_idx += 1

        body_content = f"""
        <section class="section-container">
            <div class="section-title">🧠 早間記憶快篩 ({len(recall)} 題)</div>
            {recall_html}
        </section>

        <section class="section-container">
            <div class="section-title">🪤 間隔重複錯題變體 ({len(traps)} 題)</div>
            {traps_q_html}
        </section>

        <section class="section-container">
            <div class="section-title">📑 Part 7 細節抓漏微閱讀 ({total_p7_q} 題)</div>
            {p7_sections_html}
        </section>
        """

    # Assemble Full Responsive HTML Page
    full_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day {day} {session_title} - 多益金色特訓</title>
    <style>
        :root {{
            --primary: {badge_color};
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-sub: #334155;
            --border-color: #cbd5e1;
            --accent-green: #059669;
            --accent-red: #dc2626;
            --accent-gold: #d97706;
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

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            font-size: 16px;
            line-height: 1.65;
            padding: 16px 14px 48px 14px;
            max-width: 540px;
            margin: 0 auto;
        }}

        /* Header Card */
        .hero-banner {{
            background: linear-gradient(135deg, {badge_color}, #1d4ed8);
            color: #ffffff;
            padding: 22px 18px;
            border-radius: 18px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.14);
            margin-bottom: 24px;
        }}

        .hero-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            opacity: 0.95;
            margin-bottom: 8px;
        }}

        .phase-badge {{
            background: rgba(255, 255, 255, 0.25);
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 700;
            font-size: 13px;
        }}

        .hero-title {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.3px;
            margin-bottom: 6px;
        }}

        .hero-topic {{
            font-size: 15px;
            opacity: 0.98;
            line-height: 1.5;
        }}

        /* Section Container */
        .section-container {{
            margin-bottom: 26px;
        }}

        .section-title {{
            font-size: 19px;
            font-weight: 800;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            color: var(--text-main);
        }}

        /* Chunk Cards */
        .chunk-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.04);
        }}

        .chunk-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
        }}

        .chunk-num {{
            background: rgba(37, 99, 235, 0.15);
            color: var(--primary);
            font-size: 13px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
        }}

        .chunk-title {{
            font-size: 19px;
            font-weight: 800;
            color: var(--primary);
        }}

        .chunk-meaning {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
        }}

        .chunk-scenario {{
            font-size: 15px;
            color: var(--text-sub);
            margin-bottom: 8px;
            background: rgba(148, 163, 184, 0.12);
            padding: 9px 12px;
            border-radius: 8px;
            line-height: 1.6;
        }}

        .chunk-para {{
            font-size: 14px;
            color: var(--text-sub);
        }}

        .chunk-para code {{
            background: rgba(5, 150, 105, 0.15);
            color: #047857;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 14px;
            font-family: inherit;
            font-weight: 700;
        }}

        .alert-box {{
            margin-top: 10px;
            font-size: 14px;
            color: #dc2626;
            background: rgba(220, 38, 38, 0.12);
            padding: 9px 12px;
            border-radius: 8px;
            font-weight: 600;
            line-height: 1.5;
        }}

        /* Visual Anchor Card */
        .anchor-card {{
            background: var(--card-bg);
            border: 2px solid var(--accent-gold);
            border-radius: 16px;
            padding: 18px 16px;
            box-shadow: 0 4px 14px rgba(217, 119, 6, 0.14);
        }}

        .anchor-badge {{
            display: inline-block;
            background: var(--accent-gold);
            color: #ffffff;
            font-size: 13px;
            font-weight: 800;
            padding: 3px 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            text-transform: uppercase;
        }}

        .anchor-title {{
            font-size: 19px;
            font-weight: 800;
            margin-bottom: 10px;
        }}

        .anchor-rule {{
            font-size: 16px;
            color: var(--text-main);
            margin-bottom: 8px;
            line-height: 1.6;
        }}

        .golden-banner {{
            background: rgba(217, 119, 6, 0.15);
            border-left: 4px solid var(--accent-gold);
            padding: 11px 14px;
            margin-top: 12px;
            font-size: 16px;
            font-weight: 800;
            color: var(--text-main);
            border-radius: 0 8px 8px 0;
            line-height: 1.5;
        }}

        /* Question Blocks */
        .question-block {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 16px;
            margin-bottom: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }}

        .q-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .q-tag {{
            font-size: 13px;
            font-weight: 800;
            background: rgba(37, 99, 235, 0.15);
            color: var(--primary);
            padding: 3px 9px;
            border-radius: 6px;
        }}

        .q-time {{
            font-size: 13px;
            color: var(--text-sub);
            font-weight: 700;
        }}

        .q-text {{
            font-size: 17px;
            font-weight: 700;
            line-height: 1.6;
            margin-bottom: 14px;
        }}

        .options-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
            margin-bottom: 12px;
        }}

        .opt-btn {{
            background: rgba(148, 163, 184, 0.1);
            border: 1px solid var(--border-color);
            padding: 10px 14px;
            border-radius: 10px;
            font-size: 16px;
            color: var(--text-main);
            line-height: 1.5;
        }}

        /* Per-Question Anti-Spoiler Accordion */
        .spoiler-card {{
            background: var(--card-bg);
            border: 2px dashed #64748b;
            border-radius: 12px;
            margin-top: 12px;
            overflow: hidden;
        }}

        .spoiler-summary {{
            padding: 12px 14px;
            font-weight: 800;
            font-size: 15.5px;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(100, 116, 139, 0.09);
            user-select: none;
        }}

        .tap-hint {{
            font-size: 12px;
            background: #64748b;
            color: #ffffff;
            padding: 3px 7px;
            border-radius: 6px;
            font-weight: 600;
        }}

        .spoiler-body {{
            padding: 14px;
            border-top: 1px solid var(--border-color);
            background: var(--card-bg);
        }}

        .ans-badge {{
            font-size: 17px;
            font-weight: 800;
            color: #059669;
            margin-bottom: 6px;
        }}

        .ans-analysis {{
            font-size: 15.5px;
            color: var(--text-main);
            margin-bottom: 6px;
            line-height: 1.6;
        }}

        .ans-trans {{
            font-size: 14.5px;
            color: var(--text-sub);
            line-height: 1.5;
        }}

        .trap-point {{
            font-size: 15px;
            color: #d97706;
            margin-bottom: 6px;
            line-height: 1.5;
            font-weight: 600;
        }}

        .radar-box {{
            background: rgba(217, 119, 6, 0.14);
            color: #92400e;
            padding: 11px 13px;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 8px;
            line-height: 1.6;
        }}

        /* Part 7 Micro-Reading Box */
        .p7-doc {{
            background: var(--card-bg);
            border-left: 5px solid var(--primary);
            border-radius: 0 14px 14px 0;
            padding: 16px;
            margin-bottom: 18px;
            box-shadow: 0 3px 12px rgba(0,0,0,0.05);
            border-top: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
        }}

        .p7-doc-type {{
            font-size: 13px;
            font-weight: 800;
            color: var(--primary);
            text-transform: uppercase;
            margin-bottom: 6px;
        }}

        .p7-doc-title {{
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 12px;
        }}

        .p7-doc-body {{
            font-size: 16px;
            color: var(--text-main);
            line-height: 1.75;
            white-space: normal;
        }}

        /* Quick Recall */
        .recall-item {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 12px;
        }}

        .recall-prompt {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 6px;
            line-height: 1.5;
        }}

        .recall-clue {{
            font-size: 14px;
            color: var(--text-sub);
            margin-bottom: 6px;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            font-size: 13px;
            color: var(--text-sub);
            margin-top: 32px;
            padding-top: 14px;
            border-top: 1px solid var(--border-color);
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <header class="hero-banner">
        <div class="hero-top">
            <span class="phase-badge">Phase {phase} · {phase_name}</span>
            <span>{date_str} (Day {day}/25)</span>
        </div>
        <h1 class="hero-title">{session_title}</h1>
        <div class="hero-topic">🎯 {topic}</div>
    </header>

    {body_content}

    <footer class="footer">
        多益 860+ 金色證書特訓 · 考前 25 天專屬 AI 衝刺教練<br>
        持之以恆，語感秒殺，金色必達！
    </footer>
</body>
</html>
"""
    return full_html
