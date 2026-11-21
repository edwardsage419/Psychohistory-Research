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
test('Bash variables before Chinese punctuation use explicit braces', () => {
  // macOS Bash may extend variable-name parsing into full-width punctuation.
  // bash -n only checks syntax, so this test guards the reported runtime failure.
  assert.match(source, /\$\{program\}/);
  assert.doesNotMatch(source, /\$[A-Za-z_][A-Za-z0-9_]*[\u3001-\u303f\uff00-\uffef]/u);
});

test('private install helper checks port ownership and fails closed', () => {
  assert.match(source, /tailscale serve status/);
  assert.match(source, /已配置/);
  assert.match(source, /tailscale status/);
});
