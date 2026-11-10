# -*- coding: utf-8 -*-
"""Build script for the TOEIC 25-Day Study Portal (GitHub Pages).

Generates:
1. `docs/index.html` - The Master Study Portal with today's quick launch & 25-day roadmap.
2. `docs/TOEIC_DayXX_Morning.html` & `docs/TOEIC_DayXX_Afternoon.html` for all 25 days.
3. `docs/today.html` - Auto-redirects to today's current session practice based on Taipei time.
"""

import html
import os
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from adaptive_srs_engine import build_session_payload
from html_generator import render_day_html
from master_curriculum import DAYS_DATA

BASE_DIR = Path(__file__).parent
DOCS_DIR = BASE_DIR / "docs"
TZ = ZoneInfo("Asia/Taipei")
START_DATE = date(2026, 11, 4)  # Day 1; Day 25 = 2026-11-28
EXAM_DATE = date(2026, 11, 29)


def calculate_current_day(today: date = None) -> int:
    today = today or datetime.now(TZ).date()
    return max(1, min(25, (today - START_DATE).days + 1))


def render_portal_index_html(current_day: int, token: str = "") -> str:
    now = datetime.now(TZ)
    days_left = max(0, (EXAM_DATE - now.date()).days)
    curr_sess = "morning" if now.hour < 12 else "afternoon"
    sess_label = "上午練習" if curr_sess == "morning" else "下午練習"
    sess_tag = "Morning" if curr_sess == "morning" else "Afternoon"

    today_url = f"TOEIC_Day{current_day:02d}_{sess_tag}.html"
    today_topic = DAYS_DATA.get(current_day, {}).get("topic", "")
    today_morning_url = f"TOEIC_Day{current_day:02d}_Morning.html"
    today_afternoon_url = f"TOEIC_Day{current_day:02d}_Afternoon.html"

    # Build 4 Phases roadmap cards
    phases = [
        {"num": 1, "name": "基礎高頻鞏固與訊號反射", "days": range(1, 8), "color": "#5C7866"},
        {"num": 2, "name": "核心句構與考點盲區突破", "days": range(8, 15), "color": "#7E786B"},
        {"num": 3, "name": "長文閱讀與極限秒殺特訓", "days": range(15, 22), "color": "#D7AB7A"},
        {"num": 4, "name": "全真衝刺與終極覆盤驗收", "days": range(22, 26), "color": "#8EAF9D"},
    ]

    phases_html = ""
    for p in phases:
        days_rows = ""
        for d in p["days"]:
            d_data = DAYS_DATA.get(d, {})
            d_topic = d_data.get("topic", "")
            d_date = d_data.get("date", "")
            is_today = (d == current_day)
            today_badge = '<span class="today-chip">🔥 今日進度</span>' if is_today else ""
            row_class = "day-card current-day-highlight" if is_today else "day-card"

            days_rows += f"""
            <div class="{row_class}" data-day="{d}">
                <div class="day-head">
                    <span class="day-num">Day {d:02d}</span>
                    <span class="day-date">{d_date}</span>
                    {today_badge}
                </div>
                <div class="day-topic">🎯 {html.escape(d_topic)}</div>
                <div class="day-links">
                    <a href="TOEIC_Day{d:02d}_Morning.html" class="session-btn btn-morning">☀️ 上午特訓 (43題)</a>
                    <a href="TOEIC_Day{d:02d}_Afternoon.html" class="session-btn btn-afternoon">🌤️ 下午特訓 (43題)</a>
                </div>
            </div>
            """

        phases_html += f"""
        <div class="phase-group">
            <div class="phase-header" style="border-left-color: {p['color']};">
                <span class="phase-num-badge" style="background: {p['color']};">Phase {p['num']}</span>
                <span class="phase-title">{p['name']} (Day {min(p['days'])}–{max(p['days'])})</span>
            </div>
            <div class="days-grid">
                {days_rows}
            </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>多益 860+ 25天黃金衝刺特訓網站</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-canvas: #121314;
            --surface-container: #1A1C1E;
            --surface-subtle: #24272A;
            --surface-hover: #2E3236;
            --border-hairline: rgba(255, 255, 255, 0.08);
            --border-subtle: rgba(255, 255, 255, 0.12);
            --border-focus: rgba(255, 255, 255, 0.35);
            --text-primary: #EAE6E1;
            --text-secondary: #9E9B96;
            --text-muted: #656668;
            --accent-correct: #5C7866;
            --accent-wrong: #9E5757;
            --accent-gold: #D7AB7A;
            --card-bg: #1A1C1E;
            --border-color: rgba(255, 255, 255, 0.08);
            --text-main: #EAE6E1;
            --text-sub: #9E9B96;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            font-family: "Plus Jakarta Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", "Noto Sans TC", sans-serif;
            background-color: var(--bg-canvas);
            color: var(--text-primary);
            font-size: 15.5px;
            line-height: 1.7;
            padding: 16px 14px 60px 14px;
            max-width: 780px;
            margin: 0 auto;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        @media (min-width: 640px) {{
            body {{
                padding: 24px 20px 80px 20px;
            }}
        }}

        .portal-hero {{
            background: var(--surface-container);
            border: 1px solid var(--border-hairline);
            border-radius: 8px;
            padding: 24px 20px;
            margin-bottom: 18px;
            text-align: center;
        }}

        .hero-badge {{
            display: inline-block;
            font-family: "Cinzel", sans-serif;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            font-size: 11px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 8px;
        }}

        .hero-title {{
            font-family: "Newsreader", "Lora", serif;
            font-size: 24px;
            font-weight: 500;
            letter-spacing: -0.01em;
            color: var(--text-primary);
            margin-bottom: 8px;
            line-height: 1.35;
        }}

        .hero-subtitle {{
            font-size: 13.5px;
            color: var(--text-secondary);
            line-height: 1.6;
        }}

        .hero-subtitle b {{
            color: #ffffff;
            font-feature-settings: "tnum";
            font-variant-numeric: tabular-nums;
        }}

        .quick-launch-card {{
            background: var(--surface-container);
            border: 1px solid var(--border-subtle);
            border-radius: 8px;
            padding: 18px 20px;
            margin-bottom: 22px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}

        .ql-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-hairline);
        }}

        .ql-title {{
            font-family: "Newsreader", "Lora", serif;
            font-size: 17px;
            font-weight: 500;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .ql-topic {{
            font-size: 13.5px;
            color: var(--text-secondary);
            margin-bottom: 14px;
            line-height: 1.5;
        }}

        .ql-buttons {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

        .cta-btn {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 12px 10px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.15s ease;
            background: var(--surface-subtle);
            border: 1px solid var(--border-subtle);
            color: var(--text-primary);
        }}

        .cta-btn:hover {{
            background: var(--surface-hover);
            border-color: var(--border-focus);
            color: #ffffff;
        }}

        .cta-morning {{
            border-left: 3px solid var(--accent-correct);
        }}

        .cta-afternoon {{
            border-left: 3px solid #7E786B;
        }}

        .cta-btn:active {{
            transform: scale(0.98);
        }}

        .cta-sub {{
            font-size: 11.5px;
            color: var(--text-muted);
            margin-top: 3px;
        }}

        .phase-group {{
            margin-bottom: 24px;
        }}

        .phase-header {{
            background: var(--surface-container);
            border: 1px solid var(--border-hairline);
            border-left: 3px solid var(--text-secondary);
            border-radius: 6px;
            padding: 10px 14px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .phase-num-badge {{
            font-family: "Cinzel", sans-serif;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 4px;
        }}

        .phase-title {{
            font-family: "Newsreader", "Lora", serif;
            font-size: 15px;
            font-weight: 500;
            color: var(--text-primary);
        }}

        .days-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }}

        .day-card {{
            background: var(--surface-container);
            border: 1px solid var(--border-hairline);
            border-radius: 6px;
            padding: 14px 16px;
            transition: all 0.15s ease;
        }}

        .day-card:hover {{
            border-color: var(--border-subtle);
        }}

        .current-day-highlight {{
            border-color: rgba(92, 120, 102, 0.6) !important;
            background: rgba(92, 120, 102, 0.06);
        }}

        .day-head {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
        }}

        .day-num {{
            font-family: "Cinzel", sans-serif;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.05em;
            color: var(--text-primary);
            background: var(--surface-subtle);
            border: 1px solid var(--border-hairline);
            padding: 2px 7px;
            border-radius: 4px;
        }}

        .day-date {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .today-chip {{
            font-size: 11px;
            font-weight: 600;
            background: rgba(158, 87, 87, 0.15);
            color: #fca5a5;
            border: 1px solid rgba(158, 87, 87, 0.3);
            padding: 1px 7px;
            border-radius: 4px;
            animation: pulseChip 2s infinite;
        }}

        @keyframes pulseChip {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}

        .day-topic {{
            font-size: 13.5px;
            color: var(--text-secondary);
            margin-bottom: 10px;
            line-height: 1.5;
        }}

        .day-links {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}

        .session-btn {{
            text-align: center;
            padding: 7px 8px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 12.5px;
            font-weight: 500;
            border: 1px solid var(--border-hairline);
            background: var(--surface-subtle);
            color: var(--text-primary);
            transition: all 0.15s ease;
        }}

        .session-btn:hover {{
            background: var(--surface-hover);
            border-color: var(--border-focus);
            color: #ffffff;
        }}

        .portal-footer {{
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
            letter-spacing: 0.05em;
            margin-top: 40px;
            padding-top: 18px;
            border-top: 1px solid var(--border-hairline);
            line-height: 1.8;
        }}
    </style>
</head>
<body>
    <header class="portal-hero">
        <div class="hero-badge">TOEIC 860+ MASTER PORTAL</div>
        <h1 class="hero-title">多益 25 天黃金衝刺特訓地圖</h1>
        <div class="hero-subtitle">考前倒數 <b id="portal-countdown">{days_left}</b> 天 ｜ 早晚雙軌 43 題高頻題庫 · 點擊直接作答</div>
    </header>

    <!-- Today's Quick Launch -->
    <section class="quick-launch-card">
        <div class="ql-header">
            <div class="ql-title" id="ql-title">Day {current_day:02d} · 今日進度直達</div>
            <span class="today-chip">🔥 進行中</span>
        </div>
        <div class="ql-topic" id="ql-topic">
            🎯 <b>核心考點：</b>{html.escape(today_topic)}
        </div>
        <div class="ql-buttons">
            <a href="{today_morning_url}" id="ql-btn-m" class="cta-btn cta-morning">
                <span>☀️ 上午特訓</span>
                <span class="cta-sub">43 題 · 實戰衝刺 ▶</span>
            </a>
            <a href="{today_afternoon_url}" id="ql-btn-a" class="cta-btn cta-afternoon">
                <span>🌤️ 下午特訓</span>
                <span class="cta-sub">43 題 · 深度複習 ▶</span>
            </a>
        </div>
    </section>

    <!-- Full 25-Day Roadmap -->
    <section class="roadmap-section">
        <div style="font-family: 'Cinzel', serif; font-size: 13.5px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 14px; display: flex; align-items: center; gap: 8px;">
            📚 25-Day Curriculum Roadmap
        </div>
        {phases_html}
    </section>

    <footer class="portal-footer">
        TOEIC 860+ DAILY SPRINT · EDITORIAL STUDY SYSTEM<br>
        免下載 · 跨裝置雲端進度同步 · 金色必達
    </footer>

    <script>
    (function() {{
        try {{
            // Dynamic Client-side Taipei Date & Countdown
            const startDate = new Date('2026-11-04T00:00:00+08:00');
            const examDate = new Date('2026-11-29T00:00:00+08:00');
            const now = new Date();
            const msPerDay = 86400000;
            const daysLeft = Math.max(0, Math.ceil((examDate - now) / msPerDay));
            const countdownEl = document.getElementById('portal-countdown');
            if (countdownEl) countdownEl.innerText = daysLeft;

            const diffDays = Math.floor((now - startDate) / msPerDay) + 1;
            const currentDay = Math.max(1, Math.min(25, diffDays));

            // Dynamic highlight on the road map
            const dayCards = document.querySelectorAll('.day-card');
            dayCards.forEach(card => {{
                const d = parseInt(card.getAttribute('data-day') || '0', 10);
                if (d === currentDay) {{
                    card.classList.add('current-day-highlight');
                }}
            }});
        }} catch(e) {{
            console.warn('Dynamic date calculation error:', e);
        }}
    }})();
    </script>
</body>
</html>
"""


def render_today_redirect_html() -> str:
    """Auto-redirects to today's active practice in Taipei time."""
    return """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>多益特訓即時導向中...</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600&family=Newsreader:wght@500&display=swap" rel="stylesheet">
    <script>
    (function() {
        const startDate = new Date('2026-11-04T00:00:00+08:00');
        const now = new Date();
        const diffDays = Math.floor((now - startDate) / 86400000) + 1;
        const currentDay = Math.max(1, Math.min(25, diffDays));
        const dayStr = String(currentDay).padStart(2, '0');
        const hourTaipei = (now.getUTCHours() + 8) % 24;
        const sess = hourTaipei < 12 ? 'Morning' : 'Afternoon';
        window.location.replace(`TOEIC_Day${dayStr}_${sess}.html`);
    })();
    </script>
</head>
<body style="font-family: 'Plus Jakarta Sans', -apple-system, sans-serif; background-color: #121314; color: #EAE6E1; text-align: center; padding: 60px 20px;">
    <h2 style="font-family: 'Newsreader', serif; font-size: 20px; font-weight: 500;">🚀 正在為您開啟今日多益練習...</h2>
    <p style="margin-top: 10px; font-size: 13.5px; color: #9E9B96;">
        若未自動跳轉，請點擊前往 <a href="index.html" style="color: #8EAF9D; text-decoration: underline;">特訓地圖首頁</a>。
    </p>
</body>
</html>
"""


def build_all_pages(target_dir: Path = None, token: str = ""):
    target_dir = target_dir or DOCS_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    current_day = calculate_current_day()

    print(f"🚀 Building Study Portal for GitHub Pages in {target_dir}...")
    print(f"Current Taipei Day: Day {current_day} / 25")

    # 1. Generate index.html (Master Portal)
    portal_html = render_portal_index_html(current_day, token=token)
    (target_dir / "index.html").write_text(portal_html, encoding="utf-8")
    print(f"✅ Generated docs/index.html ({len(portal_html)} bytes)")

    # 2. Generate today.html (Quick redirect)
    today_html = render_today_redirect_html()
    (target_dir / "today.html").write_text(today_html, encoding="utf-8")
    print(f"✅ Generated docs/today.html ({len(today_html)} bytes)")

    # 3. Generate .nojekyll
    (target_dir / ".nojekyll").write_text("", encoding="utf-8")

    # 2. Generate all 25 days x 2 sessions = 50 HTML reports
    count = 0
    for day_num in range(1, 26):
        day_data = DAYS_DATA.get(day_num)
        if not day_data:
            continue
        for session in ("morning", "afternoon"):
            tag = "Morning" if session == "morning" else "Afternoon"
            payload = build_session_payload(day_num, session)
            html_content = render_day_html(day_data, session=session, payload=payload, bot_token=token)
            out_file = target_dir / f"TOEIC_Day{day_num:02d}_{tag}.html"
            out_file.write_text(html_content, encoding="utf-8")
            count += 1
            print(f"[{count:02d}/50] Generated {out_file.name} ({len(html_content)} bytes)")

    print(f"🎉 All {count} practice pages + index.html successfully built in {target_dir}!")


if __name__ == "__main__":
    # For public website hosting, do NOT bake secrets into HTML files.
    # Users can sync via localStorage or pass ?token= safely on client-side.
    build_all_pages(token="")
