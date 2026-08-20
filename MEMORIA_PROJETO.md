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

## 🎉🎉 SITE NOVO 100% NO AR — INCLUINDO www (18/08, vitória final)

- **https://www.missaocomdeus.com.br CONFIRMADO FUNCIONANDO** (verificado por
  fetch ao vivo): Home completa + 12 livros + quiz + enquete, com links www.
- **nginx -t:** "syntax is ok / test is successful". Avisos "conflicting
  server name" são inofensivos (duplicidade Certbot × aaPanel, nginx ignora).
- **Como resolveu o problema:** os arquivos manuais do Certbot
  (/etc/nginx/sites-available/conectai-apioficial, conectai-frontend,
  conectai-backend) referenciavam certificados Let's Encrypt que não existiam
  mais. Correção: sed removeu as linhas ssl_certificate e trocou
  `listen 443 ssl;` por `listen 80;` (webhooks internos funcionam em HTTP).
  Backups .bak criados. O painel não mostrava esses arquivos (fora do aaPanel).
- **Falta (decisões do autor):** redirect 301 compraoseu→missaocomdeus (ou
  manter os dois); GSC nova propriedade; sitemap com novo domínio.

---

## 🎉 SITE NOVO NO AR (18/08, confirmado)

- **https://missaocomdeus.com.br ESTÁ NO AR e funcionando** (verificado por
  fetch ao vivo): Home completa (hero, quiz, biblioteca com 12 livros,
  enquete) e livro12 com capa + sumário + aula grátis.
- **DNS propagado:** missaocomdeus.com.br e www → 212.28.182.86 ✅
- **SSL ativo** (Let's Encrypt), **PHP 8.1 ativo** no config do site.
- **try_files adicionado** (URLs bonitas /livroXX sem .html).
- **NOTA nginx -t:** ainda acusa erro do apioficial.compraoseu.com
  (certificado antigo inexistente no config) — NÃO afeta o site novo; limpar
  depois removendo as linhas ssl_certificate do config do apioficial.
- **Navegador do autor:** se der NXDOMAIN, é cache local (usar janela
  anônima ou digitar sem acento: missaocomdeus.com.br).

---

## 🆕 NOVO DOMÍNIO — missaocomdeus.com.br — ✅ LIBERADO (18/08)

- **NOTÍCIA:** a HostGator confirmou que o domínio foi LIBERADO para
  gerenciamento. Próximos passos (ver guia_novo_dominio_missaocomdeus.md):
  1. Apontar DNS na HostGator: A `missaocomdeus.com.br` → 212.28.182.86 e
     A `www.missaocomdeus.com.br` → 212.28.182.86.
  2. Aguardar propagação (verificar em dnschecker.org).
  3. SSL Let's Encrypt no aaPanel (site missaocomdeus.com.br).
  4. Copiar os arquivos do site (site-contabo.zip) para
     /www/wwwroot/missaocomdeus.com.br/ e extrair.
  5. Nginx: try_files $uri $uri.html $uri/index.html =404.
  6. Decidir: redirect 301 de compraoseu.com → missaocomdeus.com.br
     (recomendado, preserva SEO) ou manter os dois.
  7. Atualizar sitemap.xml + adicionar propriedade no Google Search Console.
  8. Testar os 12 livros + enquete + e-book do quiz no novo domínio.
- **PR para o main:** PR #2 aberto (arena → main). Autor fará merge no fim
  do dia.

---

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

## 🎉 notificar.php NO AR E FUNCIONANDO (19/08) — controle total CONQUISTADO

- **E-mail da enquete chegou pelo NOSSO servidor:** remetente
  "Missão com Deus <no-reply@missaocomdeus.com.br>", com a mensagem do
  leitor e o "E-mail do leitor (para responder)" (ex.: lurdes.zenop@gmail.com).
- O fluxo completo está funcionando: voto/comentário → notificar.php
  (mail() via postfix) → e-mail no Gmail do autor, com SPF aprovado.
- **O quiz continua pelo FormSubmit** (form HTML) — opcional migrar depois.
- **CONTROLE TOTAL DOS E-MAILS: CONQUISTADO!** (postfix + SPF + notificar.php
  + PHP sendmail_path). Plano dos 3 passos concluído.

---

## 🏆 POSTFIX + SPF + E-MAIL OK (19/08) — envio próprio FUNCIONANDO

- **Postfix instalado** no servidor (myhostname/myorigin = missaocomdeus.com.br).
- **SPF adicionado na HostGator:** TXT `v=spf1 ip4:212.28.182.86 ~all`
  (autoriza o IP do servidor a enviar e-mails do domínio).
- **E-mail de teste CHEGOU ao Gmail** (status=sent no mail.log — Gmail aceitou).
- **PHP já configurado:** sendmail_path = /usr/sbin/sendmail -t -i (linha 1094
  do php.ini do PHP 8.1). PHP-FPM reiniciado.
- **notificar.php está pronto para funcionar** (envia votos/comentários via
  mail() do PHP, sem FormSubmit; fallback FormSubmit mantido).
- **PARA FINALIZAR:** subir o site-contabo.zip atualizado (notificar.php +
  index.html) nos dois domínios e testar um voto na enquete (e-mail deve vir
  de no-reply@missaocomdeus.com.br).

---

## 📧 notificar.php CRIADO (19/08) — e-mail 100% nosso

- **site-contabo/notificar.php criado:** endpoint que envia os e-mails dos
  votos/comentários direto pelo PHP (mail()), sem depender do FormSubmit.
- **Fluxo:** a enquete chama notificar.php PRIMEIRO (controle total); se o
  mail() do servidor falhar, usa FormSubmit como FALLBACK (código antigo).
- **Proteção:** 5s entre envios do mesmo IP (reusa enquete_ips.json).
- **PARA ATIVAR no servidor:** subir o zip novo (notificar.php + index.html
  atualizado) nos dois domínios; o mail() do PHP precisa estar habilitado no
  aaPanel (PHP.ini → mail function / SMTP). Se mail() falhar, continua
  caindo no FormSubmit (que está ativado e funcionando).
- Testado: JS válido, fallback preservado. zip regenerado.

---

## 🚀 SEO NOVO DOMÍNIO (18/08) — sitemap e robots atualizados

- **sitemap.xml** → https://missaocomdeus.com.br/ (13 URLs: Home + livro01-10 +
  livro12 + quiz). livro11 EXCLUÍDO (lançamento 27/08).
- **robots.txt** → aponta sitemap novo; bloqueia /quiz, /stats.html,
  /enquete.php.
- **Guia criado:** analise/migracao_contabo/guia_seo_novo_dominio.md (GSC:
  adicionar propriedade, enviar sitemap, solicitar indexação 1-2/dia,
  palavras-chave alvo).
- Pendente: autor adicionar a propriedade no GSC (tag HTML ou DNS) e enviar
  o sitemap; títulos das páginas ainda "Portal O Despertar" (ajustar depois).

---

## 🚫 LIVRO 11 (Novo Testamento) FORA DO AR até o lançamento (18/08)

- **Descoberta:** o arquivo site-contabo/livro11.html (contém "O Novo
  Testamento como nunca lido", o Livro 01 da Home com countdown até 27/08)
  estava acessível em /livro11, SEM proteção (versão do autor).
- **DECISÃO (com o autor): APAGAR o arquivo livro11.html dos DOIS domínios**
  (compraoseu.com e missaocomdeus.com.br) até o lançamento.
  - Não se perde nada: está salvo no GitHub.
  - No lançamento (27/08), subir a versão PROTEGIDA (após autor aprovar a
    leitura).
  - Card da Home continua "Em breve" sem link; sitemap NÃO lista /livro11
    (verificado) — Google não rastreia.
  - sw.js tem /livro11 no cache (inofensivo; arquivo não existe).
- **Card "Livro 11 · Disponível" da Home (A Sabedoria dos Mestres) é OUTRO
  livro (arquivo livro02.html) — permanece no ar normalmente.**

---

## 📊 STATS COM VISITAS REAIS (18/08, 2ª rodada)

- **gerar_estatisticas.py atualizado** para separar BOTS de visitas HUMANAS:
  - Filtra URLs de ataque (wp-login, .env, wp-admin, xmlrpc, 222.php,
    info.php, scanners...) e User-Agents de bots (python-requests, sqlmap,
    curl, Googlebot, etc.).
  - Novo painel mostra: Total geral (bruto) + **👥 Visitas REAIS (sem bots)**
    + **🤖 Bots/ataques bloqueados**, além de variação e projeção REAIS.
  - Testado com log simulado (30 reais + 40 bots → separou corretamente).
- **PARA ATIVAR no servidor:** subir o script novo para
  /home/deploy/gerar_estatisticas.py e rodar
  `python3 /home/deploy/gerar_estatisticas.py` (gera no compraoseu e copia
  para o missaocomdeus — espelhamento).
- Com isso o autor verá os números VERDADEIROS de irmãos (ex.: dos ~1600
  brutos, as visitas reais são ~600).

---

## 🏆 REDIRECT 301 CONFIRMADO (18/08) — site UNIFICADO

- **compraoseu.com e www.compraoseu.com → missaocomdeus.com.br (301)** com
  `(www\.)?compraoseu\.com` + `$request_uri` (preserva o caminho).
- **Confirmado ao vivo:** compraoseu.com/livro05 → missaocomdeus.com.br/livro05
  (abre a Evolução da Alma no novo domínio, links internos atualizados).
- **nginx -t:** syntax is ok (avisos "conflicting server name" inofensivos,
  do Certbot × aaPanel).
- **Próximo passo (combinado):** notificar.php (e-mail 100% nosso via PHP,
  sem FormSubmit) → depois GSC nova propriedade + sitemap do novo domínio.

---

## ✅ FORM SUBMIT ATIVADO (18/08) — e-mails funcionando

- **FormSubmit ATIVADO com sucesso** ("Form Activated") para
  https://missaocomdeus.com.br/ — os e-mails de votos/comentários do quiz e
  da enquete chegam normalmente em compraoseu.com@gmail.com.
- A ativação foi feita a partir do site missaocomdeus.com.br (por isso o
  "Form at: missaocomdeus.com.br").
- **PLANO FUTURO (em segundo plano, decidido com o autor):** criar um
  endpoint próprio `notificar.php` (e-mail via PHP no nosso servidor) para
  ficar 100% sob nosso controle, sem depender do FormSubmit. Fazer DEPOIS do
  redirect do domínio (prioridade: unificar o site primeiro).

---

## 🔁 REGRA DE ESPELHAMENTO (18/08) — IMPORTANTE

- **A partir de agora, TODA atualização do site deve ser aplicada nos DOIS
  domínios:** compraoseu.com e missaocomdeus.com.br (mesmos arquivos na
  pasta /www/wwwroot/<domínio>/).
- O **gerar_estatisticas.py** foi atualizado para gerar o stats.html no
  compraoseu.com E COPIAR para /www/wwwroot/missaocomdeus.com.br/stats.html
  (espelhamento automático ao rodar o comando).
- A **enquete** NÃO deve ser zerada (decisão do autor: preservar quem já
  respondeu). O arquivo enquete_dados.json no servidor está com a estrutura
  nova (ansiedade/magoas/medo/paz) e votos preservados (99 em 18/08).
- **Redirect 301** compraoseu.com → missaocomdeus.com.br: guia em
  analise/migracao_contabo/guia_redirect_novo_dominio.md (decisão do autor
  se aplica agora ou mantém os dois).

---

## 🐛 BUG DO E-MAIL DA ENQUETE CORRIGIDO (19/08) — FALLBACK HTTP

- **Problema:** o e-mail da enquete não chegava quando o voto era feito pelo
  site (só via curl no terminal).
- **Causa raiz (encontrada):** a função notificarEmail() tinha apenas
  `.catch()`. Quando o notificar.php retorna ERRO HTTP (500, ex.: mail()
  falhou), o fetch RESOLVE (não rejeita) — então o fallback do FormSubmit
  NUNCA disparava. Resultado: nenhum e-mail.
- **Correção:** adicionada verificação `.then(function(r){ if(!r.ok){
  fallback(); } })` — se o notificar.php responder erro HTTP OU houver erro
  de rede, o fallback do FormSubmit dispara. Aplicada nas duas Homes e no
  gerador. JS validado. zip regenerado.
- **Para aplicar:** subir o index.html atualizado nos dois domínios.

---

## 💾 BACKUP — GUIA CRIADO (19/08)

- **analise/migracao_contabo/guia_backup_completo.md criado** com todos os
  comandos de backup para salvar no notebook:
  - GitHub já é o backup principal (site-contabo.zip a cada atualização).
  - Backup do chatbot CONECTAÍ (em /home/deploy/conectai — NÃO está no GitHub
    nem no backup do painel!) — zip + baixar.
  - Backup dos configs nginx/php (pasta backup_configs).
  - Votos da enquete (enquete_dados.json) ficam no servidor (zip não inclui
    de propósito).
  - Rotina: semanal chatbot + configs; mensal repositório GitHub.

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
- **Acesso (atualizado 18/08):** ALÉM do hero, o Livro 12 agora tem CARD na
  biblioteca (depois do Livro 11, antes do card Apoio): selo "Livro 12 ·
  Disponível", capa https://i.ibb.co/6RRTBY06/livro12.jpg, badges "Mensagens
  diárias" e "🔒 Protegido", botões "Ler grátis" → /livro12 e "Portal" →
  https://pay.kiwify.com.br/iVfp2bi.
- **Capa do livro:** adicionada a imagem .capa-livro no topo da seção capa
  (padrão dos livros 04/05/09/10), com CSS .capa .capa-livro.
- **Decisão anterior do autor:** dar visibilidade antes de publicar na
  biblioteca — cumprida; agora está na biblioteca como o 12º livro.

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
