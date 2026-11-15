#!/usr/bin/env bash
# Explicit user/operator action only; never called by install/start/verify.
set -euo pipefail
PROJECT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
REQUEST=$(mktemp /tmp/psychohistory-pr-request-XXXXXX.json)
trap 'rm -f "$REQUEST"' EXIT
python3.12 - "$PROJECT" "$REQUEST" <<'PY'
from pathlib import Path
import json,sys
project=Path(sys.argv[1])
Path(sys.argv[2]).write_text(json.dumps({'title':'feat(platform): Psychohistory Platform v0.1 synthetic research workflow [skip ci]','head':'feat/psychohistory-platform-v0.1','base':'main','draft':True,'body':(project/'reports/PR_DRAFT.md').read_text()},ensure_ascii=False))
PY
gh api --method POST repos/edwardsage419/Psychohistory-Research/pulls --input "$REQUEST"
