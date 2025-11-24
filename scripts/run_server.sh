#!/bin/bash
echo "[*] Starting FastAPI server..."
source venv/bin/activate 2>/dev/null || echo "Warning: venv not activated"
#export $(grep -v '^#' .env | xargs)
uvicorn server.main:app --host ${SERVER_HOST:-0.0.0.0} --port ${SERVER_PORT:-8000} --reload
