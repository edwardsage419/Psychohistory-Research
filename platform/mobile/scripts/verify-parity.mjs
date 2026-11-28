import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { readFileSync } from 'node:fs';
import { createInterface } from 'node:readline';
import { pathToFileURL } from 'node:url';
import { analyze } from '../src/decision.mjs';

const cases = JSON.parse(readFileSync(0, 'utf8'));

async function compare(implementation, run) {
  let failures = 0;
  for (const item of cases) {
    try {
      const actual = await run(item.state);
      assert.equal(actual.input_hash, item.input_hash, 'canonical input SHA-256');
      assert.deepEqual(actual.temporal_scope, item.temporal_scope, 'current candidate scope');
      for (const [id, expected] of Object.entries(item.expect)) {
        const outcome = actual.methods.find(row => row.model_id === id);
        assert.equal(outcome.status, expected.status, `${id} admission: ${outcome.reasons.join(' ')}`);
        if (!expected.result) continue;
        for (const [field, value] of Object.entries(expected.result)) {
          assert.deepEqual(outcome.result[field], value, `${id}.${field}`);
        }
      }
      console.log(`PASS ${implementation} ${item.name}`);
    } catch (error) {
      failures++;
      console.error(`FAIL ${implementation} ${item.name}: ${error.message}`);
    }
  }
  console.log(`${cases.length - failures}/${cases.length} Python ↔ ${implementation} contract cases passed.`);
  if (failures) process.exitCode = 1;
}

await compare('Node', analyze);
const browserName = process.env.MOBILE_PARITY_BROWSER;
if (browserName) {
  assert.ok(['chromium', 'webkit'].includes(browserName), 'Expected chromium or webkit');
  const module = process.env.PLAYWRIGHT_MODULE;
  const { [browserName]: engine } = await import(module ? pathToFileURL(module) : 'playwright');
  const child = spawn(process.execPath, ['scripts/preview.mjs', '--port', '0'], { stdio: ['ignore', 'pipe', 'inherit'] });
  const closed = once(child, 'close');
  const output = createInterface({ input: child.stdout });
  const launched = once(output, 'line', { signal: AbortSignal.timeout(30_000) });
  let browser;
  try {
    const [line] = await Promise.race([launched, closed.then(() => { throw new Error('Static preview failed to start'); })]);
    assert.match(line, /^Preview http:\/\/127\.0\.0\.1:\d+\/$/);
    const executablePath = browserName === 'chromium' ? process.env.CHROMIUM_BIN : undefined;
    browser = await engine.launch({ executablePath });
    const page = await browser.newPage();
    await page.goto(line.slice('Preview '.length));
    const source = await page.locator('script[type="module"]').getAttribute('src');
    const decision = new URL(source.replace(/app\.mjs$/, 'decision.mjs'), page.url()).href;
    await compare(browserName, state => page.evaluate(async ({ decision, state }) => {
      const { analyze } = await import(decision);
      return analyze(state);
    }, { decision, state }));
  } finally {
    await browser?.close();
    child.kill();
    await closed;
  }
}
