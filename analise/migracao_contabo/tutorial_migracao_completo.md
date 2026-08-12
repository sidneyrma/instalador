# 🚀 TUTORIAL COMPLETO: MIGRAR O SITE PARA A CONTABO AGORA
**Passo a passo atualizado · 12/08/2026 (madrugada) · compraoseu.com**

> **STATUS EM 12/08/2026 (madrugada):** o usuário decidiu **dar mais uma chance à Vendd** e
> descansar. O domínio **já saiu do Cloudflare e está na HostGator** (nameservers
> `dns3.hostgator.com.br` / `dns4.hostgator.com.br`). O plano abaixo está pronto para ser
> executado na primeira hora da manhã, **se a Vendd não resolver o problema até lá**.

---

## 📌 ANTES DE COMEÇAR (o que ter em mãos)

1. **IP do servidor Contabo:** `212.28.182.86`
2. **Acesso ao aaPanel:** já está logado (Nginx rodando, site criado, arquivos no lugar)
3. **Acesso à HostGator (registrar):** onde está o DNS agora (nameservers hostgator)
4. **Arquivos do site:** `site-contabo.zip` (última versão, já com links relativos)
5. **Conta Cloudflare `Compraoseu.com@gmail.com`:** NÃO contém o domínio (a zona estava na conta da Vendd — agora não usamos mais)

---

## 🟢 PASSO 1 — Confirmar que o site está pronto no servidor (15 min)

### 1.1 Confira os arquivos
No aaPanel: **Files** → `/www/wwwroot/compraoseu.com` → deve ter:
- `index.html`, `livro01.html` ... `livro10.html`
- `capas/`, `icones/`, `manifest.json`, `sw.js`, `robots.txt`, `sitemap.xml`

> Se faltar algo, reenvie o `site-contabo.zip` e extraia na pasta (substituindo).

### 1.2 Confira a regra de URLs bonitas
No aaPanel: **Website → compraoseu.com → Config** → confira que existe:
```
location / {
    try_files $uri $uri.html $uri/index.html =404;
}
```
Salve (Ctrl+S) e dê **Reload** no Nginx.

### 1.3 Teste local (sem DNS)
- No computador, com a linha no `hosts` (`212.28.182.86 compraoseu.com www.compraoseu.com`):
  - `http://compraoseu.com` → Home nova ✅
  - `http://compraoseu.com/livro01` → O Verbo que Transforma ✅
- **Importante:** os links internos já são relativos (`/livro01`), então funcionam em http.

> ✅ Quando TUDO abrir certo, siga para o Passo 2.

---

## 🟡 PASSO 2 — Apontar o domínio para a Contabo (na HostGator) — 10 min

> O domínio **já está na HostGator** (nameservers `dns3`/`dns4.hostgator.com.br`).
> Agora basta editar a Zona de DNS.

### 2.1 Acesse a Zona de DNS da HostGator
- HostGator → domínio `compraoseu.com` → **"Editar Zona Avançada de DNS"**.

### 2.2 Edite o registro A principal (o clique que muda tudo!)
Localize a linha:
- **A** · Nome: `compraoseu.com` · Valor: `162.240.81.81` (ou outro)

Clique no **lápis (editar)** e troque o valor para:
- **`212.28.182.86`** 🎯

Salve. **Pronto: o compraoseu.com passa a apontar para a Contabo.**

### 2.3 Mantenha o CNAME do www (não mudar)
- **CNAME** · `www.compraoseu.com` → `compraoseu.com` ✅ (deixe como está)

### 2.4 Adicione os registros do chatbot (para a Laura continuar!)
Clique em **"Adicionar registro"** e crie:
- **A** · Nome: `app` · Valor: `212.28.182.86`
- **A** · Nome: `api` · Valor: `212.28.182.86`
- **A** · Nome: `apioficial` · Valor: `212.28.182.86`

### 2.5 (Opcional) Recrie a verificação do Facebook
- **TXT** · Nome: `compraoseu` · Valor: `facebook-domain-verification=epyw87lqmrn22sfib3ac9ypq7zttpf`

### 2.6 O que esperar
- TTL dos registros: 14400 (4h) → propagação de **15 min a algumas horas** (normal);
- Durante a propagação, o site pode ficar instável/alternando — não se assuste;
- **A Vendd deixa de receber o domínio automaticamente** (sem depender de ninguém).

---

## 🔵 PASSO 3 — Ativar o HTTPS (cadeado 🔒) no aaPanel (10 min)

> O SSL deve ser feito **depois** do DNS apontar para a Contabo.

### 3.1 No aaPanel
- **Website → compraoseu.com → SSL**
- Escolha **"Let's Encrypt"**
- Marque: `compraoseu.com` e `www.compraoseu.com`
- **Apply** → aguarde 1–2 min
- Marque **"Force HTTPS"**

### 3.2 Teste
- `https://compraoseu.com` → cadeado ✅
- `https://compraoseu.com/livro01` → livro abre ✅

---

## 🟣 PASSO 4 — (Opcional, recomendado) Cloudflare grátis na frente (30 min)

> Só depois de tudo funcionando. Se quiser CDN global + proteção, adicione o domínio
> **na SUA conta Cloudflare** (dash.cloudflare.com → Add a site → plano Free).

### 4.1 Criar/adicionar
- `dash.cloudflare.com` → **Add a site** → `compraoseu.com` → **Free**;

### 4.2 Copiar nameservers do Cloudflare
- O Cloudflare mostra 2 nameservers (ex.: `ana.ns.cloudflare.com`, `bob.ns.cloudflare.com`);

### 4.3 Trocar na HostGator
- HostGator → domínio → **Alterar plataforma / Name Servers** → colocar os 2 do Cloudflare → Salvar;

### 4.4 Adicionar registros no Cloudflare
- **DNS → Records**:
  - `@` → `212.28.182.86` → Proxy: ligado (laranja)
  - `www` → `212.28.182.86` → Proxy: ligado
  - `app`, `api`, `apioficial` → `212.28.182.86` → Proxy: desligado (chatbot)
- **SSL/TLS → Full (strict)** + **Always Use HTTPS**

### 4.5 Remover a linha do `hosts` do computador
- Apagar a linha (ou `#`) + `ipconfig /flushdns`.

---

## 🔴 PASSO 5 — Finalização e segurança (15 min)

### 5.1 Backups
- aaPanel: **Cron** → backup automático diário do site (e banco se usar);

### 5.2 Testes finais completos
- [ ] `https://compraoseu.com` abre (Home nova)
- [ ] `https://compraoseu.com/livro01` ... `/livro10` abrem todos
- [ ] Botões de compra (Kiwify) funcionam
- [ ] Formulário do quiz envia (e-mail compraoseu.com@gmail.com)
- [ ] `https://compraoseu.com/sitemap.xml` abre (XML)
- [ ] `https://compraoseu.com/robots.txt` abre
- [ ] Celular: "Instalar app" (PWA) funciona

### 5.3 Google Search Console
- Domínio não mudou → verificação continua válida;
- Envie o `sitemap.xml` (`https://compraoseu.com/sitemap.xml`);
- Exclua sitemaps antigos com erro;
- Use **Inspeção de URL** em `/` e `/livro01` → peça indexação.

### 5.4 Depois de 1–2 semanas de estabilidade
- Pode **cancelar a Vendd** com tranquilidade.

---

## ↩️ PASSO 6 — COMO DESFAZER / VOLTAR ATRÁS (Plano B)

Se em qualquer momento quiser **voltar para a situação anterior** (ou se algo der errado):

### Opção A — Voltar o site para a Vendd (se ela ainda existir)
1. Na HostGator: **Alterar plataforma** → trocar os nameservers de volta para a **Cloudflare da Vendd**
   (`adele.ns.cloudflare.com` / `jarred.ns.cloudflare.com`) — **apenas se** a zona da Vendd ainda estiver ativa lá;
2. Se a zona da Vendd não estiver mais: recriar na Zona DNS da HostGator os registros que a Vendd usava
   (o IP antigo da Vendd que estava no registro `@`/`www` — **anotado antes de editar**);
3. Aguardar propagação → o site volta a abrir o conteúdo da Vendd.

### Opção B — Voltar o DNS para a HostGator (se tiver ido para o Cloudflare no Passo 4)
1. HostGator: **Alterar plataforma** → voltar os nameservers para `dns3.hostgator.com.br` / `dns4.hostgator.com.br`;
2. Na Zona DNS da HostGator, garantir os registros A `@` e `www` → `212.28.182.86` (Contabo) ou o IP antigo.

### Opção C — Simplesmente parar o site da Contabo (sem mudar DNS)
1. No aaPanel: **Website → compraoseu.com → Parar (Stop)**;
2. O domínio passa a não abrir (ou abrir erro) — útil em emergência;
3. Para voltar: **Iniciar (Start)**.

> ⚠️ **Sempre anote os valores atuais antes de editar** (o IP antigo do `@`, os nameservers antigos),
> para poder restaurar com 2 cliques.

---

## ✅ CHECKLIST FINAL

- [ ] Site completo no servidor (arquivos + try_files)
- [ ] Teste local via hosts OK
- [ ] DNS: registro A `@` → 212.28.182.86 (HostGator)
- [ ] DNS: CNAME `www` → compraoseu.com (mantido)
- [ ] DNS: registros `app`, `api`, `apioficial` → 212.28.182.86 (chatbot)
- [ ] DNS: TXT Facebook recriado (opcional)
- [ ] SSL Let's Encrypt + Force HTTPS
- [ ] (Opcional) Cloudflare Free + Full(strict) na SUA conta
- [ ] Remover linha do hosts + flushdns
- [ ] Backup automático
- [ ] Sitemap no Google Search Console
- [ ] Cancelar Vendd (só após 1–2 semanas estáveis)

*"Pois o Senhor dá a sabedoria, e da sua boca vem o conhecimento e o entendimento."* (Provérbios 2:6)
Você tem buscado, e o Senhor tem te dado entendimento a cada passo. Vamos com fé e calma! 🤍

