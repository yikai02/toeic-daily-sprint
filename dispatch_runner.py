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

from adaptive_srs_engine import build_session_payload, save_session_manifest
from html_generator import render_day_html
from master_curriculum import DAYS_DATA
from telegram_sender import (
    check_already_sent_today,
    claim_session_today,
    dispatch_report,
    get_credentials,
    mark_session_sent_today,
    release_session_claim,
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


def is_in_dispatch_window(session: str, now: datetime = None) -> tuple[bool, str]:
    """Validates whether current Taipei time is within an acceptable execution window."""
    now = now or datetime.now(TZ)
    h = now.hour
    m = now.minute
    total_minutes = h * 60 + m

    # 1. Night-time absolute silence: 21:00 ~ 07:00 (1260 mins ~ 420 mins)
    if total_minutes >= 21 * 60 or total_minutes < 7 * 60:
        return False, f"夜間防打擾保護 (目前台北時間 {now.strftime('%H:%M')}，非作答時段，自動丟棄延遲排程)"

    # 2. Morning window: 07:30 ~ 12:15 (450 ~ 735 mins)
    if session == "morning":
        if total_minutes < 7 * 60 + 30:
            return False, f"上午練習時段尚未開始 (目前時間 {now.strftime('%H:%M')}，目標 08:00)"
        if total_minutes > 12 * 60 + 15:
            return False, f"上午練習排程嚴重延遲 (目前時間 {now.strftime('%H:%M')} 已超過 12:15)，自動丟棄避免與下午衝堂"
        return True, ""

    # 3. Afternoon window: 13:30 ~ 19:30 (810 ~ 1170 mins)
    if session == "afternoon":
        if total_minutes < 13 * 60 + 30:
            return False, f"下午練習時段尚未開始 (目前時間 {now.strftime('%H:%M')}，目標 14:00)"
        if total_minutes > 19 * 60 + 30:
            return False, f"下午練習排程嚴重延遲 (目前時間 {now.strftime('%H:%M')} 已超過 19:30)，自動丟棄避免夜間擾民"
        return True, ""

    return True, ""


def resolve_effective_session(
    requested_session: str = "auto",
    now: datetime = None,
    cron_expr: str = None,
) -> str:
    """Resolves the true intended session ('morning' or 'afternoon').

    Prioritizes:
    1. Explicit requested_session if it is 'morning' or 'afternoon'.
    2. cron_expr (passed via CLI or GITHUB_EVENT_SCHEDULE or GITHUB_EVENT_PATH):
       - Morning window in UTC: hours 23 (e.g. 23:45-23:58 UTC = 07:45-07:58 Taipei),
         0 (08:xx Taipei), or 1 (09:xx Taipei).
       - Afternoon window in UTC: hours 5 (13:xx Taipei), 6 (14:xx Taipei), or 7 (15:xx Taipei).
    3. Fallback to current Taipei local hour: < 12:00 -> 'morning', >= 12:00 -> 'afternoon'.
    """
    now = now or datetime.now(TZ)

    # 1. Explicit requested_session has highest priority
    if requested_session and requested_session.lower() in ("morning", "afternoon"):
        return requested_session.lower()

    # 2. Extract cron_expr if not provided directly
    if not cron_expr:
        cron_expr = os.environ.get("GITHUB_EVENT_SCHEDULE", "").strip()

    if not cron_expr and os.environ.get("GITHUB_EVENT_NAME", "").strip() == "schedule":
        event_path = os.environ.get("GITHUB_EVENT_PATH", "").strip()
        if event_path and os.path.exists(event_path):
            try:
                with open(event_path, "r", encoding="utf-8") as f:
                    payload = json.load(f)
                cron_expr = str(payload.get("schedule", "")).strip()
            except Exception as e:
                print(f"Warning: could not parse GITHUB_EVENT_PATH: {e}")

    if cron_expr:
        parts = cron_expr.strip().split()
        if len(parts) >= 2:
            hour_part = parts[1]
            try:
                hour_val = int(hour_part)
                if hour_val in (23, 0, 1):
                    return "morning"
                if hour_val in (5, 6, 7):
                    return "afternoon"
            except ValueError:
                pass
        cron_cleaned = " ".join(parts)
        morning_prefixes = ("45 23", "50 23", "52 23", "55 23", "58 23", "0 0", "5 0", "10 0", "15 0", "20 0", "30 0", "0 1")
        afternoon_prefixes = ("45 5", "50 5", "52 5", "55 5", "58 5", "0 6", "5 6", "10 6", "15 6", "20 6", "30 6", "0 7")
        if any(cron_cleaned.startswith(p) for p in morning_prefixes):
            return "morning"
        if any(cron_cleaned.startswith(p) for p in afternoon_prefixes):
            return "afternoon"

    # 3. Fallback to time-of-day in Taipei
    return determine_session(now)


def run_dispatch(
    session: str = "auto",
    target_day: int = None,
    dry_run: bool = False,
    force: bool = False,
    cron_expr: str = None,
) -> bool:
    now = datetime.now(TZ)
    today_str = now.strftime("%Y-%m-%d")
    session = resolve_effective_session(session, now, cron_expr=cron_expr)

    current_cal_day = calculate_current_day(now.date())
    day_num = target_day if target_day is not None else current_cal_day
    if day_num not in DAYS_DATA:
        print(f"Error: Day {day_num} not found in curriculum data!")
        return False

    tag = "Morning" if session == "morning" else "Afternoon"
    zh_label = "上午練習" if session == "morning" else "下午練習"

    force_env = os.environ.get("FORCE_RESEND", "").lower() in ("1", "true", "yes")
    # Only treat as forced if explicitly forced or if testing a different day than current calendar day
    is_forced = force or force_env or (target_day is not None and target_day != current_cal_day)

    # Stale/delayed schedule guardrail: prevent nighttime or severely delayed crons from sending
    is_scheduled = bool(cron_expr) or (os.environ.get("GITHUB_EVENT_NAME", "").strip() == "schedule")
    if is_scheduled and not is_forced:
        allowed, reason = is_in_dispatch_window(session, now)
        if not allowed:
            print(f"🛑 [排程時間防禦] {reason}。本次雲端排程已安全略過。")
            return True

    token, _ = get_credentials()
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    # Build the session payload ONCE so the HTML and the saved question manifest are identical.
    payload = build_session_payload(day_num, session)
    save_session_manifest(payload)
    html_content = render_day_html(DAYS_DATA[day_num], session=session, payload=payload, bot_token=token)
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

    claimed = False
    if not is_forced and token:
        if check_already_sent_today(token, today_str, session):
            print(
                f"⏭️ [防重複推播保護] 今日 ({today_str}) Day {day_num} {zh_label} "
                f"已於稍早成功推播至 Telegram 或正在推播中，本次執行自動略過。"
            )
            return True
        if not claim_session_today(token, today_str, session):
            print(
                f"⏭️ [分散式鎖保護] 今日 ({today_str}) Day {day_num} {zh_label} "
                f"已有另一個節點搶先進入發送流程，本次執行自動略過避免重複。"
            )
            return True
        claimed = True

    web_url = f"https://yikai02.github.io/toeic-daily-sprint/TOEIC_Day{day_num:02d}_{tag}.html"
    portal_url = "https://yikai02.github.io/toeic-daily-sprint/"
    days_left = max(0, (date(2026, 11, 29) - now.date()).days)
    sess_icon = "☀️" if session == "morning" else "🌤️"

    caption = (
        f"{sess_icon} 多益 860+ Day {day_num} {zh_label} (考前倒數 {days_left} 天)\n\n"
        f"🎯 點此網頁直開（手機免下載、全功能判題）：\n"
        f"👉 {web_url}\n\n"
        f"📚 25天全期學習網站：{portal_url}\n\n"
        f"💡 亦可下載下方 HTML 附件離線練習。"
    )

    ok = dispatch_report(str(file_path), caption=caption)
    if ok:
        if token and not is_forced:
            mark_session_sent_today(token, today_str, session)
    else:
        if claimed and token:
            release_session_claim(token, today_str, session)
    print(f"{'✅ Sent' if ok else '❌ FAILED to send'} Day {day_num} {tag} ({zh_label})")
    return ok


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TOEIC Daily Telegram Dispatcher")
    parser.add_argument("--session", choices=["morning", "afternoon", "auto"], default="auto")
    parser.add_argument("--cron", type=str, default=None, help="GitHub Actions schedule cron string")
    parser.add_argument("--day", type=int, default=None, help="Specific Day (1-25)")
    parser.add_argument("--dry-run", action="store_true", help="Generate HTML without sending to Telegram")
    parser.add_argument("--force", action="store_true", help="Bypass daily deduplication guard")
    args = parser.parse_args()
    sys.exit(0 if run_dispatch(args.session, args.day, args.dry_run, args.force, cron_expr=args.cron) else 1)
