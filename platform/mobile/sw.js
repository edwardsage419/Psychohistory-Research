/* Release placeholders are filled by npm run build. CacheStorage holds public files only. */
const CURRENT_RELEASE = '__MOBILE_RELEASE_SHA256__';
const PUBLIC_PATHS = new Set(JSON.parse('__MOBILE_PUBLIC_PATHS__'));
const SCOPE = new URL(self.registration.scope);
const CACHE_PREFIX = `psychohistory-mobile:1:${encodeURIComponent(SCOPE.href)}:`;
const LIFECYCLE_CACHE = `${CACHE_PREFIX}lifecycle`;
const INDEX = new URL('index.html', SCOPE).href;
const MANIFEST = new URL('release-manifest.json', SCOPE).href;
const STATE = new URL('.mobile-cache-state', SCOPE).href;
const SHA256 = /^[a-f0-9]{64}$/;
const assetPath = /^releases\/([a-f0-9]{64})\/(.+)$/;
const mediaTypes = {
  html: ['text/html'], css: ['text/css'], webmanifest: ['application/manifest+json', 'application/json'],
  png: ['image/png'], svg: ['image/svg+xml'], mjs: ['text/javascript', 'application/javascript'],
};
let repair;

function cacheName(release) {
  return `${CACHE_PREFIX}${release}`;
}

function publicResponse(bytes, contentType, status = 200) {
  return new Response(bytes, {
    status,
    headers: { 'Content-Type': contentType, 'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff' },
  });
}

async function digest(bytes) {
  return Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)),
    byte => byte.toString(16).padStart(2, '0')).join('');
}

function validPublicPath(path, revision) {
  if (path === 'index.html') return true;
  const match = assetPath.exec(path);
  return match?.[1] === revision && PUBLIC_PATHS.has(match[2]);
}

async function readManifest(response, release) {
  if (!response || response.status !== 200) throw new Error('Missing release manifest');
  const bytes = await response.arrayBuffer();
  if (await digest(bytes) !== release) throw new Error('Release manifest integrity failure');
  const manifest = JSON.parse(new TextDecoder().decode(bytes));
  if (manifest.schema !== 1 || !SHA256.test(manifest.revision) || !Array.isArray(manifest.files)) {
    throw new Error('Incompatible release manifest');
  }
  const files = new Map();
  for (const file of manifest.files) {
    if (typeof file.path !== 'string' || !validPublicPath(file.path, manifest.revision)
      || files.has(file.path) || !SHA256.test(file.sha256) || !Number.isSafeInteger(file.bytes)
      || file.bytes < 0 || mediaTypes[file.path.split('.').at(-1)]?.[0] !== file.contentType) {
      throw new Error('Invalid public release file');
    }
    files.set(file.path, file);
  }
  if (!files.has('index.html') || !files.has(`releases/${manifest.revision}/src/app.mjs`)) {
    throw new Error('Incomplete release manifest');
  }
  return { release, files, bytes };
}

async function verifyAsset(response, file) {
  const contentType = response?.headers.get('Content-Type')?.split(';')[0].trim().toLowerCase();
  if (response?.status !== 200 || !mediaTypes[file.path.split('.').at(-1)].includes(contentType)) {
    throw new Error(`Release resource unavailable: ${file.path}`);
  }
  const bytes = await response.arrayBuffer();
  if (bytes.byteLength !== file.bytes || await digest(bytes) !== file.sha256) {
    throw new Error(`Release resource integrity failure: ${file.path}`);
  }
  const type = /^(text\/|application\/manifest\+json)/.test(file.contentType)
    ? `${file.contentType}; charset=utf-8` : file.contentType;
  return publicResponse(bytes, type);
}

function fetchPublic(url, signal) {
  return fetch(url, { method: 'GET', mode: 'same-origin', credentials: 'omit', redirect: 'error', cache: 'no-store', signal });
}

async function downloadRelease(timeoutMs) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const manifest = await readManifest(await fetchPublic(MANIFEST, controller.signal), CURRENT_RELEASE);
    const assets = await Promise.all(Array.from(manifest.files, async ([path, file]) => {
      const url = new URL(path, SCOPE).href;
      return [url, await verifyAsset(await fetchPublic(url, controller.signal), file)];
    }));
    return { manifest, assets };
  } finally {
    clearTimeout(timeout);
    controller.abort();
  }
}

async function cachedManifest(release) {
  try {
    const name = cacheName(release);
    if (!await caches.has(name)) return null;
    const cache = await caches.open(name);
    return { ...await readManifest(await cache.match(MANIFEST), release), cache };
  } catch {
    return null;
  }
}

async function verifiedRelease(release) {
  if (!release) return null;
  const manifest = await cachedManifest(release);
  if (!manifest) return null;
  try {
    const assets = new Map(await Promise.all(Array.from(manifest.files, async ([path, file]) => {
      const url = new URL(path, SCOPE).href;
      return [path, await verifyAsset(await manifest.cache.match(url), file)];
    })));
    return { release, shell: assets.get('index.html') };
  } catch {
    return null;
  }
}

async function stageCurrent(timeoutMs) {
  const { manifest, assets } = await downloadRelease(timeoutMs);
  if (await verifiedRelease(CURRENT_RELEASE)) return;

  const name = cacheName(CURRENT_RELEASE);
  await caches.delete(name);
  try {
    const cache = await caches.open(name);
    for (const [url, response] of assets) await cache.put(url, response);
    // The verified manifest is the commit marker. A partial release is never read.
    await cache.put(MANIFEST, publicResponse(manifest.bytes, 'application/json'));
  } catch (error) {
    await caches.delete(name).catch(() => {});
    throw error;
  }
}

async function lifecycle() {
  try {
    if (await caches.has(LIFECYCLE_CACHE)) {
      const cache = await caches.open(LIFECYCLE_CACHE);
      const state = await (await cache.match(STATE))?.json();
      if (state && typeof state.current === 'string' && SHA256.test(state.current)
        && (state.previous === null || (typeof state.previous === 'string' && SHA256.test(state.previous)))) {
        return [state.current, state.previous];
      }
    }
  } catch { /* CacheStorage can be unavailable or evicted. */ }
  return [];
}

async function previousRelease(releases) {
  for (const release of releases ?? await lifecycle()) {
    if (release === CURRENT_RELEASE) continue;
    const previous = await verifiedRelease(release);
    if (previous) return previous;
  }
  return null;
}

async function rememberCurrent(activating = false) {
  const retained = await lifecycle();
  if (retained[0] === CURRENT_RELEASE || (!activating && retained.length)) return;
  const previous = (await previousRelease(retained))?.release ?? null;
  try {
    const cache = await caches.open(LIFECYCLE_CACHE);
    await cache.put(STATE, publicResponse(JSON.stringify({ current: CURRENT_RELEASE, previous }), 'application/json'));
    if (!activating) return;
    const names = await caches.keys();
    // A new candidate may already be staging while this worker activates.
    if (self.registration.installing || self.registration.waiting) return;
    const keep = new Set([CURRENT_RELEASE, previous]);
    await Promise.all(names.filter(name => {
      if (!name.startsWith(CACHE_PREFIX)) return false;
      const release = name.slice(CACHE_PREFIX.length);
      return SHA256.test(release) && !keep.has(release);
    }).map(name => caches.delete(name)));
  } catch { /* Keep the old release if metadata or cleanup cannot be written. */ }
}

async function activateCurrent() {
  // The normal waiting phase keeps open clients on their current release.
  if (await verifiedRelease(CURRENT_RELEASE)) await rememberCurrent(true);
  await self.clients.claim();
}

async function openApp() {
  const current = await verifiedRelease(CURRENT_RELEASE);
  if (current) {
    await rememberCurrent();
    return current.shell;
  }
  try {
    repair ??= stageCurrent(4500).finally(() => { repair = null; });
    await repair;
    const restored = await verifiedRelease(CURRENT_RELEASE);
    if (restored) {
      await rememberCurrent();
      return restored.shell;
    }
  } catch { /* A failed repair may still leave a verified previous release. */ }

  const previous = await previousRelease();
  if (previous) return previous.shell;
  return publicResponse(`<!doctype html><html lang="zh-Hans"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>离线工作台暂不可用</title>
<main><h1>离线工作台暂不可用</h1><p>本机缺少完整、可校验的应用文件。请重新连接网络后从原安装地址重开，重新下载应用文件。</p>
<p>应用缓存只含公开程序文件。个人记录的可用性取决于设备保留的加密存储和授权记录。</p>
<p><a href="./">重新尝试</a></p></main></html>`, 'text/html; charset=utf-8', 503);
}

async function openAsset(path) {
  const releases = new Set([CURRENT_RELEASE, ...await lifecycle()]);
  for (const release of releases) {
    if (!release) continue;
    const manifest = await cachedManifest(release);
    const file = manifest?.files.get(path);
    if (!file) continue;
    try {
      return await verifyAsset(await manifest.cache.match(new URL(path, SCOPE).href), file);
    } catch {
      return publicResponse('应用文件不可用。请重新打开工作台。', 'text/plain; charset=utf-8', 503);
    }
  }
  return publicResponse('找不到此应用版本的文件。', 'text/plain; charset=utf-8', 404);
}

function isInScope(url) {
  return url.origin === SCOPE.origin && url.pathname.startsWith(SCOPE.pathname);
}

self.addEventListener('install', event => event.waitUntil(stageCurrent(20000)));
self.addEventListener('activate', event => event.waitUntil(activateCurrent()));
self.addEventListener('fetch', event => {
  const { request } = event;
  if (request.method !== 'GET' || request.headers.has('Authorization') || request.headers.has('Range')) return;
  const url = new URL(request.url);
  if (!isInScope(url) || url.href.includes('?') || url.hash) return;
  if (request.mode === 'navigate' && (url.href === SCOPE.href || url.href === INDEX)) {
    event.respondWith(openApp());
    return;
  }
  const path = url.pathname.slice(SCOPE.pathname.length);
  const match = assetPath.exec(path);
  if (match && PUBLIC_PATHS.has(match[2])) event.respondWith(openAsset(path));
});

self.addEventListener('message', event => {
  const port = event.ports[0];
  if (!port || event.data?.type !== 'mobile-release-status' || !event.source?.url
    || !isInScope(new URL(event.source.url))) return;
  event.waitUntil((async () => {
    const available = await verifiedRelease(CURRENT_RELEASE) ?? await previousRelease();
    port.postMessage({ type: 'mobile-release-status', ready: Boolean(available),
      release: available?.release ?? null, fallback: Boolean(available && available.release !== CURRENT_RELEASE) });
  })());
});
