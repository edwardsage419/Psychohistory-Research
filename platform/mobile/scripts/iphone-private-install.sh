#!/usr/bin/env bash
# Start a temporary, tailnet-only HTTPS installer for the offline iPhone PWA.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL_PORT="${MOBILE_PREVIEW_PORT:-8766}"
HTTPS_PORT="${MOBILE_TAILNET_HTTPS_PORT:-8443}"
PREVIEW_PID=""
LOGFILE=""

fail() { printf '错误：%s\n' "$*" >&2; exit 1; }
valid_port() {
  [[ "$1" =~ ^[0-9]{1,5}$ ]] || return 1
  (( 10#$1 >= 1024 && 10#$1 <= 65535 ))
}
valid_port "$LOCAL_PORT" || fail "本地端口必须在 1024 至 65535 之间。"
valid_port "$HTTPS_PORT" || fail "HTTPS 端口必须在 1024 至 65535 之间。"

for program in node curl; do
  command -v "$program" >/dev/null 2>&1 || fail "请先安装并配置 ${program}。"
done

# The macOS GUI executable must be called using its real path.
# A manually created symlink in /usr/local/bin can crash with
# 'bundleIdentifier is unknown to the registry' on macOS.
if [[ "$(uname -s)" == "Darwin" && -x /Applications/Tailscale.app/Contents/MacOS/Tailscale ]]; then
  tailscale_cli() {
    TAILSCALE_BE_CLI=1 /Applications/Tailscale.app/Contents/MacOS/Tailscale "$@"
  }
else
  command -v tailscale >/dev/null 2>&1 || fail "请先安装 Tailscale。"
  tailscale_cli() {
    TAILSCALE_BE_CLI=1 command tailscale "$@"
  }
fi

node -e 'if (Number(process.versions.node.split(".")[0]) < 22) process.exit(1)' ||
  fail "需要 Node.js 22 或更新版本。"
tailscale_cli status >/dev/null 2>&1 ||
  fail "请在 Mac 登录 Tailscale，让 iPhone 加入同一个私人网络。"

# Do not overwrite another existing Serve endpoint.
SERVE_STATUS="$(tailscale_cli serve status 2>&1 || true)"
if printf '%s\n' "$SERVE_STATUS" | grep -Eq ":${HTTPS_PORT}([^0-9]|$)"; then
  fail "HTTPS 端口 $HTTPS_PORT 已配置，请检查现有 Serve 配置。"
fi
node - "$LOCAL_PORT" <<'NODE' || fail "本地端口 $LOCAL_PORT 已被占用。"
const net = require('node:net');
const port = Number(process.argv[2]);
const server = net.createServer();
server.once('error', () => process.exit(1));
server.listen(port, '127.0.0.1', () => server.close());
NODE

cleanup() {
  if [[ -n "$PREVIEW_PID" ]]; then
    kill "$PREVIEW_PID" 2>/dev/null || true
    wait "$PREVIEW_PID" 2>/dev/null || true
  fi
  if [[ -n "$LOGFILE" ]]; then rm -f "$LOGFILE"; fi
}
trap cleanup EXIT

LOGFILE="$(mktemp "${TMPDIR:-/tmp}/psychohistory-mobile-serve.XXXXXX")"
chmod 600 "$LOGFILE"
node "$ROOT/scripts/preview.mjs" --host 127.0.0.1 --port "$LOCAL_PORT" >"$LOGFILE" 2>&1 &
PREVIEW_PID=$!

READY=0
for _ in {1..80}; do
  if curl --fail --silent --max-time 1 "http://127.0.0.1:$LOCAL_PORT/release-manifest.json" >/dev/null 2>&1; then
    READY=1; break
  fi
  if ! kill -0 "$PREVIEW_PID" 2>/dev/null; then cat "$LOGFILE" >&2; fail "静态应用构建或启动失败。"; fi
  sleep 0.2
done
[[ "$READY" == 1 ]] || { cat "$LOGFILE" >&2; fail "本机安装文件未就绪。"; }

printf '\n已启动公开应用文件的本地静态服务：127.0.0.1:%s\n' "$LOCAL_PORT"
printf '即将启动私人 Tailscale Serve HTTPS:%s（只允许 tailnet 内可访问的设备）。\n' "$HTTPS_PORT"
printf '请在 iPhone Safari 打开终端输出的 HTTPS 地址，添加到主屏幕，并在主屏幕应用中确认离线资源就绪。\n'
printf '勿启用 Funnel，勿传输真实个人数据。完成安装后按 Ctrl+C 结束此安装会话。\n\n'
tailscale_cli serve "--https=$HTTPS_PORT" "http://127.0.0.1:$LOCAL_PORT"
