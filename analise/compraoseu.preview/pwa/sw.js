/* ============================================================
   SERVICE WORKER — Portal O Despertar (PWA)
   Arquivo: sw.js
   Publicar em: https://www.compraoseu.com/sw.js
   (se a Vendd permitir upload de arquivos estáticos)
   ============================================================ */
const CACHE = 'portal-despertar-v1';
const URLS = [
  '/',
  '/livro01',
  '/livro02',
  '/livro03',
  '/livro04',
  '/livro05',
  '/livro06',
  '/livro07',
  '/livro08'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(URLS)).catch(() => {})
  );
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (e) => {
  // navegação: rede primeiro, fallback para cache (leitura pode exigir internet p/ proteção)
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).catch(() => caches.match(e.request).then((r) => r || caches.match('/')))
    );
    return;
  }
  // demais: cache primeiro, depois rede
  e.respondWith(
    caches.match(e.request).then((r) => r || fetch(e.request))
  );
});
