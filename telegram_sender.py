# -*- coding: utf-8 -*-
"""Telegram dispatcher: sends the HTML report as a document only (no extra text).

Includes cloud-shared idempotency state via Telegram Bot metadata
(getMyShortDescription / setMyShortDescription) so that multiple triggers
(Mac LaunchAgent workflow_dispatch, local fallback, or delayed GitHub Actions
cron schedule) never send duplicate files on the same day.
"""

import os
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

ENV_PATH = Path(__file__).parent / ".env"
TZ = ZoneInfo("Asia/Taipei")


def load_env() -> dict:
    env_vars = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars


def get_credentials():
    env_vars = load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or env_vars.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or env_vars.get("TELEGRAM_CHAT_ID", "")
    return token.strip(), chat_id.strip()


def _redact(text: str, token: str) -> str:
    return text.replace(token, "***") if token else text


def _session_tag_prefix(session: str, today_str: str) -> str:
    prefix = "MORNING_SENT" if session.lower() == "morning" else "AFTERNOON_SENT"
    return f"{prefix}:{today_str}"


def get_bot_short_description(token: str) -> str:
    """Fetches the bot's cloud short_description (silent metadata, zero chat messages)."""
    if not token:
        return ""
    url = f"https://api.telegram.org/bot{token}/getMyShortDescription"
    try:
        resp = requests.get(url, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("ok"):
                return str((data.get("result") or {}).get("short_description", "")).strip()
    except requests.RequestException as e:
        print(f"Warning: getMyShortDescription failed (non-blocking): {_redact(str(e), token)}")
    return ""


def check_already_sent_today(token: str, today_str: str, session: str) -> bool:
    """Checks Telegram Bot cloud state to see if today's morning/afternoon practice was already sent."""
    if not token:
        return False
    desc = get_bot_short_description(token)
    tag_prefix = _session_tag_prefix(session, today_str)
    return tag_prefix in desc


def mark_session_sent_today(token: str, today_str: str, session: str) -> bool:
    """Records in Telegram Bot cloud metadata that today's session has been dispatched."""
    if not token:
        return False
    cur_desc = get_bot_short_description(token)
    other_session = "afternoon" if session.lower() == "morning" else "morning"
    other_prefix = _session_tag_prefix(other_session, today_str)

    preserved_other = ""
    for part in cur_desc.split("|"):
        part = part.strip()
        if part.startswith(other_prefix):
            preserved_other = part

    now_hm = datetime.now(TZ).strftime("%H:%M:%S")
    this_tag = f"{_session_tag_prefix(session, today_str)} {now_hm}"
    if session.lower() == "morning":
        new_desc = f"{this_tag} | {preserved_other}" if preserved_other else this_tag
    else:
        new_desc = f"{preserved_other} | {this_tag}" if preserved_other else this_tag

    url = f"https://api.telegram.org/bot{token}/setMyShortDescription"
    try:
        resp = requests.post(
            url,
            json={"short_description": new_desc[:120]},
            timeout=8,
        )
        if resp.status_code == 200 and resp.json().get("ok"):
            print(f"🔒 Recorded cloud idempotency state: {new_desc[:120]}")
            return True
    except requests.RequestException as e:
        print(f"Warning: setMyShortDescription failed: {_redact(str(e), token)}")
    return False


def send_telegram_document(token: str, chat_id: str, file_path: str, caption: str = "",
                           max_retries: int = 3) -> bool:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    for attempt in range(1, max_retries + 1):
        try:
            with open(file_path, "rb") as f:
                resp = requests.post(
                    url,
                    data={"chat_id": chat_id, "caption": caption[:1000]},
                    files={"document": (os.path.basename(file_path), f, "text/html")},
                    timeout=30,
                )
            if resp.status_code == 200 and resp.json().get("ok"):
                return True
            if resp.status_code == 429:
                retry_after = int(resp.json().get("parameters", {}).get("retry_after", 3))
                time.sleep(retry_after)
                continue
            print(f"Telegram sendDocument failed ({resp.status_code}): {_redact(resp.text, token)}")
            if 400 <= resp.status_code < 500:  # permanent error (bad chat/token): don't retry
                return False
        except requests.RequestException as e:
            print(f"Telegram sendDocument error (attempt {attempt}): {_redact(str(e), token)}")
        time.sleep(2 ** attempt)
    return False


def dispatch_report(html_file_path: str, caption: str = "") -> bool:
    token, chat_id = get_credentials()
    if not token or not chat_id:
        print("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID missing (set env vars or GitHub Secrets).")
        return False
    return send_telegram_document(token, chat_id, html_file_path, caption=caption)
