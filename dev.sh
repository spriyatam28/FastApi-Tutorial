#!/usr/bin/env bash

set -e

# Environment variable for development

export ENV="development"

echo "🔃 Installing all dependencies and synchronizing them..."

uv sync

echo "✅ Starting ruff check on the current directory..."

ruff check .

echo "Click the link for API docs"
echo http://127.0.0.1:8000/docs

echo "🚀 Starting FastAPI dev server..."

uv run uvicorn src.main:app --reload --port 8000