# MEMÓRIA DO PROJETO — MISSÃO COM DEUS
## Atualizado em: 21/08/2026

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

---

## 📊 ENQUETE NOVA — "Qual é a maior batalha da sua mente hoje?" (18/08)

Pergunta de baixa fricção e alta especificidade (pré-segmentação do funil:
cada resposta indica qual livro ofertar). Aprovada em conjunto com o autor
(que também trocou ideia com outro modelo — união de conselhos).

- **Pergunta:** "Qual é a maior batalha da sua mente hoje?"
- **Opções:** 😰 Ansiedade e preocupação · 😔 Mágoas e lembranças do passado
  · 😨 Medo do futuro · 🕊️ Falta de paz e propósito
- **Comentário em camadas (ajuste do Claude):**
  1. Durante o voto (pergunta única, leve): "Quer compartilhar? (opcional) O
     que você tem feito para vencer essa batalha?"
  2. Após o resultado (segundo microcompromisso): convite "X% também lutam
     com isso — você já leu algo que te ajudou?" (foca no campo de comentário)
- **Privacidade:** e-mail opcional; aviso que relatos podem ser usados com
  anonimato. Estrutura mantida (PHP, FormSubmit, modo mensagem, WhatsApp).
- **Chaves novas:** ansiedade/magoas/medo/paz (PHP, HTML e JS atualizados).
- Aplicado em site-contabo/index.html, paginas/home_preview.html, enquete.php
  e gerador adicionar_enquete.py. JS/HTML/PHP validados. zip regenerado.
- **CHAVE NOVA (18/08, 2ª rodada):** localStorage trocado de
  despertar_enquete_votada → despertar_enquete_votada_v2. Motivo: quem votou
  na enquete ANTIGA (leitura online) ficava preso no modo mensagem na nova
  pergunta. Com a chave v2, todos podem votar na nova enquete (batalha da
  mente) sem limpar o navegador. O autor confirmou que na janela anônima
  funcionava; agora funciona no navegador normal também.

---

## 🎥 CANAL YOUTUBE + AULAS GRÁTIS (18/08)

- **Canal:** @portal.o.despertar (título "Missão com Deus"). Sandbox acessou
  o título, mas o corpo do canal retorna 401 (YouTube bloqueia automação);
  Studio exige login (não acessível daqui).
- **Estrutura Kiwify (confirmada):** Evolução da Alma R$19,90 (só as aulas
  dela) · Anestesia Mental R$19,90 (só as dele) · Pacote completo R$49,00.
- **Ideia do autor (aguardando aval):** liberar aulas-grátis (teaser) embaixo
  dos livros online, com links diretos youtu.be:
  - Anestesia Mental (livro online): Módulo 04 "O Impulso sem Consciência"
    https://youtu.be/fO5RIdrFzMw
  - Anestesia Mental (grátis): Módulo 02 "O Despertar da Consciência"
    https://youtu.be/YSw_MY8NNZI
  - Evolução da Alma: Módulo 02 "O Despertar da Alma"
    https://youtu.be/ZwBDxpnFV6s
  - Evolução da Alma (grátis): Módulo 04 "Perdão como libertação da alma"
    https://youtu.be/fO5RIdrFzMw (mesmo link do primeiro — conferir)
- **VERDADE TÉCNICA (honestidade):** um link de vídeo público NÃO esconde o
  canal — ao clicar, o YouTube mostra o canal e a aba de vídeos. Caminhos:
  (a) marcar as aulas pagas como NÃO LISTADAS (unlisted) → somem da lista
  pública do canal e funcionam por link dentro da Kiwify (resolve o problema
  do autor com a Kiwify); (b) embutir o vídeo na nossa página (iframe
  youtube-nocookie) para tocar sem sair do site; (c) aceitar a descoberta do
  canal (conteúdo grátis vira marketing — pode ser positivo).
- **✅ APLICADO (18/08):** blocos "🎬 Aula grátis do canal" com iframe
  youtube-nocookie inseridos antes da seção #fim:
  - livro05 (Evolução da Alma): Módulo 04 — Perdão como libertação da alma
    (fO5RIdrFzMw)
  - livro09 (Anestesia Mental): Módulo 04 — O Impulso sem Consciência
    (f_GxlRva2CQ — link CORRIGIDO pelo autor)
  - Aplicado em site-contabo/livro05.html, livro09.html e previews com leitor.
  - Vídeos do autor estão como "Não listado" (unlisted) no YouTube → canal
    protegido; iframe usa youtube-nocookie (privacidade). JS/HTML OK; zip
    regenerado.

---

## 📖 LIVRO 12 — REORGANIZAÇÃO + EDIÇÕES (18/08, 2ª sessão)

Pedidos do autor aplicados em site-contabo/livro12.html e
paginas/livro12_leitor_preview.html (script:
analise/compraoseu.preview/ajustar_livro12_estrutura.py):

- **"Como usar este guia" SUBIU por inteiro** para dentro da página
  "Sobre este guia" (abaixo do box Atenção). Deixou de ser página separada;
  âncora antiga #como-usar preservada (span) para links salvos.
- **"Mensagens para o Dia a Dia" e "Orações no Nome de Jesus" SUBIRAM**
  para logo depois de "Sobre este guia" (antes da Gratidão). Sumário
  reordenado na mesma sequência. A **videoaula permanece no FIM**.
- **Paz e Emoções:** mensagem longa de Mateus 6 encurtada — "Não andeis
  ansiosos pelo dia de amanhã, nem pela vossa vida. (Mateus 6:25-34)" —
  padrão de apenas lembrar a passagem.
- **Proteção e Segurança:** removidas as DUAS partes longas do Salmo 23
  ("O Senhor é o meu pastor... Deitar-me faz..." e "Preparas uma mesa...").
  Ficaram só as afirmações curtas.
- **Relacionamentos e Perdão:** Salmo 51 encurtado até "Não me lances fora
  da tua presença. (Salmo 51:10-11)"; Mateus encurtado até "fazei bem aos
  que vos odeiam. (Mateus 5:44)".
- Navegação Anterior/Próximo refeita na nova ordem; "como-usar" removido do
  mapa NOMES do leitor. JS/HTML validados; zip regenerado (sem dados da
  enquete).

## 📱 MENU MOBILE DA HOME (18/08)

- Antes: ao tocar nos três traços (☰), o menu abria em tela cheia,
  centralizado, com links brancos.
- Agora: menu abre como CARTÃO ALINHADO À DIREITA (debaixo do ☰), com
  borda e sombra, e os links em DOURADO (var(--gold-light)) para melhor
  leitura. Botão "Entrar no Portal" continua como botão dourado.
- Aplicado em site-contabo/index.html e paginas/home_preview.html.

## ⚠️ NOTA DE CONTINUIDADE (18/08)

O autor abriu novo chat (branch arena/01a01525-instalador) e trouxe todo o
trabalho da branch arena/019fcd27-instalador via merge fast-forward — nada
se perdeu. O zip que o autor baixou antes NÃO continha estas mudanças
porque elas ainda não haviam sido feitas (o chat anterior encerrou antes).
Agora estão feitas e dentro do site-contabo.zip.

---

## 🃏 LIVRO 12 PUBLICADO NA BIBLIOTECA + CAPA (18/08, 3ª sessão)

- **Card 12 na biblioteca da Home** (depois do Livro 11, antes do card
  Apoio), mesmo padrão visual dos demais:
  - Capa: https://i.ibb.co/6RRTBY06/livro12.jpg (imgbb, como as outras)
  - Título: "Comece o dia com Afirmações, Declarações e Orações"
  - Legenda: "Mensagens diárias para o seu dia a dia: versículos de
    declaração, gratidão, afirmações e orações no Nome de Jesus para
    começar cada manhã na presença de Deus."
  - Badges: "Mensagens diárias" + "🔒 Protegido"
  - Botões: "Ler grátis" → /livro12 · "Portal" → pay.kiwify.com.br/iVfp2bi
  - Aplicado em site-contabo/index.html e paginas/home_preview.html
    (preview aponta para livro12_leitor_preview.html).
- **Capa DENTRO do livro12** (seção .capa, classe .capa-livro, igual aos
  livros 04/05/09/10): imagem + CSS adicionados em site-contabo/livro12.html
  e paginas/livro12_leitor_preview.html.
- **Sitemap NÃO alterado** de propósito: o livro11 também não está no
  sitemap; manter coerência (adicionar os dois juntos se o autor quiser).
- JS/HTML validados (divs balanceadas); zip regenerado sem dados da enquete.

## ⚠️ ATENÇÃO — ESTA SESSÃO FICOU SELADA APÓS O MERGE DO PR #1

O PR #1 foi mesclado no main e a sessão travou envios ao GitHub. As
mudanças ACIMA (card 12 + capa no livro12) estão SOMENTE nesta sessão do
Arena (commit local) e no zip baixável da conversa — AINDA NÃO estão no
GitHub. No PRÓXIMO CHAT: refazer/aplicar o card 12 e a capa conforme esta
seção descreve (ou pedir ao autor o zip desta sessão) e dar push ao main.

## 📊 CONTADOR DE VISITAS v2 (18/08 — criado, AINDA NÃO aplicado no servidor)

- Arquivo: analise/compraoseu.preview/gerar_estatisticas_v2.py
- Sugestão 1 (filtros): só conta respostas 200/304 de User-Agent que NÃO é
  robô (descarta Googlebot/Bing, curl/python, scanners, prévias de
  WhatsApp/Facebook e UA vazio). Descartes exibidos com transparência.
- Sugestão 2 (pessoas): cartões "👤 Visitantes únicos" hoje/ontem/total
  (IPs distintos) + coluna por dia. Inclui livro11 e livro12 no ranking.
- TESTE com log sintético: 35 requisições (13 humanas de 5 pessoas + 22
  robôs/ataques) → v1 mostrou 35; v2 mostrou 13 páginas e 5 visitantes. ✅
- Para aplicar (autor decide): backup do /home/deploy/gerar_estatisticas.py,
  colar a v2 no lugar (mesmo nome), rodar 1x manualmente; cron de 1h
  continua igual. O stats.html passa a mostrar os valores prudentes.
- LOG/OUT agora aceitam variáveis de ambiente (STATS_LOG/STATS_OUT) p/ teste.

## 🌐 REDIRECIONAMENTO ATIVO + PAINEL v2 RODADO (20/08 — relato do autor)

- O autor ativou o novo domínio missaocomdeus.com.br e o REDIRECIONAMENTO
  de compraoseu.com para ele. Consequência: o log antigo
  /www/wwwlogs/compraoseu.com.log PAROU de crescer em 18/08 20:03 — as
  visitas novas agora caem no log do DOMÍNIO NOVO (missaocomdeus).
- O autor testou a v2 (stats_teste dentro do site missaocomdeus): funcionou.
  Hoje/ontem = 0 porque o script lia o log antigo (parado). Basta apontar
  STATS_LOG para o log do missaocomdeus (v2 aceita variável de ambiente).
- NÚMEROS REAIS revelados pela v2 (histórico 11-18/08, log antigo):
  · 1.987 páginas vistas por humanos · 579 pessoas (IPs únicos)
  · 7.379 robôs descartados (61%) · 2.764 ataques/erros (23%)
  · Por dia: ~200-400 páginas humanas, ~60-120 pessoas/dia
  · O painel v1 mostrava ~1.300-1.600/dia: era ~80% robô/ruído.
  · Quiz = 0 na v2: o /quiz responde REDIRECIONAMENTO (301) e cai nos
    descartados — refinamento futuro: contar 301 do /quiz como clique.
- PENDÊNCIA para o próximo chat: atualizar o LOG padrão do script para o
  log do missaocomdeus (ou somar os dois logs) e o rótulo do domínio no
  cabeçalho do painel; subir a v2 ao GitHub.

## 📊 v2 RODANDO NO DOMÍNIO NOVO (20/08 22:14 — números reais)

- Log novo (missaocomdeus) começa em 18/08 17:00 (nascimento do redirect).
- 2 dias: 388 pessoas únicas · 19/08 = 524 págs/217 pessoas · 20/08 = 424/125.
- Robôs 2.003 e ataques 727 descartados — filtros funcionando.
- QUIZ = 0 explicado: (a) o /quiz responde REDIRECIONAMENTO (301) e a
  peneira descarta código != 200/304; (b) os testes antigos do autor estão
  no log velho do compraoseu, anterior ao corte. Os cliques não sumiram —
  estão nos "descartados". Refinamento pendente: contar 301 de /quiz.
- QUIZ "PAIS E FILHOS" (novidade do autor, fora do repo): página
  /guia-pais-filhos (9 acessos) e /guia-pais-filhos.html (2). Aparece em
  "Outras páginas" porque NÃO está na lista PAGINAS do script. Pendência
  próximo chat: adicionar ('/guia-pais-filhos', 'Guia Pais e Filhos —
  Quiz') ao PAGINAS da v2, contar 301 do /quiz, trocar o rótulo do domínio
  no cabeçalho e criar a página guia-pais-filhos no repo (hoje só existe
  no servidor).
- Barras "//enquete.php" com barra dupla: só estética da exibição.

## 🧩 v2 REFINADA (20/08, noite): Guia Pais e Filhos no ranking

- sw.js pré-carrega '/quiz' (lista URLS) → é ELE que gera os GET /quiz com
  referer sw.js (não são cliques). No missaocomdeus /quiz responde 404
  (rewrite não migrou). PENDÊNCIAS próximo chat: atualizar sw.js (remover
  /quiz ou corrigir; incluir /livro12), criar redirect /quiz e
  /quiz-pais-filhos → /guia-pais-filhos no nginx do missaocomdeus.
- v2 atualizada no repo: PAGINAS ganhou ('/guia-pais-filhos','Guia Pais e
  Filhos — Quiz') e as condições de contagem agora usam `path in PAGINAS`
  (antes a página nova caía em 'outros' mesmo listada). Testado com log
  sintético: guia aparece no ranking com contagem exata. Autor valida
  dados a partir de 18/08 17:00 (nascimento do log missaocomdeus).

## ✅ PAINEL v2 OFICIALIZADO NO missaocomdeus (20/08, noite)

- Autor aplicou o comando: Guia Pais e Filhos no ranking (14º, 9 acessos)
  e contador reconhecendo páginas novas. Painel validado pelo autor.
- v2 do repo CONVERTIDA para o domínio novo (6 trocas): LOG padrão =
  missaocomdeus.com.br.log · OUT = missaocomdeus.com.br/stats.html ·
  rótulos e links do painel = missaocomdeus.com.br.
- OFICIALIZAÇÃO no servidor (comando passado ao autor): backup da v1
  (gerar_estatisticas-v1.bak), v2 assume o nome gerar_estatisticas.py,
  roda sem env vars e o cron de 1h continua igual. Painel oficial:
  https://missaocomdeus.com.br/stats.html (stats_teste.html pode apagar;
  stats.html antigo do compraoseu fica obsoleto).
- Verificar no aaPanel se o Cron aponta para /home/deploy/gerar_estatisticas.py.

## 🏁 ENCERRAMENTO DA MIGRAÇÃO DAS ESTATÍSTICAS (20/08, 22:43 — CONCLUÍDO)

- /home/deploy final: gerar_estatisticas.py (v2 oficial, era missaocomdeus)
  · gerar_estatisticas-v1.bak (v1 de recordação) · gerar_estatisticas_v2-antes.bak
  (intermediário, pode apagar). stats.html oficial JÁ com dados reais.
- DECISÃO: NÃO apagar o site compraoseu.com do aaPanel — ele sustenta o
  REDIRECIONAMENTO 301 (links antigos, Google, WhatsApp, PWA instalado).
  Mas NÃO precisa mais atualizar os arquivos dele: o 301 acontece antes de
  qualquer página ser servida. Dali em diante toda mudança é SÓ no
  missaocomdeus. Manter o SSL do compraoseu renovando (o redirect https
  depende dele) e a renovação do domínio.
- Museu: /www/wwwroot/compraoseu.com/ guarda o enquete_dados.json com os
  votos da era antiga (não apagar sem exportar se quiser o histórico).
- ÚLTIMA VERIFICAÇÃO pendente do autor: aaPanel → Cron → conferir tarefa
  horária chamando python3 /home/deploy/gerar_estatisticas.py; e 1h depois
  recarregar stats.html conferindo o "gerado em" atualizado sozinho.
- PRÓXIMO CHAT (lista fechada): subir ao GitHub v2 final + card livro12 +
  capa livro12; sw.js (tirar /quiz, incluir /livro12); redirect /quiz e
  /quiz-pais-filhos → /guia-pais-filhos no nginx; criar guia-pais-filhos
  no repo; sitemap/SEO do missaocomdeus; refinar contagem do quiz.

## 🧹 LIMPEZA FINAL (20/08, noite — pelo autor)

- Backups do gerar_estatisticas apagados do /home/deploy (v2 oficial no GitHub).
- Pasta compraoseu.com esvaziada pelo autor (mantidos .user.ini e o site vivo
  apenas como redirecionador 301; SSL precisa continuar renovando).
- Votos da enquete antiga: orientado salvar antes em
  /home/deploy/enquete_museu_compraoseu.json.
- Cópias no GitHub feitas pelo autor via copiar/colar + commit: MEMORIA
  completo, gerar_estatisticas.py (v2 oficial) e stats.
- Regra de ouro estabelecida: toda mudança agora é SÓ no missaocomdeus.com.br.

## 🩺 CONSULTORIA 21/08 (manhã) — testes do autor confirmados no painel

- Testes do autor registrados: Guia Pais e Filhos (+1 hoje), enquete
  (enquete.php 194→214, voto dentro; e-mail FormSubmit recebido = prova).
- DESCOBERTA: Quiz Autoavaliação mora DENTRO da Home (seção #quiz, envia
  por FormSubmit) — a linha '/quiz' do ranking NUNCA poderá contar (relíquia
  da era Vendd). Termômetro real do quiz = e-mails FormSubmit +
  /guia-pais-filhos. Linha '/quiz' removida da v2 do repo; comando de
  remoção passado ao autor para o servidor (backup -antes-quiz.bak).
- Saúde geral OK: queda matinal -64,8% é variação normal (comparar à noite);
  31 pessoas até 9h30; robôs/ataques filtrados. Refinamento futuro anotado:
  excluir /stats* e /enquete.php (AJAX) do total geral (visitas do próprio
  admin inflam levemente).

## 📖 LEITURA DO PAINEL EXPLICADA AO AUTOR (21/08)

- /guia-pais-filhos (10) = ABERTURAS da página (não conclusões). Conclusões
  do quiz = e-mails FormSubmit. Downloads do PDF jesus-quer-falar (8) =
  provável termômetro de conclusão do quiz Pais e Filhos (PDF ofertado no
  final); confirmar origem com: grep jesus-quer-falar no log + referer.
- /stats.html (96) + /stats (31) = mesma página, duas portas (try_files do
  nginx serve $uri.html); log anota o que foi digitado.
- /stats_teste.html (3) = histórico do log (arquivo já apagado; log não
  esquece o passado; futuras batidas = 404 descartado).
- Polimentos futuros: tirar barra dupla '//' da tabela outras; excluir
  /stats* e /enquete.php do total geral (visitas do admin).

## 🎁 CORREÇÃO IMPORTANTE (21/08): PDF é o presente do Quiz AUTOAVALIAÇÃO

- Confirmado no index.html (linha ~1280): ao completar o Quiz Autoavaliação
  na Home, aparece a tela "🎁 Sua surpresa chegou!" com botão que baixa
  /ebooks/jesus-quer-falar.pdf. O PDF é termômetro do AUTOAVALIAÇÃO
  (não do Pais e Filhos, como suposto antes).
- Referers medidos pelo autor: 3 downloads vindos da Home (= conclusões do
  quiz com clique no presente) + 21 diretos (compartilhamento WhatsApp/
  releituras/robôs; dos 24 totais, 8 passaram na peneira humana).
- Funil do Autoavaliação: Home → e-mails FormSubmit (conclusões) → clique
  no presente (log). Guia Pais e Filhos não mostrou downloads no referer
  (fim dele não oferta PDF ou ninguém clicou — página está só no servidor).
- Ideia futura: cartão "🎁 Presentes baixados" no painel (contar
  jesus-quer-falar.pdf com referer da Home).

## 🏁 ENCERRAMENTO FINAL DA TEMPORADA DE ESTATÍSTICAS (21/08)

- Entendimento final corrigido com o autor: o PDF jesus-quer-falar é o
  presente do quiz AUTOAVALIAÇÃO (Home), não do Pais e Filhos. Cada quiz
  com seus termômetros: Autoavaliação = e-mails + downloads do presente;
  Pais e Filhos = linha no ranking + e-mails.
- Autor orientado a: aplicar último polimento (aposentar /quiz + cartão
  'Quiz Pais e Filhos'), copiar gerar_estatisticas.py do deploy para o
  GitHub (lápis + colar + commit) e acrescentar bloco 'MAPA FINAL DOS
  QUIZZES' no MEMORIA do GitHub. Depois apagar -antes-quiz.bak.
- Estado final: painel v2 oficial, cron horário, dados 100% humanos,
  funis dos dois quizzes mapeados, GitHub espelhado pelo autor.

## 🔔 LIÇÃO FINAL (21/08): por que o Quiz Autoavaliação nunca entrou nas stats

- Causa raiz: o quiz mora DENTRO da Home (âncora #quiz não chega ao servidor)
  e envia respostas direto ao FormSubmit (externo) — invisível ao log.
- O que deveria ter sido feito (opções para implementar no futuro):
  A) Página própria /quiz.html (como o guia-pais-filhos, que nasceu certo);
  B) "Sininhos" JS (técnica Vendd): fetch('/q-quiz-inicio') no 1º clique e
     fetch('/q-quiz-fim') na conclusão + 2 arquivos vazios (200) + 2 linhas
     no PAGINAS do gerar_estatisticas → funil completo início×conclusão
     (revela também desistências, que nem o e-mail mostra).
- Implementação estimada: ~30 min num próximo chat (index.html + arquivos
  + PAGINAS + subir ao GitHub). Vale aplicar o mesmo sininho de conclusão
  no guia-pais-filhos.

## 🎬 PRÓXIMA ETAPA PLANEJADA: PÁGINA TRILOGIA DA ALMA (21/08)

- Autor vai testar o agente Manus (conectado ao GitHub) para criar a
  página /trilogia-da-alma — área de alunos com as 7 videoaulas da
  Trilogia Evolução da Alma (IDs: _zRVlsh9T9E, ZwBDxpnFV6s, j8fr9kvOhMk,
  fO5RIdrFzMw, pL2rd8sm-rk, ycGZ4Vjv2MY, 9IfeARq38UA — vídeos NÃO listados).
- ATENÇÃO: as 7 aulas são o CURSO PAGO da Kiwify (R$19,90) — página deve
  ter portão com código de acesso + noindex + fora do sitemap.
- Prompt profissional completo salvo em: analise/prompt_manus_trilogia.md
  (padrão visual, youtube-nocookie, progresso localStorage, portão,
  marcadores q-trilogia-m01..07 + PAGINAS no gerar_estatisticas — a página
  já nasce DENTRO das estatísticas, lição aprendida do quiz da Home).
- Qualquer agente (Manus ou chat daqui) deve LER o MEMORIA antes e
  REGISTRAR sua obra nele depois — regra da casa.

## 🎬 PROMPT AMPLIADO PARA O MANUS (21/08): 2 cursos + sininhos do quiz

- Novo prompt COMPLETO em analise/prompt_manus_cursos.md (substitui o
  prompt_manus_trilogia.md como versão a usar). Encomendas:
  1) /trilogia-da-alma (código EVLTRLAM26, 7 aulas, chaves trilogia_*)
  2) /anestesia-mental (código NSTMNT26, 7 aulas, chaves anestesia_*,
     vídeos: yVv_BKMJ4DE, YSw_MY8NNZI, 4IwyK4pmaJI, f_GxlRva2CQ,
     Fw4RE6ld_UU, 31XPvz6DSeY, dYwYB9uDhnI)
  3) Sininhos do Quiz Autoavaliação na Home (q-quiz-inicio/q-quiz-fim,
     1x por sessão, index + home_preview)
  4) gerar_estatisticas_v2.py: +16 linhas no PAGINAS
- REGRA-MESTRA no prompt: Manus NÃO pode commitar no main sem aprovação
  do autor ("APROVADO"); se precisar, branch manus/cursos + PR.
- Cercas: só os arquivos listados; na Home só o JS do quiz; nada de
  bibliotecas externas/rastreadores; UTF-8; validação HTML/JS.
- ALERTA dado ao autor: Módulo 05 da Anestesia veio com título repetido
  do 02 ("O Despertar da Consciência") — conferir antes de enviar.
- Códigos/constantes no topo do JS (CODIGO_ACESSO, LINK_COMPRA) para
  trocas fáceis; aceitar código com trim e sem case-sensitive.

## 🎓 CURSOS PUBLICADOS NO SERVIDOR (21/08 — Manus + Arena + autor)

- PR #3 do Manus mesclado no main (versão ORIGINAL — as 4 correções que o
  Manus mostrou nunca foram pushadas; merge levou o commit antigo).
- Estado do main: mod02 Anestesia "A Anestesia Mental" (correto), mod05
  "Da" maiúsculo (cosmético), fetch dos sininhos com ".html" (bug),
  rascunho_memoria.md na raiz (cosmético), LINK_COMPRA não ligado ao botão
  (cosmético — href está certo hardcoded).
- SOLUÇÃO SERVER-SIDE (comando único do Arena, executado pelo autor):
  16 marcadores criados; sininhos do quiz instalados no index DO SERVIDOR
  (preservando menu dourado + card 12); título mod05 polido; painel
  ganhou normalização que REMOVE ".html" do fim dos paths (une /pagina e
  /pagina.html — neutraliza o bug do fetch e une /stats stats.html) +
  16 linhas no PAGINAS. Painel regenerado com sucesso.
- Códigos: Trilogia EVLTRLAM26 · Anestesia NSTMNT26 (constantes no JS).
- PENDÊNCIAS COSMÉTICAS (futuro): espelhar index.html do servidor no
  GitHub (GitHub está sem menu dourado; livro12.html sem capa também),
  apagar rascunho_memoria.md da raiz, polir mod05/LINK_COMPRA no GitHub.

## 🧭 MENU DA HOME: CURSOS ADICIONADOS (21/08)

- Sininhos do Quiz Home confirmados no painel do autor (linhas 17-18:
  iniciaram/concluíram — zeradas, recém-nascidas).
- Menu (navlinks) da Home ganhou 2 itens antes do botão dourado
  "🔓 Entrar no Portal" (mantido por último, vai à área de membros Kiwify):
  "🎓 Curso Trilogia" → /trilogia-da-alma e "🎓 Curso Anestesia" →
  /anestesia-mental. No celular aparecem no cartão dourado à direita.
- Aplicado em site-contabo/index.html e paginas/home_preview.html do repo;
  comando server-side idempotente (âncora = linha do nav-cta) passado ao
  autor para o index DO SERVIDOR.

## 🔒 CADEADO ANTI-YOUTUBE + PLANO DE DOAÇÕES (21/08, encerramento)

- Cadeado sandbox aplicado pelo autor nos 14 vídeos dos cursos: FUNCIONOU
  (play e tela cheia OK; clique no logo/canal do YouTube não sai mais do
  player). Backups: trilogia/anestesia-antes-cadeado.bak.
- DOAÇÕES sem expor o nome do autor (receio: Pix pessoal e MEI no nome):
  SOLUÇÃO = Kiwify (checkout mostra a marca, fatura mostra KIWIFY; Pix
  gerado pela plataforma). Card "🙏 Apoie o Portal" JÁ existe na Home
  (Apoiar com R$9,90 → pay.kiwify.com.br/CF9nhFx).
  Plano: criar degraus R$4,90/9,90/19,90/49,90 na Kiwify + campanha
  Vakinha p/ valor livre + página /apoie no padrão do site (nascer contada
  no painel). 
- IDEIAS PRIORIZADAS p/ próximos chats: 1) SEO missaocomdeus (sitemap +
  Search Console do domínio novo — Google só conhece compraoseu!);
  2) página /apoie; 3) Canal WhatsApp "Palavra do Dia" (conteúdo do
  livro12); 4) seção de depoimentos reais (comentários da enquete, com
  permissão); 5) higiene: sw.js (tirar /quiz, incluir livro12 e cursos),
  espelho GitHub, cartão "Presentes baixados" no painel.

## 🗺️ SEO DO DOMÍNIO NOVO — RAIZ DOS ✗ ENCONTRADA (21/08)

- GSC do missaocomdeus: sitemap enviado 18/08 lia COM SUCESSO... 13 URLs
  do COMPRAOSEU (arquivo copiado sem adaptar). robots.txt idem. 11 HTML
  com og:url do domínio antigo. Canonicals são RELATIVOS (ok!).
- Correção (comando passado ao autor + aplicada no repo): sitemap NOVO com
  14 URLs missaocomdeus (agora inclui livro11, livro12 e guia-pais-filhos);
  robots novo; etiquetas https://(www.)compraoseu.com → missaocomdeus nos
  HTML. Reenviar sitemap no GSC; pedir indexação 2/dia na ordem:
  / → livro12 → livro05 → livro09 → livro04 → demais.
- Expectativa honesta: ✗ virando ✓ em 1-3 semanas (domínio de 3 dias);
  301 do compraoseu transfere autoridade.

## 🏆 GSC COMPRAOSEU PEDIU REVALIDAÇÃO → OPORTUNIDADE DE OURO (21/08)

- Causa provável: validação antiga era por arquivo/etiqueta no site; a
  pasta foi esvaziada + 301 em tudo → Google perdeu a prova. Único método
  agora: TXT no DNS (imune a redirect).
- Orientação dada: NUNCA "Remover propriedade"; adicionar registro TXT
  (tipo TXT, nome @, valor google-site-verification=...) no painel DNS do
  compraoseu (indícios de Cloudflare no código) → Validar.
- TESOURO: com o compraoseu revalidado, usar a ferramenta MUDANÇA DE
  ENDEREÇO (Configurações da propriedade compraoseu → Change of Address →
  missaocomdeus.com.br). Transfere indexação/autoridade oficialmente —
  maior acelerador da migração SEO. Fazer ANTES de esperar os 301 agirem
  sozinhos. Depois: manter 2 inspeções/dia no missaocomdeus.

## ✅ SEO DO MISSAOCOMDEUS EXECUTADO COM SUCESSO (21/08, noite)

- Autor rodou os comandos: cadeado sandbox nos 14 vídeos ✅; sitemap novo +
  robots + 12 páginas com etiquetas corrigidas ✅.
- GSC (missaocomdeus): sitemap.xml reenviado 21/08 → lido 21/08 → SUCESSO,
  14 PÁGINAS DESCOBERTAS (antes: 13 URLs do domínio errado).
- "Erro" do cp '...' = autor colou a linha de exemplo com reticências;
  inofensivo, nada executado.
- PENDENTE (próximos dias, ordem): 1) TXT no DNS do compraoseu → Validar
  no GSC; 2) ferramenta MUDANÇA DE ENDEREÇO (compraoseu → missaocomdeus);
  3) seguir 2 inspeções/dia priorizando / → livro12 → livro05 → livro09.

## 🔑 COMPRAOSEU REVALIDADO NO GSC (21/08, noite)

- NS confirmados: dns3/dns4.hostgator.com.br (os DOIS domínios na HostGator).
- Autor plantou o TXT (método "Fornecedor do nome do domínio") na zona DNS
  da HostGator → propagou rápido → "Aceder à propriedade" = VALIDADO.
- Falta confirmar/executar o CLIQUE DE OURO: propriedade compraoseu →
  ⚙️ Configurações → Mudança de endereço → missaocomdeus.com.br →
  Confirmar. Sinal de sucesso: aviso "site a ser movido" no topo das duas
  propriedades. Depois: só manter 2 inspeções/dia no missaocomdeus.

## 🏆 MUDANÇA DE ENDEREÇO APROVADA — MIGRAÇÃO SEO OFICIALIZADA (21/08)

- GSC: "Validação aprovada" — www.compraoseu.com → missaocomdeus.com.br.
  Checks: Redirecionamento 301 da página inicial ✅ + Validação de ambos ✅.
- A partir de agora o Google transfere OFICIALMENTE indexação/autoridade
  (processo de semanas; aviso "site em movimento" fica no topo — normal).
- REGRAS DE OURO pós-mudança (NÃO violar por pelo menos 6-12 meses):
  1) MANTER o 301 do compraoseu ativo (nunca desligar o site redirecionador);
  2) MANTER SSL do compraoseu renovando; 3) MANTER a renovação do domínio
  compraoseu; 4) NÃO remover o TXT do DNS nem as propriedades do GSC.
- Rotina do autor: 2 inspeções/dia no missaocomdeus (/ → livro12 →
  livro05 → livro09 → livro04 → demais) e acompanhar ✗ virando ✓.

## 📧 NOVO E-MAIL OFICIAL + SAGA DO INSTAGRAM (21/08)

- E-MAIL NOVO: portalmissaocomdeus@gmail.com (autor criou; o antigo
  compraoseu.com@gmail.com sai de cena). FormSubmit aparecia em 2 pontos
  do index (quiz→presente e-book + notificação da enquete). Repo
  atualizado; comando server-side varre *.html e *.php (pega também o
  guia-pais-filhos que só existe no servidor).
- ⚠️ FORMSUBMIT EXIGE ATIVAÇÃO do e-mail novo: no 1º envio, chega e-mail
  "Confirm your email" no portalmissaocomdeus@gmail.com (ver SPAM) — tem
  que CLICAR, senão quiz/enquete param de notificar em silêncio. Testar
  quiz completo após a troca.
- E-mail profissional missaocomdeus@missaocomdeus.com.br: HostGator só
  domínio (sem hospedagem) = e-mail pago (Titan). RECOMENDADO futuro:
  Zoho Mail FREE (domínio próprio, 5 usuários, MX na zona DNS HostGator)
  — guia num próximo chat. Por ora Gmail resolve 100%.
- INSTAGRAM (histórico): conta pessoal antiga suspensa (+3 contas FB em
  cascata); nova pessoal suspensa e RECUPERADA via recurso; conta da
  Laura (laura.compraoseu@gmail) suspensa 2x, pede documentos — autor
  NÃO enviou (correto: docs de homem p/ perfil feminino = risco de
  cascata). Sobraram: FB "Missão com Deus" (vivo) e TikTok ~4.000
  seguidores (vivo).
- ORIENTAÇÃO dada: nova conta IG como MARCA "Portal Missão com Deus"
  (não persona humana), criada vinculada à página FB sobrevivente
  (Central de Contas Meta = mais confiança), com e-mail novo; aquecer
  devagar (perfil completo, poucos posts primeiros dias, sem follow em
  massa, sem spam de links). Laura só como "mentora virtual" declarada —
  perfil se passando por pessoa real com fotos de IA é ímã de suspensão
  (provável causa das quedas). TikTok é o ativo mais forte: crescer lá
  e apontar bio para missaocomdeus.com.br.

## 📬 E-MAIL NOVO 100% ATIVO (21/08 — FORM ACTIVATED)

- Comando no servidor atualizou 4 arquivos: index.html, enviar_guia.php,
  notificar.php (PHPs que o autor lembrava!) e index_backup_quiz_pais.html.
- FormSubmit ATIVADO para portalmissaocomdeus@gmail.com ("Form Activated
  — Form at: https://missaocomdeus.com.br/"). O erro "token não
  encontrado" era link antigo/consumido — resolvido com novo teste.
- Falta só o teste final do quiz (notificação chegando no e-mail novo).
- ⚠️ REGRA: NÃO apagar o Gmail antigo (compraoseu.com@gmail.com) — pode
  ser login de Kiwify/YouTube/TikTok/HostGator/Contabo/Meta. Plano:
  manter vivo, ativar encaminhamento para o novo, migrar cadastros aos
  poucos.

## 📸 KIT DO NOVO INSTAGRAM (21/08 — bio profissional)

- @: portalmissaocomdeus (1ª opção, casa com o e-mail) · alternativas:
  missaocomdeus.oficial, missaocomdeusbr.
- Campo NOME (pesquisável!): "Missão com Deus | Livros Cristãos Grátis".
- BIO recomendada (opção A):
  "✝️ Uma palavra de Jesus para sua mente e alma / 📚 12 livros cristãos
  GRÁTIS online / 🎓 Cursos e devocional de 30 dias / 👇 Comece a ler
  agora" (testar opção B com linguagem da enquete após 30 dias).
- Link: https://missaocomdeus.com.br (visitas caem no painel).
- Plano 14 dias: criar vinculado à página FB sobrevivente, categoria
  Comunidade religiosa, 1 post/dia (afirmações do Livro 12 = fábrica de
  posts), destaques 📚🙏🎓✨, sem follow em massa/links/ads no 1º mês.

## 🎬 CORREÇÃO DE VÍDEO — TRILOGIA MÓDULO 03 (21/08)

- Módulo 03 (Superação das dificuldades emocionais) estava com o vídeo
  ERRADO: j8fr9kvOhMk. CORRETO: 4UmQlRiirXs. Comando server-side passado
  ao autor (backup trilogia-antes-video03.bak).
- ⚠️ O GitHub (main) ainda tem o ID errado no trilogia-da-alma.html —
  corrigir no espelho quando for feita a sincronização (lápis no GitHub:
  trocar j8fr9kvOhMk por 4UmQlRiirXs) ou no próximo chat.
- Lista DEFINITIVA Trilogia: m01 _zRVlsh9T9E · m02 ZwBDxpnFV6s ·
  m03 4UmQlRiirXs · m04 fO5RIdrFzMw · m05 pL2rd8sm-rk ·
  m06 ycGZ4Vjv2MY · m07 9IfeARq38UA.

## 💬 CAIXA DE COMENTÁRIOS NOS CURSOS (21/08 — sem Manus, direto pelo Arena)

- Pedido do autor: alunos poderem comentar/testemunhar no fim das 2
  páginas de curso. SOLUÇÃO: caixa "Deixe seu comentário ou testemunho"
  (nome opcional + texto + botão dourado), estilo .modulo do padrão,
  visível SÓ após o portão (mostrada na liberarInterface), enviando via
  FormSubmit ajax para portalmissaocomdeus@gmail.com com assunto
  "💬 Comentario de aluno - [Curso]" e página de origem; resposta de
  agradecimento no lugar da caixa após envio.
- Comando server-side ASCII gerado e TESTADO em simulação (âncoras:
  '<div id="fim">' e linha do conteudo em liberarInterface; idempotente;
  backups *-antes-comentario.bak). Passado ao autor.
- GitHub: as páginas de lá ficarão sem a caixa até o próximo espelho
  (pendência já conhecida).
