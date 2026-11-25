import assert from 'node:assert/strict';
import { execFileSync, spawn } from 'node:child_process';
import { mkdtemp, readFile, rm } from 'node:fs/promises';
import { createServer } from 'node:http';
import { once } from 'node:events';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

const browser = process.env.CHROMIUM_BIN || 'chromium';

test('mobile vault privacy contract in actual Chromium IndexedDB', { timeout: 45_000 }, async t => {
  try {
    execFileSync(browser, ['--version'], { stdio: 'ignore' });
  } catch (error) {
    if (error.code !== 'ENOENT' || process.env.CHROMIUM_BIN) throw error;
    t.skip('Chromium is unavailable');
    return;
  }
  const profile = await mkdtemp(join(tmpdir(), 'mobile-vault-browser-'));
  const files = {
    '/vault.mjs': await readFile(new URL('../src/vault.mjs', import.meta.url)),
    '/check.mjs': await readFile(new URL('./vault.browser.mjs', import.meta.url)),
  };
  const server = createServer();
  const results = new Promise(resolve => {
    server.on('request', async (request, response) => {
      if (request.url === '/results') {
        const chunks = [];
        for await (const chunk of request) chunks.push(chunk);
        response.end();
        resolve(JSON.parse(Buffer.concat(chunks).toString()));
      } else if (Object.hasOwn(files, request.url)) {
        response.writeHead(200, { 'content-type': 'text/javascript' }).end(files[request.url]);
      } else {
        response.writeHead(200, { 'content-type': 'text/html' }).end('<script type="module" src="/check.mjs"></script>');
      }
    });
  });
  t.after(async () => {
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
    await rm(profile, { recursive: true, force: true });
  });
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  const child = spawn(browser, [
    '--headless', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
    `--user-data-dir=${profile}`, `http://127.0.0.1:${server.address().port}`,
  ], { stdio: 'ignore' });
  const exit = once(child, 'exit');
  try {
    const cases = await Promise.race([
      results,
      exit.then(([code]) => { throw new Error(`Chromium exited before running vault contracts (${code})`); }),
      once(t.signal, 'abort').then(() => { throw new Error('Browser vault checks timed out'); }),
    ]);
    assert.equal(cases.length, 8);
    for (const { name, error } of cases) {
      await t.test(name, () => assert.equal(error, undefined));
    }
  } finally {
    child.kill();
    await exit;
  }
});
