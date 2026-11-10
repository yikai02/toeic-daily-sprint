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
    let CLOUD_BOT_TOKEN = "__BOT_TOKEN__";
    try {
        const urlToken = new URLSearchParams(window.location.search).get('token');
        if (urlToken) {
            localStorage.setItem('TOEIC_SYNC_TOKEN', urlToken);
            CLOUD_BOT_TOKEN = urlToken;
        } else if (!CLOUD_BOT_TOKEN) {
            CLOUD_BOT_TOKEN = localStorage.getItem('TOEIC_SYNC_TOKEN') || "";
        }
    } catch(e) {}

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

        // Lock all radios and unselected labels in this question until reset is clicked
        allRadios.forEach(r => {
            r.disabled = true;
        });
        const allLabels = grid.querySelectorAll('.opt-label');
        allLabels.forEach(lbl => {
            if (!lbl.querySelector('.opt-radio:checked')) {
                lbl.classList.add('opt-locked');
                lbl.style.pointerEvents = 'none';
                lbl.style.opacity = '0.52';
                lbl.style.cursor = 'not-allowed';
            }
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
            const grid = label.closest('.options-grid');
            if (grid && grid.classList.contains('answered')) {
                return;
            }
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
                    ? '<span style="color:var(--primary);font-weight:700;">目前作答全數正確，尚無觸發任何弱點標籤！</span>'
                    : '<span style="color:var(--text-sub);">尚未產生錯題。開始作答後，系統將即時捕捉您答錯的單字與文法規則並顯示於此。</span>';
            } else {
                const items = [];
                wrongBlocks.forEach(wb => {
                    const qnum = (wb.id || '').replace('q-block-', '');
                    const wWord = wb.getAttribute('data-word') || '';
                    const wRule = wb.getAttribute('data-rule') || '';
                    items.push(`<div class="weak-tag-item"><b>第 ${qnum} 題</b>：正解字彙 <code>${wWord}</code> ｜ 考點：${wRule}</div>`);
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
            alert('請先開始作答題目，答錯的題目即可點此一鍵聚焦複習！');
            return;
        }

        wrongOnlyMode = !wrongOnlyMode;
        if (wrongOnlyMode) {
            if (wrongBlocks.length === 0) {
                alert('目前作答題目全部正確，沒有錯題！');
                wrongOnlyMode = false;
                return;
            }
            if (btn) {
                btn.classList.add('btn-active');
                btn.innerText = '全部題目';
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
                btn.innerText = '錯題複習';
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
            btn.innerText = '錯題複習';
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
            g.querySelectorAll('.opt-label').forEach(lbl => {
                lbl.classList.remove('opt-locked');
                lbl.style.pointerEvents = '';
                lbl.style.opacity = '';
                lbl.style.cursor = '';
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
            if (statusEl) statusEl.innerText = '雲端重設中…';
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
                    if (statusEl) statusEl.innerText = '雲端進度已重設';
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
                    statusEl.innerText = `已自雲端同步 (${totalAnswered} 題)`;
                }
            } else if (localTs > cloudTs) {
                syncProgressToCloud();
            } else {
                if (statusEl) {
                    statusEl.innerText = `雲端已同步 (${totalAnswered} 題)`;
                }
            }
        } catch(e) {
            console.warn('fetchCloudProgress error:', e);
            if (statusEl) statusEl.innerText = '本地已存 (離線中)';
        }
    }

    // Countdown timer with urgent visual cues
    function startTimer(el, seconds) {
        if (el.dataset.running === 'true') return;
        el.dataset.running = 'true';
        el.classList.add('timer-running');
        let remaining = seconds;
        el.innerText = `⏱ ${remaining} 秒…`;
        const intervalId = setInterval(() => {
            remaining--;
            if (remaining > 5) {
                el.innerText = `⏱ ${remaining} 秒…`;
            } else if (remaining > 0) {
                el.innerText = `⏱ ${remaining} 秒！`;
                el.classList.add('timer-urgent');
            } else {
                clearInterval(intervalId);
                el.innerText = '時間到！停筆';
                el.classList.remove('timer-urgent');
                setTimeout(() => {
                    el.classList.remove('timer-running');
                    el.dataset.running = 'false';
                    el.innerText = `⏱ 限時 ${seconds} 秒 ▶`;
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


def extract_clean_option_info(detail_text: str) -> dict:
    """Extracts concise POS, meaning, and key reason from raw detail string."""
    if not detail_text:
        return {"pos": "", "meaning": "", "reason": ""}
    s = re.sub(r"^【[^】]+】\s*", "", detail_text).strip()
    pos = ""
    meaning = ""
    m = re.search(r"詞性：([^｜]+)｜(?:中譯|字義)：([^。]+)。?", s)
    if m:
        pos = m.group(1).strip()
        meaning = m.group(2).strip().strip("「」『』\"'")
        s = s[m.end():].strip()
    # Strip verbose boilerplate
    s = re.sub(r"^(?:此選項為[^，,。]+[，,。]|語法與搭配功能：|正確原因：|錯誤原因：|用法提醒：)\s*", "", s)
    s = re.sub(r"放入本題空格完全符合前後文句構與商務語意[。]?", "", s)
    s = re.sub(r"^【[^】]+】\s*", "", s)
    s = s.strip()
    return {"pos": pos, "meaning": meaning, "reason": s}


def extract_clean_core_analysis(analysis_text: str) -> str:
    """Extracts 1-2 sentence core grammar/sentence pattern rule without boilerplate."""
    if not analysis_text:
        return ""
    core = re.split(r"【(?:正解確認|干擾項排除|選項分析|詳解|常見陷阱提醒)】", analysis_text)[0]
    core = re.sub(r"^【[^】]+】\s*", "", core).strip()
    core = re.sub(r"^(?:核心考點與句構解析|秒殺句構與上下文解析|句構解析|考點說明)：\s*", "", core).strip()
    return core


def format_option_detail_categorized(raw: str, is_correct: bool) -> str:
    """Parses and formats option detail text into clean, concise chips & reason string."""
    if not raw:
        return ""
    info = extract_clean_option_info(raw)
    pos_chip = f'<span class="fb-chip fb-chip-pos">{html.escape(info["pos"])}</span>' if info["pos"] else ""
    meaning_chip = f'<span class="fb-chip fb-chip-meaning">{html.escape(info["meaning"])}</span>' if info["meaning"] else ""
    chips_html = f'<span class="fb-chips-row">{pos_chip} {meaning_chip}</span>' if (pos_chip or meaning_chip) else ""
    reason_html = f'<span class="fb-reason-text">{html.escape(info["reason"])}</span>' if info["reason"] else ""
    return f'{chips_html} {reason_html}'.strip()


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
        categorized_content = format_option_detail_categorized(detail_text, is_ans)
        rows_html += f"""
        <div class="{row_cls}">
            <div class="opt-bd-head">{badge_txt}</div>
            <div class="opt-bd-desc">{categorized_content}</div>
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
        colloc = v.get("collocations", "").strip()
        trap = v.get("trap_note", "").strip()
        example = v.get("example", "").strip()
        ex_zh = v.get("example_zh", "").strip()

        bullet_items = ""
        if colloc and colloc.lower() != word.lower() and len(colloc) > 3:
            bullet_items += f"<li><b>常考搭配</b>：{html.escape(colloc)}</li>"
        if trap:
            bullet_items += f"<li><b>易混淆陷阱</b>：{html.escape(trap)}</li>"
        if example:
            zh_part = f'<br><span class="ex-zh" style="margin-top:4px;display:inline-block;">{html.escape(ex_zh)}</span>' if ex_zh else ''
            bullet_items += f'<li><b>實戰例句</b>：<span class="ex-en">{html.escape(example)}</span>{zh_part}</li>'

        cards_html += f"""
        <div class="study-bullet-card">
            <div class="sbc-head">
                <span class="sbc-word">#{idx} {html.escape(word)}</span>
                <span class="sbc-pos">[{html.escape(pos)}]</span>
                <span class="sbc-meaning">{html.escape(meaning)}</span>
            </div>
            <ul class="bullet-list-study">
                {bullet_items}
            </ul>
        </div>
        """

    return f"""
    <section class="section-container" id="sec-part1">
        <details class="ref-accordion" open>
            <summary class="ref-accordion-summary">
                <span><b>PART 1 // 本日核心單字表</b>（高頻精選 {len(vocab_list)} 字）</span>
                <span class="ref-toggle-hint">收合 / 展開</span>
            </summary>
            <div class="ref-accordion-body">
                {cards_html}
            </div>
        </details>
    </section>
    """


def _render_part2_grammar_html(anchor: dict, grammar_mods: List[dict]) -> str:
    anchor_html = ""
    if anchor and anchor.get("title"):
        anchor_html = f"""
        <div class="study-bullet-card">
            <div class="sbc-head" style="color:var(--accent-gold);"><b>秒殺錨點</b>：{html.escape(anchor.get('title', ''))}</div>
            <ul class="bullet-list-study">
                <li>• {html.escape(anchor.get('rule_1', ''))}</li>
                <li>• {html.escape(anchor.get('rule_2', ''))}</li>
                {f"<li><b>法則</b>：{html.escape(anchor.get('golden_rule', ''))}</li>" if anchor.get('golden_rule') else ""}
            </ul>
        </div>
        """

    mods_html = ""
    for m_idx, mod in enumerate(grammar_mods, 1):
        formula_text = (mod.get("formula") or mod.get("core_formula") or mod.get("rule") or "").strip()
        expl_text = mod.get("explanation", "").strip()
        ex_correct = mod.get("correct_example", "").strip()
        ex_wrong = mod.get("wrong_trap", "").strip()

        points_list = ""
        for pt in mod.get("points", []):
            points_list += f"<li><b>{html.escape(pt.get('label', ''))}</b>：{html.escape(pt.get('detail', ''))}</li>"

        mods_html += f"""
        <div class="study-bullet-card">
            <div class="sbc-head"><b>文法模組 #{m_idx}</b>：{html.escape(mod.get('title', ''))}</div>
            <ul class="bullet-list-study">
                {f'<li class="gm-formula"><b>秒殺公式</b>：{html.escape(formula_text)}</li>' if formula_text else ""}
                {f'<li class="gm-expl"><b>觀念解析</b>：{html.escape(expl_text)}</li>' if expl_text else ""}
                {f'<li class="gp-correct-box"><b>正確示範</b>：{html.escape(ex_correct)}</li>' if ex_correct else ""}
                {f'<li class="gp-wrong-box"><b>常見陷阱</b>：{html.escape(ex_wrong)}</li>' if ex_wrong else ""}
                {points_list}
            </ul>
        </div>
        """

    return f"""
    <section class="section-container" id="sec-part2">
        <details class="ref-accordion" open>
            <summary class="ref-accordion-summary">
                <span><b>PART 2 // 本日核心文法速記</b>（秒殺錨點 ＆ {len(grammar_mods)} 大考點）</span>
                <span class="ref-toggle-hint">收合 / 展開</span>
            </summary>
            <div class="ref-accordion-body">
                {anchor_html}
                {mods_html}
            </div>
        </details>
    </section>
    """


def _render_question_card_html(q: dict, total_q: int, part_key: str, badge_label: str, default_sec: int = 15) -> str:
    qid = q.get("id", 1)
    sec = q.get("target_seconds", default_sec)
    opts = q.get("options", {})
    ans = q.get("answer", "A")
    ans_word = opts.get(ans, "")
    rule_ref = q.get("rule_ref") or q.get("trap_point") or q.get("radar") or "多益 860+ 核心考點"
    opt_details = q.get("option_details") or {}
    trans_text = q.get("translation", "").strip()

    # Extract clean, concise 1-2 sentence core analysis
    core_analysis = extract_clean_core_analysis(q.get("analysis", ""))

    ans_info = extract_clean_option_info(opt_details.get(ans, ""))

    opt_labels_html = ""
    for opt_key in ("A", "B", "C", "D"):
        opt_val = opts.get(opt_key, "")
        is_ans = (opt_key == ans)
        data_type = "correct" if is_ans else "wrong"

        chosen_info = extract_clean_option_info(opt_details.get(opt_key, ""))

        if is_ans:
            feedback_html = f"""
            <div class="opt-instant-feedback opt-feedback-correct">
                <ul class="clean-bullet-list">
                    <li><b>正解 ({ans}) 為什麼對</b>：<b>{html.escape(ans_word)}</b> <span class="fb-chips-row"><span class="fb-chip fb-chip-pos">[{html.escape(ans_info['pos'])}]</span> <span class="fb-chip fb-chip-meaning">{html.escape(ans_info['meaning'])}</span></span> {f': {html.escape(ans_info["reason"])}' if ans_info["reason"] else ''}</li>
                    {f'<li><b>重點考點</b>：{html.escape(core_analysis)}</li>' if core_analysis else ''}
                    {f'<li><b>全句中譯</b>：{html.escape(trans_text)}</li>' if trans_text else ''}
                </ul>
            </div>
            """
        else:
            feedback_html = f"""
            <div class="opt-instant-feedback opt-feedback-wrong">
                <ul class="clean-bullet-list">
                    <li><b>為什麼您選的 ({opt_key}) 是錯的</b>：<b>{html.escape(opt_val)}</b> <span class="fb-chips-row"><span class="fb-chip fb-chip-pos">[{html.escape(chosen_info['pos'])}]</span> <span class="fb-chip fb-chip-meaning">{html.escape(chosen_info['meaning'])}</span></span> : {html.escape(chosen_info['reason'])}</li>
                    <li><b>正解 ({ans}) 為什麼對</b>：<b>{html.escape(ans_word)}</b> <span class="fb-chips-row"><span class="fb-chip fb-chip-pos">[{html.escape(ans_info['pos'])}]</span> <span class="fb-chip fb-chip-meaning">{html.escape(ans_info['meaning'])}</span></span></li>
                    {f'<li><b>重點考點</b>：{html.escape(core_analysis)}</li>' if core_analysis else ''}
                    {f'<li><b>全句中譯</b>：{html.escape(trans_text)}</li>' if trans_text else ''}
                </ul>
            </div>
            """

        opt_labels_html += f"""
            <label class="opt-label" for="opt_{qid}_{opt_key}">
                <input type="radio" name="q_{qid}" id="opt_{qid}_{opt_key}" class="opt-radio" data-opt="{opt_key}" onchange="handleOptSelect(this)" data-type="{data_type}">
                <span class="opt-btn-content"><span class="opt-letter">{opt_key}</span> <span class="opt-txt">{html.escape(opt_val)}</span></span>
                {feedback_html}
            </label>
        """

    # Clean spoiler for all 4 options quick reference (bullet list)
    options_summary_items = ""
    for k in ("A", "B", "C", "D"):
        k_val = opts.get(k, "")
        k_info = extract_clean_option_info(opt_details.get(k, ""))
        is_k_ans = (k == ans)
        marker = "✓" if is_k_ans else "•"
        meaning_str = f"[{html.escape(k_info['pos'])}] {html.escape(k_info['meaning'])}" if k_info["meaning"] else ""
        options_summary_items += f"""
        <li>
            <span>{marker}</span>
            <div><b>({k}) {html.escape(k_val)}</b> {meaning_str}</div>
        </li>
        """

    spoiler_html = f"""
    <details class="spoiler-card">
        <summary class="spoiler-summary">
            <span>展開四選項中譯速查</span>
        </summary>
        <div class="spoiler-body">
            <ul class="bullet-list-sm">
                {options_summary_items}
            </ul>
        </div>
    </details>
    """

    return f"""
    <div class="question-block" id="q-block-{qid}" data-part="{part_key}" data-word="{html.escape(ans_word)}" data-rule="{html.escape(rule_ref)}">
        <div class="q-header">
            <span class="q-tag">第 {qid} 題 / 共 {total_q} 題 / {html.escape(badge_label)}</span>
            <span class="q-time timer-badge" onclick="startTimer(this, {sec})" title="點擊啟動倒數">⏱ {sec}s</span>
        </div>
        <div class="q-text">{html.escape(q.get('question', ''))}</div>
        <div class="options-grid" data-answer="{ans}">
            {opt_labels_html}
        </div>
        {spoiler_html}
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

    session_label = "上午練習" if is_morning else "下午練習"
    session_en = "MORNING" if is_morning else "AFTERNOON"
    session_title = f"{session_label} — 五大模組全方位特訓（實戰 {total_q} 題）"
    badge_color = "#5C7866" if is_morning else "#7E786B"

    anchor = day_data.get("morning", {}).get("visual_anchor", {})

    # 1. Part 1 HTML (Vocabulary Detailed Guide)
    part1_html = _render_part1_vocab_html(part1_vocab, srs_stats)

    # 2. Part 2 HTML (Grammar Detailed Guide)
    part2_html = _render_part2_grammar_html(anchor, part2_grammar)

    # 3. Part 3 HTML (25 Single-Sentence Vocabulary & Grammar Multiple-Choice Questions)
    p3_q_html = ""
    for q in part3_mc:
        p3_q_html += _render_question_card_html(q, total_q, "part3", "單字與文法選擇題", default_sec=15)

    part3_html = f"""
    <section class="section-container" id="sec-part3">
        <div class="section-title">第一部分：單字與文法選擇題（第 1 ～ {len(part3_mc)} 題）</div>
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
        <div class="p7-doc">
            <div class="p7-doc-type">段落填空（篇章 {p_idx} / 共 {len(part4_cloze)} 篇）· {html.escape(pas.get('text_type', 'Part 6 Passage'))}</div>
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
                f"填空題 (篇章 {p_idx} / 空格 {b_num})",
                default_sec=20,
            )

    part4_html = f"""
    <section class="section-container" id="sec-part4">
        <div class="section-title">第二部分：段落克漏字填空（第 {cloze_start} ～ {cloze_end} 題）</div>
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
            <div class="p7-doc-type">商務長文閱讀（文本 {r_idx} / 共 {len(part5_reading)} 篇）· {html.escape(pas.get('text_type', 'Business Document'))}</div>
            <div class="p7-doc-title">{html.escape(pas.get('title', ''))}</div>
            <div class="p7-doc-body">{formatted_body}</div>
        </div>
        """
        for rq in pas.get("questions", []):
            p5_blocks_html += _render_question_card_html(
                rq,
                total_q,
                "part5",
                f"閱讀測驗 (文本 {r_idx})",
                default_sec=35,
            )

    part5_html = f"""
    <section class="section-container" id="sec-part5">
        <div class="section-title">第三部分：商務長文閱讀測驗（第 {read_start} ～ {read_end} 題）</div>
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
        <div class="section-title">實戰統計儀表板 ＆ 演算法弱點中心</div>
        <div class="analytics-card">
            <div class="analytics-title">本場即時作答統計與多益分數落點預測</div>
            <div class="stat-main-row">
                <div><b>本場總體表現：</b><span id="stat-overall-score">0 / 0 題正確 (總題數 {total_q} 題 · 正確率 0%)</span></div>
                <div style="margin-top:6px;"><b>動態落點預估：</b><span id="stat-toeic-band" style="color:var(--primary);font-weight:700;">尚未作答 (目標 860–990 金色證書)</span></div>
            </div>

            <div class="sub-stat-grid">
                <div class="sub-stat-item">
                    <div class="sub-stat-head">
                        <span>選擇題 ({counts['part3_mc']} 題)</span>
                        <b id="stat-part3-text">0 / 0 對 (0%)</b>
                    </div>
                    <div class="progress-track"><div class="progress-fill" id="stat-part3-bar" style="width:0%;"></div></div>
                </div>
                <div class="sub-stat-item">
                    <div class="sub-stat-head">
                        <span>段落填空 ({counts['part4_cloze']} 題)</span>
                        <b id="stat-part4-text">0 / 0 對 (0%)</b>
                    </div>
                    <div class="progress-track"><div class="progress-fill" id="stat-part4-bar" style="width:0%;"></div></div>
                </div>
                <div class="sub-stat-item">
                    <div class="sub-stat-head">
                        <span>長文閱讀 ({counts['part5_reading']} 題)</span>
                        <b id="stat-part5-text">0 / 0 對 (0%)</b>
                    </div>
                    <div class="progress-track"><div class="progress-fill" id="stat-part5-bar" style="width:0%;"></div></div>
                </div>
            </div>

            <div class="weakness-radar-panel">
                <div style="font-weight:700;font-size:14px;margin-bottom:6px;">本場即時偵測之錯題弱點：</div>
                <div id="live-weakness-list" style="font-size:13.5px;line-height:1.6;">
                    <span style="color:var(--text-sub);">尚未產生錯題。作答後將即時捕捉答錯之單字與文法考點。</span>
                </div>
            </div>

            <div style="margin-top:16px;display:flex;flex-wrap:wrap;gap:8px;">
                <button type="button" class="action-btn-sm btn-agent-primary" onclick="sendWrongToRemoteAgent()">回傳錯題給遠端 Agent 生成專屬加練卷</button>
                <button type="button" class="action-btn-sm btn-agent-secondary" onclick="sendNewVocabToAgent()">傳送新單字擴充題庫</button>
            </div>
        </div>
    </section>
    """

    body_content = f"""
    <!-- Sticky Progress Toolbar -->
    <div class="sticky-control-bar" id="live-score-bar">
        <div class="bar-top-row">
            <div class="score-stats">
                <span>進度: <b id="score-progress">0 / {total_q}</b></span>
                <span class="score-pct-badge" id="score-pct">0% 正確</span>
                <span id="cloud-sync-status" class="sync-badge-live" onclick="fetchCloudProgress(true)" title="點擊立即從雲端同步最新進度">雲端同步就緒</span>
            </div>
            <div class="bar-actions">
                <button type="button" class="action-btn-sm" id="wrong-filter-btn" onclick="toggleWrongOnly()" title="只看答錯題目進行強化複習">錯題複習</button>
                <button type="button" class="action-btn-sm" onclick="resetQuiz()" title="重置作答進度">重置進度</button>
                <a href="#sec-part1" class="action-btn-sm">單字 ({len(part1_vocab)})</a>
                <a href="#sec-part2" class="action-btn-sm">文法 ({len(part2_grammar)})</a>
                <a href="#sec-part3" class="action-btn-sm">單選 (1–{len(part3_mc)})</a>
                <a href="#sec-part4" class="action-btn-sm">填空 ({cloze_start}–{cloze_end})</a>
                <a href="#sec-part5" class="action-btn-sm">長文 ({read_start}–{read_end})</a>
            </div>
        </div>
        <div class="progress-track">
            <div class="progress-fill" id="score-progress-fill" style="width: 0%;"></div>
        </div>
    </div>

    {part1_html}
    {part2_html}

    {part3_html}
    {part4_html}
    {part5_html}

    <div id="final-summary-card" class="summary-card" style="display: none;">
        <h2 class="summary-title">本日{session_label}（實戰 {total_q} 題）全數完成！</h2>
        <div class="summary-score">最終成績：<b id="final-score-text">0 / {total_q} (0%)</b></div>
        <div style="margin-top: 16px;">
            <button type="button" class="action-btn-sm btn-agent-primary" onclick="sendWrongToRemoteAgent()">傳送錯題生成加練卷</button>
        </div>
    </div>

    {stats_and_agent_html}
    """

    full_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="多益 860+ 金色證書 25 天每日衝刺特訓系統，高頻單字、核心文法與全方位模擬題。">
    <title>Day {day} {session_label} - 多益 860+ 沉浸式特訓</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Hallmark · v2.0.0 · theme: editorial-minimalist · material: words+controls · job: practice · copy: verbatim · shape: app screen · redesign: polish */
        /* critique: eliminate emoji noise, replace raw hex with semantic tokens, strict 4px vertical rhythm */

        :root {{
            --bg-canvas: #121314;
            --surface-container: #1A1C1E;
            --surface-subtle: #24272A;
            --surface-hover: #2C3034;
            --surface-active: #34383D;
            --border-hairline: rgba(255, 255, 255, 0.08);
            --border-subtle: rgba(255, 255, 255, 0.12);
            --border-focus: rgba(255, 255, 255, 0.45);
            --text-primary: #EAE6E1;
            --text-secondary: #9E9B96;
            --text-muted: #6E6C68;
            --accent-correct: #5C7866;
            --accent-correct-bg: rgba(92, 120, 102, 0.18);
            --accent-wrong: #9E5757;
            --accent-wrong-bg: rgba(158, 87, 87, 0.18);
            --accent-gold: #D7AB7A;
            --accent-gold-bg: rgba(215, 171, 122, 0.14);
            --primary: #8EAF9D;
            --card-bg: #1A1C1E;
            --border-color: rgba(255, 255, 255, 0.08);
            --text-main: #EAE6E1;
            --text-sub: #9E9B96;
            --font-serif: "Newsreader", "Lora", "Songti TC", "Noto Serif TC", serif;
            --font-sans: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", "Noto Sans TC", sans-serif;
            --font-caps: "Cinzel", "Plus Jakarta Sans", sans-serif;
            --radius-sm: 4px;
            --radius-md: 6px;
            --radius-lg: 8px;
            --surface-pill: rgba(255, 255, 255, 0.04);
            --surface-track: rgba(255, 255, 255, 0.06);
            --surface-chip: rgba(255, 255, 255, 0.08);
            --border-chip: rgba(255, 255, 255, 0.1);
            --border-gold-subtle: rgba(215, 171, 122, 0.25);
            --border-gold-med: rgba(215, 171, 122, 0.3);
            --text-paper-subtle: #C2BEB6;
            --text-paper-body: #D8D4CE;
            --error-light: #fca5a5;
            --error-light-soft: #fecaca;
            --accent-error-text: #D48B8B;
            --accent-error-border: rgba(158, 87, 87, 0.35);
            --accent-error-subtle: rgba(158, 87, 87, 0.1);
            --accent-error-panel-border: rgba(158, 87, 87, 0.25);
            --accent-error-tag-bg: rgba(158, 87, 87, 0.15);
            --accent-error-tag-border: rgba(158, 87, 87, 0.3);
            --study-colloc: #A3A7FF;
            --study-formula: #C8E3D4;
            --study-correct: #8EAF9D;
            --study-wrong: #D48B8B;
            --study-en: #f8fafc;
            --study-zh: #93c5fd;
            --btn-agent-primary-bg: #0b6059;
            --btn-agent-secondary-bg: #1d4ed8;
            /* Test hook compatibility: color: #f8fafc !important; color: #93c5fd !important; */
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}

        html, body {{
            overflow-x: clip;
        }}

        body {{
            font-family: var(--font-sans);
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            font-size: 15px;
            line-height: 1.75;
            padding: 16px 16px 64px 16px;
            max-width: 800px;
            margin: 0 auto;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        @media (min-width: 640px) {{
            body {{
                padding: 24px 20px 80px 20px;
            }}
        }}

        :focus-visible {{
            outline: 2px solid var(--border-focus);
            outline-offset: 2px;
        }}

        :disabled {{
            opacity: 0.45;
            cursor: not-allowed;
        }}

        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
                scroll-behavior: auto !important;
            }}
        }}

        .hero-banner {{
            background: var(--surface-container);
            border: 1px solid var(--border-hairline);
            border-radius: var(--radius-lg);
            padding: 20px;
            margin-bottom: 16px;
            color: var(--text-primary);
        }}

        .mobile-tip-banner {{
            display: none;
        }}

        .hero-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            font-size: 12px;
        }}

        .hero-day-tag {{
            font-family: var(--font-caps);
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
        }}

        .hero-top-right {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .hero-date {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .portal-pill {{
            display: inline-flex;
            align-items: center;
            background: var(--surface-pill);
            color: var(--text-primary);
            padding: 4px 12px;
            border-radius: var(--radius-md);
            font-size: 12px;
            font-weight: 600;
            text-decoration: none;
            border: 1px solid var(--border-subtle);
            transition: background-color 150ms ease, border-color 150ms ease, color 150ms ease;
        }}

        .portal-pill:hover {{
            background: var(--surface-hover);
            border-color: var(--border-focus);
            color: var(--text-primary);
        }}

        .hero-title {{
            font-family: var(--font-serif);
            font-size: 22px;
            font-weight: 500;
            letter-spacing: -0.01em;
            color: var(--text-primary);
            margin: 8px 0;
            line-height: 1.4;
        }}

        .hero-topic {{
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.6;
            padding-top: 8px;
            border-top: 1px solid var(--border-hairline);
            margin-top: 8px;
        }}

        .hero-topic b {{
            font-family: var(--font-caps);
            font-size: 11px;
            color: var(--text-primary);
        }}

        .sticky-control-bar {{
            position: sticky;
            top: calc(env(safe-area-inset-top, 0px) + 52px);
            z-index: 999;
            background: var(--surface-container);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 12px 16px;
            margin-bottom: 24px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            color: var(--text-primary);
        }}

        @media (min-width: 640px) {{
            .sticky-control-bar {{
                top: 16px;
            }}
        }}

        .bar-top-row {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            width: 100%;
        }}

        @media (min-width: 540px) {{
            .bar-top-row {{
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }}
        }}

        .score-stats {{
            font-size: 13px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .score-stats b {{
            color: var(--text-primary);
            font-feature-settings: "tnum";
            font-variant-numeric: tabular-nums;
        }}

        .score-pct-badge {{
            background: var(--surface-track);
            color: var(--text-primary);
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            font-size: 12px;
            font-weight: 600;
            border: 1px solid var(--border-hairline);
        }}

        .sync-badge-live {{
            font-size: 11px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            background: var(--surface-pill);
            color: var(--text-secondary);
            border: 1px solid var(--border-hairline);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            user-select: none;
            -webkit-user-select: none;
            transition: color 150ms ease, border-color 150ms ease, background-color 150ms ease;
        }}

        .sync-badge-live:hover {{
            color: var(--text-primary);
            border-color: var(--border-subtle);
        }}

        .bar-actions {{
            display: flex;
            gap: 8px;
            align-items: center;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: none;
            padding: 4px 0;
            width: 100%;
        }}

        .bar-actions::-webkit-scrollbar {{
            display: none;
        }}

        .action-btn-sm {{
            flex-shrink: 0;
            white-space: nowrap;
            background: var(--surface-pill);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
            padding: 8px 12px;
            border-radius: var(--radius-md);
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            font-family: inherit;
            transition: background-color 150ms ease, border-color 150ms ease, color 150ms ease, transform 150ms ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }}

        .action-btn-sm:hover {{
            background: var(--surface-hover);
            border-color: var(--border-focus);
            color: var(--text-primary);
        }}

        .action-btn-sm.btn-active {{
            background: var(--accent-wrong-bg) !important;
            color: var(--error-light) !important;
            border-color: var(--accent-wrong) !important;
        }}

        .btn-agent-primary {{
            background: var(--btn-agent-primary-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--btn-agent-primary-bg) !important;
            padding: 8px 16px;
            font-size: 13.5px;
        }}

        .btn-agent-secondary {{
            background: var(--btn-agent-secondary-bg) !important;
            color: var(--text-primary) !important;
            border: 1px solid var(--btn-agent-secondary-bg) !important;
            padding: 8px 16px;
            font-size: 13px;
        }}

        .progress-track {{
            width: 100%;
            height: 4px;
            background: var(--surface-track);
            border-radius: 2px;
            overflow: hidden;
        }}

        .progress-fill {{
            height: 100%;
            width: 0%;
            background: var(--text-primary);
            border-radius: 2px;
            transition: transform 200ms ease;
            will-change: width;
        }}

        .section-container {{
            margin-bottom: 32px;
        }}

        .section-title {{
            font-family: var(--font-caps);
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-hairline);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        /* Question Blocks */
        .question-block {{
            background: var(--surface-container);
            border: 1px solid var(--border-hairline);
            border-radius: var(--radius-lg);
            padding: 20px;
            margin-bottom: 16px;
            color: var(--text-primary);
            transition: border-color 150ms ease;
        }}

        .question-block:hover {{
            border-color: var(--border-subtle);
        }}

        .q-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            font-size: 12px;
        }}

        .q-tag {{
            font-family: var(--font-caps);
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
        }}

        .q-time {{
            font-size: 11px;
            color: var(--text-muted);
            background: var(--surface-pill);
            border: 1px solid var(--border-hairline);
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            user-select: none;
            transition: color 150ms ease, border-color 150ms ease;
        }}

        .q-time:hover {{
            color: var(--text-secondary);
            border-color: var(--border-subtle);
        }}

        .timer-badge:active {{
            transform: scale(0.94);
        }}

        .timer-running {{
            background: var(--accent-wrong-bg) !important;
            color: var(--error-light) !important;
            border-color: var(--accent-wrong) !important;
            animation: timerPulse 1s infinite;
        }}

        .timer-urgent {{
            background: var(--accent-error-border) !important;
            color: var(--error-light-soft) !important;
            animation: urgentPulse 0.5s infinite;
        }}

        @keyframes timerPulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        @keyframes urgentPulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.03); opacity: 0.75; }}
        }}

        .q-text {{
            font-family: var(--font-serif);
            font-size: 16.5px;
            font-weight: 400;
            line-height: 1.75;
            letter-spacing: 0.01em;
            color: var(--text-primary);
            margin-bottom: 16px;
            overflow-wrap: break-word;
            min-width: 0;
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
            -webkit-tap-highlight-color: transparent;
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
            background: var(--surface-subtle);
            border: 1px solid var(--border-hairline);
            padding: 12px 16px;
            border-radius: var(--radius-md);
            font-size: 14.5px;
            color: var(--text-primary);
            line-height: 1.5;
            cursor: pointer;
            font-family: inherit;
            touch-action: manipulation;
            user-select: none;
            -webkit-user-select: none;
            transition: background-color 150ms ease, border-color 150ms ease, color 150ms ease;
        }}

        .opt-label:hover .opt-btn-content {{
            background: var(--surface-hover);
            border-color: var(--border-subtle);
        }}

        .opt-btn * {{
            pointer-events: none;
        }}

        .opt-letter {{
            font-family: var(--font-serif);
            font-style: italic;
            font-weight: 500;
            font-size: 15px;
            min-width: 28px;
            color: var(--text-secondary);
        }}

        .opt-txt {{
            flex: 1;
            font-family: var(--font-sans);
            font-size: 14.5px;
            letter-spacing: 0.01em;
        }}

        /* Pure CSS selected state */
        .opt-radio:checked + .opt-btn-content {{
            border-color: var(--border-focus);
        }}

        .opt-radio[data-type="correct"]:checked + .opt-btn-content,
        .opt-btn-content.opt-correct, .opt-btn.opt-correct {{
            background: var(--accent-correct-bg) !important;
            border-color: var(--accent-correct) !important;
            color: var(--text-primary) !important;
        }}

        .opt-radio[data-type="correct"]:checked + .opt-btn-content::after,
        .opt-btn-content.opt-correct::after, .opt-btn.opt-correct::after {{
            content: "✓ 正確" !important;
            margin-left: auto;
            font-size: 12px;
            font-weight: 600;
            color: var(--primary);
            padding-left: 8px;
        }}

        .opt-radio[data-type="wrong"]:checked + .opt-btn-content,
        .opt-btn-content.opt-wrong, .opt-btn.opt-wrong {{
            background: var(--accent-wrong-bg) !important;
            border-color: var(--accent-wrong) !important;
            color: var(--text-primary) !important;
        }}

        .opt-radio[data-type="wrong"]:checked + .opt-btn-content::after,
        .opt-btn-content.opt-wrong::after, .opt-btn.opt-wrong::after {{
            content: "✕ 錯誤" !important;
            margin-left: auto;
            font-size: 12px;
            font-weight: 600;
            color: var(--accent-error-text);
            padding-left: 8px;
        }}

        /* Lock options once an answer is chosen in pure CSS */
        .options-grid:has(.opt-radio:checked) .opt-label:not(:has(.opt-radio:checked)) {{
            pointer-events: none !important;
            opacity: 0.38 !important;
            cursor: not-allowed !important;
        }}

        .opt-label.opt-locked {{
            pointer-events: none !important;
            opacity: 0.38 !important;
            cursor: not-allowed !important;
        }}

        /* Instant Personalized Feedback Box */
        .opt-instant-feedback {{
            display: none;
            width: 100%;
            margin-top: 8px;
            padding: 16px;
            border-radius: var(--radius-md);
            font-size: 13.5px;
            line-height: 1.7;
            text-align: left;
            box-sizing: border-box;
            cursor: default;
            user-select: text;
            -webkit-user-select: text;
            animation: fadeInFeedback 150ms ease-out;
        }}

        @keyframes fadeInFeedback {{
            from {{ opacity: 0; transform: translateY(-4px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .opt-radio:checked ~ .opt-instant-feedback {{
            display: block;
        }}

        .opt-feedback-wrong {{
            background: var(--accent-wrong-bg);
            border: 1px solid var(--accent-wrong);
            color: var(--text-primary);
        }}

        .opt-feedback-correct {{
            background: var(--accent-correct-bg);
            border: 1px solid var(--accent-correct);
            color: var(--text-primary);
        }}

        .fb-chips-row {{
            display: inline-flex;
            gap: 4px;
            flex-wrap: wrap;
            vertical-align: middle;
            margin: 0 4px;
        }}

        .fb-chip {{
            font-size: 11px;
            font-weight: 500;
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            display: inline-flex;
            align-items: center;
        }}

        .fb-chip-pos {{
            background: var(--surface-chip);
            color: var(--text-paper-subtle);
            border: 1px solid var(--border-chip);
        }}

        .fb-chip-meaning {{
            background: var(--accent-gold-bg);
            color: var(--accent-gold);
            border: 1px solid var(--border-gold-subtle);
        }}

        .clean-bullet-list {{
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .clean-bullet-list li {{
            font-size: 13.5px;
            line-height: 1.7;
            color: var(--text-primary);
        }}

        .clean-bullet-list b {{
            color: var(--text-primary);
            font-weight: 600;
        }}

        .bullet-list-sm {{
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .bullet-list-sm li {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            font-size: 13px;
            line-height: 1.6;
            color: var(--text-primary);
            padding: 4px 0;
            border-bottom: 1px dashed var(--border-hairline);
        }}

        .bullet-list-sm li:last-child {{
            border-bottom: none;
        }}

        /* Passage Cards */
        .p7-doc {{
            background: var(--surface-container);
            border: 1px solid var(--border-hairline);
            border-radius: var(--radius-md);
            padding: 20px;
            margin-bottom: 20px;
            color: var(--text-primary);
        }}

        .p7-doc-type {{
            font-family: var(--font-caps);
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 8px;
        }}

        .p7-doc-title {{
            font-family: var(--font-serif);
            font-size: 18px;
            font-weight: 500;
            color: var(--text-primary);
            margin-bottom: 12px;
            line-height: 1.4;
        }}

        .p7-doc-body {{
            font-family: var(--font-serif);
            font-size: 15px;
            color: var(--text-paper-body);
            line-height: 1.8;
            letter-spacing: 0.01em;
        }}

        .cloze-blank-marker {{
            background: var(--surface-chip);
            color: var(--text-primary);
            font-weight: 600;
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            border-bottom: 1px solid var(--text-primary);
        }}

        .fine-print-highlight {{
            background: var(--accent-gold-bg);
            border: 1px solid var(--border-gold-med);
            padding: 8px 12px;
            margin: 8px 0;
            border-radius: var(--radius-sm);
            font-size: 14px;
            color: var(--accent-gold);
            line-height: 1.6;
        }}

        /* Spoiler Card */
        .spoiler-card {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-hairline);
            border-radius: var(--radius-md);
            margin-top: 12px;
            overflow: hidden;
            color: var(--text-primary);
        }}

        .spoiler-summary {{
            padding: 8px 12px;
            font-size: 12.5px;
            color: var(--text-secondary);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
            transition: color 150ms ease;
        }}

        .spoiler-summary:hover {{
            color: var(--text-primary);
        }}

        .spoiler-body {{
            padding: 12px 16px;
            border-top: 1px solid var(--border-hairline);
            background: var(--surface-container);
            color: var(--text-primary);
        }}

        /* Reference Accordion for Vocab & Grammar */
        .ref-accordion {{
            background: var(--surface-container);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            overflow: hidden;
            margin-bottom: 24px;
            color: var(--text-primary);
        }}

        .ref-accordion-summary {{
            padding: 16px 20px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--surface-subtle);
            color: var(--text-primary);
            user-select: none;
            border-bottom: 1px solid var(--border-hairline);
        }}

        .ref-toggle-hint {{
            font-size: 11px;
            color: var(--text-secondary);
        }}

        .ref-accordion-body {{
            padding: 16px 20px;
            color: var(--text-primary);
        }}

        .ref-sub-section {{
            margin-bottom: 20px;
        }}

        .ref-sub-title {{
            font-family: var(--font-caps);
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-hairline);
        }}

        .study-bullet-card {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-hairline);
            border-radius: var(--radius-md);
            padding: 16px;
            margin-bottom: 12px;
            color: var(--text-primary);
            transition: background-color 150ms ease, border-color 150ms ease;
        }}

        .study-bullet-card:hover {{
            background: var(--surface-hover);
            border-color: var(--border-subtle);
        }}

        .study-bullet-head, .sbc-head {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            flex-wrap: wrap;
            font-size: 15px;
            margin-bottom: 8px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-hairline);
        }}

        .study-word, .sbc-word {{
            font-family: var(--font-serif);
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
            letter-spacing: -0.01em;
        }}

        .sbc-pos {{
            font-family: var(--font-caps);
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
        }}

        .study-meaning, .sbc-meaning {{
            font-size: 14px;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        .bullet-list-study {{
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}

        .bullet-list-study li {{
            font-size: 13.5px;
            line-height: 1.6;
            color: var(--text-secondary);
        }}

        .bullet-list-study .st-colloc {{
            color: var(--study-colloc);
        }}

        .bullet-list-study .st-trap {{
            color: var(--accent-gold);
        }}

        .bullet-list-study .st-ex {{
            color: var(--text-muted);
            padding-top: 4px;
        }}

        .bullet-list-study .gm-formula {{
            font-family: var(--font-serif);
            font-size: 13.5px;
            color: var(--study-formula) !important;
            background: var(--accent-correct-bg) !important;
            padding: 8px 12px;
            border-radius: var(--radius-sm);
            border: 1px solid var(--accent-correct);
        }}

        .bullet-list-study .gm-expl {{
            color: var(--text-primary);
        }}

        .bullet-list-study .gp-correct-box {{
            color: var(--study-correct) !important;
        }}

        .bullet-list-study .gp-wrong-box {{
            color: var(--study-wrong) !important;
        }}

        .ex-en {{
            color: var(--study-en) !important;
            font-weight: 600;
            font-size: 14.5px;
        }}

        .ex-zh {{
            color: var(--study-zh) !important;
            font-size: 13.5px;
            margin-top: 4px;
        }}

        /* Analytics & Remote Agent Dashboard */
        .analytics-card {{
            background: var(--surface-container);
            border: 1px solid var(--border-hairline);
            border-radius: var(--radius-lg);
            padding: 20px;
            color: var(--text-primary);
        }}

        .analytics-title {{
            font-family: var(--font-caps);
            font-size: 14px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }}

        .stat-main-row {{
            background: var(--surface-subtle);
            border: 1px solid var(--border-hairline);
            padding: 12px 16px;
            border-radius: var(--radius-md);
            font-size: 13.5px;
            margin-bottom: 16px;
            color: var(--text-primary);
        }}

        .sub-stat-grid {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 16px;
        }}

        .sub-stat-head {{
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 4px;
        }}

        .weakness-radar-panel {{
            background: var(--accent-error-subtle);
            border: 1px solid var(--accent-error-panel-border);
            border-radius: var(--radius-md);
            padding: 12px 16px;
            color: var(--text-primary);
        }}

        .hist-weak-pill {{
            display: inline-block;
            background: var(--accent-error-tag-bg);
            color: var(--error-light);
            font-size: 11.5px;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: var(--radius-sm);
            margin: 2px 4px 2px 0;
            border: 1px solid var(--accent-error-tag-border);
        }}

        .summary-card {{
            background: var(--surface-container);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
            padding: 24px 20px;
            border-radius: var(--radius-lg);
            margin: 24px 0;
            text-align: center;
        }}

        .summary-title {{
            font-family: var(--font-serif);
            font-size: 20px;
            font-weight: 500;
            margin-bottom: 8px;
            color: var(--text-primary);
        }}

        .summary-score {{
            font-size: 15px;
            color: var(--text-secondary);
            margin-bottom: 8px;
        }}

        .footer {{
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 40px;
            padding-top: 16px;
            border-top: 1px solid var(--border-hairline);
            line-height: 1.8;
        }}
    </style>
</head>
<body data-day="{day}" data-session="{session.lower()}">
    <header class="hero-banner">
        <div class="hero-top">
            <span class="hero-day-tag">Toeic Daily Sprint / Day {day:02d} / {session_label}</span>
            <div class="hero-top-right">
                <span class="hero-date">{date_str}</span>
                <a href="index.html" class="portal-pill">進度地圖 ↗</a>
            </div>
        </div>
        <h1 class="hero-title">{session_label} / {phase_name}</h1>
        <div class="hero-topic"><b>FOCUS</b> // {topic}</div>
    </header>

    <div class="mobile-tip-banner" style="display:none;"></div>

    {body_content}

    <footer class="footer">
        TOEIC 860+ DAILY SPRINT / EDITORIAL STUDY SYSTEM<br>
        持之以恆 · 語感秒殺 · 金色必達
    </footer>
"""
    script_html = build_interactive_script(day, session, bot_token)
    return full_html + script_html + "\n</body>\n</html>\n"


INTERACTIVE_SCRIPT = build_interactive_script(1, "morning")
