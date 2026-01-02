#!/usr/bin/env bash

set -e

# Environment variable for development
export ENV="development"

echo "🔃 Installing all dependencies and synchronizing them..."

uv sync

echo "✅ Starting ruff check on the current directory..."

# Check the code for linting and formatting errors
ruff check . && ruff format .

# Link to access OpenAPI docs
echo "Open the link for OpenAPI docs"
echo http://127.0.0.1:8000/docs

echo "🚀 Starting development server..."

uv run uvicorn src.main:app --reload --port 8000