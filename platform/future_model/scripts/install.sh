#!/usr/bin/env bash
set -euo pipefail
PROJECT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
VENV=${PH_VENV:-"$PROJECT/.venv"}
python3.12 -c 'import sys; assert sys.version_info[:2]==(3,12)'
node -e 'if(Number(process.versions.node.split(".")[0])!==24)throw Error("Node.js 24 LTS required")'
python3.12 -m venv "$VENV"
export PIP_CACHE_DIR=${PIP_CACHE_DIR:-/tmp/psychohistory-pip-cache}
export npm_config_cache=${npm_config_cache:-/tmp/psychohistory-npm-cache}
export PIP_DISABLE_PIP_VERSION_CHECK=1
"$VENV/bin/python" -m pip install --index-url https://pypi.org/simple --only-binary=:all: -r "$PROJECT/requirements.lock"
npm --prefix "$PROJECT/web" --registry=https://registry.npmjs.org ci --no-audit --no-fund --ignore-scripts
npm --prefix "$PROJECT/web" run build
