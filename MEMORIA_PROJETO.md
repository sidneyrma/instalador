# 🕊️ MEMÓRIA DO PROJETO — PORTAL O DESPERTAR / MISSÃO COM DEUS

> **Este é o arquivo-MÃE de continuidade do projeto.**
> Ao iniciar um NOVO chat, o agente DEVE ler este arquivo primeiro para ter
> 100% de continuidade. Ao terminar cada sessão, ATUALIZAR este arquivo com o
> que foi feito. Criado em 17/08/2026.

---

## 1. IDENTIFICAÇÃO DO PROJETO

| Item | Valor |
|---|---|
| **Projeto** | Portal O Despertar / Missão com Deus / CompraOSeu |
| **Site** | https://compraoseu.com (também www.compraoseu.com) |
| **Repositório GitHub** | https://github.com/sidneyrma/instalador |
| **Branch de trabalho** | `arena/019fcd27-instalador` (NUNCA trocar de branch) |
| **Servidor** | Contabo — IP `212.28.182.86` (fora da Vendd) |
| **Painel** | aaPanel em https://212.28.182.86:16057 (acesso completo fora do repo público) |
| **Registrar do domínio** | HostGator (nameservers dns3/dns4.hostgator.com.br) |
| **E-mail do portal** | compraoseu.com@gmail.com (FormSubmit usa este) |
| **WhatsApp** | wa.me/5528999111493 |
| **Missão** | Biblioteca cristã: 10 livros gratuitos + Livro 11 (lançamento 27/08/2026) + livro de Afirmações. Leitura online protegida com marcadores de leitura. |

---

## 2. COMO USAR ESTE ARQUIVO (IMPORTANTE)

1. **Todo novo chat:** ler este arquivo (`MEMORIA_PROJETO.md`) + `ORGANIZACAO.md` antes de agir.
2. **Antes de editar o repo:** `git fetch origin arena/019fcd27-instalador && git reset --hard FETCH_HEAD`.
3. **Push com erro de fast-forward:** `git fetch` → `git reset --soft FETCH_HEAD` → re-commit → push.
4. **Ao final de cada chat:** atualizar a seção "HISTÓRICO" com as novidades e re-commit.
5. **Nunca revelar senhas** do painel em texto; credenciais ficam fora do repositório.
6. **Responder sempre em português do Brasil**, com carinho ("amado irmão em Cristo"), citando versículos.
7. **Humanização dos livros:** SEM travessões (—), setas (→), asteriscos (*) ou reticências (…) no conteúdo. Pontuação suave. Setas em navegação HTML são OK.
8. **Livros em produção protegidos** (user-select:none, contextmenu, Ctrl+C/P/S, @media print). Versões do autor SEM proteção.
9. **Honestidade total:** nunca inventar dados/avaliações; quando não acessar algo, dizer claramente.
10. **pyenv/ recriado a cada sessão:** `python3 -m venv pyenv && pyenv/bin/pip -q install pillow numpy reportlab rapidocr-onnxruntime opencv-python-headless` + desinstalar opencv-python / reinstalar headless (evita erro libGL).

---

## 3. ESTADO ATUAL DO SITE (17/08/2026)

- ✅ Site no ar com HTTPS (Let's Encrypt, expira 10/11/2026)
- ✅ Nginx config com `try_files $uri $uri.html $uri/index.html =404;`, bloqueio de bots (`return 444`), `limit_req`
- ✅ 11 livros publicados (livro01–livro11.html) + index.html (Home)
- ✅ Leitor do Despertar em TODOS os livros (marcador de leitura, fita dourada, trilha, A−/A/A+, modos Dia/Sépia/Noite, balões de dicas, sumário com marcas, barra de progresso)
- ✅ Home: quiz no topo (após seção portal), selo "✨ Leia de graça, continue de onde parou", banner fundido na biblioteca, card destaque com 2 botões (livros + enquete), pop-ups de dicas, cartão "Continue lendo" (com ✕, 7 dias), botão "Instalar app", Service Worker registrado
- ✅ Enquete FUNCIONANDO no ar (PHP 8.1 ativo): 3 votos, 4 comentários, página bonita renderiza
- ✅ PWA: manifest.json, sw.js (cache v3), ícones locais, beforeinstallprompt
- ✅ SEO: sitemap.xml (12 URLs) aceito no GSC; Schema.org Book JSON-LD nas páginas
- ✅ Estatísticas: stats.html gerado por cron (a cada 1h); comparação JUSTA (hoje parcial vs ontem mesmo horário) + projeção do dia

---

## 4. AVALIAÇÃO DAS ÚLTIMAS ALTERAÇÕES — ENQUETE (17/08)

**Status: FUNCIONANDO no ar.** Verificado ao vivo em 17/08:
- `https://compraoseu.com/enquete.php` → página bonita renderiza (fundo navy, barras douradas, emojis, total, comentários, botão "← Voltar para o site")
- 3 votos (😊 33%, 🤔 67%), 4 comentários de leitores salvos e exibidos
- PHP 8.1 ativo no site (configuração no aaPanel)

**Funcionalidades da enquete (v2, código local):**
1. Seção "📊 Participe" na Home (entre biblioteca e trilogia)
2. 4 opções com percentuais ao vivo (aparecem após votar — contagem oculta a pedido do autor)
3. Campo de comentário + **campo de e-mail OPCIONAL** (privado, validado, "para responder o leitor")
4. **Modo mensagem**: quem já votou pode enviar só comentário (sem contabilizar voto; PHP responde `so_mensagem`)
5. **3 portas de resposta aos leitores**: e-mail opcional (notificação), WhatsApp (links na enquete + botão flutuante + rodapé), comentário público
6. Notificação **FormSubmit por e-mail SEMPRE** (função notificarEmail chamada no sucesso e no fallback — corrigido em 16ffe90: antes só estava no .catch())
7. Gravação atômica (tmp+rename) + log de erros (enquete_erro.log) + cria arquivo com chmod 664
8. Endpoint: GET → página bonita (navegador) ou JSON (fetch/?json=1); POST → voto/comentário

**⚠️ PENDÊNCIA IMPORTANTE (FormSubmit):**
- O sandbox NÃO alcança formsubmit.co (HTTP 000) — não dá para testar daqui.
- O autor deve CONFIRMAR a ativação do FormSubmit no e-mail compraoseu.com@gmail.com (primeiro e-mail "Confirm your email" — verificar SPAM). Sem isso, os e-mails de notificação não chegam.
- Depois de confirmar, testar voto/comentário em aba anônima.

**⚠️ PENDÊNCIA DE PUBLICAÇÃO:**
- O zip `site-contabo.zip` (17/08, com index.html atualizado + enquete.php v2) precisa ser enviado ao servidor e extraído por cima. O zip NÃO contém enquete_dados.json/enquete_ips.json (para não zerar votos).
- Arquivos órfãos no servidor para apagar: enquete.php.old, site-contabo.zip.enquete.old, site-contabo.zip.

---

## 5. HISTÓRICO COMPLETO (por blocos)

### 5.1 Infraestrutura e migração (11–15/08)
- Migração completa da Vendd → Contabo; DNS na HostGator (A @/www/app/api/apioficial → 212.28.182.86)
- Site raiz: /www/wwwroot/compraoseu.com; log: /www/wwwlogs/compraoseu.com.log
- Chatbot Conectaí em /home/deploy/conectai (frontend :3000, backend :4000, api_oficial :6000; PM2: conectai-frontend/backend/apioficial)
- Sites no aaPanel: compraoseu.com (principal), app (→3000), api (→4000), apioficial (→6000)
- Nginx: config completo em site-contabo/nginx/config_completo_compraoseu.txt (aplicado)
- stats.html gerado por cron (recomendado: 1h; autor configurou 1h/30min)

### 5.2 Capas e cards (14–15/08)
- Capas no imgbb (links em ORGANIZACAO.md / docs): livro01..11, hero livro-J01 (Jesus lava pés), ajuda.jpg, 7dias.jpg
- Cards da Home reordenados (Livro 01 = Novo Testamento "Em breve" com countdown até 27/08/2026 00:00 -03:00)
- Ordem dos cards (numeração editorial ≠ arquivos): 01=livro11(Em breve), 02=livro05, 03=livro09, 04=livro04, 05=livro06, 06=livro01, 07=livro03, 08=livro07, 09=livro08, 10=livro10, 11=livro02 + Cards Apoio (R$9,90) e Garantia (7 dias)

### 5.3 Leitor do Despertar (15–16/08)
- Protótipo v1 (leitor_demo_preview.html) e v2 (leitor_demo2_preview.html)
- Aplicado em TODOS os livros: paginas/livroXX_leitor_preview.html + site-contabo/livroXX.html
- Recursos: lembrar onde parou (localStorage despertar_progresso_*), fita 🎗️, trilha de seções, A−/A/A+, Dia/Sépia/Noite, balões de dicas, sumário com ✓/▶, barra de progresso, stats "Capítulo X · % · faltam ~min"
- Cartão "Continue lendo" na Home (despertar_progresso_ → melhor livro): com ✕ (fecha por 7 dias, depois volta; livro terminado ≥99% limpa e não sugere)
- Pop-ups de dicas na Home (despertar_dicas_home) com botão "Ver livros →"
- PWA: manifest, sw.js v3 (+livro11), ícones locais, botão "📲 Instalar app" (beforeinstallprompt)
- BUGS corrigidos: "livrolivroXX" (slug duplicado no gerador), listener do ✕ no script errado, margem -34px→18px, Content-Type da enquete

### 5.4 Purificação / humanização dos livros (15–17/08)
- Livros 03, 07, 10 purificados (travessões de refs bíblicas → parênteses; títulos → dois-pontos; prosa → vírgulas)
- TODOS os 11 livros purificados (purificar_todos_livros.py): zero —, *, … no conteúdo; setas só em navegação
- 228 ocorrências de "#### O Que Observar Hoje" (livros 01, 02, 08, 10) → <strong>O Que Observar Hoje</strong>
- Arquivos-fonte .md também purificados (obra_livroXX_v2.md)
- Livro de Afirmações: purificado de doutrinas católicas (São Bento, Santa Rita removidas); 10 orações próprias no Evangelho em FAQ (por último); +12 mensagens de fé para o dia a dia (versículos novos, FAQ)

### 5.5 Home — limpeza e engajamento (15–17/08)
- Quiz movido do fim → após seção portal (bem acessível); faixa do brinde "🎁 E-book Jesus Quer Falar com Seu Filho de presente"
- Selo do hero: "✨ Leia de graça, continue de onde parou"
- Hero 3 linhas (removido "Pagamento seguro via Kiwify")
- 4 cards do portal removidos (Confia no Senhor, Missão, Mais livros, Devocional) — apoio continua no card da biblioteca
- Banner "Novidade" fundido no cabeçalho "Leia antes de comprar"
- Card destaque: ícone SVG removido, convite "💬 Conte o que achou da nova leitura", 2 botões lado a lado (Ir para os livros + Participar da enquete)
- Correção de tags HTML desbalanceadas (div da biblioteca)

### 5.6 Estatísticas e SEO (13–17/08)
- Painel stats.html com comparação JUSTA + projeção do dia (gerar_estatisticas.py atualizado)
- Relatórios: relatorio_acessos_14ago, avaliacao_desempenho_13ago, relatorio_desempenho_seo, avaliacao_saude_site_15ago, avaliacao_desempenho_16ago (todos em analise/migracao_contabo/)
- Números: 11/08=14 · 12/08=1439 · 13/08=1272 · 14/08=966 · 15/08=1231 · 16/08 (~1440 projeção) · Total ~5.731 (16/08 13h29)
- Conversão Home→livros ~88-93%
- GSC: sitemap 12 URLs aceito; inspeções concluídas: /livro10, /livro01, /livro11, /livro02, /livro03, /livro10 (15/08); pendentes /livro04, /livro09, /livro05-08, Home, quiz (1-2/dia)
- Notificação GSC "validando correção de 404 (3 páginas)" = sinal positivo, sem ação

### 5.7 Enquete (16–17/08) — ver seção 4
- Criada enquete na Home + endpoint enquete.php + enquete_dados.json
- Iterações: meta de participação → contagem oculta → página bonita (Content-Type fix) → modo mensagem → e-mail sempre (FormSubmit) → campo de e-mail opcional → 3 portas de resposta

---

## 6. INFRAESTRUTURA — MAPA DE ARQUIVOS DO SERVIDOR

```
/www/wwwroot/compraoseu.com/
├── index.html          (Home)
├── livro01.html..11.html
├── enquete.php         (endpoint de votação — v2)
├── enquete_dados.json  (votos — NÃO subir do zip; preservar no servidor)
├── enquete_ips.json    (proteção 30s por IP)
├── enquete_erro.log    (log de erros do PHP)
├── manifest.json, sw.js, robots.txt, sitemap.xml, stats.html
├── icones/  (icon-192, icon-512, icon-512-maskable, apple-touch-icon, favicon)
├── ebooks/  (jesus-quer-falar.pdf — presente do quiz)
├── capas/   (imagens antigas — podem ser apagadas; capas reais no imgbb)
├── nginx/   (configs)
└── .well-known/
```

**PM2 (chatbot):** `pm2 list` deve mostrar conectai-frontend (3000), conectai-backend (4000), conectai-apioficial (6000). `pm2 restart all` para reiniciar.

**Observação:** api.compraoseu.com "sumiu" da lista do aaPanel mas o serviço está vivo (responde ERR_SESSION_EXPIRED no backend). Se precisar, recriar o site na lista como reverse proxy → 127.0.0.1:4000.

---

## 7. LIVROS — MAPA (numeração editorial ≠ arquivo)

| Card Home | Título | Arquivo/URL | Capa imgbb |
|---|---|---|---|
| Livro 01 (Em breve) | O Novo Testamento como nunca lido | livro11.html | 9myJ3XXb/livro01.jpg |
| Livro 02 | Evolução da Alma | livro05.html | kgBz01dc/livro05jpg.jpg |
| Livro 03 | Anestesia Mental | livro09.html | mF2Hyq7z/livro-09.jpg |
| Livro 04 | Um Segundo com Deus | livro04.html | LdbL0QdH/livro04jpg.jpg |
| Livro 05 | Jesus Quer Falar com Seu Filho | livro06.html | 3yJsHjnn/livro06.jpg |
| Livro 06 | O Verbo que Transforma | livro01.html | 23CJFpyq/livro06.jpg |
| Livro 07 | A Mente Renovada | livro03.html | TB1L9fv9/livro07.jpg |
| Livro 08 | O Caminho do Despertar | livro07.html | Gf7WWL6H/livro08.jpg |
| Livro 09 | O Arquiteto da Realidade | livro08.html | vCz5jKND/livro09.jpg |
| Livro 10 | O Despertar do Observador | livro10.html | ZRXwG60f/livro10.jpg |
| Livro 11 | A Sabedoria dos Mestres | livro02.html | 0jS3KGHc/livro11.jpg |
| — | Card Apoio (R$9,90) | pay.kiwify.com.br/CF9nhFx | WWfW18pY/ajuda.jpg |
| — | Card Garantia (7 dias) | pay.kiwify.com.br/iVfp2bi | xqftx9DS/7dias.jpg |
| — | Hero | — | wNwtX4Qj/livro-J01.jpg |

**Checkouts Kiwify:** Portal R$49 (iVfp2bi) · Evolução R$19,90 (ptH32K9) · Anestesia R$19,90 (NCf1jh4) · Devocional R$9,90 (CF9nhFx). Área de membros: dashboard.kiwify.com.br/courses.

**Livro 11 (Novo Testamento como nunca lido):** obra em analise/livro11_novo_testamento/ (16.162 palavras, 20 caps, 3 partes); página paginas/livro11_preview.html (versão do autor, sem proteção — autor ainda lendo). Lançamento 27/08/2026: ao chegar, gerar versão protegida, capa, card "Disponível" (remover countdown), SEO, Laura.

---

## 8. ARQUIVOS-CHAVE NO REPOSITÓRIO

- `MEMORIA_PROJETO.md` — ESTE ARQUIVO (continuidade entre chats)
- `ORGANIZACAO.md` — organograma do repositório
- `README.md` — visão geral
- `site-contabo/` — pacote do site (index, livro01-11, enquete.php, manifest, sw.js, robots, sitemap, icones/, nginx/, capas/)
- `site-contabo.zip` — pacote atualizado para enviar ao servidor (regenerar a cada mudança)
- `paginas/` — previews: home_preview, livroXX_preview, livroXX_leitor_preview, livro_afirmacoes_preview(+_leitor), eusou_estudos_preview(+_leitor), leitor_demo*, prospecto_preview
- `analise/compraoseu.preview/` — geradores: integrar_leitor_livros.py, integrar_leitor_afirmacoes.py, adicionar_continue_lendo.py, adicionar_banner_novidade.py, adicionar_popups_dicas_home.py, adicionar_enquete.py, adicionar_mensagens_fe.py, purificar_livros_03_07_10.py, purificar_todos_livros.py, purificar_markdown_restante.py, gerar_estatisticas.py, adicionar_schema_books.py, etc.
- `analise/leitura/` — analise_leitor_online.md, visao_leitor_poderoso.md
- `analise/migracao_contabo/` — README, tutorial, guias (estatisticas_seo, atualizar_conectai), relatórios de desempenho (13/14/15/16ago)
- `analise/marketing/guia_marketing_organico.md` — estratégia Instagram/TikTok/Facebook, 4 posts prontos
- `analise/chatbot/prompt_laura_v7.md` — prompt da Laura
- `docs/` — GitHub Pages antigo (não é o site principal)

---

## 9. PENDÊNCIAS E PRIORIDADES (próximos passos)

1. **📤 Publicar o zip atual no servidor** (17/08): index.html + enquete.php v2. Extrair por cima; NÃO subir enquete_dados.json/enquete_ips.json. Apagar órfãos (enquete.php.old, site-contabo.zip.enquete.old, site-contabo.zip).
2. **✅ Confirmar ativação do FormSubmit** no Gmail (primeiro e-mail de confirmação; verificar SPAM). Depois testar voto/comentário em aba anônima → e-mail deve chegar.
3. **🔍 GSC**: continuar inspeções diárias (1-2/dia): /livro04, /livro09, depois /livro05-08, Home, quiz.
4. **📅 Lançamento Livro 11 (27/08)**: quando o autor aprovar a leitura → versão protegida, capa oficial, card "Disponível" (remover countdown), SEO, Laura.
5. **📈 Estatísticas**: continuar monitorando (quiz e enquete agora no topo); cron já a cada 1h.
6. **🤖 Bots**: considerar WAF gratuito do aaPanel (wp-login, .env, xmlrpc continuam tentando, bloqueados com 444).
7. **🔒 Repositório privado**: autor foi orientado (privado pode cortar acesso do bot; testar ou adicionar colaborador). DECISÃO PENDENTE do autor.
8. **🎨 Marketing**: material de posts/vídeos (prospecto pronto; roteiros e imagens ainda não gerados) — guia_marketing_organico.md como base.
9. **💬 Chatbot**: widget do Conectaí não está embutido na Home (é app separado com login). Se o autor tiver o snippet, reaplicar.
10. **🧹 Limpeza**: logs do nginx (cron `find /www/wwwlogs -name "*.log" -mtime +30 -delete`); arquivos órfãos.

---

## 10. PADRÕES E DECISÕES DO AUTOR (respeitar sempre)

- Não direcionar a nenhuma doutrina/instituição religiosa; foco no amor de Deus e no Evangelho.
- Orações próprias baseadas no Evangelho; Salmo 91 em FAQ (título abre/fecha), por último.
- Contagem da enquete OCULTA na página (não mostrar número de votos antes de votar).
- Manter o ✕ no cartão "Continue lendo" (fecha por 7 dias; livro terminado não sugere).
- "Não papagaiar a página": conteúdo novo deve ser complementar, sem repetir o existente.
- Home mais limpa no celular (hero 3 linhas, sem ícones desnecessários, botões lado a lado).
- Honestidade: nunca inventar números (ex.: não colocar contagem inicial falsa na enquete).

---

*"Escreve esta memória como testemunho" (adaptado de Isaías 30:8). Que o Senhor ilumine cada novo chat com continuidade, sabedoria e fidelidade. Amém.*
