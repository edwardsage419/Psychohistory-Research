// Executed in a Chromium tab outside the app's service worker scope.
const equal = (actual, expected) => {
  if (actual !== expected) throw new Error(`Expected ${String(expected)}, received ${String(actual)}`);
};

function state(worker, expected) {
  if (worker.state === expected) return Promise.resolve();
  return new Promise((resolve, reject) => {
    worker.addEventListener('statechange', () => {
      if (worker.state === expected) resolve();
      if (worker.state === 'redundant' && expected !== 'redundant') reject(new Error('Worker installation failed'));
    });
  });
}

function launch() {
  const frame = document.createElement('iframe');
  return new Promise(resolve => {
    frame.addEventListener('load', () => resolve(frame), { once: true });
    frame.src = '/mobile/';
    document.body.append(frame);
  });
}

function updateWorker(registration, expected) {
  return new Promise((resolve, reject) => {
    registration.addEventListener('updatefound', async () => {
      const candidate = registration.installing;
      try {
        await state(candidate, expected);
        resolve(candidate);
      } catch (error) {
        reject(error);
      }
    }, { once: true });
    registration.update().catch(reject);
  });
}

const setFixture = state => fetch(`/fixture/${state}`, { method: 'POST' }).then(response => {
  equal(response.status, 204);
});

async function checkOfflineLifecycle() {
  const registration = await navigator.serviceWorker.register('/mobile/sw.js', { scope: '/mobile/', updateViaCache: 'none' });
  await state(registration.installing ?? registration.active, 'activated');
  const first = await launch();
  equal(first.contentDocument.title, 'Release one');
  equal(Boolean(first.contentWindow.navigator.serviceWorker.controller), true);

  await setFixture('bad');
  await updateWorker(registration, 'redundant');
  const prior = await launch();
  equal(prior.contentDocument.title, 'Release one');
  prior.remove();

  await setFixture('two');
  const update = await updateWorker(registration, 'installed');
  equal(registration.waiting, update);
  const stillOld = await launch();
  equal(stillOld.contentDocument.title, 'Release one');
  first.remove();
  stillOld.remove();
  await state(update, 'activated');
  const fresh = await launch();
  equal(fresh.contentDocument.title, 'Release two');
  const currentModule = fresh.contentDocument.querySelector('script').src;
  fresh.remove();

  const names = await caches.keys();
  equal(names.length, 3);
  for (const name of names) {
    const cache = await caches.open(name);
    if (await cache.match(currentModule)) {
      await cache.put(currentModule, new Response("document.title = 'corrupted';", { headers: { 'content-type': 'text/javascript' } }));
    }
  }
  await setFixture('offline');
  const fallback = await launch();
  equal(fallback.contentDocument.title, 'Release one');
  fallback.remove();

  for (const name of names) await caches.delete(name);
  const evicted = await launch();
  equal(evicted.contentDocument.title, '离线工作台暂不可用');
  evicted.remove();

  await setFixture('two');
  const repaired = await launch();
  equal(repaired.contentDocument.title, 'Release two');
  repaired.remove();
  await setFixture('offline');
  const offline = await launch();
  equal(offline.contentDocument.title, 'Release two');
}

let result;
try {
  await checkOfflineLifecycle();
  result = { pass: true };
} catch (error) {
  result = { pass: false, error: error.stack };
}
await fetch('/result', { method: 'POST', body: JSON.stringify(result) });
