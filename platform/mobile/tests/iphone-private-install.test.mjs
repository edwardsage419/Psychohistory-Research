import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const path = fileURLToPath(new URL('../scripts/iphone-private-install.sh', import.meta.url));
const source = readFileSync(path, 'utf8');

test('private install helper has valid Bash syntax', () => {
  execFileSync('bash', ['-n', path]);
});
test('private install helper binds loopback and never uses public funnel', () => {
  assert.match(source, /--host 127\.0\.0\.1/);
  assert.match(source, /tailscale serve "--https=/);
  assert.doesNotMatch(source, /tailscale funnel\s/);
  assert.doesNotMatch(source, /tailscale serve --bg/);
  assert.match(source, /trap cleanup EXIT/);
});
test('private install helper checks port ownership and fails closed', () => {
  assert.match(source, /tailscale serve status/);
  assert.match(source, /已配置/);
  assert.match(source, /tailscale status/);
});
