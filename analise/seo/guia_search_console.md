# 🔍 GOOGLE SEARCH CONSOLE — GUIA COMPLETO (Missão com Deus)

**Objetivo:** verificar o site no Google, enviar o sitemap e acompanhar a indexação das páginas.

---

## 1) ADICIONAR O SITE (5 minutos)

1. Acesse **https://search.google.com/search-console** (faça login com sua conta Google);
2. Clique em **"Adicionar propriedade"**;
3. Escolha uma das opções:

### 🅰️ Opção recomendada: **Prefixo de URL**
1. Digite: `https://www.compraoseu.com/`
2. Clique em **"Continuar"**;
3. Escolha o **método de verificação: Tag HTML**;
4. O Google mostra um **meta tag** (ex.: `<meta name="google-site-verification" content="XXXX...">`);
5. **Copie essa tag** e cole no HEAD da página principal na Vendd;
6. Clique em **"Verificar"** → pronto!

### 🅱️ Opção alternativa: **Domínio** (verifica www e sem www)
1. Digite: `compraoseu.com` (sem https);
2. O Google mostra um **registro TXT** no DNS;
3. Adicione no seu provedor de domínio (onde comprou o domínio);
4. Clique em **"Verificar"** → pronto!

### 🅲 Se você escolheu "Domínio" e apareceu a janela da **Cloudflare**:

> **Você está aqui!** O Google detectou que o DNS do `compraoseu.com` está na Cloudflare
> e mostra: *"Valide a propriedade do domínio através do registo de DNS"* com os botões
> **"Iniciar validação"** e **"Validar mais tarde"**.

**Caminho 1 — Rápido (recomendado, se você tem acesso à conta Cloudflare):**
1. Clique em **"Iniciar validação"**;
2. O Google pede para você **autorizar o acesso à sua conta Cloudflare** (você faz login na Cloudflare com o e-mail de lá);
3. Confirme a permissão → o Google adiciona o registro TXT sozinho;
4. Aguarde a validação concluir (não feche a aba). ✅

**Caminho 2 — Manual (se não lembra do acesso à Cloudflare):**
1. Clique em **"Validar mais tarde"**;
2. No painel, a propriedade aparece como **"Não verificado"**;
3. Acesse o painel da **Cloudflare** (onde o domínio está) → **DNS → Registros**;
4. Adicione um registro do tipo **TXT** com o valor que o Google mostrou;
5. Volte ao Search Console → **"Verificar"**.

> 💡 **Alternativa ainda mais simples:** se preferir não mexer no DNS, remova essa
> propriedade de domínio e crie uma do tipo **Prefixo de URL** (`https://www.compraoseu.com/`)
> com verificação por **Tag HTML** na Vendd (Opção A acima).

> 💡 **Recomendo a Opção A (Tag HTML)** — é a mais simples na Vendd, sem mexer no DNS.

---

## 2) ENVIAR O SITEMAP

### Passo 1 — Publicar o sitemap.xml na Vendd
O arquivo `sitemap.xml` (deste repositório) precisa estar acessível em:
```
https://www.compraoseu.com/sitemap.xml
```
**Como fazer na Vendd:**
- Procure uma opção de **upload de arquivos/arquivos estáticos** na Vendd e suba o `sitemap.xml`;
- OU verifique se a Vendd gera sitemap automático (muitas plataformas têm "Sitemap automático");
- Se a Vendd não permitir, use um **sitemap hospedado** (ex.: em outro domínio) — mas o ideal é no próprio domínio.

### Passo 2 — Enviar no Search Console
1. No painel do GSC, menu lateral → **"Sitemaps"** (ou "Mapas do site");
2. Em **"Adicionar um novo sitemap"**, digite: `sitemap.xml`;
3. Clique em **"Enviar"**;
4. Aguarde — o status deve mudar para **"Sucesso"** (pode levar algumas horas).

---

## 3) VERIFICAR A INDEXAÇÃO

### Inspeção de URL (teste individual)
1. Menu **"Inspeção de URL"** (barra no topo);
2. Digite: `https://www.compraoseu.com/` → Enter;
3. Clique em **"Testar URL ao vivo"**;
4. Se estiver tudo certo, clique em **"Solicitar indexação"**.

Repita para as páginas principais: `/livro01` a `/livro10`.

### Relatório de páginas
1. Menu **"Índice" → "Páginas"**;
2. Veja quantas páginas foram indexadas e se há erros;
3. Páginas com **"Não encontrado (404)"** = URLs excluídas ou renomeadas (os erros que você viu antes);
4. Páginas com **"Rastreadas, mas não indexadas"** = são as do `/quiz` (noindex — correto) ou novas (aguardando).

---

## 4) INTERPRETAR OS "ERROS" DO SITEMAP (que você viu)

Os "1 erro" que apareceram nos seus sitemaps anteriores eram provavelmente:

| Erro | Causa | Solução |
|---|---|---|
| **URLs antigas excluídas** | Páginas que você removeu da Vendd (ex.: `/obrigado`, `/conectai`, versões antigas) | Deixe-as fora do sitemap (o novo sitemap só tem as 10 atuais) |
| **Sitemap malformado** | XML com erro de sintaxe | Use o `sitemap.xml` que criei (validado) |
| **Página noindex no sitemap** | O `/quiz` tem noindex | O novo sitemap ainda o inclui (é aceitável), mas o Google avisa |

**Como limpar:** depois de enviar o sitemap novo, no GSC → Sitemaps → exclua os antigos (clique em "Excluir" ao lado de cada um). O novo substitui.

---

## 5) MEUS SITEMAPS ESTÃO COM "1 ERRO" — O QUE FAZER (atualizado 10/08/2026)

**Situação:** o GSC mostra vários sitemaps enviados (ex.: `/obrigado`, `/quiz`, `/livro01`...),
cada um com "1 erro" e "0 páginas descobertas". Isso aconteceu porque cada **página**
foi enviada como se fosse um sitemap — mas uma página HTML **não é** um sitemap XML.
O Google tenta ler como XML, falha, e marca "1 erro".

> ✅ **Boa notícia:** sitemap com erro **NÃO impede** a indexação das páginas!
> O Google ainda encontra e indexa suas páginas pelos links. Mas é melhor limpar.

### Passo 1 — Como EXCLUIR os sitemaps com erro

Na página **Sitemaps** do GSC, a forma de excluir varia conforme a versão da interface:

- **Opção A (interface atual):** passe o mouse sobre a linha do sitemap → aparece um
  **ícone de lixeira** (🗑) ou um menu **⋮ (três pontinhos)** à direita → clique →
  **"Excluir" / "Delete"**;
- **Opção B (interface antiga):** clique no **link do sitemap** (ex.: `/livro01`) → abre
  a página de detalhes → no canto superior direito há um menu **"Mais" (⋮)** →
  **"Excluir sitemap"**;
- **Opção C:** se não houver ícone visível, clique na **caixa de seleção** (checkbox)
  da linha → no topo da tabela aparece o botão **"Excluir"**.

Repita para TODOS os que têm "1 erro" (obrigado, quiz, livro01 a livro09...).

> ⚠️ **IMPORTANTE (correção 10/08):** o campo "Adicionar um novo sitemap" mostra o
> prefixo `https://www.compraoseu.com/` **fixo e inapagável**. Isso é proposital:
> **o Google SÓ aceita sitemap no MESMO domínio da propriedade.** Portanto NÃO é
> possível enviar o sitemap hospedado no GitHub Pages ali — essa opção foi testada
> e o GSC não permite. Envie apenas `sitemap.xml` (caminho curto) quando o arquivo
> existir no domínio.

### Passo 2 — Enviar o sitemap CORRETO (quando existir no domínio)

Como a Vendd ainda não permite subir o `sitemap.xml` no domínio (atualização deve sair
essa semana — confirmação da Gabi), **não há sitemap para enviar neste momento**.

**Enquanto isso, use a INSPEÇÃO DE URL para solicitar indexação de cada página:**

1. No GSC, menu lateral → **"Inspeção de URL"**;
2. Digite `https://www.compraoseu.com/` → Enter → **"Testar URL ao vivo"**;
3. Se estiver tudo certo → **"Solicitar indexação"**;
4. Repita para: `/livro01`, `/livro02`, `/livro03`, `/livro04`, `/livro05`,
   `/livro06`, `/livro07`, `/livro08`, `/livro09`.

**Quando a Vendd liberar upload (essa semana):**

1. Suba o `sitemap.xml` do repositório em `https://www.compraoseu.com/sitemap.xml`;
2. Na caixa "Adicionar um novo sitemap", digite apenas:
   ```
   sitemap.xml
   ```
3. Clique em **"Enviar"** → status deve mudar para **"Sucesso"** e as 11 URLs aparecerão
   como descobertas (pode levar algumas horas).

**Verifique também:** na Vendd, em Configurações → SEO, se existe "Sitemap automático".
Se a plataforma gerar um endereço próprio (ex.: /sitemap.xml), ative e use esse endereço.

---

## 6) RECOMENDAÇÕES FINAIS

- ✅ **Envie o sitemap novo** (com as 12 URLs corretas — ver Passo 2 acima);
- ✅ **Solicite indexação** das páginas principais após publicar;
- ⏳ **Aguarde 3-7 dias** para o Google rastrear (páginas novas demoram mais);
- 📊 Acompanhe em **"Performance"** (cliques, impressões, palavras-chave);
- 🎯 Se alguma página não indexar em 2 semanas, use a **Inspeção de URL** para solicitar novamente.

---

## 📁 ARQUIVOS CRIADOS

| Arquivo | Uso |
|---|---|
| `sitemap.xml` | Subir na Vendd quando liberar upload, e enviar `sitemap.xml` no GSC (11 URLs) |
| `robots.txt` | Orientar buscadores + apontar o sitemap |
| `guia_search_console.md` | Este guia |

*Guia atualizado em 10/08/2026 · Portal O Despertar · Missão com Deus · CompraOSeu*
