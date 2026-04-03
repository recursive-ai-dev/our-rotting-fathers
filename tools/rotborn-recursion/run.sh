#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ ! -d ".venv" ]; then
    echo "No .venv found. Run ./setup.sh first."
    exit 1
fi

source .venv/bin/activate
python3 run_app.py
