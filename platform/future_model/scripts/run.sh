#!/usr/bin/env bash
set -euo pipefail
PROJECT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
export PYTHONPATH="$PROJECT/src${PYTHONPATH:+:$PYTHONPATH}"
exec "${PH_VENV:-$PROJECT/.venv}/bin/python" -m psychohistory.cli "$@"
