#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Setting up Rotborn Recursion Engine..."

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip --quiet
pip install Pillow PyQt6 --quiet

echo "Done. Run ./run.sh to launch the GUI."
