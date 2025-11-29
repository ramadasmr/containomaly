#!/bin/bash
set -e
echo "[*] Running agent once to collect docker ps and send to server..."
source venv/bin/activate 2>/dev/null || echo "Warning: venv not activated"
#export $(grep -v '^#' .env | xargs)
python -m agent.main --once
