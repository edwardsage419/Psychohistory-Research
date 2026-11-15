#!/usr/bin/env bash
set -euo pipefail
PROJECT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$PROJECT"
export PYTHONDONTWRITEBYTECODE=1
VENV=${PH_VENV:-"$PROJECT/.venv"}
"$VENV/bin/python" -m pip check
"$VENV/bin/python" -m pytest -q -p no:cacheprovider
npm --prefix web run build
PYTHONPATH=src python3.12 -S -c 'from psychohistory.engine import run_experiment; a=run_experiment(rounds=3,population=8); assert a==run_experiment(rounds=3,population=8); print("Independent stdlib-only core: PASS")'
