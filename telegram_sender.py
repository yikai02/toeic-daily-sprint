# -*- coding: utf-8 -*-
"""Telegram dispatcher: sends the HTML report as a document only (no extra text).

Credentials come ONLY from environment variables (GitHub Secrets in CI) or a
local, git-ignored .env file. Nothing sensitive is hardcoded.
"""

import os
import time
from pathlib import Path

import requests

ENV_PATH = Path(__file__).parent / ".env"


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
