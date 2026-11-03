# -*- coding: utf-8 -*-
"""
Sets GitHub Actions secrets for yikai02/toeic-daily-sprint using PyNaCl.
"""

import base64
import requests
from nacl import encoding, public

TOKEN = "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"
REPO = "yikai02/toeic-daily-sprint"

HEADERS = {
    "User-Agent": "curl/8.0",
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_public_key():
    url = f"https://api.github.com/repos/{REPO}/actions/secrets/public-key"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    return data["key_id"], data["key"]

def encrypt_secret(public_key_b64: str, secret_value: str) -> str:
    public_key = public.PublicKey(public_key_b64.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")

def set_secret(secret_name: str, secret_value: str):
    key_id, public_key_b64 = get_public_key()
    encrypted_value = encrypt_secret(public_key_b64, secret_value)
    url = f"https://api.github.com/repos/{REPO}/actions/secrets/{secret_name}"
    payload = {
        "encrypted_value": encrypted_value,
        "key_id": key_id
    }
    resp = requests.put(url, headers=HEADERS, json=payload)
    if resp.status_code in [201, 204]:
        print(f"✅ Secret {secret_name} set successfully (HTTP {resp.status_code})")
        return True
    else:
        print(f"❌ Failed to set {secret_name}: {resp.status_code} {resp.text}")
        return False

if __name__ == "__main__":
    set_secret("TELEGRAM_BOT_TOKEN", "9073523773:AAFmu6fcg2TikM5MWYzwTbUWf7AYR3Yb6yk")
    set_secret("TELEGRAM_CHAT_ID", "8716060696")
