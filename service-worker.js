/* Kill-switch service worker.
   Older deploys of My Buddy AAC registered a precaching service worker; newer
   deploys stopped shipping one, which left old clients (esp. iOS Safari)
   permanently serving the stale cached build. This SW replaces any old one,
   deletes all caches, and reloads open pages so every client gets the fresh
   deploy. It caches nothing itself. */
self.addEventListener('install', function () {
  self.skipWaiting();
});
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys()
      .then(function (keys) { return Promise.all(keys.map(function (k) { return caches.delete(k); })); })
      .then(function () { return self.clients.matchAll({ type: 'window' }); })
      .then(function (clients) {
        clients.forEach(function (client) { client.navigate(client.url); });
      })
  );
});
self.addEventListener('fetch', function () { /* pass-through: no caching */ });
