#!/bin/sh
# entrypoint.sh — runs Alembic migrations then starts the server.

set -e

echo "==> Running Alembic migrations..."
uv run alembic upgrade head

echo "==> Starting FastAPI..."
# Use uv run to ensure the right environment is used
exec uv run fastapi dev app/main.py --host 0.0.0.0 --port 8000
