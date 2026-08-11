# 🆘 MENSAGEM PRONTA PARA O SUPORTE DA VENDD

**Motivo:** habilitar o PWA completo (manifest.json + service worker sw.js) no domínio compraoseu.com.

---

## Mensagem 1 — Pedido de como subir arquivos estáticos

> Olá, equipe Vendd! Tudo bem?
>
> Meu site é https://www.compraoseu.com (plataforma Vendd).
>
> Gostaria de saber **como fazer upload de arquivos estáticos no meu domínio**,
> para habilitar o PWA (Progressive Web App) do meu site.
>
> Preciso disponibilizar 2 arquivos em:
> - https://www.compraoseu.com/manifest.json
> - https://www.compraoseu.com/sw.js
>
> A Vendd tem alguma área de "Arquivos / Assets / Mídia" ou "Código personalizado"
> onde eu possa publicar esses arquivos? Se sim, onde fica no painel?
>
> Se não houver essa opção, existe outra forma recomendada pela Vendd para
> adicionar manifest.json e service worker ao site?
>
> Agradeço desde já pela atenção!

---

## Mensagem 2 — Se pedirem o conteúdo dos arquivos

> Obrigado pelo retorno!
>
> Segue o conteúdo dos arquivos que preciso publicar:
>
> **manifest.json**
> ```json
> {
>   "name": "Portal O Despertar — Missão com Deus",
>   "short_name": "Portal O Despertar",
>   "description": "Livros online gratuitos, devocional e portal de estudos para despertar sua mente, fortalecer sua fé e transformar sua vida.",
>   "id": "portal-o-despertar",
>   "start_url": "https://www.compraoseu.com/",
>   "scope": "https://www.compraoseu.com/",
>   "display": "standalone",
>   "orientation": "portrait",
>   "background_color": "#0e1a2e",
>   "theme_color": "#0e1a2e",
>   "lang": "pt-BR",
>   "icons": [
>     {
>       "src": "https://sidneyrma.github.io/instalador/icones/icon-192.png",
>       "sizes": "192x192",
>       "type": "image/png",
>       "purpose": "any"
>     },
>     {
>       "src": "https://sidneyrma.github.io/instalador/icones/icon-512.png",
>       "sizes": "512x512",
>       "type": "image/png",
>       "purpose": "any"
>     },
>     {
>       "src": "https://sidneyrma.github.io/instalador/icones/icon-512-maskable.png",
>       "sizes": "512x512",
>       "type": "image/png",
>       "purpose": "maskable"
>     }
>   ]
> }
> ```
>
> **sw.js**
> ```javascript
> const CACHE = 'portal-despertar-v1';
> const URLS = ['/', '/livro01', '/livro02', '/livro03', '/livro04', '/livro05', '/livro06', '/livro07', '/livro08'];
>
> self.addEventListener('install', (e) => {
>   e.waitUntil(caches.open(CACHE).then((c) => c.addAll(URLS)).catch(() => {}));
>   self.skipWaiting();
> });
>
> self.addEventListener('activate', (e) => {
>   e.waitUntil(caches.keys().then((keys) =>
>     Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
>   ));
>   self.clients.claim();
> });
>
> self.addEventListener('fetch', (e) => {
>   if (e.request.mode === 'navigate') {
>     e.respondWith(fetch(e.request).catch(() => caches.match(e.request).then((r) => r || caches.match('/'))));
>     return;
>   }
>   e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request)));
> });
> ```
>
> Muito obrigado!

---

## 📌 LEMBRETE: o que JÁ FUNCIONA sem o suporte

Mesmo aguardando o retorno da Vendd, o **atalho com o ícone do livro dourado**
já funciona — basta o visitante adicionar o site à tela inicial do celular:

- **Android (Chrome):** abrir `compraoseu.com` → menu **⋮** → "Adicionar à tela inicial"
- **iPhone (Safari):** abrir → Compartilhar → "Adicionar à Tela de Início"

O ícone usado é o `apple-touch-icon.png` / manifest do GitHub Pages (já no ar).
O service worker é que trará o **botão "Instalar" automático + offline** — esse sim
depende do upload na Vendd.

*Portal O Despertar · Missão com Deus · CompraOSeu*
