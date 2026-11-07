# -*- coding: utf-8 -*-
"""Dispatch runner for the TOEIC 25-Day Sprint.

Picks the current Day (Taipei time), renders the mobile HTML, sends it to Telegram.
Includes cloud-shared idempotency (getMyShortDescription / setMyShortDescription)
and GitHub Actions schedule-event disambiguation so each day's Morning and
Afternoon practice is dispatched strictly ONCE and never duplicated.
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from html_generator import render_day_html
from master_curriculum import DAYS_DATA
from telegram_sender import (
    check_already_sent_today,
    dispatch_report,
    get_credentials,
    mark_session_sent_today,
)

BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "reports"

TZ = ZoneInfo("Asia/Taipei")
START_DATE = date(2026, 11, 4)  # Day 1; Day 25 = 2026-11-28
TOTAL_DAYS = 25


def calculate_current_day(today: date = None) -> int:
    """Day number based on Taipei calendar date, clamped to 1..25."""
    today = today or datetime.now(TZ).date()
    return max(1, min(TOTAL_DAYS, (today - START_DATE).days + 1))


def determine_session(now: datetime = None) -> str:
    """Returns 'morning' (< 12:00) or 'afternoon' (>= 12:00) in Taipei time."""
    now = now or datetime.now(TZ)
    return "afternoon" if now.hour >= 12 else "morning"


def resolve_effective_session(requested_session: str, now: datetime = None) -> str:
    """Resolves the true intended session.

    When triggered by GitHub Actions 'schedule' event, GitHub's free cron queue can
    delay '0 0 * * *' (08:00 Taipei) past 12:00 PM Taipei. Reading the actual cron
    expression from GITHUB_EVENT_PATH prevents a delayed morning cron from being
    misclassified as 'afternoon' by daily_dispatch.yml's hour>=12 shell check.
    """
    now = now or datetime.now(TZ)
    event_name = os.environ.get("GITHUB_EVENT_NAME", "").strip()
    if event_name == "schedule":
        event_path = os.environ.get("GITHUB_EVENT_PATH", "").strip()
        if event_path and os.path.exists(event_path):
            try:
                with open(event_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                cron_expr = str(payload.get("schedule", "")).strip()
                if cron_expr in ("0 0 * * *", "55 23 * * *"):
                    return "morning"
                if cron_expr in ("0 6 * * *", "55 5 * * *"):
                    return "afternoon"
            except Exception as e:
                print(f"Warning: could not parse GITHUB_EVENT_PATH: {e}")
        # Fallback for schedule event: afternoon cron ('0 6 * * *') never fires before 14:00 Taipei
        return "afternoon" if now.hour >= 14 else "morning"

    if requested_session == "auto" or not requested_session:
        return determine_session(now)
    return requested_session.lower()


def run_dispatch(
    session: str = "auto",
    target_day: int = None,
    dry_run: bool = False,
    force: bool = False,
) -> bool:
    now = datetime.now(TZ)
    today_str = now.strftime("%Y-%m-%d")
    session = resolve_effective_session(session, now)

    day_num = target_day if target_day is not None else calculate_current_day(now.date())
    if day_num not in DAYS_DATA:
        print(f"Error: Day {day_num} not found in curriculum data!")
        return False

    tag = "Morning" if session == "morning" else "Afternoon"
    zh_label = "上午練習" if session == "morning" else "下午練習"

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    html_content = render_day_html(DAYS_DATA[day_num], session=session)
    file_path = REPORTS_DIR / f"TOEIC_Day{day_num:02d}_{tag}.html"
    file_path.write_text(html_content, encoding="utf-8")
    print(f"Generated {file_path.name} ({len(html_content)} bytes), Day {day_num} ({zh_label})")

    if dry_run:
        print(f"[DRY RUN] Generated {file_path.name} successfully. Network dispatch skipped.")
        return True

    try:
        from remote_agent_coach import process_pending_telegram_updates
        processed_msgs = process_pending_telegram_updates(send_remedial_file=True, poll_timeout=0)
        if processed_msgs > 0:
            print(f"🤖 [遠端 Agent] 已同步並回應 {processed_msgs} 則 Telegram 弱點／加練指令。")
    except Exception as exc:
        print(f"[遠端 Agent 同步略過] {exc}")

    token, _ = get_credentials()
    force_env = os.environ.get("FORCE_RESEND", "").lower() in ("1", "true", "yes")
    is_forced = force or force_env or (target_day is not None)

    if not is_forced and token:
        if check_already_sent_today(token, today_str, session):
            print(
                f"⏭️ [防重複推播保護] 今日 ({today_str}) Day {day_num} {zh_label} "
                f"已於稍早成功推播至 Telegram，本次執行自動略過。"
            )
            return True

    ok = dispatch_report(str(file_path))
    if ok and token and not (target_day is not None and not force):
        mark_session_sent_today(token, today_str, session)
    print(f"{'✅ Sent' if ok else '❌ FAILED to send'} Day {day_num} {tag} ({zh_label})")
    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TOEIC Daily Telegram Dispatcher")
    parser.add_argument("--session", choices=["morning", "afternoon", "auto"], default="auto")
    parser.add_argument("--day", type=int, default=None, help="Specific Day (1-25)")
    parser.add_argument("--dry-run", action="store_true", help="Generate HTML without sending to Telegram")
    parser.add_argument("--force", action="store_true", help="Bypass daily deduplication guard")
    args = parser.parse_args()
    sys.exit(0 if run_dispatch(args.session, args.day, args.dry_run, args.force) else 1)
