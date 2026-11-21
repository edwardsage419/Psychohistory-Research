/* Only public application files are cached. Personal data NEVER enters CacheStorage. */
const VERSION = 'psychohistory-mobile-dev-01';
const ASSETS = ['./', './index.html', './styles.css', './manifest.webmanifest', './assets/icon.svg',
  './src/app.mjs', './src/core.mjs', './src/vault.mjs', './README.md'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(VERSION).then(cache => cache.addAll(ASSETS)));
});
self.addEventListener('activate', event => {
  event.waitUntil(Promise.all([
    caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith('psychohistory-mobile-') && key !== VERSION).map(key => caches.delete(key)))),
    self.clients.claim(),
  ]));
});
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;
  if (url.pathname.includes('/api/') || url.pathname.endsWith('/token')) return;
  event.respondWith(caches.match(req, { ignoreSearch: req.mode === 'navigate' }).then(hit => hit || fetch(req)));
});
