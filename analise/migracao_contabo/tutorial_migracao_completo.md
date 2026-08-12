# 🚀 TUTORIAL COMPLETO: MIGRAR O SITE PARA A CONTABO AGORA
**Passo a passo atualizado · 11/08/2026 · compraoseu.com**

> Este guia é para quando você decidir "virar a chave" e colocar o site definitivamente no
> servidor Contabo. Faça com calma, na ordem, e cada passo é reversível.

---

## 📌 ANTES DE COMEÇAR (o que ter em mãos)

1. **IP do servidor Contabo:** `212.28.182.86`
2. **Acesso ao aaPanel:** já está logado (Nginx rodando, site criado, arquivos no lugar)
3. **Acesso à Hostinger:** onde estão os registros DNS (você já me mostrou)
4. **Arquivos do site:** `site-contabo.zip` (última versão, já com links relativos)

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

## 🟡 PASSO 2 — Trocar o DNS na Hostinger (a "chave" — 10 min)

### 2.1 Entre na Hostinger
- Painel da Hostinger → **Domínios** → **compraoseu.com** → **Gerenciar** → **DNS / Zona DNS**.

### 2.2 Anote os valores atuais (para poder voltar)
- Registro `A` com nome `@` → conteúdo atual: **"Subdomínio Vendd"** (ou um IP) ⚠️ anote
- Registro `A` com nome `www` → conteúdo atual: **"Subdomínio Vendd"** ⚠️ anote

### 2.3 Edite os DOIS registros `@` e `www`
- Clique em **Editar** (lápis) no registro `@`:
  - **Tipo:** A
  - **Nome:** @ (deixe como está)
  - **Conteúdo/IP:** `212.28.182.86`
  - **Proxy (nuvem):** deixe **desligado/cinza** por enquanto (se for Cloudflare, ver Passo 4)
  - Salvar
- Repita para o registro `www` (mesmo conteúdo `212.28.182.86`).

### 2.4 O que esperar
- A propagação do DNS leva de **15 minutos a algumas horas** (normal);
- Você pode acompanhar pelo site `whatsmydns.net` (veja se `212.28.182.86` aparece).

### 2.5 Teste no celular (dados móveis, fora do Wi-Fi, aba anônima)
- `http://compraoseu.com` → se abrir a Home nova, **a chave virou!** 🎉
- Se ainda abrir a Vendd: aguarde mais (propagação) ou confira se os registros foram salvos.

> ⚠️ **Enquanto propaga:** a Vendd ainda atende parte do mundo. Não cancele nada ainda.

---

## 🔵 PASSO 3 — Ativar o HTTPS (cadeado 🔒) no aaPanel (10 min)

> O SSL precisa ser feito **depois** do DNS apontar para a Contabo (o certificado valida o domínio).

### 3.1 No aaPanel
- **Website → compraoseu.com → SSL**
- Escolha **"Let's Encrypt"**
- Marque os domínios: `compraoseu.com` e `www.compraoseu.com`
- Clique em **Apply** (Aplicar)
- Aguarde 1–2 minutos (ele cria o certificado automaticamente)

### 3.2 Forçar HTTPS
- No mesmo painel SSL, marque **"Force HTTPS"** (forçar https)
- Agora `https://compraoseu.com` funciona com cadeado ✅
- **Obs.:** os links internos relativos (`/livro01`) funcionam tanto em http quanto https, então nada quebra.

### 3.3 Teste
- Acesse `https://compraoseu.com` (com https) → cadeado ✅
- Teste `https://compraoseu.com/livro01` → livro abre ✅

---

## 🟣 PASSO 4 — (Opcional, recomendado) Cloudflare grátis na frente (30 min)

> O Cloudflare é um "porteiro global" gratuito: deixa o site **mais rápido no mundo todo** (CDN),
> protege contra ataques e ainda dá um escudo de segurança. Não é obrigatório, mas é o que a
> Vendd tinha de bom (CDN) e agora você teria de graça.

### 4.1 Criar conta
- Acesse `dash.cloudflare.com` → **Sign up** → confirme o e-mail.

### 4.2 Adicionar o site
- Clique em **Add a site** → digite `compraoseu.com` → escolha o plano **Free** (grátis).

### 4.3 Copiar os nameservers do Cloudflare
- O Cloudflare vai te mostrar **2 nameservers** (ex.: `ana.ns.cloudflare.com` e `bob.ns.cloudflare.com`);
- Anote-os (você vai usá-los no próximo passo).

### 4.4 Trocar os nameservers na Hostinger
- Na Hostinger → Domínio → **Gerenciar** → **Nameservers** (ou "Servidores de nomes");
- Troque os atuais pelos **2 do Cloudflare**;
- Salvar. (Isso substitui toda a zona DNS para o Cloudflare gerenciar.)

### 4.5 Configurar o DNS no Cloudflare
- No Cloudflare → seu site → **DNS → Records**;
- Adicione os registros A:
  - `@` → `212.28.182.86` → **Proxy: ligado** (nuvem laranja)
  - `www` → `212.28.182.86` → **Proxy: ligado**
- Se quiser, recrie também o registro TXT do Facebook (opcional) e os registros do app:
  - `app`, `api`, `apioficial` → `212.28.182.86` → **Proxy: desligado** (para o chatbot não passar pelo Cloudflare, ou deixe ligado se quiser)

### 4.6 Ativar SSL no Cloudflare
- **SSL/TLS → Overview** → modo **"Full (strict)"** (já que o aaPanel tem certificado);
- **Edge Certificates** → ative "Always Use HTTPS" (sempre usar https).

### 4.7 Aguardar ativação
- O Cloudflare leva de **15 min a 24h** para ativar (normalmente 1–2 h);
- Quando ativar, recebe e-mail "Cloudflare is now active".

### 4.8 Remover a linha do `hosts` no seu computador
- Como o DNS público agora aponta para a Contabo (via Cloudflare), a linha do arquivo `hosts` não é mais necessária;
- Apague a linha (ou coloque `#` na frente) → salve → `ipconfig /flushdns` no Prompt;
- Teste `https://compraoseu.com` — deve abrir com cadeado, rápido, no mundo todo.

---

## 🔴 PASSO 5 — Finalização e segurança (15 min)

### 5.1 Backups
- No aaPanel: **Cron (tarefa agendada)** → crie um backup automático diário do site e do banco (se usar);
- Ou **Website → Backup** → crie um backup manual agora.

### 5.2 Testes finais completos
- [ ] `https://compraoseu.com` abre (Home nova)
- [ ] `https://compraoseu.com/livro01` ... `/livro10` abrem todos
- [ ] Botões de compra (Kiwify) funcionam
- [ ] Formulário do quiz envia (e-mail compraoseu.com@gmail.com)
- [ ] `https://compraoseu.com/sitemap.xml` abre (XML)
- [ ] `https://compraoseu.com/robots.txt` abre
- [ ] Celular: consegue "Instalar app" (PWA) no menu do navegador

### 5.3 Google Search Console
- O domínio não mudou, então a verificação continua válida;
- Envie o `sitemap.xml` (`https://compraoseu.com/sitemap.xml`);
- Exclua os sitemaps antigos que estavam com erro;
- Use **Inspeção de URL** em `/`, `/livro01` e peça para indexar.

### 5.4 Depois de 1–2 semanas de estabilidade
- Aí sim pode **cancelar a Vendd** com tranquilidade (ou manter se quiser como reserva).

---

## ⚠️ PLANO B (se algo der errado a qualquer momento)

Se em qualquer passo o site parar de abrir:
1. Na **Hostinger**, volte os registros `@` e `www` para **"Subdomínio Vendd"** (o valor que anotou no Passo 2.2);
2. Se tiver trocado nameservers para o Cloudflare, volte para os nameservers originais da Hostinger;
3. Aguarde a propagação (15 min–2 h) → o site volta para a Vendd;
4. O site na Contabo continua intacto no servidor (nada foi apagado) → pode tentar de novo depois.

**Ou seja: o risco de ficar sem site é praticamente zero.** Tudo é reversível.

---

## ✅ CHECKLIST FINAL

- [ ] Site completo no servidor (arquivos + try_files)
- [ ] Teste local via hosts OK
- [ ] DNS `@` e `www` → 212.28.182.86
- [ ] SSL Let's Encrypt + Force HTTPS
- [ ] (Opcional) Cloudflare Free + Full(strict)
- [ ] Remover linha do hosts + flushdns
- [ ] Backup automático
- [ ] Sitemap no Google Search Console
- [ ] Cancelar Vendd (só após 1–2 semanas estáveis)

*"Pois o Senhor dá a sabedoria, e da sua boca vem o conhecimento e o entendimento."* (Provérbios 2:6)
Você tem buscado, e o Senhor tem te dado entendimento a cada passo. Vamos com fé e calma! 🤍
