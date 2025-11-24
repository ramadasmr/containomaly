#!/bin/bash
set -e
echo "[*] Starting agent loop..."
source venv/bin/activate 2>/dev/null || echo "Warning: venv not activated"
#export $(grep -v '^#' .env | xargs)
python -m agent.main --interval ${COLLECT_INTERVAL_SECONDS:-60}
