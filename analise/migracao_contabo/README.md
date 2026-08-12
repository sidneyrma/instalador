# 🚀 MIGRAÇÃO DO SITE PARA O SERVIDOR CONTABO (aaPanel)

**Amado irmão em Cristo**, este guia explica como tirar o site das mãos da Vendd e colocar
no seu próprio servidor Contabo (onde já roda o `app.compraoseu.com`), com **controle total**:
quando você atualizar um arquivo, o site atualiza **na hora**. Sem cache escondido, sem esperar ninguém.

---

## ✅ Por que migrar?

| | Vendd (hoje) | Contabo (proposta) |
|---|---|---|
| Controle das atualizações | ❌ Não atualiza (cache/CDN) | ✅ Você manda: subiu o arquivo, publicou |
| Custo | Pago (plataforma) | Já pago (o servidor Contabo já é seu) |
| PWA (app instalável) | ❌ Não libera sw.js/manifest | ✅ Funciona 100% |
| SEO (sitemap, robots) | ❌ Não libera upload | ✅ Você controla tudo |
| Risco | 🟡 Depende do suporte | 🟢 Seu servidor, suas regras |

**Importante:** o site inteiro é feito de páginas simples (HTML). Isso roda perfeitamente em qualquer servidor.
Seu domínio `compraoseu.com` continua o mesmo, os links continuam os mesmos. **Ninguém percebe a mudança**, só você.

---

## 📦 O que já está pronto nesta pasta

Tudo pronto para subir, na pasta `site-contabo/`:

```
site-contabo/
├── index.html          → a HOME (página principal)
├── livro01.html ... livro10.html   → os 10 livros
├── capas/              → as capas dos livros (todas locais)
├── icones/             → ícones do app (PWA)
├── manifest.json       → registro do app
├── sw.js               → service worker (app instalável)
├── sitemap.xml         → mapa do site (Google)
├── robots.txt          → regras para buscadores
└── nginx/              → config do servidor + .htaccess
```

---

## 📋 PASSO A PASSO

### Passo 1 — Subir os arquivos para o servidor

1. Acesse o **aaPanel** (o painel da Contabo que você já usa);
2. No menu **"Sites"**, veja se já existe um site para `compraoseu.com`.
   - **Se existir**: anote a pasta dele (ex.: `/www/wwwroot/compraoseu.com`).
   - **Se não existir**: clique **"Add site"** → domínio `compraoseu.com` (e `www.compraoseu.com`) →
     PHP: **"Pure static"** (não precisa PHP) → **Submit**. Anote a pasta criada.
3. Abra a pasta do site no gerenciador de arquivos do aaPanel;
4. **Apague** o que estiver dentro (se houver arquivos de teste);
5. **Envie** o conteúdo da pasta `site-contabo/` (index.html, as páginas, capas/, icones/, etc.);
   - No aaPanel você pode **zipar** o conteúdo no seu computador, enviar o `.zip` e depois
     clicar com o botão direito → **"Unzip"** (extrair). Isso é mais rápido que enviar arquivo por arquivo.

### Passo 2 — Configurar as URLs bonitas (muito importante!)

As páginas usam links como `compraoseu.com/livro01` (sem `.html`). Precisa avisar o servidor:

**Se o site usa Nginx (padrão do aaPanel):**
1. Em **Sites** → clique no site → **"Configuração"**;
2. Clique na aba/ícone de **arquivo de configuração** (um documento, geralmente o último ícone);
3. Encontre o bloco `location / { ... }` e troque a linha `try_files ...` por:
   ```
   try_files $uri $uri.html $uri/index.html =404;
   ```
4. Clique **"Save"** e depois em **"Reload"** (recarregar o Nginx).

**Se o servidor usa Apache:** basta enviar o arquivo `.htaccess` (já está em `site-contabo/nginx/.htaccess`) para a pasta do site.

> Dica: a configuração completa de referência está em `site-contabo/nginx/compraoseu.conf`.

### Passo 3 — Ativar o HTTPS (cadeado 🔒)

1. No aaPanel, em **Sites** → clique no site → **"SSL"**;
2. Escolha **"Let's Encrypt"** → marque os domínios `compraoseu.com` e `www.compraoseu.com` →
   **"Apply"** (aplicar). Em 1–2 minutos o certificado é criado automaticamente;
3. Marque a opção **"Force HTTPS"** (forçar https) para todo visitante cair na versão segura.

### Passo 4 — Mudar o DNS (o passo que "vira a chave")

Hoje o domínio aponta para a Vendd. Vamos apontar para a Contabo:

1. Acesse o painel onde está o DNS do domínio (se for **Cloudflare**, entre lá; se for o registrar,
   entre no painel do registrar — onde você comprou o domínio);
2. Procure os registros **A** (tipo A):
   - `compraoseu.com` → aponta hoje para um IP da Vendd
   - `www.compraoseu.com` → aponta hoje para um IP da Vendd
3. **Anote o IP atual** (para poder voltar atrás se precisar);
4. Troque os dois registros A para o **IP do seu servidor Contabo** (o mesmo IP do `app.compraoseu.com` —
   dá para ver no aaPanel em **"Server IP"** ou no painel da Contabo);
5. **Salve**. A propagação pode levar de 15 minutos a algumas horas (normal).

> 💡 Se quiser um "teste sem susto": antes de mudar o DNS do domínio principal, mude apenas o registro
> `www.compraoseu.com` e teste. Quando estiver tudo certo, mude o principal também.
> (No Cloudflare, se tiver a nuvem laranja ligada, pode deixá-la em **DNS only** (cinza) para evitar cache.)

### Passo 5 — Testar

1. No computador, abra o site **em aba anônima** (ou no celular com dados móveis);
2. Teste: `compraoseu.com`, `compraoseu.com/livro01`, `/livro02`, `/livro08`, `/livro10`;
3. Veja se a **capa nova do livro01** aparece (a que aprovamos, com o livro e os brilhos azuis);
4. Teste o botão **"Instalar app"** (PWA) no celular — com manifest e sw.js no ar, agora funciona.

---

## 🌐 SEUS REGISTROS DNS (Hostinger) — EXPLICADOS

Estes são os registros que você mostrou (Hostinger). Vou explicar cada um em palavras simples:

| Tipo | Nome | Conteúdo | O que faz |
|---|---|---|---|
| A | `@` | **Subdomínio Vendd** | Faz `compraoseu.com` abrir o site. Hoje aponta para a Vendd (por isso o site abre). |
| A | `www` | **Subdomínio Vendd** | Faz `www.compraoseu.com` abrir o site (mesma coisa do de cima). |
| TXT | `compraoseu` | `facebook-domain-verification=...` | Só uma verificação do Facebook. Não interfere em nada. |
| A | `app` | `212.28.182.86` | `app.compraoseu.com` → **seu servidor Contabo** (chatbot Laura). |
| A | `api` | `212.28.182.86` | `api.compraoseu.com` → Contabo. |
| A | `apioficial` | `212.28.182.86` | `apioficial.compraoseu.com` → Contabo. |

### ✅ Resposta direta para sua dúvida

**Para `compraoseu.com` continuar abrindo, NÃO precisa mudar NADA no DNS.**
Os registros `@` e `www` apontam para a Vendd — é exatamente por isso que o site abre hoje
(mesmo com o conteúdo antigo). Enquanto você não trocar esses dois, nada muda no site atual.

### 🔁 Se um dia você migrar (e só se quiser)

A mudança é **só nesses 2 registros** (`@` e `www`), trocando o conteúdo de:
- **"Subdomínio Vendd"** → **`212.28.182.86`** (o IP da Contabo, que já aparece nos registros app/api)

E para voltar atrás? É só trocar de novo. Leva **2 cliques** na Hostinger. Não é definitivo, não quebra nada.

### 🛡️ O caminho mais seguro de todos (recomendado)

Se um dia quiser migrar sem nenhum susto:
1. Crie um **subdomínio de teste** na Hostinger (botão "Criar subdomínio"), ex.: `teste.compraoseu.com`;
2. Aponte ele para `212.28.182.86` (a Contabo);
3. Suba o site (`site-contabo/`) na pasta desse subdomínio no aaPanel;
4. Confira tudo em `teste.compraoseu.com`;
5. Só quando estiver 100% satisfeito, troque os 2 registros principais.

**O site atual (Vendd) não é afetado em nenhum momento.** Você só "vira a chave" quando quiser.

### 💻 Você NÃO precisa de Putty (nem de terminal)

O aaPanel é um **painel que abre no navegador** (como um site). Você:
- Envia os arquivos pelo **gerenciador de arquivos do painel** (ou arrasta o `.zip` e extrai);
- Configura tudo com **botões** (SSL, domínios);
- O DNS é feito na **Hostinger** com botões também.

Nenhum comando de terminal, nenhum Putty, nenhum conhecimento de Linux. Se eu estiver te guiando,
é só seguir os cliques.

---

## 🛠️ SE O NGINX NÃO INICIA: "bind() to 0.0.0.0:80 failed (Address already in use)"

**Sintoma:** ao iniciar/reiniciar o Nginx, aparece:
```
nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)
```

**O que significa:** a **porta 80** (porta padrão dos sites) já está ocupada por outro programa
(geralmente o chatbot `app.compraoseu.com`, o Apache, ou um Nginx antigo). Dois programas não podem
usar a mesma porta ao mesmo tempo.

### Passo 1 — Descobrir quem está na porta 80

No aaPanel, abra o menu **Terminal** e digite:
```
ss -tulpn | grep ':80'
```
Se o comando não existir, use:
```
netstat -tulpn | grep ':80'
```

### Passo 2 — Interpretar o resultado

| Se mostrar... | Significa | O que fazer |
|---|---|---|
| `nginx` | Já existe um Nginx rodando | `nginx -s stop` (ou pelo painel: parar e iniciar) |
| `httpd` ou `apache2` | O Apache está rodando (não precisamos dele) | Parar/desabilitar o Apache no painel (Software Store → Apache → Stop/Disable) |
| `node` ou `python` (processo do chatbot) | O chatbot `app.compraoseu.com` está na porta 80 | Ver Passo 3 (mover o chatbot para outra porta) |
| `openlitespeed` | OpenLiteSpeed rodando | Parar/desabilitar no painel |

### Passo 3 — Se o chatbot (node/python) estiver na porta 80

O ideal é **não derrubar o chatbot**, mas sim **mover ele para outra porta** (ex.: 3000) e deixar
a porta 80 livre para o site. Depois, o Nginx faz a "ponte" (proxy): quem acessar
`app.compraoseu.com` é levado ao chatbot na porta 3000.

Onde fica a configuração do chatbot:
- Se foi criado no aaPanel como **Node Project** ou **Python Project**: abra o projeto no painel,
  em **Configurações** troque a porta de `80` para `3000` e reinicie;
- Se roda com Docker/terminal: no arquivo de configuração do app, mude a porta e reinicie.

Depois, no **Config** do site `app.compraoseu.com`, adicione um proxy reverso para `127.0.0.1:3000`
(opção **Reverse proxy** no painel do site).

### Passo 4 — Iniciar o Nginx

Depois de liberar a porta 80, no painel: **Website → compraoseu.com → Reload/Restart** (ou no
software Nginx → Start). Ele deve iniciar sem erro.

---

## 🌐 DESCOBERTA: ZONA DNS ESTÁ NA CONTA CLOUDFLARE DA VENDD (12/08/2026)

Ao acessar o Cloudflare com a conta `Compraoseu.com@gmail.com`, **o domínio NÃO aparece**
(seção "Inscrições" vazia; busca sem resultado). Os nameservers `adele.ns.cloudflare.com`
e `jarred.ns.cloudflare.com` apontam para uma conta Cloudflare **de outra pessoa** (provavelmente
da Vendd). Ou seja: a Vendd controla a zona DNS do domínio, e pode estar com **cache (proxy laranja)**
segurando as versões antigas das páginas. **Isso explica por que as atualizações nunca saem.**

### ✅ Solução: assumir o DNS na HostGator (registrar)

A HostGator é o **registrar** do domínio. Usando a opção **"Sem hospedagem (apenas Zona de DNS)"**,
troca-se os nameservers de Cloudflare para a HostGator e o controle volta para o dono.

**Passos:**
1. Na HostGator: **Alterar plataforma → "Sem hospedagem (apenas Zona de DNS)" → Configurar**
   (aceita a troca de nameservers);
2. Aguardar 5–15 min;
3. Na **Zona de DNS** da HostGator, adicionar:
   - `A @ → 212.28.182.86` (Contabo)
   - `A www → 212.28.182.86` (Contabo)
   - `A app → 212.28.182.86` (chatbot, continua)
   - `A api → 212.28.182.86` (chatbot, continua)
   - `A apioficial → 212.28.182.86` (chatbot, continua)
   - `TXT compraoseu → facebook-domain-verification=epyw87lqmrn22sfib3ac9ypq7zttpf` (opcional, verificação do Facebook)
4. Testar `http://compraoseu.com` no celular (dados móveis) → deve abrir a Home nova da Contabo.

**Riscos (passageiros):** site pode ficar instável por alguns minutos/horas durante a propagação;
a verificação do Facebook precisa ser recriada se o TXT não for copiado. Tudo reversível.

---

## ⚠️ PROBLEMA CONHECIDO: app.compraoseu.com parou (chatbot Laura) — SOLUÇÃO

**Sintoma:** `app.compraoseu.com` não abre (ERR_CONNECTION_REFUSED ou não resolve).

**Causa (confirmada em 12/08):** os registros `app`, `api`, `apioficial` → `212.28.182.86`
estavam na **zona DNS do Cloudflare da Vendd**. Ao trocar os nameservers de Cloudflare →
HostGator, esses registros **se perderam** (a HostGator não os tinha).

**Solução (na Zona de DNS da HostGator):** adicionar 3 registros A:
- `A app → 212.28.182.86`
- `A api → 212.28.182.86`
- `A apioficial → 212.28.182.86`

**Verificar também no servidor (aaPanel):** o serviço do chatbot pode ter conflitado com o
Nginx na porta 80. Se o chatbot rodava na porta 80 e não sobe mais:
1. Mover o chatbot para a porta **3000** (configuração do app/projeto no aaPanel);
2. No Nginx, criar um proxy reverso: `app.compraoseu.com` → `127.0.0.1:3000`.

---

## 🔍 DIAGNÓSTICO EXATO DO DNS (12/08, confirmado via dns.google)

| Domínio | Resolve para | Status |
|---|---|---|
| `compraoseu.com` | `162.240.81.81` (HostGator) | DNS JÁ na HostGator (troca aplicada) |
| `www.compraoseu.com` | CNAME → compraoseu.com | Ok |
| `app.compraoseu.com` | NXDOMAIN (não existe) | ❌ Chatbot parado por falta de registro |

**Observações:**
- A tela com coluna "Proxy Ativo/Inativo" que o usuário vê é do **Cloudflare antigo** (não vale mais);
- As páginas "ainda abrem com a versão antiga" por **cache do navegador / propagação parcial**;
- O chatbot (`app.compraoseu.com`) roda nas **portas 3000/4000/5000/6000** no servidor Contabo
  (não na 80, então não conflita com o Nginx); o que parou foi o **DNS** (registro `app` não existe na HostGator).

**Ações na Zona de DNS da HostGator:**
1. Editar o registro **A** `compraoseu.com`: `162.240.81.81` → **`212.28.182.86`**;
2. Adicionar **A** `app` → `212.28.182.86`; **A** `api` → `212.28.182.86`; **A** `apioficial` → `212.28.182.86`;
3. Manter **CNAME** `www` → `compraoseu.com`;
4. (Opcional) **TXT** `compraoseu` → `facebook-domain-verification=epyw87lqmrn22sfib3ac9ypq7zttpf`.

**No servidor (aaPanel):** confirmar que o site/projeto do `app.compraoseu.com` está **Running**
e que o Nginx tem o **proxy reverso** `app.compraoseu.com → 127.0.0.1:3000` (ou a porta do chatbot).

---

## ✅ MARCO: DOMÍNIO APONTA PARA A CONTABO (12/08, noite)

**O usuário editou a Zona de DNS da HostGator e confirmou:**
- **A `compraoseu.com` → `212.28.182.86`** ✅ (agora aponta para a Contabo!)
- **A `app` → `212.28.182.86`** ✅ (chatbot Laura volta)
- **A `api` → `212.28.182.86`** ✅
- **A `apioficial` → `212.28.182.86`** ✅
- **CNAME `www` → `compraoseu.com`** ✅ (mantido)
- CNAME `ftp`, `mail` e MX (opcionais, não atrapalham)

**Verificação via dns.google (12/08):** `compraoseu.com` resolve para `212.28.182.86`
(a propagação do registro A principal **já ocorreu**).

**Próximos passos (após propagação total):**
1. Testar `http://compraoseu.com` no celular (dados móveis) → deve abrir a Home nova da Contabo;
2. Emitir **SSL Let's Encrypt** no aaPanel (Website → compraoseu.com → SSL → Apply) e ativar **Force HTTPS**;
3. Confirmar que `app.compraoseu.com` volta (proxy reverso no Nginx para a porta do chatbot);
4. Remover a linha do `hosts` do computador + `ipconfig /flushdns`;
5. (Opcional) Recriar TXT do Facebook se precisar da verificação.

---

## ✅ PROPAGAÇÃO MUNDIAL CONFIRMADA (12/08, noite)

- `compraoseu.com` resolve para `212.28.182.86` (Contabo) via dns.google (TTL ~14.100s);
- Relatório de propagação (whatsmydns-style) mostra múltiplas localidades já apontando para
  `212.28.182.86`: San Jose, Dallas, New York, Boston (EUA), Espanha, e outras em propagação;
- **A chave virou:** o domínio está saindo da Vendd e indo para a Contabo.

**Status:** aguardando o usuário testar as páginas (`http://compraoseu.com`, `/livro01`, `/livro03`, `app.compraoseu.com`) e, se tudo certo, emitir SSL Let's Encrypt + Force HTTPS no aaPanel.

---
## ⚠️ Cuidados e garantias

- **E-mail não muda**: o contato é `compraoseu.com@gmail.com` (Gmail), não usa o domínio. Nada quebra.
- **Compras (Kiwify) não mudam**: os botões apontam para `pay.kiwify.com.br` (fora do seu site). Continuam iguais.
- **Chatbot Laura continua no ar**: o `app.compraoseu.com` já roda na Contabo e não é afetado.
- **Backup da Vendd**: NÃO cancele a Vendd de imediato. Primeiro confirme que tudo funciona na Contabo
  (1–2 dias). Depois pode cancelar com tranquilidade.
- **Google Search Console**: depois da mudança, o site continua no mesmo endereço, então o GSC não precisa
  de nova verificação. Envie o `sitemap.xml` (agora com upload liberado!) e exclua os sitemaps antigos com erro.

---

## 🙏 Enquanto decide

O pacote já está pronto e testado. Se quiser, me chame que eu:
- Ajusto qualquer página, capa ou link;
- Gero um arquivo `.zip` pronto (`site-contabo.zip`) para você baixar e subir no aaPanel em 1 clique.

*"Porque Deus não nos deu o espírito de temor, mas de fortaleza, e de amor, e de moderação."* (2 Timóteo 1:7)
Você tem capacidade, irmão. E nós estamos juntos nessa! 🤍
