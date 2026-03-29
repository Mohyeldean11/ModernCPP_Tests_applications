#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [ -x ".venv/bin/python" ]; then
  if .venv/bin/python -m pip --version >/dev/null 2>&1; then
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python checklist_app.py
    exit 0
  fi
fi

if python3 -m venv .venv 2>/dev/null; then
  if .venv/bin/python -m pip --version >/dev/null 2>&1; then
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python checklist_app.py
    exit 0
  fi
fi

python3 -m pip install --user --break-system-packages -r requirements.txt
python3 checklist_app.py
