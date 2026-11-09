# -*- coding: utf-8 -*-
"""
HTML Generator for TOEIC 25-Day Golden Certificate (860+) Sprint (`html_generator.py`)
--------------------------------------------------------------------------------------
Generates standalone, mobile-optimized interactive HTML practice files for both
`☀️ 上午練習` and `🌤️ 下午練習`, structured into 5 comprehensive parts + Live Analytics:
  - 第一部分：單字表詳細介紹 (16 deduplicated vocabulary items with TOEIC frequency tier & SRS priority)
  - 第二部分：文法詳細介紹 (Visual Anchor + 2 Deep-Dive 860+ Grammar Modules with ✅ vs ❌ comparisons)
  - 第三部分：選擇題練習 — 單字與文法 (25 complex multi-clause MC questions, Q1..Q25)
  - 第四部分：填空選擇題 — 段落克漏字 (3 passages × 4 blanks = 12 Cloze MC questions, Q26..Q37)
  - 第五部分：閱讀測驗 — 商務長文閱讀 (2 long-form passages = 6 Reading MC questions, Q38..Q43)
  - 📊 實戰統計與弱點分析儀表板 + 🤖 遠端 AI Agent 演算法連動中心
"""

import html
import os
import re
from typing import Dict, List

from adaptive_srs_engine import build_session_payload

INTERACTIVE_SCRIPT_TEMPLATE = """
    <!-- Interactive 5-Part Quiz Engine, Real-Time Cloud Sync & Remote Agent Bridge -->
    <script>
    let totalAnswered = 0;
    let correctCount = 0;
    let wrongOnlyMode = false;
    let isApplyingCloud = false;
    let syncTimeout = null;
    const day = document.body.dataset.day || '__DAY__';
    const session = document.body.dataset.session || '__SESSION__';
    const STORAGE_KEY = `toeic_860_v2_d${day}_${session}`;
    const CLOUD_BOT_TOKEN = "__BOT_TOKEN__";

    document.addEventListener('DOMContentLoaded', () => {
        updateScoreBar();
        restoreProgress();
        if (CLOUD_BOT_TOKEN) {
            fetchCloudProgress();
        }
    });

    window.handleOptSelect = function(el, skipSync = false) {
        if (!el) return;
        let radio = el;
        if (el.tagName && el.tagName.toLowerCase() !== 'input') {
            radio = el.querySelector('.opt-radio') || el.closest('.opt-label')?.querySelector('.opt-radio') || el;
        }
        const grid = radio.closest('.options-grid');
        if (!grid || grid.classList.contains('answered')) return;

        grid.classList.add('answered');
        totalAnswered++;

        if (radio.tagName && radio.tagName.toLowerCase() === 'input') {
            radio.checked = true;
        }

        const chosen = radio.getAttribute('data-opt');
        const correct = grid.getAttribute('data-answer');
        const qBlock = radio.closest('.question-block');
        const contentEl = radio.nextElementSibling || radio;
        const allRadios = grid.querySelectorAll('.opt-radio');
        const allBtns = grid.querySelectorAll('.opt-btn, .opt-btn-content');

        if (chosen === correct) {
            contentEl.classList.add('opt-correct');
            correctCount++;
            if (qBlock) qBlock.classList.add('has-correct');
        } else {
            contentEl.classList.add('opt-wrong');
            if (qBlock) qBlock.classList.add('has-wrong');
            allRadios.forEach(r => {
                if (r.getAttribute('data-opt') === correct) {
                    if (r.nextElementSibling) r.nextElementSibling.classList.add('opt-correct');
                }
            });
            allBtns.forEach(b => {
                if (b.getAttribute('data-opt') === correct) {
                    b.classList.add('opt-correct');
                }
            });
        }

        allRadios.forEach(r => {
            r.disabled = true;
        });

        updateScoreBar();
        if (!skipSync) {
            saveProgress();
        }
    };
    window.handleOptClick = window.handleOptSelect;

    document.addEventListener('click', (e) => {
        // If clicking inside .opt-instant-feedback, do not re-trigger selection
        if (e.target.closest('.opt-instant-feedback')) return;

        const label = e.target.closest('.opt-label');
        if (label) {
            const radio = label.querySelector('.opt-radio');
            if (radio && !radio.disabled) {
                handleOptSelect(radio);
            }
            return;
        }
        const btn = e.target.closest('.opt-btn');
        if (btn) handleOptSelect(btn);
    });

    // When user manually opens spoiler details without clicking an option, highlight correct answer
    document.addEventListener('toggle', (e) => {
        if (e.target.tagName && e.target.tagName.toLowerCase() === 'details' && e.target.open) {
            const qBlock = e.target.closest('.question-block');
            if (qBlock) {
                const grid = qBlock.querySelector('.options-grid');
                if (grid && !grid.classList.contains('answered')) {
                    const correct = grid.getAttribute('data-answer');
                    const correctRadio = grid.querySelector('.opt-radio[data-opt="' + correct + '"]');
                    if (correctRadio && correctRadio.nextElementSibling) {
                        correctRadio.nextElementSibling.classList.add('opt-correct');
                    }
                    const correctBtn = grid.querySelector('.opt-btn[data-opt="' + correct + '"]');
                    if (correctBtn) correctBtn.classList.add('opt-correct');
                }
            }
        }
    }, true);

    function computeSubPartStats(partName) {
        const blocks = document.querySelectorAll(`.question-block[data-part="${partName}"]`);
        let ans = 0;
        let corr = 0;
        blocks.forEach(b => {
            if (b.classList.contains('has-correct')) {
                ans++;
                corr++;
            } else if (b.classList.contains('has-wrong')) {
                ans++;
            }
        });
        return { total: blocks.length, answered: ans, correct: corr };
    }

    function estimateToeicBand(pct, answeredCount) {
        if (answeredCount === 0) return '尚未作答 (目標 860–990 金色證書)';
        if (pct >= 92) return `約 930–990 分 🏆 滿分金色證書水準 (${pct}%)`;
        if (pct >= 85) return `約 865–925 分 🥇 穩拿 860+ 金色證書 (${pct}%)`;
        if (pct >= 75) return `約 785–855 分 🎯 距離金色證書僅差臨門一腳 (${pct}%)`;
        if (pct >= 65) return `約 680–780 分 ⚡ 建議點擊下方 Agent 強化錯題 (${pct}%)`;
        return `約 550–675 分 🔥 建議回傳錯題由遠端 Agent 啟動高頻加權複習 (${pct}%)`;
    }

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

        // Update Live Analytics Dashboard if present
        const statOverall = document.getElementById('stat-overall-score');
        const statBand = document.getElementById('stat-toeic-band');
        if (statOverall) {
            statOverall.innerText = `${correctCount} / ${totalAnswered} 題正確 (總題數 ${total} 題 · 正確率 ${pct}%)`;
        }
        if (statBand) {
            statBand.innerText = estimateToeicBand(pct, totalAnswered);
        }

        ['part3', 'part4', 'part5'].forEach(pKey => {
            const st = computeSubPartStats(pKey);
            const txtEl = document.getElementById(`stat-${pKey}-text`);
            const barEl = document.getElementById(`stat-${pKey}-bar`);
            if (txtEl && st.total > 0) {
                const subPct = st.answered > 0 ? Math.round((st.correct / st.answered) * 100) : 0;
                txtEl.innerText = `${st.correct} / ${st.answered} 對 (共 ${st.total} 題 · 正確率 ${subPct}%)`;
                if (barEl) barEl.style.width = `${subPct}%`;
            }
        });

        // Update Triggered Weakness List
        const weakBox = document.getElementById('live-weakness-list');
        if (weakBox) {
            const wrongBlocks = document.querySelectorAll('.question-block.has-wrong');
            if (wrongBlocks.length === 0) {
                weakBox.innerHTML = totalAnswered > 0
                    ? '<span style="color:#059669;font-weight:700;">🎉 目前作答全數正確，尚無觸發任何弱點標籤！</span>'
                    : '<span style="color:var(--text-sub);">尚未產生錯題。開始作答後，系統將即時捕捉您答錯的單字與文法規則並顯示於此。</span>';
            } else {
                const items = [];
                wrongBlocks.forEach(wb => {
                    const qnum = (wb.id || '').replace('q-block-', '');
                    const wWord = wb.getAttribute('data-word') || '';
                    const wRule = wb.getAttribute('data-rule') || '';
                    items.push(`<div class="weak-tag-item">❌ <b>第 ${qnum} 題</b>：正解字彙 <code>${wWord}</code> ｜ 考點：${wRule}</div>`);
                });
                weakBox.innerHTML = items.join('');
            }
        }

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
        if (!confirm('確定要清除本次作答紀錄，重新開始特訓嗎？這將同步重設雲端紀錄。')) return;
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
            g.querySelectorAll('.opt-radio').forEach(r => {
                r.checked = false;
                r.disabled = false;
            });
            g.querySelectorAll('.opt-btn-content, .opt-btn').forEach(b => {
                b.classList.remove('opt-correct', 'opt-wrong');
            });
        });
        document.querySelectorAll('details.spoiler-card').forEach(d => d.open = false);
        const card = document.getElementById('final-summary-card');
        if (card) card.style.display = 'none';
        try { localStorage.removeItem(STORAGE_KEY); } catch(e) {}
        updateScoreBar();

        if (CLOUD_BOT_TOKEN) {
            const statusEl = document.getElementById('cloud-sync-status');
            if (statusEl) statusEl.innerText = '☁️ 雲端重設中...';
            const sessTag = (session === 'morning' || session === 'm') ? 'M' : 'A';
            const dayStr = String(day).padStart(2, '0');
            const totalQ = document.querySelectorAll('.question-block').length;
            const currentRecord = `${sessTag}:D${dayStr}${sessTag}:${Date.now()}:${'-'.repeat(totalQ)}`;

            fetch(`https://api.telegram.org/bot${CLOUD_BOT_TOKEN}/getMyDescription`)
                .then(r => r.json())
                .then(gData => {
                    const existing = (gData.result && gData.result.description) || '';
                    const otherTag = (sessTag === 'M') ? 'A:' : 'M:';
                    const parts = existing.split(' | ').filter(p => p.startsWith(otherTag));
                    parts.push(currentRecord);
                    return fetch(`https://api.telegram.org/bot${CLOUD_BOT_TOKEN}/setMyDescription`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ description: parts.join(' | ') })
                    });
                })
                .then(() => {
                    if (statusEl) statusEl.innerText = '☁️ 雲端進度已重設';
                })
                .catch(() => {});
        }
    }

    function getLocalAnswers() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return { timestamp: 0, answers: {} };
            const parsed = JSON.parse(raw);
            if (parsed && typeof parsed === 'object' && parsed.answers) {
                return parsed;
            }
            return { timestamp: Date.now(), answers: parsed || {} };
        } catch(e) {
            return { timestamp: 0, answers: {} };
        }
    }

    function saveLocalProgress(ts = Date.now()) {
        try {
            const answers = {};
            document.querySelectorAll('.question-block').forEach(qb => {
                const qid = qb.id;
                const grid = qb.querySelector('.options-grid.answered');
                if (grid) {
                    const checkedRadio = grid.querySelector('.opt-radio:checked');
                    if (checkedRadio) {
                        answers[qid] = checkedRadio.getAttribute('data-opt');
                    } else {
                        const picked = grid.querySelector('.opt-btn-content.opt-correct, .opt-btn-content.opt-wrong, .opt-btn.opt-correct, .opt-btn.opt-wrong');
                        if (picked) {
                            answers[qid] = picked.getAttribute('data-opt') || picked.closest('.opt-label')?.querySelector('.opt-radio')?.getAttribute('data-opt');
                        }
                    }
                }
            });
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                timestamp: ts,
                answers: answers
            }));
        } catch(e) {}
    }

    function saveProgress() {
        saveLocalProgress();
        triggerCloudSync();
    }

    function restoreProgress() {
        try {
            const local = getLocalAnswers();
            const data = local.answers;
            if (!data) return;
            Object.keys(data).forEach(qid => {
                const qb = document.getElementById(qid);
                if (!qb) return;
                const optLetter = data[qid];
                const target = qb.querySelector(`.opt-radio[data-opt="${optLetter}"]`) || qb.querySelector(`.opt-btn[data-opt="${optLetter}"]`);
                if (target && !target.closest('.options-grid').classList.contains('answered')) {
                    handleOptSelect(target, true);
                }
            });
        } catch(e) {}
    }

    function triggerCloudSync() {
        if (isApplyingCloud || !CLOUD_BOT_TOKEN) return;
        const statusEl = document.getElementById('cloud-sync-status');
        if (statusEl) statusEl.innerText = '☁️ 雲端同步中...';

        clearTimeout(syncTimeout);
        syncTimeout = setTimeout(() => {
            syncProgressToCloud();
        }, 800);
    }

    async function syncProgressToCloud() {
        if (!CLOUD_BOT_TOKEN) return;
        const statusEl = document.getElementById('cloud-sync-status');
        try {
            const nowTs = Date.now();
            saveLocalProgress(nowTs);
            const local = getLocalAnswers();

            const totalQ = document.querySelectorAll('.question-block').length;
            let ansChars = '';
            for (let i = 1; i <= totalQ; i++) {
                const opt = local.answers[`q-block-${i}`];
                ansChars += (opt && ['A', 'B', 'C', 'D'].includes(opt)) ? opt : '-';
            }

            const sessTag = (session === 'morning' || session === 'm') ? 'M' : 'A';
            const dayStr = String(day).padStart(2, '0');
            const currentRecord = `${sessTag}:D${dayStr}${sessTag}:${nowTs}:${ansChars}`;

            // Fetch current description to merge and preserve other session
            const getResp = await fetch(`https://api.telegram.org/bot${CLOUD_BOT_TOKEN}/getMyDescription`);
            let existing = '';
            if (getResp.ok) {
                const gData = await getResp.json();
                existing = (gData.result && gData.result.description) || '';
            }

            const otherTag = (sessTag === 'M') ? 'A:' : 'M:';
            const parts = existing.split(' | ').filter(p => p.startsWith(otherTag));
            parts.push(currentRecord);
            const newDescription = parts.join(' | ');

            const setResp = await fetch(`https://api.telegram.org/bot${CLOUD_BOT_TOKEN}/setMyDescription`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ description: newDescription })
            });

            if (setResp.ok && statusEl) {
                statusEl.innerText = `☁️ 雲端已同步 (${totalAnswered}/${totalQ} 題)`;
            }
        } catch(e) {
            console.warn('syncProgressToCloud error:', e);
            if (statusEl) statusEl.innerText = '☁️ 本地已存 (離線模式)';
        }
    }

    async function fetchCloudProgress(forceManual = false) {
        if (!CLOUD_BOT_TOKEN) return;
        const statusEl = document.getElementById('cloud-sync-status');
        if (statusEl) statusEl.innerText = '☁️ 雲端同步中...';

        try {
            const resp = await fetch(`https://api.telegram.org/bot${CLOUD_BOT_TOKEN}/getMyDescription`);
            if (!resp.ok) throw new Error('Cloud fetch failed');
            const res = await resp.json();
            const desc = (res.result && res.result.description) || '';

            const sessTag = (session === 'morning' || session === 'm') ? 'M' : 'A';
            const dayStr = String(day).padStart(2, '0');
            const targetPrefix = `${sessTag}:D${dayStr}${sessTag}:`;

            let record = '';
            desc.split(' | ').forEach(part => {
                if (part.startsWith(targetPrefix)) {
                    record = part.substring(targetPrefix.length);
                }
            });

            if (!record) {
                const local = getLocalAnswers();
                if (Object.keys(local.answers).length > 0) {
                    syncProgressToCloud();
                } else if (statusEl) {
                    statusEl.innerText = '☁️ 雲端同步就緒';
                }
                return;
            }

            const rParts = record.split(':');
            const cloudTs = parseInt(rParts[0], 10) || 0;
            const ansChars = rParts[1] || '';

            const local = getLocalAnswers();
            const localTs = local.timestamp || 0;

            if (cloudTs > localTs || forceManual) {
                isApplyingCloud = true;
                for (let i = 0; i < ansChars.length; i++) {
                    const ch = ansChars[i];
                    if (ch === 'A' || ch === 'B' || ch === 'C' || ch === 'D') {
                        const qid = `q-block-${i + 1}`;
                        const qb = document.getElementById(qid);
                        if (qb) {
                            const grid = qb.querySelector('.options-grid');
                            if (grid && !grid.classList.contains('answered')) {
                                const target = grid.querySelector(`.opt-radio[data-opt="${ch}"]`) || grid.querySelector(`.opt-btn[data-opt="${ch}"]`);
                                if (target) {
                                    handleOptSelect(target, true);
                                }
                            }
                        }
                    }
                }
                isApplyingCloud = false;
                saveLocalProgress(cloudTs);
                if (statusEl) {
                    statusEl.innerText = `☁️ 已自雲端同步 (${totalAnswered} 題)`;
                }
            } else if (localTs > cloudTs) {
                syncProgressToCloud();
            } else {
                if (statusEl) {
                    statusEl.innerText = `☁️ 雲端已同步 (${totalAnswered} 題)`;
                }
            }
        } catch(e) {
            console.warn('fetchCloudProgress error:', e);
            if (statusEl) statusEl.innerText = '☁️ 本地已存 (離線中)';
        }
    }

    // Countdown timer with urgent visual cues
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

    function sendWrongToRemoteAgent() {
        const wrongBlocks = document.querySelectorAll('.question-block.has-wrong');
        const wrongIds = [];
        const wrongWords = [];
        wrongBlocks.forEach(qb => {
            const qnum = (qb.id || '').replace(/^q-block-/, '').trim();
            if (qnum) wrongIds.push(qnum);
            const w = (qb.getAttribute('data-word') || '').trim();
            if (w) wrongWords.push(w);
        });
        const dNum = String(day).padStart(2, '0');
        const sessLabel = (session === 'morning' || session === 'm') ? 'morning' : 'afternoon';
        let cmdText = '';
        if (session === 'agent') {
            // Agent drill pages: question numbers are local to this page, so report by answer word
            if (wrongWords.length === 0) {
                alert('目前沒有答錯的題目可回報。');
                return;
            }
            cmdText = `錯題字彙 ${wrongWords.join(' ;; ')}`;
        } else if (wrongIds.length > 0) {
            cmdText = `錯題回報 Day${dNum} ${sessLabel}: ${wrongIds.join(', ')} || ${wrongWords.join(' ;; ')}`;
        } else {
            const manual = prompt('目前頁面上尚無答錯標記，您可直接輸入想回報的題號（1~43，如 3, 18, 29, 40）或想加練的主題（如 段落填空、假設語氣）：', '3, 18, 29');
            if (!manual) return;
            cmdText = /^[0-9, ，、\\s]+$/.test(manual)
                ? `錯題回報 Day${dNum} ${sessLabel}: ${manual}`
                : `加練 ${manual}`;
        }
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(cmdText);
            }
        } catch(e) {}
        const tgUrl = `https://t.me/Toeic_practice_bot?text=${encodeURIComponent(cmdText)}`;
        window.open(tgUrl, '_blank');
    }

    function requestAgentTopicDrill(topic) {
        const cmdText = `加練 ${topic}`;
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(cmdText);
            }
        } catch(e) {}
        const tgUrl = `https://t.me/Toeic_practice_bot?text=${encodeURIComponent(cmdText)}`;
        window.open(tgUrl, '_blank');
    }

    function sendNewVocabToAgent() {
        const input = prompt('📥 請輸入您想新增至單字庫的單字（格式：單字 : 中文意思與搭配，多筆可用分號或換行分隔，重複單字將自動去重）：', 'scrutinize : 仔細審查；徹底檢驗');
        if (!input) return;
        const cmdText = `新增單字 ${input}`;
        try {
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(cmdText);
            }
        } catch(e) {}
        const tgUrl = `https://t.me/Toeic_practice_bot?text=${encodeURIComponent(cmdText)}`;
        window.open(tgUrl, '_blank');
    }
    </script>
"""


def build_interactive_script(day: int = 1, session: str = "morning", bot_token: str = "") -> str:
    bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN", "")
    return (
        INTERACTIVE_SCRIPT_TEMPLATE
        .replace("__DAY__", str(day))
        .replace("__SESSION__", session.lower())
        .replace("__BOT_TOKEN__", bot_token)
    )


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


def _render_part1_vocab_html(vocab_list: List[dict], srs_stats: dict) -> str:
    cards_html = ""
    for idx, v in enumerate(vocab_list, 1):
        word = v.get("word", "")
        pos = v.get("pos", "")
        meaning = v.get("meaning", "")
        colloc = v.get("collocations", "")
        trap = v.get("trap_note", "")
        example = v.get("example", "")
        freq_stars = v.get("freq_stars", "⭐⭐⭐ 超高頻必考")
        src_badge = v.get("source_badge", "📘 核心單字")
        pri_reason = v.get("priority_reason", "⚡ 多益高頻核心")
        pri_score = v.get("priority_score", 8.5)
        err_cnt = int(v.get("error_count", 0))

        border_style = "border-left: 5px solid #dc2626;" if err_cnt > 0 else (
            "border-left: 5px solid #2563eb;" if int(v.get("freq_tier", 2)) == 3 else "border-left: 5px solid #7c3aed;"
        )
        trap_html = f'<div class="alert-box">⚠️ <b>考點與易混淆陷阱：</b>{html.escape(trap)}</div>' if trap else ""

        # 1. Example sentence with Chinese translation
        ex_html = ""
        if example:
            ex_zh = v.get("example_zh", "").strip()
            if ex_zh:
                ex_html = f"""
                <div class="vocab-example">
                    <div class="ex-en">📖 <b>商務例句：</b>{html.escape(example)}</div>
                    <div class="ex-zh">📝 <b>例句中譯：</b>{html.escape(ex_zh)}</div>
                </div>
                """
            else:
                ex_html = f'<div class="vocab-example">📖 <b>商務例句：</b>{html.escape(example)}</div>'

        # 3. Smart Collocation / Synonym detection (never say "必考搭配與同義替換", don't force if no point)
        colloc_html = ""
        raw_colloc = v.get("collocations", "").strip()
        if raw_colloc and raw_colloc.lower() != word.lower() and len(raw_colloc) > 3:
            # Filter out non-collocation meta descriptions
            if not (raw_colloc.endswith("情境高頻。") or raw_colloc.endswith("動作描寫。") or raw_colloc.endswith("日常辦公營運指派。")):
                has_syn = any(k in raw_colloc for k in ("同義", "=", "等同於", "換成", "synonym", "paraphrase"))
                has_col = any(k in raw_colloc for k in ("搭配", "片語", "短語", "access", "figure", "to", "for", "with", "of", "in", "on", "at", "service", "policy", "roadmap", "layout", "regulations", "selection"))
                if has_syn and not has_col:
                    colloc_html = f'<div class="chunk-scenario">🔄 <b>同義詞：</b>{html.escape(raw_colloc)}</div>'
                elif has_col and not has_syn:
                    colloc_html = f'<div class="chunk-scenario">💼 <b>常考搭配：</b>{html.escape(raw_colloc)}</div>'
                elif has_syn and has_col:
                    colloc_html = f'<div class="chunk-scenario">💼 <b>常考搭配與同義詞：</b>{html.escape(raw_colloc)}</div>'
                else:
                    colloc_html = f'<div class="chunk-scenario">💼 <b>常考搭配：</b>{html.escape(raw_colloc)}</div>'

        # 5. Changed "核心字義：" to "中文："
        # 2. Removed "排程演算法說明：" entirely!
        cards_html += f"""
        <div class="chunk-card" style="{border_style}">
            <div class="vocab-badge-row">
                <span class="chunk-num">單字 #{idx}</span>
                <span class="freq-badge">{html.escape(freq_stars)}</span>
                <span class="src-badge">{html.escape(src_badge)}</span>
                <span class="srs-score-badge" title="演算法優先級權重">權重 P={pri_score}</span>
            </div>
            <div class="chunk-header" style="margin-top:6px;">
                <span class="chunk-title">{html.escape(word)}</span>
                <span class="pos-badge">{html.escape(pos)}</span>
            </div>
            <div class="chunk-meaning">💡 <b>中文：</b>{html.escape(meaning)}</div>
            {colloc_html}
            {ex_html}
            {trap_html}
        </div>
        """

    total_db = srs_stats.get("total_unique_vocab", 168)
    return f"""
    <section class="section-container" id="sec-part1">
        <div class="section-title">📚 第一部分：單字表詳細介紹（⚡ 21天高頻衝刺 · 本場排程 {len(vocab_list)} 字 ／ 精準核心庫 {total_db} 字）</div>
        <div class="part-intro-banner">
            🎯 <b>21天倒數高頻衝刺模式：</b>已全面過濾邊緣生僻詞彙！本期練習嚴選<b>多益最常考超高頻核心單字（Tier 3）與您的實戰弱點單字</b>，依權重由高排到低呈現，將寶貴時間 100% 聚焦於真正能突破 860+ 金色證書的必考關鍵題！
        </div>
        {cards_html}
    </section>
    """


def _render_part2_grammar_html(anchor: dict, grammar_mods: List[dict]) -> str:
    anchor_html = ""
    if anchor and anchor.get("title"):
        anchor_html = f"""
        <div class="anchor-card">
            <div class="anchor-badge">⚡ 本日視覺秒殺錨點 (Visual Anchor)</div>
            <h3 class="anchor-title">{html.escape(anchor.get('title', ''))}</h3>
            <p class="anchor-rule">🔹 {html.escape(anchor.get('rule_1', ''))}</p>
            <p class="anchor-rule">🔹 {html.escape(anchor.get('rule_2', ''))}</p>
            <div class="golden-banner">🏆 {html.escape(anchor.get('golden_rule', ''))}</div>
        </div>
        """

    mods_html = ""
    for m_idx, mod in enumerate(grammar_mods, 1):
        pts_html = ""
        for pt in mod.get("points", []):
            pts_html += f"""
            <div class="grammar-point-box">
                <div class="gp-label">📌 {html.escape(pt.get('label', ''))}</div>
                <div class="gp-detail">{html.escape(pt.get('detail', ''))}</div>
                <div class="gp-compare">
                    <div class="gp-correct">{html.escape(pt.get('correct_ex', ''))}</div>
                    <div class="gp-wrong">{html.escape(pt.get('wrong_ex', ''))}</div>
                </div>
            </div>
            """

        # 4. Fixed formula and explanation, correct example, and wrong trap with high-contrast classes
        formula_text = (mod.get("formula") or mod.get("core_formula") or mod.get("rule") or "").strip()
        formula_html = f'<div class="gm-formula">📐 <b>秒殺公式：</b>{html.escape(formula_text)}</div>' if formula_text else ""
        expl_text = mod.get("explanation", "").strip()
        expl_html = f'<div class="gm-expl">💡 <b>觀念解析：</b>{html.escape(expl_text)}</div>' if expl_text else ""
        ex_correct = mod.get("correct_example", "").strip()
        ex_wrong = mod.get("wrong_trap", "").strip()
        compare_html = ""
        if ex_correct or ex_wrong:
            compare_html = f"""
            <div class="gp-compare" style="margin-top:10px;">
                {f'<div class="gp-correct-box">✅ <b>正確示範：</b>{html.escape(ex_correct)}</div>' if ex_correct else ''}
                {f'<div class="gp-wrong-box">⚠️ <b>常見陷阱：</b>{html.escape(ex_wrong)}</div>' if ex_wrong else ''}
            </div>
            """

        mods_html += f"""
        <div class="grammar-mod-card">
            <div class="gm-header">
                <span class="gm-cat">{html.escape(mod.get('category', '860+ 核心文法模組'))}</span>
                <span class="gm-id">Module #{m_idx}</span>
            </div>
            <h3 class="gm-title">{html.escape(mod.get('title', ''))}</h3>
            {formula_html}
            {expl_html}
            {compare_html}
            {pts_html}
        </div>
        """

    return f"""
    <section class="section-container" id="sec-part2">
        <div class="section-title">📐 第二部分：文法詳細介紹（微觀訊號 · 一山不容二虎 · 假設語氣 · 易混淆辨析）</div>
        {anchor_html}
        {mods_html}
    </section>
    """


def _render_question_card_html(q: dict, total_q: int, part_key: str, badge_label: str, default_sec: int = 15) -> str:
    qid = q.get("id", 1)
    sec = q.get("target_seconds", default_sec)
    opts = q.get("options", {})
    ans = q.get("answer", "A")
    ans_word = opts.get(ans, "")
    rule_ref = q.get("rule_ref") or q.get("trap_point") or q.get("radar") or "多益 860+ 核心句構與商務搭配"
    opt_details = q.get("option_details") or {}
    trans_text = q.get("translation", "").strip()
    opt_bd_html = _render_option_details_html(q)
    trans_html = (
        f'<div class="ans-trans">📝 <b>全句中譯：</b>{html.escape(trans_text)}</div>'
        if trans_text
        else ""
    )

    opt_labels_html = ""
    for opt_key in ("A", "B", "C", "D"):
        opt_val = opts.get(opt_key, "")
        is_ans = (opt_key == ans)
        data_type = "correct" if is_ans else "wrong"

        chosen_detail = opt_details.get(opt_key, "").strip()
        correct_detail = opt_details.get(ans, "").strip()

        if is_ans:
            feedback_html = f"""
            <span class="opt-instant-feedback opt-feedback-correct">
                <span class="fb-correct-congrats">🎉 <b>太棒了！您選擇的 ({opt_key}) 是正確答案！</b></span>
                <span class="fb-heading fb-heading-correct">✅ <b>為什麼 ({opt_key}) 是對的：</b></span>
                <span class="fb-correct-detail">{html.escape(chosen_detail)}</span>
                {f'<span class="fb-trans">📝 <b>全句中譯：</b>{html.escape(trans_text)}</span>' if trans_text else ''}
            </span>
            """
        else:
            feedback_html = f"""
            <span class="opt-instant-feedback opt-feedback-wrong">
                <span class="fb-wrong-tag">❌ <b>您選擇的 ({opt_key}) 是錯誤選項</b></span>
                <span class="fb-heading fb-heading-wrong">⚠️ <b>為什麼您選的 ({opt_key}) 是錯的：</b></span>
                <span class="fb-wrong-detail">{html.escape(chosen_detail)}</span>
                <span class="fb-heading fb-heading-correct">✅ <b>正確答案是 ({ans}) {html.escape(ans_word)}，為什麼對：</b></span>
                <span class="fb-correct-detail">{html.escape(correct_detail)}</span>
                {f'<span class="fb-trans">📝 <b>全句中譯：</b>{html.escape(trans_text)}</span>' if trans_text else ''}
            </span>
            """

        opt_labels_html += f"""
            <label class="opt-label" for="opt_{qid}_{opt_key}">
                <input type="radio" name="q_{qid}" id="opt_{qid}_{opt_key}" class="opt-radio" data-opt="{opt_key}" onchange="handleOptSelect(this)" data-type="{data_type}">
                <span class="opt-btn-content"><span class="opt-letter">{opt_key}</span> <span class="opt-txt">{html.escape(opt_val)}</span></span>
                {feedback_html}
            </label>
        """

    return f"""
    <div class="question-block" id="q-block-{qid}" data-part="{part_key}" data-word="{html.escape(ans_word)}" data-rule="{html.escape(rule_ref)}">
        <div class="q-header">
            <span class="q-tag">第 {qid} 題 / 共 {total_q} 題 · {html.escape(badge_label)}</span>
            <span class="q-time timer-badge" onclick="startTimer(this, {sec})" title="點擊啟動倒數">⏱️ 限時 {sec} 秒 ▶</span>
        </div>
        <div class="q-text">{html.escape(q.get('question', ''))}</div>
        <div class="options-grid" data-answer="{ans}">
            {opt_labels_html}
        </div>

        <details class="spoiler-card">
            <summary class="spoiler-summary">
                <span>🛡️ 查看第 {qid} 題完整四選項對照表與文法考點剖析</span>
                <span class="tap-hint">完整對照</span>
            </summary>
            <div class="spoiler-body">
                <div class="ans-badge"><b>正解：({ans}) {html.escape(ans_word)}</b></div>
                <div class="trap-point">🎯 <b>對應考點／弱點規則：</b>{html.escape(rule_ref)}</div>
                <div class="ans-analysis">💡 <b>秒殺句構與上下文解析：</b>{html.escape(q.get('analysis', ''))}</div>
                {opt_bd_html}
                {trans_html}
            </div>
        </details>
    </div>
    """


def render_day_html(
    day_data: dict,
    session: str = "morning",
    payload: dict = None,
    bot_token: str = "",
) -> str:
    bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN", "")
    day = int(day_data.get("day", 1))
    date_str = day_data.get("date", "")
    phase = day_data.get("phase", 1)
    phase_name = day_data.get("phase_name", "")
    topic = day_data.get("topic", "")

    is_morning = session.lower().startswith("m")
    if payload is None:
        payload = build_session_payload(day, "morning" if is_morning else "afternoon")

    part1_vocab = payload["part1_vocab"]
    part2_grammar = payload["part2_grammar"]
    part3_mc = payload["part3_mc_questions"]
    part4_cloze = payload["part4_cloze_passages"]
    part5_reading = payload["part5_reading_passages"]
    counts = payload["counts"]
    srs_stats = payload["srs_stats"]
    total_q = counts["total_questions"]

    session_label = "☀️ 上午練習" if is_morning else "🌤️ 下午練習"
    session_title = f"{session_label} — 五大模組全方位特訓（實戰 {total_q} 題）"
    badge_color = "#2563eb" if is_morning else "#7c3aed"

    anchor = day_data.get("morning", {}).get("visual_anchor", {})

    # 1. Part 1 HTML (Vocabulary Detailed Guide)
    part1_html = _render_part1_vocab_html(part1_vocab, srs_stats)

    # 2. Part 2 HTML (Grammar Detailed Guide)
    part2_html = _render_part2_grammar_html(anchor, part2_grammar)

    # 3. Part 3 HTML (25 Single-Sentence Vocabulary & Grammar Multiple-Choice Questions)
    p3_q_html = ""
    for q in part3_mc:
        p3_q_html += _render_question_card_html(q, total_q, "part3", "第三部分：單字與文法選擇題", default_sec=15)

    part3_html = f"""
    <section class="section-container" id="sec-part3">
        <div class="section-title">⚡ 第三部分：選擇題練習 — 單字與文法實戰（第 1 ～ {len(part3_mc)} 題，共 {len(part3_mc)} 題）</div>
        <div class="part-intro-banner">
            🎯 <b>命題演算法說明：</b>本區共 <b>{len(part3_mc)} 題高複雜度多子句單選題</b>，優先涵蓋全單字庫核心字彙、高頻短字及您曾答錯的弱點規則，每題均附 <code>(A)(B)(C)(D)</code> 四個選項之詞性、字義與正誤原因詳解。
        </div>
        {p3_q_html}
    </section>
    """

    # 4. Part 4 HTML (3 Cloze Passages × 4 Blanks = 12 Cloze Multiple-Choice Questions)
    cloze_start = len(part3_mc) + 1
    cloze_end = cloze_start + counts["part4_cloze"] - 1
    p4_blocks_html = ""
    for p_idx, pas in enumerate(part4_cloze, 1):
        raw_text = html.escape(pas.get("content", "")).replace("\n", "<br>")
        # Highlight 【第 XX 題 (空格 X)】 markers in the Cloze passage
        formatted_body = re.sub(
            r"(【第\s*\d+\s*題\s*\(空格\s*\d+\)】)",
            r'<span class="cloze-blank-marker">\1</span>',
            raw_text,
        )
        p4_blocks_html += f"""
        <div class="p7-doc" style="border-left-color: #d97706;">
            <div class="p7-doc-type" style="color: #d97706;">🧩 第四部分：克漏字段落填空（篇章 {p_idx} / 共 {len(part4_cloze)} 篇）· {html.escape(pas.get('text_type', 'Part 6 Passage'))}</div>
            <div class="p7-doc-title">{html.escape(pas.get('title', ''))}</div>
            <div class="p7-doc-body">{formatted_body}</div>
        </div>
        """
        for cq in pas.get("questions", []):
            b_num = cq.get("blank_num", 1)
            p4_blocks_html += _render_question_card_html(
                cq,
                total_q,
                "part4",
                f"第四部分：填空選擇題 (篇章 {p_idx} · 空格 {b_num})",
                default_sec=20,
            )

    part4_html = f"""
    <section class="section-container" id="sec-part4">
        <div class="section-title">🧩 第四部分：填空選擇題 — 段落克漏字實戰（第 {cloze_start} ～ {cloze_end} 題，共 {counts['part4_cloze']} 題）</div>
        <div class="part-intro-banner">
            💡 <b>克漏字弱點突破特訓：</b>本區包含 <b>{len(part4_cloze)} 篇完整商務文本、共 {counts['part4_cloze']} 題段落填空選擇題（超過 10 題高強度要求）</b>，專門訓練前後文語意連貫、轉折副詞（<code>nonetheless / thereby / namely</code>）與微觀訊號搭配！
        </div>
        {p4_blocks_html}
    </section>
    """

    # 5. Part 5 HTML (2 Long-Form Reading Passages = 6 Multiple-Choice Questions)
    read_start = cloze_end + 1
    read_end = total_q
    p5_blocks_html = ""
    for r_idx, pas in enumerate(part5_reading, 1):
        raw_body = html.escape(pas.get("content", "")).replace("\n", "<br>")
        formatted_body = re.sub(
            r"(\*[^\n<]+)",
            r'<div class="fine-print-highlight">\1</div>',
            raw_body,
        )
        p5_blocks_html += f"""
        <div class="p7-doc">
            <div class="p7-doc-type">📄 第五部分：商務長文閱讀（文本 {r_idx} / 共 {len(part5_reading)} 篇）· {html.escape(pas.get('text_type', 'Business Document'))}</div>
            <div class="p7-doc-title">{html.escape(pas.get('title', ''))}</div>
            <div class="p7-doc-body">{formatted_body}</div>
        </div>
        """
        for rq in pas.get("questions", []):
            p5_blocks_html += _render_question_card_html(
                rq,
                total_q,
                "part5",
                f"第五部分：閱讀測驗 (文本 {r_idx})",
                default_sec=35,
            )

    part5_html = f"""
    <section class="section-container" id="sec-part5">
        <div class="section-title">📑 第五部分：閱讀測驗 — 多篇商務長文實戰（第 {read_start} ～ {read_end} 題，共 {counts['part5_reading']} 題）</div>
        <div class="part-intro-banner">
            🔍 <b>長文防漏看雷達：</b>鎖定星號註腳（<code>*</code>）、但書條件（<code>provided that / subject to</code>）與跨段同義字替換，每題皆附四選項正誤詳解。
        </div>
        {p5_blocks_html}
    </section>
    """

    # 6. Live Statistics & Algorithmic Remote AI Agent Dashboard
    top_weak_words = srs_stats.get("top_weak_words", [])
    if top_weak_words:
        weak_history_badges = " ".join(
            f'<span class="hist-weak-pill">{html.escape(w)} (錯 {c} 次)</span>'
            for w, c in top_weak_words
        )
    else:
        weak_history_badges = '<span style="color:var(--text-sub);font-size:13.5px;">目前尚無歷史累計錯題紀錄；回報錯題後，演算法將自動調升該單字與規則之每日出現權重！</span>'

    stats_and_agent_html = f"""
    <section class="section-container" id="sec-analytics">
        <div class="section-title">📊 實戰統計儀表板 ＆ 🤖 遠端 AI Agent 演算法弱點中心</div>
        <div class="analytics-card">
            <div class="analytics-title">📈 本場即時作答統計與多益分數落點預測</div>
            <div class="stat-main-row">
                <div>🎯 <b>本場總體表現：</b><span id="stat-overall-score">0 / 0 題正確 (總題數 {total_q} 題 · 正確率 0%)</span></div>
                <div style="margin-top:4px;">🏆 <b>動態落點預估：</b><span id="stat-toeic-band" style="color:var(--primary);font-weight:800;">尚未作答 (目標 860–990 金色證書)</span></div>
            </div>

            <div class="sub-stat-grid">
                <div class="sub-stat-item">
                    <div class="sub-stat-head">
                        <span>⚡ 第三部分：單字與文法 ({counts['part3_mc']} 題)</span>
                        <b id="stat-part3-text">0 / 0 對 (0%)</b>
                    </div>
                    <div class="progress-track"><div class="progress-fill" id="stat-part3-bar" style="width:0%;"></div></div>
                </div>
                <div class="sub-stat-item">
                    <div class="sub-stat-head">
                        <span>🧩 第四部分：段落填空選擇題 ({counts['part4_cloze']} 題)</span>
                        <b id="stat-part4-text">0 / 0 對 (0%)</b>
                    </div>
                    <div class="progress-track"><div class="progress-fill" id="stat-part4-bar" style="width:0%;background:linear-gradient(90deg,#d97706,#f59e0b);"></div></div>
                </div>
                <div class="sub-stat-item">
                    <div class="sub-stat-head">
                        <span>📑 第五部分：商務長文閱讀 ({counts['part5_reading']} 題)</span>
                        <b id="stat-part5-text">0 / 0 對 (0%)</b>
                    </div>
                    <div class="progress-track"><div class="progress-fill" id="stat-part5-bar" style="width:0%;background:linear-gradient(90deg,#2563eb,#6366f1);"></div></div>
                </div>
            </div>

            <div class="weakness-radar-panel">
                <div style="font-weight:800;font-size:14.5px;margin-bottom:6px;">🩺 本場即時偵測之錯題單字與文法弱點：</div>
                <div id="live-weakness-list" style="font-size:13.5px;line-height:1.6;">
                    <span style="color:var(--text-sub);">尚未產生錯題。開始作答後，系統將即時捕捉您答錯的單字與文法規則並顯示於此。</span>
                </div>
            </div>

            <div class="weakness-radar-panel" style="margin-top:10px;background:rgba(37,99,235,0.06);">
                <div style="font-weight:800;font-size:14px;margin-bottom:4px;">🧠 遠端 Agent 演算法記憶庫（SM-2 間隔重複 ＋ 頻率與錯題指數加權）：</div>
                <div style="font-size:13px;color:var(--text-sub);margin-bottom:6px;">
                    已去重總單字數：<b>{srs_stats['total_unique_vocab']} 字</b>（含 ⭐⭐⭐ 超高頻短字 <b>{srs_stats['tier3_ultra_freq']} 字</b>、⭐⭐ 商務核心 <b>{srs_stats['tier2_high_freq']} 字</b>、⭐ 860+ 進階 <b>{srs_stats['tier1_advanced_860']} 字</b>）｜已追蹤個人弱點字：<b>{srs_stats['tracked_weak_words']} 字</b>
                </div>
                <div>{weak_history_badges}</div>
            </div>

            <div style="margin-top:14px;display:flex;flex-wrap:wrap;gap:8px;">
                <button type="button" class="action-btn-sm" style="background:#0f766e;color:#fff;padding:8px 13px;font-size:13.5px;" onclick="sendWrongToRemoteAgent()">🤖 一鍵回傳本場錯題給遠端 Agent（演算法加權＋生成專屬特訓卷）</button>
                <button type="button" class="action-btn-sm" style="background:#1d4ed8;color:#fff;padding:8px 13px;font-size:13.5px;" onclick="sendNewVocabToAgent()">📥 傳送新單字給遠端 Agent（自動去重擴充題庫）</button>
                <button type="button" class="action-btn-sm" onclick="requestAgentTopicDrill('微觀訊號與介系詞搭配')">⚡ 加練：微觀訊號 (Signals 1-4)</button>
                <button type="button" class="action-btn-sm" onclick="requestAgentTopicDrill('一山不容二虎與分詞構句')">⚡ 加練：一山不容二虎與分詞</button>
                <button type="button" class="action-btn-sm" onclick="requestAgentTopicDrill('重要性假設語氣與條件句')">⚡ 加練：假設語氣與條件句</button>
                <button type="button" class="action-btn-sm" onclick="requestAgentTopicDrill('段落填空克漏字特訓')">⚡ 加練：第四部分段落填空</button>
            </div>
        </div>
    </section>
    """

    body_content = f"""
    <!-- Quick Section Jump Pills -->
    <div class="quick-nav-bar">
        <a href="#sec-part1" class="qnav-pill">1️⃣ 單字表 ({counts['vocab_items']})</a>
        <a href="#sec-part2" class="qnav-pill">2️⃣ 文法詳解 ({counts['grammar_modules']})</a>
        <a href="#sec-part3" class="qnav-pill">3️⃣ 單字文法題 ({counts['part3_mc']})</a>
        <a href="#sec-part4" class="qnav-pill">4️⃣ 填空選擇題 ({counts['part4_cloze']})</a>
        <a href="#sec-part5" class="qnav-pill">5️⃣ 閱讀測驗 ({counts['part5_reading']})</a>
        <a href="#sec-analytics" class="qnav-pill">📊 統計與Agent</a>
    </div>

    {part1_html}
    {part2_html}

    <!-- Sticky Progress Toolbar -->
    <div class="sticky-control-bar" id="live-score-bar">
        <div class="bar-top-row">
            <div class="score-stats">
                <span>📝 {session_label}進度: <b id="score-progress">0 / {total_q}</b></span>
                <span class="score-pct-badge" id="score-pct">0% 正確</span>
                <span id="cloud-sync-status" class="sync-badge-live" onclick="fetchCloudProgress(true)" title="點擊立即從雲端同步最新進度">☁️ 雲端同步就緒</span>
            </div>
            <div class="bar-actions">
                <button type="button" class="action-btn-sm" onclick="toggleAllSpoilers(true)" title="展開全部題目解析">👁️ 全開</button>
                <button type="button" class="action-btn-sm" onclick="toggleAllSpoilers(false)" title="收合全部題目解析">🙈 全收</button>
                <button type="button" class="action-btn-sm" id="wrong-filter-btn" onclick="toggleWrongOnly()" title="只看答錯題目進行強化複習">❌ 錯題</button>
                <button type="button" class="action-btn-sm" onclick="sendWrongToRemoteAgent()" title="將錯題回傳給遠端 Agent 動態生成客製特訓卷">🤖 Agent 加練</button>
                <button type="button" class="action-btn-sm" onclick="resetQuiz()" title="重置作答進度">🔄 重置</button>
            </div>
        </div>
        <div class="progress-track">
            <div class="progress-fill" id="score-progress-fill" style="width: 0%;"></div>
        </div>
    </div>

    {part3_html}
    {part4_html}
    {part5_html}

    <div id="final-summary-card" class="summary-card" style="display: none;">
        <div class="summary-icon">🏆</div>
        <h3 class="summary-title">本日{session_label}（五大模組 · 實戰 {total_q} 題）全數完成！</h3>
        <div class="summary-score">最終成績：<b id="final-score-text">0 / {total_q} (0%)</b></div>
        <div class="summary-tip">點擊下方按鈕將本場錯題回傳給遠端 AI Agent，演算法將自動調升弱點單字與文法規則之複習頻率！</div>
        <div style="margin-top: 12px;">
            <button type="button" class="action-btn-sm" style="background:#0f766e;color:#fff;padding:8px 16px;font-size:14px;" onclick="sendWrongToRemoteAgent()">🤖 一鍵傳送錯題給遠端 Agent 生成專屬加練卷</button>
        </div>
    </div>

    {stats_and_agent_html}
    """

    full_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Day {day} {session_label} - 多益 860+ 五合一特訓</title>
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
            max-width: 580px;
            margin: 0 auto;
        }}

        .hero-banner {{
            background: linear-gradient(135deg, {badge_color}, #1d4ed8);
            color: #ffffff;
            padding: 22px 18px;
            border-radius: 18px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.14);
            margin-bottom: 14px;
        }}

        .mobile-tip-banner {{
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid rgba(99, 102, 241, 0.25);
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 13px;
            line-height: 1.5;
            color: var(--text-main);
            margin-bottom: 14px;
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
            font-size: 21px;
            font-weight: 800;
            letter-spacing: -0.3px;
            margin-bottom: 6px;
        }}

        .hero-topic {{
            font-size: 14.5px;
            opacity: 0.98;
            line-height: 1.5;
        }}

        .quick-nav-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-bottom: 18px;
        }}

        .qnav-pill {{
            text-decoration: none;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            font-size: 12.5px;
            font-weight: 700;
            padding: 5px 10px;
            border-radius: 999px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}

        .part-intro-banner {{
            background: rgba(37, 99, 235, 0.08);
            border-left: 4px solid var(--primary);
            padding: 10px 12px;
            border-radius: 0 10px 10px 0;
            font-size: 14px;
            color: var(--text-main);
            margin-bottom: 14px;
            line-height: 1.55;
        }}

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
            flex-wrap: wrap;
            gap: 6px;
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

        .sync-badge-live {{
            font-size: 11px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 999px;
            background: rgba(99, 102, 241, 0.12);
            color: #4f46e5;
            border: 1px solid rgba(99, 102, 241, 0.25);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            user-select: none;
            -webkit-user-select: none;
        }}

        @media (prefers-color-scheme: dark) {{
            .sync-badge-live {{
                background: rgba(99, 102, 241, 0.25);
                color: #c7d2fe;
                border-color: rgba(99, 102, 241, 0.4);
            }}
        }}

        .bar-actions {{
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
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

        .section-container {{
            margin-bottom: 28px;
        }}

        .section-title {{
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            color: var(--text-main);
            line-height: 1.4;
        }}

        .chunk-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 15px;
            margin-bottom: 12px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.04);
        }}

        .vocab-badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            align-items: center;
        }}

        .chunk-num {{
            background: rgba(37, 99, 235, 0.15);
            color: var(--primary);
            font-size: 12px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 6px;
        }}

        .freq-badge {{
            background: rgba(217, 119, 6, 0.15);
            color: #b45309;
            font-size: 12px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 6px;
        }}

        .src-badge {{
            background: rgba(16, 185, 129, 0.14);
            color: #047857;
            font-size: 11.5px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
        }}

        .srs-score-badge {{
            margin-left: auto;
            font-size: 11.5px;
            font-weight: 700;
            color: var(--text-sub);
            background: rgba(148, 163, 184, 0.15);
            padding: 2px 7px;
            border-radius: 6px;
        }}

        .chunk-header {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            margin-bottom: 6px;
            flex-wrap: wrap;
        }}

        .chunk-title {{
            font-size: 19px;
            font-weight: 800;
            color: var(--primary);
        }}

        .pos-badge {{
            font-size: 13px;
            font-weight: 700;
            color: var(--text-sub);
        }}

        .chunk-meaning {{
            font-size: 16px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 6px;
        }}

        .chunk-scenario {{
            font-size: 14.5px;
            color: var(--text-main);
            margin-bottom: 6px;
            line-height: 1.55;
            background: rgba(148, 163, 184, 0.08);
            padding: 8px 11px;
            border-radius: 8px;
        }}

        .vocab-example {{
            font-size: 15px;
            color: var(--text-main);
            margin-top: 10px;
            line-height: 1.6;
            padding: 10px 14px;
            border-left: 4px solid #2563eb;
            background: rgba(37, 99, 235, 0.08);
            border-radius: 0 10px 10px 0;
        }}

        .ex-en {{
            color: var(--text-main);
            font-weight: 700;
            font-size: 15px;
            line-height: 1.6;
        }}

        .ex-zh {{
            color: #1d4ed8;
            margin-top: 6px;
            font-size: 14.5px;
            font-weight: 600;
            padding-top: 6px;
            border-top: 1px solid rgba(37, 99, 235, 0.2);
            line-height: 1.55;
        }}

        .alert-box {{
            background: rgba(220, 38, 38, 0.1);
            color: #b91c1c;
            padding: 8px 11px;
            border-radius: 8px;
            font-size: 13.5px;
            font-weight: 700;
            margin-top: 7px;
            line-height: 1.5;
        }}

        /* Grammar Module Cards */
        .anchor-card {{
            background: var(--card-bg);
            border: 2px solid var(--accent-gold);
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 14px;
        }}

        .anchor-badge {{
            display: inline-block;
            background: var(--accent-gold);
            color: #ffffff;
            font-size: 12px;
            font-weight: 800;
            padding: 3px 8px;
            border-radius: 6px;
            margin-bottom: 6px;
        }}

        .anchor-title {{
            font-size: 18px;
            font-weight: 800;
            color: var(--accent-gold);
            margin-bottom: 8px;
        }}

        .anchor-rule {{
            font-size: 15px;
            color: var(--text-main);
            margin-bottom: 6px;
        }}

        .golden-banner {{
            background: rgba(217, 119, 6, 0.15);
            border-left: 4px solid var(--accent-gold);
            padding: 9px 12px;
            margin-top: 8px;
            font-size: 15px;
            font-weight: 800;
            border-radius: 0 8px 8px 0;
        }}

        .grammar-mod-card {{
            background: var(--card-bg);
            border: 1.5px solid var(--border-color);
            border-radius: 15px;
            padding: 16px;
            margin-bottom: 14px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.04);
        }}

        .gm-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }}

        .gm-cat {{
            font-size: 12.5px;
            font-weight: 800;
            color: var(--primary);
            background: rgba(37, 99, 235, 0.12);
            padding: 3px 8px;
            border-radius: 6px;
        }}

        .gm-id {{
            font-size: 12px;
            font-weight: 700;
            color: var(--text-sub);
        }}

        .gm-title {{
            font-size: 17.5px;
            font-weight: 800;
            margin-bottom: 8px;
            color: var(--text-main);
        }}

        .gm-formula {{
            background: #ecfdf5;
            border-left: 4px solid #059669;
            color: #065f46;
            padding: 11px 14px;
            border-radius: 0 8px 8px 0;
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 10px;
            line-height: 1.6;
        }}

        .gm-expl {{
            background: #f0fdfa;
            border-left: 4px solid #0284c7;
            color: #0f172a;
            padding: 11px 14px;
            border-radius: 0 8px 8px 0;
            font-size: 14.5px;
            margin-bottom: 12px;
            line-height: 1.65;
        }}

        .grammar-point-box {{
            background: rgba(148, 163, 184, 0.07);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 11px 12px;
            margin-bottom: 10px;
        }}

        .gp-label {{
            font-size: 15px;
            font-weight: 800;
            color: var(--text-main);
            margin-bottom: 4px;
        }}

        .gp-detail {{
            font-size: 14px;
            color: var(--text-main);
            margin-bottom: 8px;
            line-height: 1.55;
        }}

        .gp-compare {{
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 13.5px;
        }}

        .gp-correct-box {{
            background: #f0fdf4;
            border-left: 4px solid #16a34a;
            padding: 8px 12px;
            margin-bottom: 4px;
            border-radius: 4px;
            font-size: 0.95rem;
            color: #166534;
            line-height: 1.5;
            font-weight: 500;
        }}

        .gp-wrong-box {{
            background: #fef2f2;
            border-left: 4px solid #dc2626;
            padding: 8px 12px;
            border-radius: 4px;
            font-size: 0.95rem;
            color: #991b1b;
            line-height: 1.5;
            font-weight: 500;
        }}

        .gp-correct {{
            color: #047857;
            background: rgba(16, 185, 129, 0.12);
            padding: 5px 8px;
            border-radius: 6px;
            font-weight: 600;
        }}

        .gp-wrong {{
            color: #b91c1c;
            background: rgba(239, 68, 68, 0.1);
            padding: 5px 8px;
            border-radius: 6px;
            font-weight: 600;
        }}

        .cloze-blank-marker {{
            background: rgba(217, 119, 6, 0.22);
            color: #b45309;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 5px;
            border-bottom: 2px solid #d97706;
        }}

        @media (prefers-color-scheme: dark) {{
            .gm-formula {{
                background: rgba(6, 78, 59, 0.45) !important;
                border-left-color: #34d399 !important;
                color: #6ee7b7 !important;
            }}
            .gm-expl {{
                background: rgba(15, 23, 42, 0.6) !important;
                border-left-color: #38bdf8 !important;
                color: #f1f5f9 !important;
            }}
            .gp-correct-box {{
                background: rgba(6, 78, 59, 0.4) !important;
                border-left-color: #22c55e !important;
                color: #86efac !important;
            }}
            .gp-wrong-box {{
                background: rgba(127, 29, 29, 0.4) !important;
                border-left-color: #ef4444 !important;
                color: #fca5a5 !important;
            }}
            .gp-correct {{ color: #6ee7b7; }}
            .gp-wrong {{ color: #fca5a5; }}
            .cloze-blank-marker {{ color: #fcd34d; }}
            .freq-badge {{ color: #fcd34d; }}
            .src-badge {{ color: #6ee7b7; }}
            .alert-box {{ color: #fca5a5; }}
            .vocab-example {{
                background: rgba(30, 58, 138, 0.35) !important;
                border-left-color: #60a5fa !important;
            }}
            .ex-en {{
                color: #f8fafc !important;
            }}
            .ex-zh {{
                color: #93c5fd !important;
                border-top-color: rgba(147, 197, 253, 0.3) !important;
            }}
            .ans-trans {{
                background: rgba(99, 102, 241, 0.2) !important;
                color: #e0e7ff !important;
            }}
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
            flex-wrap: wrap;
            gap: 6px;
        }}

        .q-tag {{
            font-size: 12.5px;
            font-weight: 800;
            background: rgba(37, 99, 235, 0.15);
            color: var(--primary);
            padding: 3px 9px;
            border-radius: 6px;
        }}

        .q-time {{
            font-size: 12.5px;
            color: var(--text-sub);
            font-weight: 700;
            background: rgba(100, 116, 139, 0.1);
            padding: 3px 8px;
            border-radius: 6px;
            cursor: pointer;
            user-select: none;
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
            font-size: 16.5px;
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

        .opt-label {{
            display: block;
            width: 100%;
            cursor: pointer;
            margin: 0;
            padding: 0;
            touch-action: manipulation;
            -webkit-tap-highlight-color: rgba(99, 102, 241, 0.2);
            user-select: none;
            -webkit-user-select: none;
        }}

        .opt-radio {{
            position: absolute;
            opacity: 0;
            width: 0;
            height: 0;
            pointer-events: none;
        }}

        .opt-btn-content, .opt-btn {{
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
            font-family: inherit;
            touch-action: manipulation;
            -webkit-tap-highlight-color: rgba(99, 102, 241, 0.2);
            user-select: none;
            -webkit-user-select: none;
            transition: all 0.15s ease;
        }}

        .opt-btn * {{
            pointer-events: none;
        }}

        .opt-letter {{
            font-weight: 800;
            min-width: 28px;
            color: var(--text-sub);
        }}

        .opt-txt {{
            flex: 1;
        }}

        /* Pure CSS selected state (works 100% even without JavaScript in iOS Quick Look!) */
        .opt-radio:checked + .opt-btn-content {{
            border-color: var(--primary);
            font-weight: 700;
        }}

        .opt-radio[data-type="correct"]:checked + .opt-btn-content {{
            background: #ecfdf5 !important;
            border-color: #10b981 !important;
            color: #065f46 !important;
            font-weight: 700;
        }}

        .opt-radio[data-type="correct"]:checked + .opt-btn-content::after {{
            content: "✓ 正確" !important;
            margin-left: auto;
            font-size: 13px;
            font-weight: 800;
            color: #059669;
            padding-left: 8px;
        }}

        .opt-radio[data-type="wrong"]:checked + .opt-btn-content {{
            background: #fef2f2 !important;
            border-color: #ef4444 !important;
            color: #991b1b !important;
            font-weight: 700;
        }}

        .opt-radio[data-type="wrong"]:checked + .opt-btn-content::after {{
            content: "✗ 錯誤" !important;
            margin-left: auto;
            font-size: 13px;
            font-weight: 800;
            color: #dc2626;
            padding-left: 8px;
        }}

        .opt-btn-content.opt-correct, .opt-btn.opt-correct {{
            background: #ecfdf5 !important;
            border-color: #10b981 !important;
            color: #065f46 !important;
            font-weight: 700;
        }}

        .opt-btn-content.opt-correct::after, .opt-btn.opt-correct::after {{
            content: "✓ 正確" !important;
            margin-left: auto;
            font-size: 13px;
            font-weight: 800;
            color: #059669;
            padding-left: 8px;
        }}

        .opt-btn-content.opt-wrong, .opt-btn.opt-wrong {{
            background: #fef2f2 !important;
            border-color: #ef4444 !important;
            color: #991b1b !important;
            font-weight: 700;
        }}

        .opt-btn-content.opt-wrong::after, .opt-btn.opt-wrong::after {{
            content: "✗ 錯誤" !important;
            margin-left: auto;
            font-size: 13px;
            font-weight: 800;
            color: #dc2626;
            padding-left: 8px;
        }}

        /* Instant Personalized Feedback Box (Works instantly in iOS Quick Look offline & browsers!) */
        .opt-instant-feedback {{
            display: none;
            width: 100%;
            margin-top: 8px;
            padding: 12px 14px;
            border-radius: 10px;
            font-size: 14px;
            line-height: 1.6;
            text-align: left;
            box-sizing: border-box;
            cursor: default;
            user-select: text;
            -webkit-user-select: text;
            animation: fadeInFeedback 0.2s ease-out;
        }}

        @keyframes fadeInFeedback {{
            from {{ opacity: 0; transform: translateY(-4px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .opt-radio:checked ~ .opt-instant-feedback {{
            display: block;
        }}

        .opt-feedback-wrong {{
            background: #fff5f5;
            border: 1.5px solid #fecaca;
            border-left: 5px solid #ef4444;
            color: #1e293b;
        }}

        .fb-wrong-tag {{
            display: block;
            font-size: 15px;
            font-weight: 800;
            color: #dc2626;
            margin-bottom: 6px;
        }}

        .fb-heading {{
            display: block;
            font-size: 13.5px;
            font-weight: 700;
            margin-bottom: 3px;
        }}

        .fb-heading-wrong {{
            color: #991b1b;
        }}

        .fb-wrong-detail {{
            display: block;
            background: rgba(239, 68, 68, 0.08);
            border-radius: 6px;
            padding: 8px 10px;
            color: #7f1d1d;
            font-size: 13.5px;
            line-height: 1.55;
            margin-bottom: 10px;
        }}

        .fb-heading-correct {{
            color: #047857;
        }}

        .fb-correct-detail {{
            display: block;
            background: rgba(16, 185, 129, 0.08);
            border-radius: 6px;
            padding: 8px 10px;
            color: #064e3b;
            font-size: 13.5px;
            line-height: 1.55;
            margin-bottom: 8px;
        }}

        .opt-feedback-correct {{
            background: #f0fdf4;
            border: 1.5px solid #bbf7d0;
            border-left: 5px solid #10b981;
            color: #1e293b;
        }}

        .fb-correct-congrats {{
            display: block;
            font-size: 15px;
            font-weight: 800;
            color: #059669;
            margin-bottom: 6px;
        }}

        .fb-trans {{
            display: block;
            font-size: 13px;
            color: #334155;
            border-top: 1px dashed #cbd5e1;
            padding-top: 8px;
            margin-top: 6px;
            line-height: 1.55;
        }}

        @media (prefers-color-scheme: dark) {{
            .opt-radio[data-type="correct"]:checked + .opt-btn-content,
            .opt-btn-content.opt-correct, .opt-btn.opt-correct {{
                background: #064e3b !important;
                border-color: #10b981 !important;
                color: #a7f3d0 !important;
            }}
            .opt-radio[data-type="wrong"]:checked + .opt-btn-content,
            .opt-btn-content.opt-wrong, .opt-btn.opt-wrong {{
                background: #7f1d1d !important;
                border-color: #ef4444 !important;
                color: #fecaca !important;
            }}
            .opt-feedback-wrong {{
                background: rgba(69, 10, 10, 0.6) !important;
                border-color: rgba(239, 68, 68, 0.4) !important;
                border-left-color: #ef4444 !important;
                color: #f8fafc !important;
            }}
            .fb-wrong-tag {{
                color: #fca5a5 !important;
            }}
            .fb-heading-wrong {{
                color: #fca5a5 !important;
            }}
            .fb-wrong-detail {{
                background: rgba(127, 29, 29, 0.45) !important;
                color: #fecaca !important;
            }}
            .fb-heading-correct {{
                color: #6ee7b7 !important;
            }}
            .fb-correct-detail {{
                background: rgba(6, 78, 59, 0.45) !important;
                color: #a7f3d0 !important;
            }}
            .opt-feedback-correct {{
                background: rgba(6, 78, 59, 0.55) !important;
                border-color: rgba(16, 185, 129, 0.4) !important;
                border-left-color: #34d399 !important;
                color: #f8fafc !important;
            }}
            .fb-correct-congrats {{
                color: #6ee7b7 !important;
            }}
            .fb-trans {{
                color: #cbd5e1 !important;
                border-top-color: rgba(148, 163, 184, 0.3) !important;
            }}
        }}

        .spoiler-card {{
            background: var(--card-bg);
            border: 2px dashed #64748b;
            border-radius: 12px;
            margin-top: 12px;
            overflow: hidden;
        }}

        .spoiler-summary {{
            padding: 11px 14px;
            font-weight: 800;
            font-size: 15px;
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

        .trap-point {{
            font-size: 14.5px;
            color: #d97706;
            margin-bottom: 6px;
            line-height: 1.5;
            font-weight: 700;
        }}

        .ans-analysis {{
            font-size: 15px;
            color: var(--text-main);
            margin-bottom: 6px;
            line-height: 1.6;
        }}

        .ans-trans {{
            font-size: 14px;
            color: var(--text-sub);
            line-height: 1.5;
            margin-top: 6px;
        }}

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
            font-size: 14px;
            line-height: 1.55;
            border-left: 3.5px solid #94a3b8;
            background: var(--card-bg);
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
            font-size: 14px;
            margin-bottom: 2px;
        }}

        .opt-bd-correct .opt-bd-head {{ color: #059669; }}
        .opt-bd-wrong .opt-bd-head {{ color: #dc2626; }}

        .p7-doc {{
            background: var(--card-bg);
            border-left: 5px solid var(--primary);
            border-radius: 0 14px 14px 0;
            padding: 16px;
            margin-bottom: 16px;
            border-top: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
            border-bottom: 1px solid var(--border-color);
        }}

        .p7-doc-type {{
            font-size: 12.5px;
            font-weight: 800;
            color: var(--primary);
            margin-bottom: 6px;
        }}

        .p7-doc-title {{
            font-size: 17.5px;
            font-weight: 800;
            margin-bottom: 10px;
        }}

        .p7-doc-body {{
            font-size: 15.5px;
            color: var(--text-main);
            line-height: 1.75;
        }}

        .fine-print-highlight {{
            background: rgba(217, 119, 6, 0.12);
            border-left: 3px solid var(--accent-gold);
            padding: 6px 10px;
            margin: 8px 0;
            border-radius: 0 6px 6px 0;
            font-weight: 600;
        }}

        /* Analytics & Remote Agent Dashboard */
        .analytics-card {{
            background: var(--card-bg);
            border: 2px solid #0f766e;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 14px rgba(15, 118, 110, 0.08);
        }}

        .analytics-title {{
            font-size: 17px;
            font-weight: 800;
            color: #0f766e;
            margin-bottom: 10px;
        }}

        .stat-main-row {{
            background: rgba(15, 118, 110, 0.07);
            padding: 10px 12px;
            border-radius: 10px;
            font-size: 14.5px;
            margin-bottom: 12px;
        }}

        .sub-stat-grid {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 14px;
        }}

        .sub-stat-head {{
            display: flex;
            justify-content: space-between;
            font-size: 13.5px;
            margin-bottom: 4px;
        }}

        .weakness-radar-panel {{
            background: rgba(220, 38, 38, 0.06);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 10px 12px;
        }}

        .weak-tag-item {{
            padding: 4px 0;
            border-bottom: 1px dashed var(--border-color);
        }}

        .weak-tag-item:last-child {{
            border-bottom: none;
        }}

        .hist-weak-pill {{
            display: inline-block;
            background: rgba(220, 38, 38, 0.12);
            color: #dc2626;
            font-size: 12px;
            font-weight: 700;
            padding: 2px 8px;
            border-radius: 999px;
            margin: 2px 4px 2px 0;
        }}

        .summary-card {{
            background: linear-gradient(135deg, #059669, #0d9488);
            color: #ffffff;
            padding: 22px 18px;
            border-radius: 16px;
            margin: 24px 0;
            text-align: center;
        }}

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
<body data-day="{day}" data-session="{session.lower()}">
    <header class="hero-banner">
        <div class="hero-top">
            <span class="phase-badge">Phase {phase} · {phase_name}</span>
            <span>{date_str} (Day {day}/25)</span>
        </div>
        <h1 class="hero-title">{session_title}</h1>
        <div class="hero-topic">🎯 {topic}</div>
    </header>

    <div class="mobile-tip-banner">
        📱 <b>手機作答專屬升級</b>：點擊任一選項即會<b>立即直接展開詳解</b>（包含您選的選項為什麼錯、正確答案為什麼對與全句中譯）！若在 iPhone / iPad Telegram 預覽想享受動態計分板與 Telegram 錯題回傳，亦可點擊右上角「<b>分享圖示 ➔ 以 Safari 或 Chrome 開啟</b>」！
    </div>

    {body_content}

    <footer class="footer">
        多益 860+ 金色證書特訓 · 五大模組全方位升級 ＆ 遠端 AI Agent 演算法弱點追蹤<br>
        持之以恆，語感秒殺，金色必達！
    </footer>
"""
    script_html = build_interactive_script(day, session, bot_token)
    return full_html + script_html + "\n</body>\n</html>\n"


INTERACTIVE_SCRIPT = build_interactive_script(1, "morning")
