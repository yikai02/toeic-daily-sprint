# -*- coding: utf-8 -*-
"""
Verification script: tests connection to Telegram Bot.
Run this script or tap Start on Telegram @Toeic_practice_bot.
"""

import sys
from telegram_sender import get_credentials, auto_detect_chat_id, send_telegram_message, send_telegram_document
from pathlib import Path

def test():
    token, chat_id = get_credentials()
    print(f"Testing with Token: {token[:10]}... and Chat ID: {chat_id}")
    
    # Check updates
    detected_id = auto_detect_chat_id(token)
    if detected_id:
        print(f"✅ Auto-detected active chat_id from Telegram: {detected_id}")
        chat_id = detected_id

    if not chat_id:
        print("❌ chat_id is missing or empty. Please send /start to @Toeic_practice_bot on Telegram!")
        return False
        
    print(f"Sending test hello to {chat_id}...")
    text_ok = send_telegram_message(token, chat_id, "🎉 <b>【多益金色證書衝刺】Telegram Bot 自動推播已成功連線！</b>\n\n每天 <b>08:00 (早間晨報)</b> 與 <b>14:00 (盤後特訓)</b> 將會準時把手機專用 HTML 與複習報告推送給您！")
    
    html_file = Path(__file__).parent / "reports" / "TOEIC_Day01_Morning.html"
    if html_file.exists() and text_ok:
        print("Sending Day 1 Morning HTML file...")
        doc_ok = send_telegram_document(token, chat_id, str(html_file), caption="Day 1 早間晨報 HTML (點擊直接在手機全螢幕瀏覽)")
        if doc_ok:
            print("✅ HTML document sent successfully!")
            return True
    return text_ok

if __name__ == "__main__":
    test()
