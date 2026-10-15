/*
 * Service worker: what makes the app work with no internet.
 *
 * Bump CACHE whenever you export a new graph.json, otherwise phones that
 * already installed the app will keep serving the old map forever.
 */

const CACHE = 'jainnav-v5';

const FILES = [
  './',
  './index.html',
  './graph.json',
  './manifest.json',
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(FILES))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  // Cache first. The building does not change while someone is walking through
  // it, so serving the cached copy instantly is always the right call.
  event.respondWith(
    caches.match(event.request).then(hit => {
      if (hit) return hit;
      return fetch(event.request)
        .then(response => {
          if (response.ok && new URL(event.request.url).origin === location.origin) {
            const copy = response.clone();
            caches.open(CACHE).then(cache => cache.put(event.request, copy));
          }
          return response;
        })
        .catch(() => caches.match('./index.html'));
    })
  );
});
