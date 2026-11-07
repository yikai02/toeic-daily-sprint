# -*- coding: utf-8 -*-
"""
HTML Generator for TOEIC 25-Day Sprint.

Generates standalone, mobile-optimized HTML reports.
Features:
- Large readable typography (16px+ body, 24px hero, 19px chunk titles, 17px questions)
- Interactive Tap-to-Answer with instant visual feedback (Green for correct, Red for wrong)
- Sticky Live Score & Progress Bar with one-click Expand/Collapse/Reset
- Clickable 15-second Countdown Timers for Part 5 reflex training
- Dedicated Anti-spoiler <details> accordions directly beneath each question
- Part 7 Fine-Print Radar Highlights for conditional clauses and asterisks
- Consecutive numbering (Questions 1 to 20) across all daily sessions
- Zero external dependencies, 100% offline-ready, responsive dark mode support
"""

import html
import re

INTERACTIVE_SCRIPT = """
    <!-- Interactive Quiz Engine & Live Stats -->
    <script>
    let totalAnswered = 0;
    let correctCount = 0;
    let wrongOnlyMode = false;
    const day = document.body.dataset.day || '1';
    const session = document.body.dataset.session || 'm';
    const STORAGE_KEY = `toeic_sprint_d${day}_${session}`;

    document.addEventListener('DOMContentLoaded', () => {
        updateScoreBar();
        restoreProgress();
    });

    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.opt-btn');
        if (!btn) return;
        const grid = btn.closest('.options-grid');
        if (!grid || grid.classList.contains('answered')) return;

        grid.classList.add('answered');
        totalAnswered++;

        const chosen = btn.getAttribute('data-opt');
        const correct = grid.getAttribute('data-answer');
        const allBtns = grid.querySelectorAll('.opt-btn');
        const qBlock = btn.closest('.question-block');

        if (chosen === correct) {
            btn.classList.add('opt-correct');
            correctCount++;
            if (qBlock) qBlock.classList.add('has-correct');
        } else {
            btn.classList.add('opt-wrong');
            if (qBlock) qBlock.classList.add('has-wrong');
            allBtns.forEach(b => {
                if (b.getAttribute('data-opt') === correct) {
                    b.classList.add('opt-correct');
                }
            });
        }

        if (qBlock) {
            const details = qBlock.querySelector('details.spoiler-card');
            if (details) details.open = true;
        }

        updateScoreBar();
        saveProgress();
    });

    // When user manually opens spoiler details without clicking an option, show correct answer
    document.addEventListener('toggle', (e) => {
        if (e.target.tagName && e.target.tagName.toLowerCase() === 'details' && e.target.open) {
            const qBlock = e.target.closest('.question-block');
            if (qBlock) {
                const grid = qBlock.querySelector('.options-grid');
                if (grid && !grid.classList.contains('answered')) {
                    const correct = grid.getAttribute('data-answer');
                    const correctBtn = grid.querySelector('.opt-btn[data-opt="' + correct + '"]');
                    if (correctBtn) correctBtn.classList.add('opt-correct');
                }
            }
        }
    }, true);

    function updateScoreBar() {
        const progEl = document.getElementById('score-progress');
        const pctEl = document.getElementById('score-pct');
        const fillEl = document.getElementById('score-progress-fill');
        const total = document.querySelectorAll('.question-block').length;
        if (!progEl || !pctEl || total === 0) return;

        const pct = totalAnswered > 0 ? Math.round((correctCount / totalAnswered) * 100) : 0;
        const fillPct = Math.round((totalAnswered / total) * 100);

        progEl.innerText = `${totalAnswered} / ${total}`;
        pctEl.innerText = `${pct}% 正確 (${correctCount} 題對)`;
        if (fillEl) fillEl.style.width = `${fillPct}%`;

        const card = document.getElementById('final-summary-card');
        if (card && totalAnswered === total && total > 0) {
            card.style.display = 'block';
            const fText = document.getElementById('final-score-text');
            if (fText) fText.innerText = `${correctCount} / ${total} (${pct}%)`;
        }
    }

    function toggleAllSpoilers(open) {
        document.querySelectorAll('details.spoiler-card').forEach(d => d.open = open);
    }

    function toggleWrongOnly() {
        const btn = document.getElementById('wrong-filter-btn');
        const wrongBlocks = document.querySelectorAll('.question-block.has-wrong');
        const answeredGrids = document.querySelectorAll('.options-grid.answered');

        if (answeredGrids.length === 0) {
            alert('💡 請先開始作答題目，答錯的題目即可點此一鍵聚焦複習！');
            return;
        }

        wrongOnlyMode = !wrongOnlyMode;
        if (wrongOnlyMode) {
            if (wrongBlocks.length === 0) {
                alert('🎉 太厲害了！目前作答題目全部正確，沒有錯題！');
                wrongOnlyMode = false;
                return;
            }
            if (btn) {
                btn.classList.add('btn-active');
                btn.innerText = '📋 全部';
            }
            document.querySelectorAll('.question-block').forEach(qb => {
                if (qb.classList.contains('has-wrong')) {
                    qb.style.display = 'block';
                    const d = qb.querySelector('details.spoiler-card');
                    if (d) d.open = true;
                } else {
                    qb.style.display = 'none';
                }
            });
        } else {
            if (btn) {
                btn.classList.remove('btn-active');
                btn.innerText = '❌ 錯題';
            }
            document.querySelectorAll('.question-block').forEach(qb => {
                qb.style.display = 'block';
            });
        }
    }

    function resetQuiz() {
        if (!confirm('確定要清除本次作答紀錄，重新開始特訓嗎？')) return;
        totalAnswered = 0;
        correctCount = 0;
        wrongOnlyMode = false;
        const btn = document.getElementById('wrong-filter-btn');
        if (btn) {
            btn.classList.remove('btn-active');
            btn.innerText = '❌ 錯題';
        }
        document.querySelectorAll('.question-block').forEach(qb => {
            qb.style.display = 'block';
            qb.classList.remove('has-correct', 'has-wrong');
        });
        document.querySelectorAll('.options-grid').forEach(g => {
            g.classList.remove('answered');
            g.querySelectorAll('.opt-btn').forEach(b => {
                b.classList.remove('opt-correct', 'opt-wrong');
            });
        });
        document.querySelectorAll('details.spoiler-card').forEach(d => d.open = false);
        const card = document.getElementById('final-summary-card');
        if (card) card.style.display = 'none';
        try { sessionStorage.removeItem(STORAGE_KEY); } catch(e) {}
        updateScoreBar();
    }

    function saveProgress() {
        try {
            const data = {};
            document.querySelectorAll('.question-block').forEach(qb => {
                const qid = qb.id;
                const grid = qb.querySelector('.options-grid.answered');
                if (grid) {
                    const picked = grid.querySelector('.opt-btn.opt-correct, .opt-btn.opt-wrong');
                    if (picked) data[qid] = picked.getAttribute('data-opt');
                }
            });
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(data));
        } catch(e) {}
    }

    function restoreProgress() {
        try {
            const raw = sessionStorage.getItem(STORAGE_KEY);
            if (!raw) return;
            const data = JSON.parse(raw);
            if (!data) return;
            Object.keys(data).forEach(qid => {
                const qb = document.getElementById(qid);
                if (!qb) return;
                const optLetter = data[qid];
                const btn = qb.querySelector(`.opt-btn[data-opt="${optLetter}"]`);
                if (btn && !btn.closest('.options-grid').classList.contains('answered')) {
                    btn.click();
                }
            });
        } catch(e) {}
    }

    // 15-second countdown timer with urgent visual cues
    function startTimer(el, seconds) {
        if (el.dataset.running === 'true') return;
        el.dataset.running = 'true';
        el.classList.add('timer-running');
        let remaining = seconds;
        el.innerText = `⏱️ ${remaining} 秒...`;
        const intervalId = setInterval(() => {
            remaining--;
            if (remaining > 5) {
                el.innerText = `⏱️ ${remaining} 秒...`;
            } else if (remaining > 0) {
                el.innerText = `🔥 ${remaining} 秒！`;
                el.classList.add('timer-urgent');
            } else {
                clearInterval(intervalId);
                el.innerText = '⏰ 時間到！秒殺停筆';
                el.classList.remove('timer-urgent');
                setTimeout(() => {
                    el.classList.remove('timer-running');
                    el.dataset.running = 'false';
                    el.innerText = `⏱️ 限時 ${seconds} 秒 ▶`;
                }, 2800);
            }
        }, 1000);
    }
    </script>
"""


def _render_option_details_html(q: dict) -> str:
    """Renders the detailed per-option breakdown (meaning, POS, why right/wrong)."""
    opt_details = q.get("option_details")
    if not opt_details or not isinstance(opt_details, dict):
        return ""
    opts = q.get("options", {})
    ans = q.get("answer", "A")
    rows_html = ""
    for letter in ("A", "B", "C", "D"):
        detail_text = opt_details.get(letter, "")
        if not detail_text:
            continue
        opt_word = opts.get(letter, "")
        is_ans = (letter == ans)
        row_cls = "opt-bd-row opt-bd-correct" if is_ans else "opt-bd-row opt-bd-wrong"
        badge_txt = f"✓ ({letter}) {html.escape(opt_word)}" if is_ans else f"✗ ({letter}) {html.escape(opt_word)}"
        rows_html += f"""
        <div class="{row_cls}">
            <div class="opt-bd-head">{badge_txt}</div>
            <div class="opt-bd-desc">{html.escape(detail_text)}</div>
        </div>
        """
    if not rows_html:
        return ""
    return f"""
    <div class="opt-breakdown-box">
        <div class="opt-breakdown-title">📋 各選項詞性、意思與正誤詳解：</div>
        {rows_html}
    </div>
    """


def render_day_html(day_data: dict, session: str = "morning") -> str:
    day = day_data.get("day", 1)
    date_str = day_data.get("date", "")
    phase = day_data.get("phase", 1)
    phase_name = day_data.get("phase_name", "")
    topic = day_data.get("topic", "")

    is_morning = (session.lower() == "morning")
    session_title = "☀️ 上午練習 — 實戰 20 題" if is_morning else "🌤️ 下午練習 — 實戰 20 題"
    badge_color = "#2563eb" if is_morning else "#7c3aed"

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

        # Build Part 5 Questions (With interactive selection & per-question spoiler card)
        p5_questions_html = ""
        for q in part5:
            qid = q.get("id", 1)
            sec = q.get("target_seconds", 15)
            opts = q.get("options", {})
            ans = q.get("answer", "A")
            opt_bd_html = _render_option_details_html(q)
            p5_questions_html += f"""
            <div class="question-block" id="q-block-{qid}">
                <div class="q-header">
                    <span class="q-tag">第 {qid} 題 / 共 {len(part5)} 題</span>
                    <span class="q-time timer-badge" onclick="startTimer(this, {sec})" title="點擊啟動倒數">⏱️ 限時 {sec} 秒 ▶</span>
                </div>
                <div class="q-text">{html.escape(q['question'])}</div>
                <div class="options-grid" data-answer="{ans}">
                    <button type="button" class="opt-btn" data-opt="A"><span class="opt-letter">A</span> <span class="opt-txt">{html.escape(opts.get('A', ''))}</span></button>
                    <button type="button" class="opt-btn" data-opt="B"><span class="opt-letter">B</span> <span class="opt-txt">{html.escape(opts.get('B', ''))}</span></button>
                    <button type="button" class="opt-btn" data-opt="C"><span class="opt-letter">C</span> <span class="opt-txt">{html.escape(opts.get('C', ''))}</span></button>
                    <button type="button" class="opt-btn" data-opt="D"><span class="opt-letter">D</span> <span class="opt-txt">{html.escape(opts.get('D', ''))}</span></button>
                </div>

                <!-- 專屬單題防雷按鈕 -->
                <details class="spoiler-card">
                    <summary class="spoiler-summary">
                        <span>🛡️ 點擊查看第 {qid} 題答案與深度解析</span>
                        <span class="tap-hint">防雷揭曉</span>
                    </summary>
                    <div class="spoiler-body">
                        <div class="ans-badge"><b>正解：({ans}) {html.escape(opts.get(ans, ''))}</b></div>
                        <div class="ans-analysis">💡 <b>句構與核心解析：</b>{html.escape(q['analysis'])}</div>
                        {opt_bd_html}
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

        <!-- Sticky Progress Toolbar -->
        <div class="sticky-control-bar" id="live-score-bar">
            <div class="bar-top-row">
                <div class="score-stats">
                    <span>📝 上午練習進度: <b id="score-progress">0 / {len(part5)}</b></span>
                    <span class="score-pct-badge" id="score-pct">0% 正確</span>
                </div>
                <div class="bar-actions">
                    <button type="button" class="action-btn-sm" onclick="toggleAllSpoilers(true)" title="展開全部題目解析">👁️ 全開</button>
                    <button type="button" class="action-btn-sm" onclick="toggleAllSpoilers(false)" title="收合全部題目解析">🙈 全收</button>
                    <button type="button" class="action-btn-sm" id="wrong-filter-btn" onclick="toggleWrongOnly()" title="只看答錯題目進行強化複習">❌ 錯題</button>
                    <button type="button" class="action-btn-sm" onclick="resetQuiz()" title="重置作答進度">🔄 重置</button>
                </div>
            </div>
            <div class="progress-track">
                <div class="progress-fill" id="score-progress-fill" style="width: 0%;"></div>
            </div>
        </div>

        <section class="section-container">
            <div class="section-title">⚡ Part 5 實戰校正題 (第 1 ～ {len(part5)} 題，共 {len(part5)} 題)</div>
            {p5_questions_html}
        </section>

        <div id="final-summary-card" class="summary-card" style="display: none;">
            <div class="summary-icon">🎉</div>
            <h3 class="summary-title">本日上午練習（實戰 20 題）完成！</h3>
            <div class="summary-score">最終成績：<b id="final-score-text">0 / {len(part5)} (0%)</b></div>
            <div class="summary-tip">保持這個視覺秒殺語感，11/29 金色證書（860+）勢在必得！</div>
        </div>
        """

    else:
        # Afternoon Session
        a_data = day_data.get("afternoon", {})
        recall = a_data.get("quick_recall", [])
        traps = a_data.get("spaced_traps", [])
        p7 = a_data.get("part7", {})

        # Quick Recall (Warm-up)
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

        passages = p7.get("passages")
        if not passages:
            passages = [{
                "text_type": p7.get("text_type", "Business Document"),
                "title": p7.get("title", ""),
                "content": p7.get("content", ""),
                "questions": p7.get("questions", [])
            }]
        total_p7_q = sum(len(p.get("questions", [])) for p in passages)
        total_aft_q = len(traps) + total_p7_q

        # Spaced Traps (Questions 1 to len(traps))
        traps_q_html = ""
        for idx, t in enumerate(traps, 1):
            opts = t.get("options", {})
            ans = t.get("answer", "A")
            opt_bd_html = _render_option_details_html(t)
            traps_q_html += f"""
            <div class="question-block" id="q-block-{idx}">
                <div class="q-header">
                    <span class="q-tag">第 {idx} 題 / 共 {total_aft_q} 題 (進階陷阱題)</span>
                    <span class="q-time timer-badge" onclick="startTimer(this, 20)" title="點擊啟動倒數">⏱️ 限時 20 秒 ▶</span>
                </div>
                <div class="q-text">{html.escape(t['question'])}</div>
                <div class="options-grid" data-answer="{ans}">
                    <button type="button" class="opt-btn" data-opt="A"><span class="opt-letter">A</span> <span class="opt-txt">{html.escape(opts.get('A', ''))}</span></button>
                    <button type="button" class="opt-btn" data-opt="B"><span class="opt-letter">B</span> <span class="opt-txt">{html.escape(opts.get('B', ''))}</span></button>
                    <button type="button" class="opt-btn" data-opt="C"><span class="opt-letter">C</span> <span class="opt-txt">{html.escape(opts.get('C', ''))}</span></button>
                    <button type="button" class="opt-btn" data-opt="D"><span class="opt-letter">D</span> <span class="opt-txt">{html.escape(opts.get('D', ''))}</span></button>
                </div>

                <!-- 專屬陷阱題防雷按鈕 -->
                <details class="spoiler-card">
                    <summary class="spoiler-summary">
                        <span>🛡️ 點擊查看第 {idx} 題答案與深度解析</span>
                        <span class="tap-hint">防雷揭曉</span>
                    </summary>
                    <div class="spoiler-body">
                        <div class="ans-badge"><b>正解：({ans}) {html.escape(opts.get(ans, ''))}</b></div>
                        <div class="trap-point">⚠️ <b>命題陷阱點：</b>{html.escape(t.get('trap_point', ''))}</div>
                        <div class="ans-analysis">💡 <b>句構與核心解析：</b>{html.escape(t['analysis'])}</div>
                        {opt_bd_html}
                        <div class="ans-trans">🇹🇼 <b>全句中譯：</b>{html.escape(t.get('translation', ''))}</div>
                    </div>
                </details>
            </div>
            """

        p7_sections_html = ""
        global_q_idx = len(traps) + 1
        for p_idx, pas in enumerate(passages, 1):
            raw_body = html.escape(pas.get("content", "")).replace("\n", "<br>")
            # Emphasize fine-print clauses starting with asterisk (*)
            p_body = re.sub(r'(\*[^\n<]+)', r'<div class="fine-print-highlight">\1</div>', raw_body)
            p7_doc_label = f" (文本 {p_idx})" if len(passages) > 1 else ""
            p7_sections_html += f"""
            <div class="p7-doc">
                <div class="p7-doc-type">📄 {html.escape(pas.get('text_type', 'Business Document'))}{p7_doc_label}</div>
                <div class="p7-doc-title">{html.escape(pas.get('title', ''))}</div>
                <div class="p7-doc-body">{p_body}</div>
            </div>
            """
            for pq in pas.get("questions", []):
                opts = pq.get("options", {})
                ans = pq.get("answer", "A")
                opt_bd_html = _render_option_details_html(pq)
                p7_sections_html += f"""
                <div class="question-block" id="q-block-{global_q_idx}">
                    <div class="q-header">
                        <span class="q-tag">第 {global_q_idx} 題 / 共 {total_aft_q} 題 (Part 7)</span>
                    </div>
                    <div class="q-text">{html.escape(pq['question'])}</div>
                    <div class="options-grid" data-answer="{ans}">
                        <button type="button" class="opt-btn" data-opt="A"><span class="opt-letter">A</span> <span class="opt-txt">{html.escape(opts.get('A', ''))}</span></button>
                        <button type="button" class="opt-btn" data-opt="B"><span class="opt-letter">B</span> <span class="opt-txt">{html.escape(opts.get('B', ''))}</span></button>
                        <button type="button" class="opt-btn" data-opt="C"><span class="opt-letter">C</span> <span class="opt-txt">{html.escape(opts.get('C', ''))}</span></button>
                        <button type="button" class="opt-btn" data-opt="D"><span class="opt-letter">D</span> <span class="opt-txt">{html.escape(opts.get('D', ''))}</span></button>
                    </div>

                    <!-- 專屬 Part 7 防漏看雷達按鈕 -->
                    <details class="spoiler-card">
                        <summary class="spoiler-summary">
                            <span>🔍 點擊查看第 {global_q_idx} 題答案與深度解析</span>
                            <span class="tap-hint">防雷揭曉</span>
                        </summary>
                        <div class="spoiler-body">
                            <div class="ans-badge"><b>正解：({ans}) {html.escape(opts.get(ans, ''))}</b></div>
                            <div class="radar-box">{html.escape(pq.get('radar', ''))}</div>
                            <div class="ans-analysis">💡 <b>詳解：</b>{html.escape(pq['analysis'])}</div>
                            {opt_bd_html}
                        </div>
                    </details>
                </div>
                """
                global_q_idx += 1

        body_content = f"""
        <section class="section-container">
            <div class="section-title">🧠 上午重點記憶快篩 ({len(recall)} 題語塊速查)</div>
            {recall_html}
        </section>

        <!-- Sticky Progress Toolbar -->
        <div class="sticky-control-bar" id="live-score-bar">
            <div class="bar-top-row">
                <div class="score-stats">
                    <span>📝 下午練習進度: <b id="score-progress">0 / {total_aft_q}</b></span>
                    <span class="score-pct-badge" id="score-pct">0% 正確</span>
                </div>
                <div class="bar-actions">
                    <button type="button" class="action-btn-sm" onclick="toggleAllSpoilers(true)" title="展開全部題目解析">👁️ 全開</button>
                    <button type="button" class="action-btn-sm" onclick="toggleAllSpoilers(false)" title="收合全部題目解析">🙈 全收</button>
                    <button type="button" class="action-btn-sm" id="wrong-filter-btn" onclick="toggleWrongOnly()" title="只看答錯題目進行強化複習">❌ 錯題</button>
                    <button type="button" class="action-btn-sm" onclick="resetQuiz()" title="重置作答進度">🔄 重置</button>
                </div>
            </div>
            <div class="progress-track">
                <div class="progress-fill" id="score-progress-fill" style="width: 0%;"></div>
            </div>
        </div>

        <section class="section-container">
            <div class="section-title">⚡ Part 5/6 易錯陷阱練習 (第 1 ～ {len(traps)} 題 / 共 {total_aft_q} 題)</div>
            {traps_q_html}
        </section>

        <section class="section-container">
            <div class="section-title">📑 Part 7 細節抓漏雙篇微閱讀 (第 {len(traps)+1} ～ {total_aft_q} 題 / 共 {total_aft_q} 題)</div>
            {p7_sections_html}
        </section>

        <div id="final-summary-card" class="summary-card" style="display: none;">
            <div class="summary-icon">🏆</div>
            <h3 class="summary-title">本日下午練習（實戰 20 題）全數完成！</h3>
            <div class="summary-score">最終成績：<b id="final-score-text">0 / {total_aft_q} (0%)</b></div>
            <div class="summary-tip">防漏看雷達已完全校正，今日核心弱點清零成功！</div>
        </div>
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
            margin-bottom: 20px;
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
            font-size: 23px;
            font-weight: 800;
            letter-spacing: -0.3px;
            margin-bottom: 6px;
        }}

        .hero-topic {{
            font-size: 15px;
            opacity: 0.98;
            line-height: 1.5;
        }}

        /* Sticky Control Toolbar */
        .sticky-control-bar {{
            position: sticky;
            top: 10px;
            z-index: 100;
            background: var(--card-bg);
            border: 1.5px solid var(--border-color);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.09);
            border-radius: 14px;
            padding: 10px 14px;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            backdrop-filter: blur(8px);
        }}

        .bar-top-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
        }}

        .score-stats {{
            font-size: 14px;
            font-weight: 700;
            color: var(--text-main);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .score-pct-badge {{
            background: rgba(37, 99, 235, 0.14);
            color: var(--primary);
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 800;
        }}

        .bar-actions {{
            display: flex;
            gap: 6px;
        }}

        .action-btn-sm {{
            background: rgba(100, 116, 139, 0.12);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 5px 9px;
            border-radius: 8px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.15s ease;
        }}

        .action-btn-sm:active {{
            transform: scale(0.94);
        }}

        .action-btn-sm.btn-active {{
            background: #dc2626 !important;
            color: #ffffff !important;
            border-color: #dc2626 !important;
        }}

        .progress-track {{
            width: 100%;
            height: 6px;
            background: rgba(148, 163, 184, 0.2);
            border-radius: 999px;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #10b981, #059669);
            border-radius: 999px;
            transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        /* Section Container */
        .section-container {{
            margin-bottom: 26px;
        }}

        .section-title {{
            font-size: 18px;
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
            font-size: 16.5px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
        }}

        .chunk-scenario {{
            font-size: 15px;
            color: var(--text-main);
            margin-bottom: 6px;
            line-height: 1.55;
            background: rgba(148, 163, 184, 0.08);
            padding: 9px 12px;
            border-radius: 8px;
        }}

        .chunk-para {{
            font-size: 14px;
            color: var(--text-sub);
            margin-top: 6px;
        }}

        .chunk-para code {{
            background: rgba(5, 150, 105, 0.12);
            color: #059669;
            padding: 3px 6px;
            border-radius: 4px;
            font-weight: 700;
            font-size: 13.5px;
        }}

        .alert-box {{
            background: rgba(220, 38, 38, 0.1);
            color: #b91c1c;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 13.5px;
            font-weight: 700;
            margin-top: 8px;
        }}

        /* Visual Anchor Card */
        .anchor-card {{
            background: var(--card-bg);
            border: 2px solid var(--accent-gold);
            border-radius: 16px;
            padding: 18px 16px;
            margin-bottom: 18px;
            box-shadow: 0 4px 12px rgba(217, 119, 6, 0.08);
        }}

        .anchor-badge {{
            display: inline-block;
            background: var(--accent-gold);
            color: #ffffff;
            font-size: 12px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}

        .anchor-title {{
            font-size: 19px;
            font-weight: 800;
            color: var(--accent-gold);
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
            transition: border-color 0.2s ease;
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
            background: rgba(100, 116, 139, 0.1);
            padding: 3px 8px;
            border-radius: 6px;
            user-select: none;
        }}

        .timer-badge {{
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .timer-badge:active {{
            transform: scale(0.92);
        }}

        .timer-running {{
            background: rgba(220, 38, 38, 0.15) !important;
            color: #dc2626 !important;
            font-weight: 800;
            animation: pulse 1s infinite;
        }}

        .timer-urgent {{
            background: rgba(220, 38, 38, 0.28) !important;
            color: #b91c1c !important;
            font-weight: 800;
            animation: urgent-pulse 0.5s infinite;
        }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        @keyframes urgent-pulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.04); opacity: 0.7; }}
        }}

        .q-text {{
            font-size: 17px;
            font-weight: 700;
            line-height: 1.6;
            margin-bottom: 14px;
        }}

        /* Interactive Options Grid */
        .options-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
            margin-bottom: 12px;
        }}

        .opt-btn {{
            display: flex;
            align-items: center;
            width: 100%;
            text-align: left;
            background: rgba(148, 163, 184, 0.08);
            border: 1.5px solid var(--border-color);
            padding: 12px 14px;
            border-radius: 12px;
            font-size: 16px;
            color: var(--text-main);
            line-height: 1.45;
            cursor: pointer;
            transition: all 0.15s ease;
            outline: none;
            font-family: inherit;
            -webkit-appearance: none;
        }}

        .opt-btn:active {{
            transform: scale(0.985);
        }}

        .opt-letter {{
            font-weight: 800;
            min-width: 28px;
            color: var(--text-sub);
        }}

        .opt-txt {{
            flex: 1;
        }}

        /* Correct / Wrong Tap Feedback */
        .opt-btn.opt-correct {{
            background: #ecfdf5 !important;
            border-color: #10b981 !important;
            color: #065f46 !important;
            font-weight: 700;
        }}

        .opt-btn.opt-correct::after {{
            content: "✓ 正確";
            margin-left: auto;
            font-size: 13px;
            font-weight: 800;
            color: #059669;
            padding-left: 8px;
        }}

        .opt-btn.opt-wrong {{
            background: #fef2f2 !important;
            border-color: #ef4444 !important;
            color: #991b1b !important;
            font-weight: 700;
        }}

        .opt-btn.opt-wrong::after {{
            content: "✗ 錯誤";
            margin-left: auto;
            font-size: 13px;
            font-weight: 800;
            color: #dc2626;
            padding-left: 8px;
        }}

        @media (prefers-color-scheme: dark) {{
            .opt-btn {{
                background: rgba(255, 255, 255, 0.04);
            }}
            .opt-btn.opt-correct {{
                background: #064e3b !important;
                border-color: #10b981 !important;
                color: #a7f3d0 !important;
            }}
            .opt-btn.opt-wrong {{
                background: #7f1d1d !important;
                border-color: #ef4444 !important;
                color: #fecaca !important;
            }}
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
            padding: 2px 7px;
            border-radius: 4px;
            font-weight: 700;
        }}

        .spoiler-body {{
            padding: 14px;
            border-top: 1px dashed var(--border-color);
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

        /* Per-Option Detailed Breakdown Box */
        .opt-breakdown-box {{
            background: rgba(148, 163, 184, 0.08);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 12px;
            margin: 10px 0;
        }}

        .opt-breakdown-title {{
            font-size: 14.5px;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 8px;
        }}

        .opt-bd-row {{
            padding: 8px 10px;
            border-radius: 8px;
            margin-bottom: 6px;
            font-size: 14.5px;
            line-height: 1.55;
            border-left: 3.5px solid #94a3b8;
            background: var(--card-bg);
        }}

        .opt-bd-row:last-child {{
            margin-bottom: 0;
        }}

        .opt-bd-correct {{
            border-left-color: #10b981;
            background: rgba(16, 185, 129, 0.08);
        }}

        .opt-bd-wrong {{
            border-left-color: #ef4444;
        }}

        .opt-bd-head {{
            font-weight: 800;
            font-size: 14.5px;
            margin-bottom: 2px;
        }}

        .opt-bd-correct .opt-bd-head {{
            color: #059669;
        }}

        .opt-bd-wrong .opt-bd-head {{
            color: #dc2626;
        }}

        .opt-bd-desc {{
            color: var(--text-main);
            font-size: 14px;
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

        .fine-print-highlight {{
            background: rgba(217, 119, 6, 0.12);
            border-left: 3px solid var(--accent-gold);
            padding: 6px 10px;
            margin: 8px 0;
            border-radius: 0 6px 6px 0;
            font-weight: 600;
            color: var(--text-main);
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

        /* Summary Celebration Card */
        .summary-card {{
            background: linear-gradient(135deg, #059669, #0d9488);
            color: #ffffff;
            padding: 22px 18px;
            border-radius: 16px;
            margin: 24px 0;
            text-align: center;
            box-shadow: 0 8px 20px rgba(5, 150, 105, 0.25);
        }}

        .summary-icon {{
            font-size: 32px;
            margin-bottom: 6px;
        }}

        .summary-title {{
            font-size: 20px;
            font-weight: 800;
            margin-bottom: 6px;
        }}

        .summary-score {{
            font-size: 16px;
            opacity: 0.95;
            margin-bottom: 10px;
        }}

        .summary-tip {{
            font-size: 14px;
            opacity: 0.9;
            line-height: 1.5;
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

        @media print {{
            .sticky-control-bar, .timer-badge, .tap-hint, .bar-actions {{
                display: none !important;
            }}
            details.spoiler-card {{
                border: 1px solid #cbd5e1 !important;
                display: block !important;
            }}
            .spoiler-body {{
                display: block !important;
            }}
        }}
    </style>
</head>
<body data-day="{day}" data-session="{session.lower()}">
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
"""
    return full_html + INTERACTIVE_SCRIPT + "\n</body>\n</html>\n"
