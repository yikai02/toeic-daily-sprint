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
        {"num": 1, "name": "基礎高頻鞏固與訊號反射", "days": range(1, 8), "color": "#2563eb"},
        {"num": 2, "name": "核心句構與考點盲區突破", "days": range(8, 15), "color": "#059669"},
        {"num": 3, "name": "長文閱讀與極限秒殺特訓", "days": range(15, 22), "color": "#d97706"},
        {"num": 4, "name": "全真衝刺與終極覆盤驗收", "days": range(22, 26), "color": "#7c3aed"},
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
    <style>
        :root {{
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-sub: #475569;
            --border-color: #e2e8f0;
            --accent-green: #059669;
            --accent-gold: #d97706;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-color: #0b1120;
                --card-bg: #1e293b;
                --text-main: #f8fafc;
                --text-sub: #cbd5e1;
                --border-color: #334155;
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
            line-height: 1.6;
            padding: 16px 14px 60px 14px;
            max-width: 680px;
            margin: 0 auto;
        }}

        .portal-hero {{
            background: linear-gradient(135deg, #1e3a8a, #2563eb, #3b82f6);
            color: #ffffff;
            padding: 24px 20px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(37, 99, 235, 0.22);
            margin-bottom: 18px;
            text-align: center;
        }}

        .hero-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.22);
            backdrop-filter: blur(8px);
            padding: 4px 12px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 10px;
        }}

        .hero-title {{
            font-size: 23px;
            font-weight: 800;
            letter-spacing: -0.4px;
            margin-bottom: 8px;
            line-height: 1.35;
        }}

        .hero-subtitle {{
            font-size: 14.5px;
            opacity: 0.95;
            line-height: 1.5;
        }}

        .quick-launch-card {{
            background: var(--card-bg);
            border: 2px solid var(--primary);
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 22px;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.1);
        }}

        .ql-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}

        .ql-title {{
            font-size: 17px;
            font-weight: 800;
            color: var(--primary);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .ql-topic {{
            font-size: 14px;
            color: var(--text-sub);
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
            border-radius: 12px;
            text-decoration: none;
            font-weight: 800;
            font-size: 15px;
            transition: all 0.15s ease;
            box-shadow: 0 3px 8px rgba(0,0,0,0.06);
        }}

        .cta-morning {{
            background: linear-gradient(135deg, #2563eb, #1d4ed8);
            color: #ffffff;
        }}

        .cta-afternoon {{
            background: linear-gradient(135deg, #7c3aed, #6d28d9);
            color: #ffffff;
        }}

        .cta-btn:active {{
            transform: scale(0.97);
        }}

        .cta-sub {{
            font-size: 12px;
            font-weight: 500;
            opacity: 0.9;
            margin-top: 2px;
        }}

        .phase-group {{
            margin-bottom: 24px;
        }}

        .phase-header {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-left: 5px solid var(--primary);
            border-radius: 12px;
            padding: 10px 14px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .phase-num-badge {{
            color: #ffffff;
            font-size: 11.5px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 6px;
        }}

        .phase-title {{
            font-size: 15px;
            font-weight: 800;
            color: var(--text-main);
        }}

        .days-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
        }}

        .day-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 14px;
            padding: 14px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
            transition: border-color 0.15s ease;
        }}

        .current-day-highlight {{
            border: 2px solid var(--primary) !important;
            background: rgba(37, 99, 235, 0.03);
        }}

        .day-head {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
        }}

        .day-num {{
            font-size: 14px;
            font-weight: 800;
            color: var(--primary);
            background: rgba(37, 99, 235, 0.1);
            padding: 2px 8px;
            border-radius: 6px;
        }}

        .day-date {{
            font-size: 13px;
            color: var(--text-sub);
            font-weight: 600;
        }}

        .today-chip {{
            font-size: 11.5px;
            font-weight: 800;
            background: #ef4444;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 999px;
            animation: pulseChip 1.8s infinite;
        }}

        @keyframes pulseChip {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.06); }}
        }}

        .day-topic {{
            font-size: 13.5px;
            color: var(--text-main);
            margin-bottom: 10px;
            line-height: 1.45;
        }}

        .day-links {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
        }}

        .session-btn {{
            text-align: center;
            padding: 8px 6px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 13px;
            font-weight: 700;
            border: 1px solid var(--border-color);
            background: rgba(148, 163, 184, 0.08);
            color: var(--text-main);
            transition: all 0.15s ease;
        }}

        .session-btn:hover {{
            background: rgba(37, 99, 235, 0.1);
            color: var(--primary);
            border-color: var(--primary);
        }}

        .btn-morning:hover {{
            border-color: #2563eb;
            color: #2563eb;
        }}

        .btn-afternoon:hover {{
            border-color: #7c3aed;
            color: #7c3aed;
        }}

        .portal-footer {{
            text-align: center;
            font-size: 13px;
            color: var(--text-sub);
            margin-top: 30px;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <header class="portal-hero">
        <div class="hero-badge">⚡ 多益 25 天金色證書黃金衝刺</div>
        <h1 class="hero-title">多益 860+ 實戰特訓網站</h1>
        <div class="hero-subtitle">考前倒數 <b id="portal-countdown">{days_left}</b> 天 ｜ 早晚雙軌 43 題高頻題庫 · 點擊直接作答</div>
    </header>

    <!-- Today's Quick Launch -->
    <section class="quick-launch-card">
        <div class="ql-header">
            <div class="ql-title" id="ql-title">🚀 今日練習直達：Day {current_day}</div>
            <span class="today-chip">🔥 進行中</span>
        </div>
        <div class="ql-topic" id="ql-topic">
            🎯 <b>本日核心主題：</b>{html.escape(today_topic)}
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
        <div style="font-size: 16px; font-weight: 800; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
            📚 25 天全期特訓地圖（依進度隨點隨練）
        </div>
        {phases_html}
    </section>

    <footer class="portal-footer">
        多益 860+ 金色證書特訓 · 遠端 AI Agent 演算法弱點追蹤<br>
        免下載、跨裝置雲端進度同步、金色必達！
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
<body style="font-family: -apple-system, sans-serif; text-align: center; padding: 50px 20px; color: #334155;">
    <h2>🚀 正在為您開啟今日多益練習...</h2>
    <p style="margin-top: 10px; font-size: 14px; color: #64748b;">
        若未自動跳轉，請點擊此處前往 <a href="index.html" style="color: #2563eb; font-weight: bold;">特訓網站首頁</a>。
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
