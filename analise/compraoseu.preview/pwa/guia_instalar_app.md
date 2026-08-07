# 📱 COMO SEU SITE VIRA UM "APP" NO CELULAR (PWA)

**Objetivo:** permitir que seus leitores instalem o compraoseu.com como um **aplicativo
com ícone na tela inicial** — abrindo direto o site, sem digitar endereço.

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

### Passo 1 — Suba os ícones para o imgbb
1. Acesse **imgbb.com** → Upload;
2. Suba: `icon-192.png`, `icon-512.png`, `icon-512-maskable.png`, `apple-touch-icon.png`
   (pasta `pwa/` deste repositório);
3. Copie os **links diretos** de cada um (terminam em `.png`).

### Passo 2 — Atualize o manifest.json
No arquivo `pwa/manifest.json`, **substitua** `https://i.ibb.co/ICON-PLACEHOLDER/...`
pelos links reais do imgbb (para cada ícone).

> **Importante:** o manifest precisa estar acessível em `https://www.compraoseu.com/manifest.json`.
> A Vendd permite **upload de arquivos** (área de mídia/arquivos) — suba o `manifest.json` 
> atualizado lá. Se a Vendd não permitir, use o **Caminho Alternativo** abaixo.

### Passo 3 — Cole este código no HEAD da página principal (Vendd)
```html
<!-- ===== PWA: instalar como app ===== -->
<link rel="manifest" href="https://www.compraoseu.com/manifest.json">

<!-- Ícone do app no iOS -->
<link rel="apple-touch-icon" href="https://i.ibb.co/SEU-LINK/apple-touch-icon.png">

<!-- Cor da barra no Android -->
<meta name="theme-color" content="#0e1a2e">

<!-- iOS: abrir em modo app (tela cheia) -->
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Missão com Deus">
<!-- ===== fim PWA ===== -->
```

### Passo 4 — Publique e teste
1. Abra `compraoseu.com` no celular (Android/Chrome);
2. Deve aparecer o **ícone de instalar** (ou o menu ⋮ → "Instalar app");
3. No iPhone, o "Adicionar à Tela de Início" agora usa o ícone bonito da marca;
4. O app abre **tela cheia**, com ícone próprio na tela inicial. 📲✨

---

## 🔄 CAMINHO ALTERNATIVO (se a Vendd não aceitar arquivo manifest)

Se não conseguir subir o `manifest.json`, use o **manifest embutido (data URI)** no HEAD:

```html
<link rel="manifest" href='data:application/manifest+json,{"name":"Missão com Deus — CompraOSeu","short_name":"Missão com Deus","start_url":"https://www.compraoseu.com/","display":"standalone","background_color":"%230e1a2e","theme_color":"%230e1a2e","icons":[{"src":"https://i.ibb.co/SEU-LINK/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"https://i.ibb.co/SEU-LINK/icon-512.png","sizes":"512x512","type":"image/png"}]}'>
```

*(substitua SEU-LINK pelos links reais dos ícones)*

---

## ❓ PERGUNTAS FREQUENTES

**Funciona no iPhone?** ✅ Sim — com `apple-touch-icon` + as meta tags, o "Adicionar à
Tela de Início" cria um app com ícone e abre em tela cheia.

**O app precisa de internet?** Para a leitura online, sim (o conteúdo está no site).
Uma versão com *offline* exigiria Service Worker — posso preparar depois se quiser.

**O atalho aponta para o quê?** Para `https://www.compraoseu.com/` — o leitor abre direto
na Home e continua onde parou.

**Isso ajuda a fidelizar leitores?** 🎯 **Muito!** Quem tem o ícone na tela inicial
volta com 1 toque — sem digitar endereço. É o comportamento de app que retém.

---

## 📁 ARQUIVOS (pasta `pwa/`)

| Arquivo | Uso |
|---|---|
| `manifest.json` | Manifesto do app (edite os links dos ícones) |
| `icon-192.png` | Ícone Android (192×192) |
| `icon-512.png` | Ícone Android (512×512) |
| `icon-512-maskable.png` | Ícone com área segura (máscara) |
| `apple-touch-icon.png` | Ícone do iOS (180×180) |

---

*Guia gerado em 07/08/2026 · Missão com Deus · CompraOSeu*
