# -*- coding: utf-8 -*-
"""
Main Dispatch Runner for TOEIC 25-Day Sprint.
Calculates Day from calendar, renders mobile-optimized HTML report,
and dispatches to Telegram via Bot API.
"""

import os
import sys
import argparse
from datetime import date, datetime
from pathlib import Path

from master_curriculum import DAYS_DATA
from html_generator import render_day_html
from telegram_sender import dispatch_report, auto_detect_chat_id, get_credentials

BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 2026-11-04 is Day 1; 2026-11-28 is Day 25
START_DATE = date(2026, 11, 4)

def calculate_current_day() -> int:
    today = date.today()
    if today < START_DATE:
        return 1
    diff = (today - START_DATE).days + 1
    if diff > 25:
        return 25
    return diff

def build_summary_message(day_data: dict, session: str) -> str:
    day = day_data["day"]
    phase = day_data.get("phase", 1)
    topic = day_data.get("topic", "")
    
    if session == "morning":
        m = day_data.get("morning", {})
        chunks = m.get("chunks", [])[:5]
        chunk_lines = "\n".join([f"• <b>{c['chunk']}</b> ({c['meaning']})" for c in chunks])
        anchor_title = m.get("visual_anchor", {}).get("title", "")
        golden = m.get("visual_anchor", {}).get("golden_rule", "")
        p5_count = len(m.get("part5", []))

        msg = (
            f"☀️ <b>【多益金色衝刺 860+】Day {day}/25 晨報推播</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 <b>今日主題：</b>{topic}\n\n"
            f"📦 <b>核心語塊精選：</b>\n"
            f"{chunk_lines}\n\n"
            f"⚡ <b>視覺秒殺錨點：</b>{anchor_title}\n"
            f"👉 <i>{golden}</i>\n\n"
            f"📝 <b>實戰特訓：</b>Part 5 題庫共 {p5_count} 題（每題下方皆有獨立防雷揭曉按鈕）\n\n"
            f"📱 <b>點擊上方 HTML 檔案即可在手機開啟完整大字排版！</b>"
        )
    else:
        a = day_data.get("afternoon", {})
        recall_count = len(a.get("quick_recall", []))
        traps_count = len(a.get("spaced_traps", []))
        p7_count = len(a.get("part7", {}).get("questions", []))
        total_q = recall_count + traps_count + p7_count
        p7_title = a.get("part7", {}).get("title", "商務微閱讀")

        msg = (
            f"🌙 <b>【多益金色衝刺 860+】Day {day}/25 盤後特訓</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🎯 <b>複習主題：</b>{topic}\n\n"
            f"🧠 <b>今日特訓項目（共 {total_q} 題，單題即時防雷）：</b>\n"
            f"1. 早間記憶快篩 ({recall_count} 題挖空)\n"
            f"2. 間隔重複錯題變體 ({traps_count} 題陷阱題)\n"
            f"3. Part 7 細節抓漏微閱讀 ({p7_count} 題，{p7_title})\n\n"
            f"🔍 <b>防漏看雷達已就緒！點擊上方 HTML 檔案開啟完整測驗！</b>"
        )
    return msg

def run_dispatch(session: str, target_day: int = None):
    day_num = target_day if target_day is not None else calculate_current_day()
    if day_num not in DAYS_DATA:
        print(f"Error: Day {day_num} not found in curriculum data!")
        return False
    
    day_data = DAYS_DATA[day_num]
    session_clean = session.lower()
    
    # 1. Render HTML
    html_content = render_day_html(day_data, session=session_clean)
    
    # 2. Save HTML File
    sess_tag = "Morning" if session_clean == "morning" else "Afternoon"
    filename = f"TOEIC_Day{day_num:02d}_{sess_tag}.html"
    file_path = REPORTS_DIR / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated HTML report: {file_path} ({len(html_content)} bytes)")

    # 3. Dispatch file only (no extra text messages)
    success = dispatch_report(str(file_path), summary_text="", caption="")
    if success:
        print(f"✅ Successfully dispatched Day {day_num} {sess_tag} to Telegram!")
    else:
        print(f"⚠️ Dispatch returned False. (Check if user has tapped /start on @Toeic_practice_bot)")
    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TOEIC Daily Telegram Dispatcher")
    parser.add_argument("--session", choices=["morning", "afternoon"], default="morning", help="Session to dispatch")
    parser.add_argument("--day", type=int, default=None, help="Specific Day (1-25) to dispatch")
    args = parser.parse_args()

    run_dispatch(session=args.session, target_day=args.day)
