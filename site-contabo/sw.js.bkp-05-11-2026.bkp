/* Service Worker — Missão com Deus (PWA) */
const CACHE = 'missao-com-deus-v10-seo-offline';
const URLS = ['/', '/manifest.json', '/livro04', '/livro05', '/livro06', '/livro07', '/livro09', '/livro11', '/guia-pais-filhos'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(URLS)).catch(() => {}));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k.startsWith('missao-com-deus-') && k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  // MISSAO_MEDICAO_REDE_V1: eventos e PHP nunca usam resposta offline.
  const url = new URL(e.request.url);
  if (url.origin !== self.location.origin || e.request.method !== 'GET') return;
  if (url.pathname.startsWith('/q-') || url.pathname.endsWith('.php')) {
    e.respondWith(fetch(e.request, {cache: 'no-store'}));
    return;
  }
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request).then((r) => r || caches.match('/')))
    );
    return;
  }
  e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request)));
});
