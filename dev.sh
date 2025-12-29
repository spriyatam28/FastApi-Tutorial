#!/usr/bin/env bash

set -e

echo "Installing all dependencies and synchronizing them..."

uv sync

echo "😈 Starting ruff check on the current directory..."

ruff check .

echo "🚀 Starting FastAPI dev server..."

uv run uvicorn src.main:app --reload --port 8000