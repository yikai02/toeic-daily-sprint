# -*- coding: utf-8 -*-
"""Dispatch runner for the TOEIC 25-Day Sprint.

Picks the current Day (Taipei time), renders the mobile HTML, sends it to Telegram.
Exits non-zero on failure so GitHub Actions marks the run red instead of silently passing.
"""

import argparse
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from html_generator import render_day_html
from master_curriculum import DAYS_DATA
from telegram_sender import dispatch_report

BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "reports"

TZ = ZoneInfo("Asia/Taipei")
START_DATE = date(2026, 11, 4)  # Day 1; Day 25 = 2026-11-28
TOTAL_DAYS = 25


def calculate_current_day(today: date = None) -> int:
    """Day number based on Taipei calendar date, clamped to 1..25."""
    today = today or datetime.now(TZ).date()
    return max(1, min(TOTAL_DAYS, (today - START_DATE).days + 1))


def run_dispatch(session: str, target_day: int = None) -> bool:
    day_num = target_day if target_day is not None else calculate_current_day()
    if day_num not in DAYS_DATA:
        print(f"Error: Day {day_num} not found in curriculum data!")
        return False

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    html_content = render_day_html(DAYS_DATA[day_num], session=session)
    tag = "Morning" if session == "morning" else "Afternoon"
    file_path = REPORTS_DIR / f"TOEIC_Day{day_num:02d}_{tag}.html"
    file_path.write_text(html_content, encoding="utf-8")
    print(f"Generated {file_path.name} ({len(html_content)} bytes), Day {day_num}")

    ok = dispatch_report(str(file_path))
    print(f"{'✅ Sent' if ok else '❌ FAILED to send'} Day {day_num} {tag}")
    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TOEIC Daily Telegram Dispatcher")
    parser.add_argument("--session", choices=["morning", "afternoon"], default="morning")
    parser.add_argument("--day", type=int, default=None, help="Specific Day (1-25)")
    args = parser.parse_args()
    sys.exit(0 if run_dispatch(args.session, args.day) else 1)
