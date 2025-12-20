#!/usr/bin/env bash

set -e

echo "🚀 Starting FastAPI dev server..."

uv run uvicorn src.main:app --reload --port 8000