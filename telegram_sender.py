# -*- coding: utf-8 -*-
"""
Telegram Push Dispatcher for TOEIC 25-Day Sprint.
Handles Telegram Bot API communication:
- sendDocument (HTML mobile-interactive report)
- sendMessage (Mobile-friendly summary and alert)
- Auto-detects chat_id if not present via getUpdates
"""

import os
import sys
import time
import json
import requests
from pathlib import Path

ENV_PATH = Path(__file__).parent / ".env"

def load_env():
    env_vars = {}
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    return env_vars

def save_chat_id(chat_id: str):
    env_vars = load_env()
    env_vars["TELEGRAM_CHAT_ID"] = str(chat_id)
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        for k, v in env_vars.items():
            f.write(f'{k}="{v}"\n')

def get_credentials():
    env_vars = load_env()
    token = os.environ.get("TELEGRAM_BOT_TOKEN") or env_vars.get("TELEGRAM_BOT_TOKEN", "9073523773:AAFmu6fcg2TikM5MWYzwTbUWf7AYR3Yb6yk")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID") or env_vars.get("TELEGRAM_CHAT_ID", "")
    return token, chat_id

def auto_detect_chat_id(token: str) -> str:
    """Queries getUpdates to fetch the latest chat_id if user messaged the bot."""
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if data.get("ok") and data.get("result"):
            # Get latest update
            latest = data["result"][-1]
            msg = latest.get("message") or latest.get("channel_post") or latest.get("callback_query", {}).get("message")
            if msg and "chat" in msg:
                cid = str(msg["chat"]["id"])
                save_chat_id(cid)
                return cid
    except Exception as e:
        print(f"Error checking getUpdates: {e}")
    return ""

def send_telegram_message(token: str, chat_id: str, text: str, parse_mode: str = "HTML") -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": True
    }
    for attempt in range(1, 4):
        try:
            resp = requests.post(url, json=payload, timeout=15)
            if resp.status_code == 200 and resp.json().get("ok"):
                return True
            if resp.status_code == 429:
                retry_after = int(resp.json().get("parameters", {}).get("retry_after", 3))
                time.sleep(retry_after)
                continue
            print(f"Telegram sendMessage failed: {resp.text}")
        except Exception as e:
            print(f"Telegram sendMessage error on attempt {attempt}: {e}")
            time.sleep(2 ** attempt)
    return False

def send_telegram_document(token: str, chat_id: str, file_path: str, caption: str = "") -> bool:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    for attempt in range(1, 4):
        try:
            with open(file_path, "rb") as f:
                resp = requests.post(
                    url,
                    data={"chat_id": chat_id, "caption": caption[:1000]},
                    files={"document": (os.path.basename(file_path), f, "text/html")},
                    timeout=30
                )
            if resp.status_code == 200 and resp.json().get("ok"):
                return True
            if resp.status_code == 429:
                retry_after = int(resp.json().get("parameters", {}).get("retry_after", 3))
                time.sleep(retry_after)
                continue
            print(f"Telegram sendDocument failed: {resp.text}")
        except Exception as e:
            print(f"Telegram sendDocument error on attempt {attempt}: {e}")
            time.sleep(2 ** attempt)
    return False

def dispatch_report(html_file_path: str, summary_text: str, caption: str = "") -> bool:
    token, chat_id = get_credentials()
    if not token:
        print("TELEGRAM_BOT_TOKEN missing!")
        return False
    
    # Check if chat_id exists and is valid
    if not chat_id:
        chat_id = auto_detect_chat_id(token)
        if not chat_id:
            print("Cannot dispatch: chat_id not found. Please message @Toeic_practice_bot in Telegram first.")
            return False

    # First send document
    doc_success = send_telegram_document(token, chat_id, html_file_path, caption=caption)
    
    # If failed with chat not found, try auto detecting
    if not doc_success:
        new_id = auto_detect_chat_id(token)
        if new_id and new_id != chat_id:
            chat_id = new_id
            doc_success = send_telegram_document(token, chat_id, html_file_path, caption=caption)

    # Only send the file document, no additional text messages
    return doc_success
