#!/bin/bash
# ==============================================================================
# 多益 860+ 金色證書衝刺：每日 08:00 晨報自動推播腳本
# ==============================================================================

set -uo pipefail

PROJECT_DIR="/Users/jiangyikai/Documents/Antigravity/Antigravity 多益"
LOG_DIR="${PROJECT_DIR}/reports"
LOG_FILE="${LOG_DIR}/morning_trigger.log"
mkdir -p "${LOG_DIR}"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "----------------------------------------------------------------" >> "${LOG_FILE}"
echo "[${TIMESTAMP}] 啟動多益 08:00 早間晨報 (Morning Boost) 推播流程..." >> "${LOG_FILE}"

cd "${PROJECT_DIR}"
python3 dispatch_runner.py --session morning >> "${LOG_FILE}" 2>&1 || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 晨報推播流程結束。" >> "${LOG_FILE}"
