#!/bin/bash
# ==============================================================================
# 多益 860+ 金色證書衝刺：每日 14:00 盤後複習自動推播腳本
# ==============================================================================

set -uo pipefail

PROJECT_DIR="/Users/jiangyikai/Documents/Antigravity/Antigravity 多益"
LOG_DIR="${PROJECT_DIR}/reports"
LOG_FILE="${LOG_DIR}/afternoon_trigger.log"
mkdir -p "${LOG_DIR}"

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "----------------------------------------------------------------" >> "${LOG_FILE}"
echo "[${TIMESTAMP}] 啟動多益 14:00 盤後特訓 (Afternoon Review) 推播流程..." >> "${LOG_FILE}"

cd "${PROJECT_DIR}"
python3 dispatch_runner.py --session afternoon >> "${LOG_FILE}" 2>&1 || true

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 盤後特訓推播流程結束。" >> "${LOG_FILE}"
