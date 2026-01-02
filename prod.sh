#!/usr/bin/env bash

set -e

# Set the virtual environment to run the application
source .venv/bin/activate

# Environment variables for production
export ENV="production"
export LOG_LEVEL="info"
export FASTAPI_DEBUG="0"

# Check if everything is installed
echo "✅ Checking if everything is installed correctly and synchronized..."

uv sync

# Run FastAPI with uvicorn in production mode
uvicorn src.main:app \
--host 0.0.0.0 \
--port 8000 \
--workers 4 \
--log-level "$LOG_LEVEL" \
--limit-concurrency 2000 \
--timeout-keep-alive 5 \
--proxy-headers