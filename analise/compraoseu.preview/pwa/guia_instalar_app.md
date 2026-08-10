# 📱 COMO SEU SITE VIRA UM "APP" NO CELULAR (PWA)

**Objetivo:** permitir que seus leitores instalem o compraoseu.com como um **aplicativo
com ícone na tela inicial** — abrindo direto o site, sem digitar endereço.

---

## ✅ ESCOLHIDO: Ícone da Opção A (livro aberto com luz dourada)

O ícone do app é um **livro aberto com luz**, no estilo da marca (navy + dourado).
Já gerado em todas as dimensões necessárias.

---

## 🎯 CAMINHO RÁPIDO (funciona HOJE, sem código) — recomendo começar por aqui

Qualquer pessoa pode criar o atalho no celular em 10 segundos:

**No iPhone (iOS):**
1. Abra `compraoseu.com` no Safari;
2. Toque no botão **Compartilhar** (quadrado com ↑);
3. Role e toque em **"Adicionar à Tela de Início"**;
4. Confirme em **"Adicionar"** — aparece um ícone na tela inicial 📲.

**No Android (Chrome):**
1. Abra `compraoseu.com` no Chrome;
2. Toque no menu **⋮** (três pontinhos);
3. Toque em **"Adicionar à tela inicial"** (ou **"Instalar app"** se o PWA estiver ativo);
4. Confirme — ícone na tela inicial 📲.

> 💡 Com o PWA completo (passo abaixo), o Chrome oferece o **botão "Instalar"**
> automaticamente, e o app abre **em modo tela cheia (sem barra do navegador)** —
> experiência de aplicativo de verdade.

---

## 🛠️ CAMINHO PROFISSIONAL (PWA completo) — código para colar na Vendd

### Passo 1 — Os ícones já estão prontos no GitHub Pages

Os ícones foram gerados e já estão publicados em:

| Ícone | URL |
|---|---|
| 192x192 | `https://sidneyrma.github.io/instalador/icones/icon-192.png` |
| 512x512 | `https://sidneyrma.github.io/instalador/icones/icon-512.png` |
| 512x512 maskable | `https://sidneyrma.github.io/instalador/icones/icon-512-maskable.png` |
| Apple touch | `https://sidneyrma.github.io/instalador/icones/apple-touch-icon.png` |

### Passo 2 — O manifest.json

O arquivo `analise/compraoseu.preview/pwa/manifest.json` já está atualizado com os
links dos ícones (nome: **Portal O Despertar**). Ele precisa estar acessível em:
```
https://www.compraoseu.com/manifest.json
```
**Como fazer na Vendd:** suba o `manifest.json` na área de arquivos/mídia da Vendd
e confira se fica acessível nesse endereço. Se a Vendd não permitir, veja o
**Caminho Alternativo** no fim.

### Passo 3 — Cole o código no HEAD da página principal (Vendd)

Abra o arquivo `analise/compraoseu.preview/pwa/codigo_para_vendd.html` e cole o
conteúdo no `<head>` da página principal (antes de `</head>`).

### Passo 4 — O service worker (para instalar + offline)

Suba o arquivo `analise/compraoseu.preview/pwa/sw.js` para
`https://www.compraoseu.com/sw.js` (área de arquivos da Vendd).
O código do Passo 3 já registra o SW automaticamente.

---

## 🔄 Caminho alternativo (se a Vendd não permitir subir manifest/sw.js)

Mesmo sem o PWA completo, o **Caminho Rápido** (atalho na tela inicial) funciona.
Para melhorar o ícone do atalho sem o manifest:
- No **iPhone**: o atalho usa o `apple-touch-icon.png` automaticamente se ele estiver
  no site — por isso cole no `<head>` o link:
  `<link rel="apple-touch-icon" href="https://sidneyrma.github.io/instalador/icones/apple-touch-icon.png">`
- No **Android**: o atalho usa o favicon/ícone padrão do site.

---

## ✅ CHECKLIST

- [ ] Ícones publicados no GitHub Pages (já feito, commit enviado)
- [ ] `manifest.json` atualizado com os links (já feito)
- [ ] Subir `manifest.json` e `sw.js` na Vendd (se possível)
- [ ] Colar o bloco do arquivo `codigo_para_vendd.html` no `<head>` da Home
- [ ] Testar no celular: abrir o site → "Instalar app" → ícone na tela inicial

---

*Ícone: Opção A (livro aberto com luz) · Portal O Despertar · Missão com Deus*
