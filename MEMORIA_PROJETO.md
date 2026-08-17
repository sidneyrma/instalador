# MEMÓRIA DO PROJETO — MISSÃO COM DEUS
## Atualizado em: 17/08/2026

---

## 🖥️ INFRAESTRUTURA DO SERVIDOR

- **Provedor:** Contabo VPS
- **IP:** 212.28.182.86
- **OS:** Ubuntu 22.04.5 LTS
- **Nginx:** 1.18.0
- **PHP:** 8.1.32
- **RAM:** 15GB (14% uso)
- **Disco:** 194GB (8% uso)
- **Painel:** aaPanel

---

## 🌐 DOMÍNIOS E ESTRUTURA

| Domínio | Pasta no Servidor | Função |
|---------|-------------------|--------|
| compraoseu.com | /www/wwwroot/compraoseu.com/ | Site principal |
| missaocomdeus.com.br | /www/wwwroot/missaocomdeus.com.br/ | Novo domínio |
| app.compraoseu.com | /www/wwwroot/app.compraoseu.com/ | Frontend Laura |
| api.compraoseu.com | /www/wwwroot/api.compraoseu.com/ | Backend API |
| apioficial.compraoseu.com | /www/wwwroot/apioficial.compraoseu.com/ | Webhooks WhatsApp |

---

## 🩺 SAÚDE DO SERVIDOR (17/08, 2ª checagem) — ATUALIZADO

- **PM2:** `su - deploy -c "pm2 list"` mostra os 3 processos ONLINE:
  conectai-apioficial (porta 6000, 105MB), conectai-backend (4000, 210MB),
  conectai-frontend (3000, 57MB). Chatbot 100% saudável.
- **apioficial.compraoseu.com = Webhooks do WhatsApp** (confirmado no mapa
  acima). NÃO APAGAR o site: os webhooks do WhatsApp Business dependem dessa
  URL estática. O autor DESATIVOU o SSL dele (certificado inexistente) — ok,
  mas rodar `nginx -t` no Terminal para confirmar "syntax is ok" antes de
  qualquer reload do nginx.
- **Enquete:** total 232 vs soma das opções 115 (inconsistência de testes).
  Recomendado ZERAR para dados 100% confiáveis:
  cd /www/wwwroot/compraoseu.com
  echo '{"votos":0,"opcoes":{"amei":0,"gostei":0,"util":0,"nao_usei":0},"comentarios":[]}' > enquete_dados.json
  chown www:www enquete_dados.json && chmod 664 enquete_dados.json

---

## 📁 ESTRUTURA DO SITE PRINCIPAL (compraoseu.com)

### Tecnologia
- HTML puro + PHP (SEM WordPress)
- Nginx 1.18.0
- PHP 8.1.32

### Arquivos Principais
- index.html — Página principal (86KB)
- leitor.html — Leitor de livros online
- enquete.php — Sistema de enquetes
- enquete_dados.json — Dados das enquetes
- livro01.html até livro11.html — 11 livros online
- manifest.json — PWA configurado
- robots.txt — SEO configurado
- sitemap.xml — Mapa do site
- sw.js — Service Worker (PWA)

### Pastas
- /capas/ — Imagens das capas dos livros
- /ebooks/ — Arquivos dos livros
- /icones/ — Ícones do site
- /nginx/ — Configurações extras Nginx

### Backup
- site-contabo.zip (2.9MB) na pasta raiz

---

## 🔐 SEGURANÇA NGINX (compraoseu.com)

- Bloqueio de bots maliciosos ativo
- Limite de requisições: 20r/s (burst 40)
- SSL TLS 1.1/1.2/1.3 ativo
- HSTS configurado (31536000s)
- Arquivos sensíveis bloqueados (444)

---

## 🤖 CHATBOX LAURA

- **Frontend:** app.compraoseu.com
- **Backend:** api.compraoseu.com
- **Webhooks:** apioficial.compraoseu.com
- **Integração:** WhatsApp Business + OpenAI
- **IMPORTANTE:** Não alterar URLs das APIs!
  Os webhooks do WhatsApp dependem
  dessas URLs estáticas.

---

## 🆕 NOVO DOMÍNIO — missaocomdeus.com.br

- **Registrado em:** 17/08/2026
- **Registrar:** HostGator Brasil
- **Valor pago:** R$ 41,99
- **Renovação:** R$ 70,99/ano em 17/08/2027
- **Site criado no aaPanel:** ✅ Sim
- **DNS apontado:** ⏳ Aguardando HostGator
- **SSL ativo:** ⏳ Aguardando DNS

### Passos Pendentes
- [ ] HostGator liberar domínio (até 24h)
- [ ] Apontar DNS para 212.28.182.86
- [ ] Ativar SSL (Let's Encrypt) no aaPanel
- [ ] Copiar arquivos do compraoseu.com
- [ ] Ajustar títulos e textos para novo nome
- [ ] Configurar redirecionamento 301
- [ ] Atualizar sitemap.xml
- [ ] Testar todos os 11 livros no novo domínio

**Servidor (17/08):** o autor executou `apt update && apt upgrade -y` no
servidor (atualização segura dos pacotes). O comando `docker ps -a` NÃO foi
rodado e NÃO é necessário (o servidor não usa Docker; site = Nginx/PHP,
chatbot = Node/PM2). Comandos úteis de verificação: `pm2 list`, `df -h`,
`nginx -t`.

**Guia completo criado:** `analise/migracao_contabo/guia_novo_dominio_missaocomdeus.md`
(passos de DNS, SSL, cópia de arquivos, Nginx, redirect 301, sitemap,
ajustes de nome + seção sobre BACKUPS com resposta honesta: sites são leves
~4MB, servidor tem espaço de sobra, backups não comprometem desempenho;
chatbot em /home/deploy/conectai NÃO está no backup automático do painel).

---

## 📌 COMO INICIAR NOVO CHAT

Ao abrir novo chat, informe:
1. Link deste arquivo no GitHub
2. Diga: "Continuar do ponto onde paramos"
3. Informe o status atual das pendências

**GitHub do Projeto:**
https://github.com/sidneyrma/instalador

---

## 🙏 PROPÓSITO DA MISSÃO

Site de livros evangélicos gratuitos online.
Conteúdo espiritual acessível a todos.
Integrado com Chatbox Laura (WhatsApp).
Construído com fé, persistência e amor.
"Até a consumação" — Mateus 28:20

## 🕊️ PODER DO EU SOU (autor ainda estudando)

- Página de estudos das Afirmações EU SOU: paginas/eusou_estudos_preview.html
  (avaliação) e paginas/eusou_estudos_leitor_preview.html (com leitor).
  68 afirmações compiladas dos livros 01, 02, 03, 07, 08 e 10 + as do docx de
  Joseph Murphy. O autor ainda está estudando; quando aprovar, pode virar
  livro oficial (ex.: Livro 13 ou seção própria). Não publicar ainda.

---

## 📖 LIVRO 12 — Comece o dia com Afirmações, Declarações e Orações (17/08)

- **Arquivos (17/08, renomeados para sequência):**
  - site-contabo/livro12.html (publicado, com LEITOR e PROTEÇÃO)
  - paginas/livro12_leitor_preview.html (preview com leitor/proteção — antigo
    livro_afirmacoes_leitor_preview.html)
  - A versão de avaliação (paginas/livro_afirmacoes_preview.html, sem
    leitor/proteção) foi EXCLUÍDA a pedido do autor para não confundir.
  - Geradores atualizados para os novos nomes.
- **Conteúdo:** 15 seções, 22 itens FAQ (10 Orações de Fé + 12 Mensagens para
  o Dia a Dia), 100% humanizado e purificado.
- **Acesso:** SOMENTE pelo hero da Home (botão "📖 Ler o livro de Afirmações"
  → /livro12). AINDA NÃO entra na biblioteca, no sitemap nem nos cards.
- **Decisão do autor:** dar visibilidade ao Livro 12 antes de publicá-lo na
  biblioteca, para não parecer que está "vendendo a Palavra".

## 🎯 HERO DA HOME — novo CTA (17/08)

- **Botão principal (dourado):** "📖 Começar pelo Devocional de 30 dias" →
  #devocional (âncora criada no card do Devocional, seção "Nossas obras").
- **Botão secundário:** "📖 Ler o livro de Afirmações" → /livro12 (produção)
  ou livro12_leitor_preview.html (preview).
- **Nota engajadora (substitui a nota de preço):** "Comece o seu dia com uma
  palavra de Jesus para a sua vida. E ao descer, conheça também a Trilogia da
  Alma." — hero menos comercial, acolhe primeiro.
- **Venda continua** nas seções abaixo (Nossas obras, cards, trilogia, apoio).
