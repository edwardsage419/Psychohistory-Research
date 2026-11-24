import assert from 'node:assert/strict';
import { spawn, spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { once } from 'node:events';
import { mkdtemp, mkdir, readFile, readdir, rm, writeFile, copyFile, symlink } from 'node:fs/promises';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { runInNewContext } from 'node:vm';
import { PUBLIC_MODULES } from '../scripts/build.mjs';

const mobile = new URL('../', import.meta.url);
const scope = 'https://mobile.example.test/workbench/';
const digest = bytes => createHash('sha256').update(bytes).digest('hex');

async function buildFixture(t, version, previousRoot) {
  const root = previousRoot ?? await mkdtemp(join(tmpdir(), 'psychohistory-mobile-build-'));
  if (!previousRoot) {
    t.after(() => rm(root, { recursive: true, force: true }));
    for (const directory of ['assets', 'scripts', 'src']) await mkdir(join(root, directory));
    for (const file of ['scripts/build.mjs', 'scripts/preview.mjs', 'sw.js', 'manifest.webmanifest', 'assets/icon.svg',
      'assets/apple-touch-icon.png', 'assets/icon-192.png', 'assets/icon-512.png']) {
      await copyFile(new URL(file, mobile), join(root, file));
    }
    for (const module of PUBLIC_MODULES) await writeFile(join(root, `src/${module}.mjs`), 'export {};\n');
  }
  await writeFile(join(root, 'index.html'), `<!doctype html><link rel="stylesheet" href="./styles.css"><link rel="manifest" href="./manifest.webmanifest"><p>Release ${version}</p><script type="module" src="./src/app.mjs"></script>`);
  await writeFile(join(root, 'styles.css'), `p { color: ${version === 'one' ? 'blue' : 'red'}; }`);
  await writeFile(join(root, 'src/app.mjs'), `document.title = 'Release ${version}';`);
  await writeFile(join(root, 'src/private-notes.mjs'), 'PRIVATE-NEVER-BUNDLE');
  await writeFile(join(root, 'personal-backup.json'), 'PRIVATE-NEVER-BUNDLE');
  const build = spawnSync(process.execPath, [join(root, 'scripts/build.mjs')], { encoding: 'utf8' });
  assert.equal(build.status, 0, build.stderr);
  const files = new Map();
  const dist = join(root, 'dist');
  for (const entry of await readdir(dist, { recursive: true, withFileTypes: true })) {
    if (entry.isFile()) {
      const path = join(entry.parentPath, entry.name);
      files.set(path.slice(dist.length + 1), await readFile(path));
    }
  }
  return { root, files };
}

class CacheStorageFixture {
  stores = new Map();
  failWrite = () => false;

  async keys() { return [...this.stores.keys()]; }
  async delete(name) { return this.stores.delete(name); }
  async has(name) { return this.stores.has(name); }

  async open(name) {
    if (!this.stores.has(name)) this.stores.set(name, new Map());
    const store = this.stores.get(name);
    return {
      match: async url => store.get(url)?.clone(),
      put: async (url, response) => {
        if (this.failWrite(url)) throw new Error('mock disk quota');
        store.set(url, response.clone());
      },
    };
  }
}

function loadWorker(build, { cache = new CacheStorageFixture(), originScope = scope, modify = () => {}, offline = false } = {}) {
  const listeners = new Map();
  const network = { offline, requests: [] };
  const release = JSON.parse(build.files.get('release-manifest.json'));
  const contentTypes = new Map(release.files.map(file => [file.path, file.contentType]));
  const claims = { count: 0 };
  const context = {
    self: {
      location: new URL('sw.js', originScope),
      registration: { scope: originScope },
      clients: { claim: async () => { claims.count += 1; } },
      addEventListener: (type, handler) => { listeners.set(type, handler); },
    },
    caches: cache,
    URL, Response, Request, Headers, crypto, TextDecoder, AbortController, setTimeout, clearTimeout,
    fetch: async (url, options) => {
      network.requests.push({ url: String(url), options });
      if (network.offline) throw new TypeError('offline');
      const file = String(url).slice(originScope.length);
      const bytes = build.files.get(file);
      if (!bytes) return new Response('missing', { status: 404 });
      const contentType = file === 'release-manifest.json' ? 'application/json' : contentTypes.get(file);
      const override = modify(file, bytes) ?? {};
      return new Response(override.body ?? bytes, {
        status: override.status ?? 200,
        headers: { 'content-type': override.contentType ?? contentType },
      });
    },
  };
  runInNewContext(build.files.get('sw.js').toString(), context);
  return {
    cache, network, claims,
    event(type, extras = {}) {
      let operation;
      listeners.get(type)?.({
        waitUntil: promise => { operation = promise; },
        respondWith: promise => { operation = promise; },
        ...extras,
      });
      return operation;
    },
    fetch(url = originScope, options = {}) {
      return this.event('fetch', {
        request: { url, method: 'GET', mode: 'navigate', headers: new Headers(), ...options },
      });
    },
  };
}

async function activate(worker) {
  await worker.event('install');
  await worker.event('activate');
}

const scriptPath = build => JSON.parse(build.files.get('release-manifest.json')).files
  .find(file => file.path.endsWith('/src/app.mjs')).path;

async function corrupt(cache, path) {
  for (const store of cache.stores.values()) {
    const url = new URL(path, scope).href;
    if (store.has(url)) store.set(url, new Response('not a public asset', { headers: { 'content-type': 'text/javascript' } }));
  }
}

test('build emits deterministic digests and excludes non-public files', async t => {
  const first = await buildFixture(t, 'one');
  const second = await buildFixture(t, 'one', first.root);
  assert.deepEqual(first.files, second.files);
  const manifest = JSON.parse(first.files.get('release-manifest.json'));
  for (const entry of manifest.files) {
    assert.equal(digest(first.files.get(entry.path)), entry.sha256);
    assert.equal(first.files.get(entry.path).length, entry.bytes);
  }
  assert.deepEqual([...first.files.keys()].sort(), [...manifest.files.map(file => file.path), 'release-manifest.json', 'sw.js'].sort());
  assert.ok(![...first.files.values()].some(bytes => bytes.includes('PRIVATE-NEVER-BUNDLE')));
  assert.match(first.files.get('index.html').toString(), new RegExp(`src="\\./${scriptPath(first)}"`));
  const webManifest = [...first.files].find(([path]) => path.endsWith('/manifest.webmanifest'))[1];
  assert.equal(JSON.parse(webManifest).start_url, '../../');
});

test('build runs when the CLI path traverses a symbolic link', async t => {
  const fixture = await buildFixture(t, 'one');
  const parent = await mkdtemp(join(tmpdir(), 'mobile-alias-'));
  t.after(() => rm(parent, { recursive: true, force: true }));
  const alias = join(parent, 'mobile');
  await symlink(fixture.root, alias);
  await rm(join(fixture.root, 'dist'), { recursive: true });
  const build = spawnSync(process.execPath, [join(alias, 'scripts/build.mjs')], { encoding: 'utf8' });
  assert.equal(build.status, 0, build.stderr);
  assert.deepEqual(await readFile(join(fixture.root, 'dist/release-manifest.json')), fixture.files.get('release-manifest.json'));
});

test('build rejects imports outside the packaged module graph', async t => {
  const build = await buildFixture(t, 'one');
  await writeFile(join(build.root, 'src/app.mjs'), `import './private-notes.mjs';`);
  const failed = spawnSync(process.execPath, [join(build.root, 'scripts/build.mjs')], { encoding: 'utf8' });
  assert.notEqual(failed.status, 0);
  assert.match(failed.stderr, /absent from the public release: .*private-notes/);
  const previous = await readFile(join(build.root, 'dist/release-manifest.json'));
  assert.deepEqual(previous, build.files.get('release-manifest.json'));
});

test('build fails when a required public module is missing', async t => {
  const build = await buildFixture(t, 'one');
  await rm(join(build.root, 'src/core.mjs'), { force: true });
  const failed = spawnSync(process.execPath, [join(build.root, 'scripts/build.mjs')], { encoding: 'utf8' });
  assert.notEqual(failed.status, 0);
  assert.match(failed.stderr, /core\.mjs/);
});

test('cold offline starts return the complete release with credential-free precaching', async t => {
  const build = await buildFixture(t, 'one');
  const worker = loadWorker(build);
  await activate(worker);
  assert.ok(worker.network.requests.every(({ options }) => options.credentials === 'omit' && options.redirect === 'error' && options.cache === 'no-store'));
  worker.network.offline = true;
  const requests = worker.network.requests.length;
  const shell = await worker.fetch();
  assert.equal(shell.status, 200);
  assert.match(await shell.text(), /Release one/);
  const script = await worker.fetch(new URL(scriptPath(build), scope).href, { mode: 'same-origin' });
  assert.equal(await script.text(), "document.title = 'Release one';");
  assert.equal(worker.network.requests.length, requests);
});

test('a failed candidate update leaves the previous release available offline', async t => {
  const old = await buildFixture(t, 'one');
  const candidate = await buildFixture(t, 'two', old.root);
  const current = loadWorker(old);
  await activate(current);
  const wrongManifest = loadWorker(candidate, { cache: current.cache,
    modify: (file, bytes) => file === 'release-manifest.json' ? { body: `${bytes.toString()}\n` } : {} });
  await assert.rejects(wrongManifest.event('install'), /manifest integrity/i);
  const tampered = loadWorker(candidate, { cache: current.cache, modify: file => file === scriptPath(candidate) ? { body: 'wrong' } : {} });
  await assert.rejects(tampered.event('install'), /integrity/i);
  current.cache.failWrite = url => url.endsWith(scriptPath(candidate));
  const quota = loadWorker(candidate, { cache: current.cache });
  await assert.rejects(quota.event('install'), /quota/i);
  current.network.offline = true;
  assert.match(await (await current.fetch()).text(), /Release one/);
});

test('updates keep the previous compatible release and never combine it with current files', async t => {
  const first = await buildFixture(t, 'one');
  const second = await buildFixture(t, 'two', first.root);
  const third = await buildFixture(t, 'three', first.root);
  const old = loadWorker(first);
  await activate(old);
  const previous = loadWorker(second, { cache: old.cache });
  await activate(previous);
  const current = loadWorker(third, { cache: old.cache });
  await activate(current);
  await corrupt(current.cache, scriptPath(third));
  const restarted = loadWorker(third, { cache: old.cache, offline: true });
  const shell = await restarted.fetch();
  assert.match(await shell.text(), /Release two/);
  let status;
  await restarted.event('message', {
    source: { url: scope }, data: { type: 'mobile-release-status' },
    ports: [{ postMessage: message => { status = message; } }],
  });
  assert.equal(status.ready, true);
  assert.equal(status.fallback, true);
  assert.equal(status.release, digest(second.files.get('release-manifest.json')));
  assert.equal(await (await restarted.fetch(new URL(scriptPath(second), scope).href, { mode: 'same-origin' })).text(), "document.title = 'Release two';");
  assert.equal((await restarted.fetch(new URL(scriptPath(third), scope).href, { mode: 'same-origin' })).status, 503);
  assert.equal((await restarted.fetch(new URL(scriptPath(first), scope).href, { mode: 'same-origin' })).status, 404);
});

test('activation discards an obsolete staged release that never controlled a page', async t => {
  const first = await buildFixture(t, 'one');
  const superseded = await buildFixture(t, 'two', first.root);
  const third = await buildFixture(t, 'three', first.root);
  const old = loadWorker(first);
  await activate(old);
  await loadWorker(superseded, { cache: old.cache }).event('install');
  const obsoleteHash = digest(superseded.files.get('release-manifest.json'));
  assert.ok((await old.cache.keys()).some(name => name.endsWith(obsoleteHash)));
  await activate(loadWorker(third, { cache: old.cache }));
  assert.ok(!(await old.cache.keys()).some(name => name.endsWith(obsoleteHash)));
});

test('an evicted release gives a recovery page offline and repairs itself online', async t => {
  const build = await buildFixture(t, 'one');
  const worker = loadWorker(build);
  await activate(worker);
  for (const name of await worker.cache.keys()) await worker.cache.delete(name);
  worker.network.offline = true;
  const recovery = await worker.fetch();
  assert.equal(recovery.status, 503);
  assert.match(await recovery.text(), /重新连接网络/);
  worker.network.offline = false;
  assert.match(await (await worker.fetch()).text(), /Release one/);
  worker.network.offline = true;
  assert.match(await (await worker.fetch()).text(), /Release one/);
});

test('a repaired release remains a fallback for the next verified update', async t => {
  const prior = await buildFixture(t, 'one');
  const candidate = await buildFixture(t, 'two', prior.root);
  const worker = loadWorker(prior);
  await activate(worker);
  for (const name of await worker.cache.keys()) await worker.cache.delete(name);
  assert.match(await (await worker.fetch()).text(), /Release one/);
  const updated = loadWorker(candidate, { cache: worker.cache });
  await activate(updated);
  await corrupt(worker.cache, scriptPath(candidate));
  updated.network.offline = true;
  assert.match(await (await updated.fetch()).text(), /Release one/);
});

test('workers ignore foreign, parameterized, private and authenticated requests', async t => {
  const build = await buildFixture(t, 'one');
  const otherScope = 'https://mobile.example.test/sibling/';
  const worker = loadWorker(build);
  const other = loadWorker(build, { cache: worker.cache, originScope: otherScope });
  await activate(other);
  await activate(worker);
  const requests = worker.network.requests.length;
  for (const [url, options] of [
    [otherScope, {}], ['https://api.example.test/', {}], [`${scope}?case=private`, {}], [`${scope}?`, {}],
    [`${scope}api/cases`, {}], [`${scope}personal-backup.json`, {}], [scope, { method: 'POST' }],
    [scope, { headers: new Headers({ authorization: 'Bearer private' }) }],
    [`${scope}${scriptPath(build)}?token=private`, { mode: 'same-origin' }],
  ]) {
    assert.equal(worker.fetch(url, options), undefined, url);
  }
  assert.equal(worker.network.requests.length, requests);
  other.network.offline = true;
  assert.match(await (await other.fetch()).text(), /Release one/);
});

test('preview serves the built package at a single scope without source or query routes', async t => {
  const build = await buildFixture(t, 'one');
  const server = spawn(process.execPath, [join(build.root, 'scripts/preview.mjs'), '--port', '0', '--base-path', '/local/']);
  t.after(async () => {
    if (server.exitCode === null) {
      server.kill();
      await once(server, 'exit');
    }
  });
  const startup = await Promise.race([once(server.stdout, 'data'), once(server, 'exit')]);
  assert.match(String(startup[0]), /http:\/\/127\.0\.0\.1:\d+\/local\//);
  const url = String(startup[0]).match(/https?:\/\/\S+/)[0];
  const shell = await fetch(url);
  assert.equal(shell.status, 200);
  assert.equal(await shell.text(), build.files.get('index.html').toString());
  const worker = await fetch(new URL('sw.js', url));
  assert.equal(worker.headers.get('content-type'), 'text/javascript; charset=utf-8');
  assert.equal(await worker.text(), build.files.get('sw.js').toString());
  for (const path of ['/index.html', './src/app.mjs', './?record=private', './personal-backup.json']) {
    assert.equal((await fetch(new URL(path, url))).status, 404, path);
  }
});

test('Chromium keeps offline releases atomic through failed updates, corruption and eviction', { timeout: 45_000 }, async t => {
  const chromium = process.env.CHROMIUM_BIN || 'chromium';
  const version = spawnSync(chromium, ['--version'], { encoding: 'utf8' });
  if (version.error?.code === 'ENOENT' && !process.env.CHROMIUM_BIN) {
    t.skip('Chromium is unavailable');
    return;
  }
  assert.equal(version.status, 0, version.stderr);
  const old = await buildFixture(t, 'one');
  const candidate = await buildFixture(t, 'two', old.root);
  const browserChecks = await readFile(new URL('./offline.browser.mjs', import.meta.url));
  const profile = await mkdtemp(join(tmpdir(), 'psychohistory-mobile-chromium-'));
  t.after(() => rm(profile, { recursive: true, force: true }));

  let delivery = 'one';
  const { promise: result, resolve } = Promise.withResolvers();
  const server = createServer(async (request, response) => {
    const path = request.url;
    const headers = { 'cache-control': 'no-store' };
    if (path === '/') {
      response.writeHead(200, { ...headers, 'content-type': 'text/html' })
        .end('<!doctype html><body><script type="module" src="/driver.mjs"></script>');
    } else if (path === '/driver.mjs') {
      response.writeHead(200, { ...headers, 'content-type': 'text/javascript' }).end(browserChecks);
    } else if (path === '/result' && request.method === 'POST') {
      const chunks = [];
      for await (const chunk of request) chunks.push(chunk);
      resolve(JSON.parse(Buffer.concat(chunks)));
      response.writeHead(204).end();
    } else if (/^\/fixture\/(bad|two|offline)$/.test(path) && request.method === 'POST') {
      delivery = path.slice('/fixture/'.length);
      response.writeHead(204).end();
    } else if (path.startsWith('/mobile/') && delivery !== 'offline') {
      const build = delivery === 'one' ? old : candidate;
      const file = path.slice('/mobile/'.length) || 'index.html';
      const type = new Map(JSON.parse(build.files.get('release-manifest.json')).files
        .map(entry => [entry.path, entry.contentType])).get(file)
        ?? (file === 'sw.js' ? 'text/javascript' : 'application/json');
      if (build.files.has(file)) {
        const bytes = delivery === 'bad' && file === scriptPath(candidate) ? Buffer.from('corrupted') : build.files.get(file);
        response.writeHead(200, { ...headers, 'content-type': type }).end(bytes);
      } else {
        response.writeHead(404).end();
      }
    } else if (path.startsWith('/mobile/')) {
      request.destroy();
    } else {
      response.writeHead(404).end();
    }
  });
  server.listen(0, '127.0.0.1');
  await once(server, 'listening');
  t.after(() => {
    server.closeAllConnections();
    return new Promise(resolve => server.close(resolve));
  });

  const child = spawn(chromium, ['--headless', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
    `--user-data-dir=${profile}`, `http://127.0.0.1:${server.address().port}/`], { stdio: 'ignore' });
  const exit = once(child, 'exit');
  try {
    const check = await Promise.race([result,
      exit.then(([code]) => { throw new Error(`Chromium exited before reporting offline checks (${code})`); }),
      once(t.signal, 'abort').then(() => { throw new Error(`Chromium offline check timed out in fixture ${delivery}`); })]);
    assert.equal(check.pass, true, check.error);
  } finally {
    child.kill();
    await exit;
  }
});
