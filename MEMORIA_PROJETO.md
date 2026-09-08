# MEMÓRIA DO PROJETO — MISSÃO COM DEUS
## Atualizado em: 29/08/2026 (Brasília)
## Atualizado em: 07/09/2026 (Brasília)
## Site vivo: https://missaocomdeus.com.br
## Próximo chat: «Continuar a Missão com Deus. Site vivo missaocomdeus.com.br. Leia consultoria-redes/MEMORIA_PROJETO.md»

A Arca anda sobre as águas. O que está neste arquivo é o que está no ar. O GitHub (sidneyrma/instalador) está ATRÁS do servidor. Nunca trate o GitHub como verdade.

## ESTADO DA ARCA — 07/09/2026 (o que está no ar, na ordem)

- **Página `/nossa-missao` CRIADA E CONFIRMADA NO AR.** Texto aprovado, escrita humana, sem travessão. Selos bíblicos: **Salmo 119:105** e **Filipenses 1:6**. Botões no fim: **Voltar para a Home** e **Ir para a leitura gratuita**. Autor testou em aba anônima e está tudo visível.
- **Home confirmada na entrega final pelo terminal do servidor** (`curl`): `curl -s https://missaocomdeus.com.br/ | grep -c "Nossa Missão"` retornou **2** (menu + rodapé). Ou seja, a Home pública JÁ está com a versão nova, mesmo que um cache intermediário já tenha mostrado antiga antes.
- **Menu da Home** ganhou **`🕊️ Nossa Missão`**.
- **Rodapé da Home LIMPO:**
  - removido o link do YouTube (não expor videoaulas);
  - removidas repetições internas (Portal, Livros, Trilogia, FAQ);
  - copyright simplificado (sem repetir o domínio);
  - link **`Nossa Missão`** no rodapé;
  - **`Fale conosco`** apontando para `mailto:portalmissaocomdeus@gmail.com`.
- **Arquivo de aplicação:** `site-contabo/APLICAR_NOSSA_MISSAO.py`. Já embute a página nova (com Filipenses 1:6) e o rodapé com `mailto`. Idempotente, faz backup `.bak` por arquivo alterado.
- **Workspace local sincronizado** com o servidor: `nossa-missao.html` tem os 2 versículos; `index.html` local tem `mailto` no rodapé; 0 link YouTube.
- **NÃO mexer no sitemap.xml** (regra do autor: não reenviar sitemap novo; o Google descobre `/nossa-missao` pelos links do menu/rodapé).

## CACHE DA HOME (explicação e como resolver)

- Se a Home mostrar versão antiga (YouTube / sem menu Nossa Missão) mas a página `/nossa-missao` já abrir nova, **não é erro do script**: é cache (Cloudflare / aaPanel / navegador). O arquivo no servidor já está certo.
- **Como limpar:**
  1. No **Cloudflare** (se existir): cache > **Purge Everything** / **Limpar Cache**. Se preferir só a Home, pode purgar `https://missaocomdeus.com.br/`.
  2. No **aaPanel**: conferir se existe cache do site (Nginx cache, cache de página) e limpar. Também pode reiniciar Nginx depois da limpeza.
  3. No navegador: janela **anônima + Ctrl+F5** (ou Ctrl+Shift+R). Repetir em alguns minutos se necessário.
  4. Comprovar pelo terminal (sem depender do navegador):
     ```bash
     curl -sI https://missaocomdeus.com.br/ | grep -i "cf-cache-status\|cache-control"
     curl -s https://missaocomdeus.com.br/ | grep -c "Nossa Missão"
     ```
     - O retorno de `grep -c "Nossa Missão"` deve ser **≥ 1**.
     - Se ainda for 0, a entrega da vitrine (cache) ainda não atualizou; repetir purgar cache.
- **Importante:** o `mailto:` local pode virar `/cdn-cgi/l/email-protection...` na entrega. Isso é a **Obfuscação de e-mail do Cloudflare**, não é bug. O destinatário continua `portalmissaocomdeus@gmail.com`.

## IDENTIDADE ÚNICA — MISSÃO COM DEUS (03/09/2026)

- A casa passa a ter UMA marca publica e de busca: **Missão com Deus**.
- Fora do ar: `Portal O Despertar`, `Portal O <b>Despertar</b>`, `Leitor do Despertar`.
- "Coleção do Despertar" vira **"Coleção Missão com Deus"** nos livros, capas e créditos.
- PWA: manifest `name`/`short_name`/`id` e sw `CACHE` ajustados.
- Aplicar no servidor com `APLICAR_IDENTIDADE_MISSAO.py` (backup em `.bak`).
- Não apagar/alterar `enquete_dados.json`, `enquete_ips.json`, `leituras.json`.
- Conteúdo/inspiração que usa "despertar" como tema (ex.: "O Despertar da Alma", "despertar a fé") permanece normal. Só a MARCA muda.
- Restos ainda possíveis no ar: "Liberar Módulos 5, 6 e 7" em Trilogia/Anestesia e banner Home "código grátis à Laura". O script também corrige.
- Importante: os livros 05 e 09 mostravam "Aula grátis" no **Módulo 04** (travado). Corrigido no espelho e no script para **Módulo 03** (livre). Nao reabrir o Módulo 04 como aula grátis.
- `APLICAR_IDENTIDADE_MISSAO.py` aplica marca + correcoes de confianca + modulo 03 nos livros 05/09.

## CONFIRMAÇÕES DO AUTOR — 03/09/2026

- **Identidade já aplicada no servidor** (autor confirmou): Home no ar já com **Missão com Deus** e sem a marca antiga. Conferido também por fetch em 03/09.
- **Rastreio do banner confirmado no ar:** autor testou o banner da Home e o painel mostrou **`🕊️ Falar com a Laura (banner da Home): 1`**. Ou seja, o clique caiu no lugar certo.
- **`ATUALIZAR_STATS_SIMPLES.py` RODOU NO SERVIDOR**: `Trocas aplicadas: 8 de 8`, gerou `stats.html` novo. Confirmado no /stats em 03/09.
- **Backup do site já ativo:** autor confirmou que roda backup diário programado às **03:30**. Tranquilo para qualquer ajuste futuro.
- **Foco combinado:** parar de mexer no servidor sem necessidade; usar o **Gerenciador de Arquivos do aaPanel** (upload) em vez de copiar/colar; GitHub fica como espelho/segurança, não como caminho do dia a dia.
- **`gerar_estatisticas.py` ajustado**: Colaborador R$ 19,90 saiu do ar e **não conta mais como sustento**. Sustento agora é só o acesso completo R$ 37 (`/q-semeador`). **JÁ APLICADO no servidor**.
- `/palavra` é só o caderno do autor para ver os temas e acompanhar. Não é página pública. Só quem souber o endereço acessa, igual `/stats` e `enquete.php`. Todos com `noindex, nofollow` e **fora do sitemap**. Não colocar link no menu nem no footer. Não indexar.
- Os PDFs antigos que eram referência no log **não existem mais no aaPanel**. A única referência boa do Bônus 1 é **`/ebooks/livro11-o-n-t.pdf`** (é esse que está no ar na página de obrigado).
- PDFs que existem hoje no aaPanel na pasta do site (conferido pelo autor em 03/09):
  - `Anestesia-mental-evalma.pdf`
  - `Evolucao-da-alma-evalma.pdf`
  - `jesus-quer-falar-com-seu-filho.pdf`
  - `jesus-quer-falar.pdf`
  - `livro05-evalma.pdf`
  - `livro07-ocdespertar.pdf`
  - `livro09-amental.pdf`
  - `livro11-o-n-t.pdf`
  - `livro12-a-d-o.pdf`
  - `Um-Segundo-com-Deus-Vol-01.pdf`
- **Mural eliminado.** Não existe mais projeto de mural, nem privilégio de "Colaborador(a)" (era o único privilégio do Semeador no plano antigo em que todos recebiam todos os livros). Não recriar. Não voltar com "área do semeador/colaborador" nem com mural.
- `PROMPT_LAURA_V11_CASA.txt` **já foi colado no FlowOpenAi (chatbox)**. Não precisa mais ficar na lista de pendência do prompt.
- Redes: Instagram e Facebook atuais foram banidos mais de uma vez, inclusive a página de campanha. Hoje **não há conta de Instagram ativa**. O autor vai usar outro aparelho/notebook com outro e-mail para não tomar banimento; não quer comprar/usar outro número. Não depender de IG/FB para o que sustenta a Missão até isso estar estabilizado.
- **Sessão GitHub encerrada após o merge/fechamento da PR #7.** O trabalho local continua no workspace, mas `git push`/`gh` desta sessão não está mais disponível. Para sincronizar um novo commit, usar uma nova sessão do Arena.
- Checkout oficial em uso (guardar como referência): **`https://pay.kiwify.com.br/iVfp2bi`** — "🕊️ MISSÃO COM DEUS | ACESSO IMEDIATO E VITALÍCIO À ÁREA DE MEMBROS DE ALUNOS", R$ 37,00 pagamento único, cartão em até 4x e Pix, garantia de 7 dias. Contempla Evolução da Alma + Anestesia Mental (livros digitais completos + 7 módulos em vídeo de cada) + acesso vitalício à área de membros + 4 bônus (NT, Devocional 30 dias, Jesus Quer Falar com Seu Filho e Afirmações em PDF).

## PROBLEMA COM O ATUALIZAR_STATS NO SERVIDOR (03/09/2026)

- O autor salvou `ATUALIZAR_STATS_V2.py` mas o arquivo acabou com conteúdo HTML do site (por isso `SyntaxError: invalid character '·'`). Também o nome ficou com marcação de link (`ATUALIZAR_STATS_[V2.py](http://V2.py)`).
- Para evitar isso foi criado **`ATUALIZAR_STATS_AGORA.py`**: script menor, com verificação no início, que só troca os trechos do painel, faz backup e já roda `gerar_estatisticas.py`.
- **Regra para o autor:** salvar com nome exato `ATUALIZAR_STATS_AGORA.py`, sem colchetes/parênteses/.txt; a primeira linha do arquivo deve ser `# -*- coding: utf-8 -*-`.
- Antes de rodar, conferir com: `head -1 /home/deploy/ATUALIZAR_STATS_AGORA.py`.
- Arquivo de referência: `site-contabo/ATUALIZAR_STATS_AGORA.py`. Pacote: `AAAPANEL_STATS_AGORA.zip`.
- Se o autor preferir não usar o arquivo do site, a alternativa segura é subir o `gerar_estatisticas.py` completo para `/home/deploy/` pelo Gerenciador de Arquivos do aaPanel (Upload), sem copiar/colar.

## RASTREIO DO BANNER (03/09/2026, correção)

- **Causa do teste não aparecer:** o banner da Home (CTAs de cursos) abria o WhatsApp e era contado como `/q-whats` ("Cliques no WhatsApp"). A linha `/q-codigo` ("Solicitar Código") só era contada nas páginas de área de alunos. Por isso um clique no banner da Home não aparecia na linha que o autor esperava.
- **Correção aplicada no espelho `index.html` e no servidor:**
  - Link do banner "Falar com a Laura sobre o acesso" agora dispara **`/q-laura`**.
  - Qualquer outro WhatsApp da Home continua em **`/q-whats`**.
  - **`APLICAR_RASTREIO_LAURA.py` rodou no servidor**: `Backup criado index-antes-rastreio-20260903-203031.bak`, `Trecho de rastreio trocado com sucesso`, `Pixels criados: q-laura`.
  - **Teste do autor confirmado no /stats:** `🕊️ Falar com a Laura (banner da Home): 1`.
- **Correção no `gerar_estatisticas.py` (aplicada no servidor):**
  - Nova linha na conversão: **`/q-laura`** = "Falar com a Laura (banner da Home)".
  - Nova linha: **`/q-livro-share`** = "Livros compartilhados".
  - `/q-codigo` foi renomeado para refletir a realidade: **"Fale com a Laura (área de alunos)"** (não é mais "Solicitar Código").
  - `/q-colaborador` e `/q-aula-gratis` **saíram do painel**: continuam ignorados, não contam mais.
  - No /stats ao vivo aparece: Acesso completo R$ 37 · Fale com a Laura (área de alunos) · Falar com a Laura (banner da Home) · Cliques no WhatsApp · Palavra · Livros compartilhados. **Colaborador ausente.**
- **Comando que resolveu: `ATUALIZAR_STATS_SIMPLES.py`** faz backup e troca só os trechos do painel, depois já roda `gerar_estatisticas.py`. Resposta no servidor: `Trocas aplicadas: 8 de 8`.

## LEITURA DA CASA — 03/09/2026 (números reais do /stats)

- **Hoje (03/09), até a geração do painel:** 109 pessoas · 134 visitas · 411 páginas de gente. É dia pela metade/fim de dia, então não comparar com o dia completo de ontem.
- **Ontem (02/09):** 196 pessoas · 239 visitas · 497 páginas.
- **Casa viva:** hoje ~3,8 páginas por pessoa (411/109). Acima de 3 = pessoa lê, não só passa. Esse é o sinal mais importante para o nosso cenário (espiritualidade, não religião).
- **Origem hoje:** Google/SEO 23 · site antigo 29 · direto 74 · redes 0. A busca orgânica hoje (23) ficou acima de ontem (11). Ainda é minoria, mas cresceu.
- **Sustento:** 26 cliques no acesso completo R$ 37 no total; 4 hoje. Taxa geral 1,9% sobre pessoas. Hoje a proporção ficou maior porque o dia ainda não fechou.
- **Downloads:** Bônus 1 (NT) 2 hoje · Bônus 4 (Afirmações) 2 hoje · Devocional 1 hoje · Jesus 1 hoje.
- **Conversão hoje vs dia anterior:** não confundir clique com compra. Compra real só a Kiwify mostra.
- **Leitura honesta para o nicho:** mais de 70% das visitas ainda são "direto" (link colado, WhatsApp, favorito, app) e o site antigo continua trazendo gente. SEO ainda é pequeno. Isso é normal no começo; a marca única e o sitemap novo são o caminho para o Google entender a casa.

## PALAVRA DO DIA — PÁGINA DE CONTROLE + SHARE DE ÁUDIO (05/09/2026)

- **`site-contabo/palavra.html`** (página de controle /palavra): lista agora até o **dia 60**, com os títulos/versículos das novas mensagens 31–60.
- Cada dia mantém o ícone de som. Os dias **31 a 60** usam **placeholder** no código: `var AUDIOS = { "31":"[cole aqui o link do audio 31]", ... }`. Quando o áudio estiver pronto no terminal, trocar o texto entre aspas pelo caminho real, ex.: `"/audio/palavra-dia-31.mp3"` ou `"https://..."`.
- Ao tocar num dia sem link, aparece: `🔧 Áudio em breve — cole o link no código (dia NN)`.
- **Home (`index.html`):** lista de referências (`refs`) estendida até o dia 60; removido o `if(day===31) day=30;` (agora dia 31 usa a mensagem 31).
- **Compartilhamento (Home):** o botão `Compartilha com quem você ama` agora tenta **compartilhar o MP3** no celular (Web Share com arquivo). O áudio já carrega a marca "Missão com Deus". A mensagem anexada inclui o texto e o link. Se o navegador/app não suportar compartilhar arquivo, cai no comportamento antigo (compartilhar/copiar o link + mensagem).
- **Novo botão opcional:** após ouvir, também aparece **`📥 Baixar áudio`** ao lado do botão Compartilha. Aponta para `/audio/palavra-dia-NN.mp3` com `download`; cobre iPhone/notebook/desktop, onde o compartilhamento nativo de arquivo pode não estar disponível. Assim o irmão pode guardar/repassar o MP3 (que já tem a marca e o convite ao site) mesmo quando o app não abre a folha de compartilhamento direto.
- **Limitação honesta:** compartilhar arquivo funciona melhor no Android Chrome. No iPhone/desktop, o navegador pode não apresentar o áudio — por isso os dois caminhos: Compartilhar (tenta áudio, cai no link) e Baixar áudio (para repassar manualmente).
- **Fluxo atual no fim do áudio:** botão `Compartilha com quem você ama` + `📥 Baixar áudio`.

## PALAVRA DO DIA — CICLO COMPLETO 1 A 60 (04/09/2026)

- **04–30:** arquivo `PALAVRA_AGENDA_04_30.md` (27 mensagens, fonte original; sem oração no final, desfecho "Fiquem na paz do Senhor!").
- **31–60 (novo):** arquivo `PALAVRA_AGENDA_31_60.md` com **30 mensagens novas** para fechar exatamente 60. Mantém a mesma toada teológica e vai mais fundo: pastor (23), obra aperfeiçoada (Fp 1:6), águas (Is 43:2), graça na fraqueza (2Co 12:9), pedir/buscar/bater (Mt 7:7), deleite (Sl 37:4), permanecer (Jo 15:5), mente (Fp 4:8), lágrimas (Sl 56:8), comunidade (Mt 18:20), amor (1Co 13), mente (Rm 12:2), sede (Sl 42:1), nova criatura (2Co 5:17), alegria de manhã (Sl 30:5), não temas (Is 41:10), trabalho (Cl 3:23), alegria na presença (Sl 16:11), torre forte (Pv 18:10), caniço rachado (Mt 12:20), paz (Jo 14:27), coração puro (Sl 51:10), confissão (1Jo 1:9), prosseguir (Fp 3:13-14), viva esperança (1Pe 1:3), justiça/misericórdia (Mq 6:8), pacificadores (Mt 5:9), dias (Sl 90:12), alegria/oração/gratidão (1Ts 5:16-18), lugar preparado (Jo 14:2-3).
- **Formato novo das 31–60:** após o convite ao site, cada mensagem tem **"Vamos orar. Pai, em nome de Jesus, te pedimos..." (oração curta de bênção conforme o tema)** e fecha com **"Fiquem na paz de Cristo nosso Senhor e Salvador, e tenham todos um dia abençoado!"**.
- **Arquivos .txt prontos por dia:** `site-contabo/palavras_31_60/palavra-dia-31.txt` … `palavra-dia-60.txt` (300–340 palavras, ~2 min) para gerar direto no `edge-tts`.
- **Como aplicar:** gerar no `/root/tts` (venv ativo): `edge-tts --file palavra-dia-31.txt --voice pt-BR-FranciscaNeural --write-media palavra-dia-31.mp3` e `cp` para `/www/wwwroot/missaocomdeus.com.br/audio/`. Alternar com `pt-BR-AntonioNeural` nos dias ímpares/pares.

## PAIS E FILHOS — CTA + RODAPÉ + MENU (04/09/2026)

- **Página `guia-pais-filhos.html`:** adicionado um CTA **"📝 Responder o Quiz"** logo abaixo do topo, com botão para `https://missaocomdeus.com.br/#enquete`. A ideia: quem chega pelo link convidado pode ir direto à enquete da Home (o quiz já está acima).
- **Rodapé do guia:** `Missão com Deus · missaocomdeus.com.br · Compartilhe com amor` virou link (o "missaocomdeus.com.br" e o "Compartilhe com amor" são links para a Home).
- **Menu da Home (`index.html`):** adicionado `👨‍👩‍👧 Pais e Filhos` apontando para `/guia-pais-filhos`. Texto curto (sem "(Conversas que Protegem)") para não quebrar/quebrar o menu no celular.
- **Script:** `site-contabo/APLICAR_PAIS_FILHOS_QUIZ.py` — backup dos 2 arquivos, aplica CSS/CTA/rodapé no guia e item no menu da Home; idempotente (segunda execução: "CSS ja presente / CTA ja presente / Menu ja presente").
- **Teste:** aplicado em cópia com estado antigo (guia sem CTA/rodapé link, index sem menu) e rodado de novo sem duplicar. `HTML_PARSER_OK`.
- **Observação de UX:** o autor pediu opinião sobre colocar "Pais e Filhos: (Conversas que Protegem)" no menu; recomendei o título curto **"👨‍👩‍👧 Pais e Filhos"** no menu (o parentesítico fica só na página / título interno), para não ficar longo.

## GA4 — DOMÍNIO ANTIGO (04/09/2026)

- **Já existe:** conta Analytics `365993734` com a propriedade `502120214` para `compraoseu.com`.
- **Recomendação:** NÃO excluir a antiga. Ela não atrapalha a `missaocomdeus.com.br`; é só o histórico do domínio antigo.
- **Criar uma NOVA propriedade GA4 para `missaocomdeus.com.br`** (pode ser na MESMA conta 365993734, ou em conta nova). O ideal é uma propriedade nova com o Data Stream do domínio novo, para não misturar métricas dos dois domínios.
- O `compraoseu.com` redireciona 301 para a Missão; a medição de quem chega lá já está no log/site novo. A GA4 antiga pode ficar guardada/dormindo sem problema.

## GOOGLE ADS + GA4 — ORIENTAÇÃO JÁ EXPLICADA AO AUTOR (04/09/2026)

- **DUAS coisas diferentes:**
  - Medir conversão (GA4 + Google Ads): só configuração/pixel, NÃO precisa vídeo/imagem/carrossel/copy.
  - Rodar campanha paga: precisa de copy (texto) + palavras-chave + orçamento; para **Search** NÃO precisa imagem/vídeo; para **Display/Performance Max** precisa imagem (e vídeo no PMax/Demand Gen).
- **Para começar:** campanha **Search (Busca)** com Responsive Search Ads (títulos + descrições), sem vídeo/imagem.
- **NÃO é "só domínio + palavra-chave"**: precisa conta Google Ads, campanha Busca, grupo de anúncios, palavras-chave, copy curta, orçamento e conversão na Kiwify.
- **Ordem:** 1) GA4 no site 2) criar campo de conversão no Google Ads 3) colar Pixels de Conversão na Kiwify (Compra R$ 37) 4) campanha de Busca com palavras-chave + copy + orçamento pequeno 5) avaliar 1 a 2 semanas 6) só depois Performance Max/Display.
- **Guia criado:** `GOOGLE_ADS_GA4_GUIA.md` (com exemplos de palavras-chave, títulos e descrições de anúncio).

## SITEMAP — /guia-pais-filhos INDEXÁVEL (04/09/2026)

- **O link `/guia-pais-filhos` já estava no sitemap no servidor** (verificado no ar 04/09). Não foi adicionado por mim. O Google recusou a indexação apenas porque a página tinha `noindex, nofollow`; o sitemap pedia indexar, a página pedia não indexar, e o Google obedeceu a página.
- **Decisão final:** manter `/guia-pais-filhos` **no sitemap (9 URLs)** e trocar a etiqueta da página para `index, follow`. A página fica indexável, porém **sem link público** (é acessada pelo link do e-mail do quiz Pai e Filhos).
- **Arquivo alterado:** `site-contabo/guia-pais-filhos.html` linha do `robots` agora `index, follow`.
- **Script:** `site-contabo/APLICAR_INDEXAR_GUIA.py` — backup do guia + troca segura `noindex, nofollow` → `index, follow`. Testado: backup criado, troca aplicada, segunda execução "Ja estava index, follow. Nada duplicado.", HTML ok.
- **Sitemap do workspace:** mantido com **9 URLs** (voltou a incluir `/guia-pais-filhos`). O script anterior `ATUALIZAR_SITEMAP_8.py` foi **removido** (não usar; o sitemap não precisa sair com guia).
- **Remoções já feitas pelo autor em 02/09/2026:** `/livro01`, `02`, `03`, `08`, `10` e `/ebooks/livro01-03-08-10-evalma.pdf` → "Temporariamente removido". **Não refazer.**
- **Indexação:** 9 URLs, uma por uma (Inspecionar URL → Solicitar indexação). Não existe botão de indexar todas de uma vez no GSC.
- **Ficam noindex de propósito:** `/palavra`, `/stats`, `enquete.php` (não indexar).

## NOVA ORDEM DO PAINEL /STATS (06/09/2026)

- **Objetivo:** dar mais visão ao stats, deixando os números que importam abertos e o que é "explicação" em abas (como os FAQs).
- **Nova ordem confirmada pelo autor:**
  1. **O que olhar sempre** (aberto)
  2. **Hoje e ontem** (aberto)
  3. **Páginas vistas por gente** (aberto)
  4. **🎯 Conversão (o que move a missão)** — agora **ABERTO** (subiu), cards + tabela de ações
  5. **De onde vêm / Origem da visita** (aberto)
  6. **📊 Indicador · O que é · O que observar** — agora **aba fechada** (abre com clique)
  7. **Detalhes** (restante, nas abas como antes)
- **Arquivo:** `site-contabo/ATUALIZAR_STATS_ORDEM.py` — modifica `/home/deploy/gerar_estatisticas.py`, faz backup `.bak-AAAAMMDD-HHMMSS`, reordena o template, e já roda o gerador para atualizar o `stats.html`. Idempotente (segunda execução: "Ja estava aplicado. Nada duplicado.").
- **Teste:** usado o **original exato do aaPanel** fornecido pelo autor (`gerar_estatisticas_origem_servidor.py`), depois rodado num log de teste. Resultado: `HTML_PARSER_OK`, ordem das seções correta, backup criado, sem duplicar.
- **OBS:** não mexe em números nem em leitura de log; só reordena o template HTML do gerador.
- **Como aplicar (aaPanel):** salvar `ATUALIZAR_STATS_ORDEM.py` em `/home/deploy/` e rodar `python3 ATUALIZAR_STATS_ORDEM.py`; conferir `https://missaocomdeus.com.br/stats`.

## REVERSO DO PROTEGER_PDFS.PY (04/09/2026)

- **Arquivo:** `site-contabo/DESPROTEGER_PDFS.py` (reverso testado do `PROTEGER_PDFS.py`).
- **O que faz:** abre cada PDF travado com a senha de dono `MissaoComDeus2026`, guarda uma cópia `NOME.pdf.protegido.bak` (apenas no primeiro revert) e reescreve o PDF **sem senha** e **sem proteção** (copiar/colar e imprimir liberados).
- **Teste real:** protegeu um PDF com a mesma lógica do autor (`permissions_flag=0`, AES-256), confirmou `is_encrypted=True`, rodou o reverso → `is_encrypted=False`, página intacta; segunda execução → `ABERTO`, sem nova alteração.
- **Segurança:** não mexe em PDF já aberto; não mexe em PDF cuja senha de dono não abra; salva em `.tmp` e só então substitui.
- Dependência igual ao PROTEGER: `pip3 install pypdf` (chamar `cryptography` também se AES-256 falhar no ambiente do aaPanel).
- Instalação de teste no sandbox: `pip3 install --break-system-packages pypdf cryptography`.

## BOTÃO "BAIXAR APP" NA PRIMEIRA DOBRA (04/09/2026)

- **Decisão de UX:** usar **"📲 Baixar App"** (curto) dentro do selo hero `✨ Leia de graça, continue de onde parou`. Não usar "Baixar App leitura grátis" (grande e desnecessário; a leitura grátis já está no texto acima).
- **Posição:** primeiro impacto da Home, no card sobre a imagem hero (`hero-badge`), logo abaixo do texto "Leia de graça, continue de onde parou".
- **Implementação no `index.html`:**
  - Novo botão `#instalar-app-hero` com classe `.hero-app-btn` (dourado, discreto).
  - CSS: `.hero-badge` agora em coluna com gap 9px; novo `.hero-app-btn`.
  - JS: ligado à função já existente `tentarInstalar()`; some se o app já estiver instalado; usa `beforeinstallprompt` (Android/Chrome) e orienta no iPhone/desktop.
- **Não substituir `index.html` inteiro.** Usar script `APLICAR_APP_HERO.py` (backup `.bak`, idempotente). Testado no estado antigo: CSS, HTML e JS aplicados; segunda execução "Botao ja aplicado, sem duplicar"; HTML parser OK.
- **Observação:** o botão flutuante `#instalar-app` continua existindo junto; são dois pontos de instalação (herói + canto), o que está alinhado com o pedido de mais visibilidade.

## VITRINE "NOSSAS OBRAS" — O CAMINHO DO DESPERTAR (04/09/2026)

- **Capa do Novo Testamento corrigida:** `i.ibb.co/9myJ3XXb/livro01.jpg` → `i.ibb.co/sJWVKDqB/livro11.jpg` (o nome do arquivo agora corresponde ao livro11; a imagem antiga livro01.jpg era do livro08 e não fazia referência certa).
- **Capa do Caminho do Despertar corrigida:** `i.ibb.co/Gf7WWL6H/livro08.jpg` → `i.ibb.co/YF5sWbp7/livro07.jpg` (o livro07 usa o arquivo livro07.jpg, não livro08.jpg).
- **Livro 07 adicionado à vitrine "Nossas Obras"**, antes do card Jesus Quer Falar com Seu Filho (que continua último), com descrição no mesmo padrão dos demais:
  - Título: O Caminho do Despertar
  - Descrição: "Uma jornada de fé e autoconhecimento: 12 capítulos que revelam a sabedoria dos ensinamentos de Jesus e conduzem a alma a um encontro mais profundo com Deus."
  - Itens: 12 capítulos em leitura limpa · Sabedoria dos ensinamentos de Jesus · Reflexão sobre fé, propósito e alma · Leitura gratuita no portal.
- **Aplicação segura:** script `APLICAR_VITRINE_LIVRO07.py` (backup `.bak`, trocas simples, não duplica o card). Testado em cópia com estado antigo: `capa NT 2 trocas · capa Caminho 1 troca · card Livro 07 inserido`.
- **Não substituir `index.html` inteiro no servidor.** Usar o script ou upload do Gerenciador de Arquivos se houver.

## PALAVRA DE HOJE — NOVA METODOLOGIA E AGENDA 04 A 30 (03/09/2026)

- O autor sentiu os áudios atuais "vazios, sem unção, sem força e autoridade". Decidiu substituir, um por dia, mantendo o ciclo automático de 00:00 (fuso Brasília) na Home e em `/palavra`.
- **Novo padrão aprovado pelo autor (03/09):**
  - Abertura: **"A paz de Cristo seja com todos, meus irmãos e minhas irmãs!"** (o autor escreveu "sejam"; acertei para "seja" por concordância com "a paz", que é singular. Mantém a força e soa mais firme).
  - Corpo: versículo + "Sabe..." + aplicação prática para a vida real + bênção.
  - Compartilhamento: "Se essa mensagem abençoou a sua vida, compartilha esse áudio com quem você ama..."
  - Convite final: **"E para começar todos os seus dias fortalecido na fé, venha ouvir uma nova palavra de esperança diariamente no nosso site: missaocomdeus.com.br"**.
  - Fecho: **"Fiquem na paz do Senhor!"**.
- **Arquivo criado:** `PALAVRA_AGENDA_04_30.md` com os textos prontos dos dias **04 a 30** (Filipenses 4:6-7 até Números 6:24), todos no novo padrão, **27 dias**. O convite ao site foi inserido nos 27 fechamentos.
- Os arquivos de áudio continuam sendo `/audio/palavra-dia-01.mp3` … `palavra-dia-30.mp3`. O site já troca sozinho à meia-noite; não precisa mudar código da Home.
- **Avaliação honesta:** a nova fórmula está pronta e com bons ritmo/unção. Os únicos refinos que fiz foram a concordância "seja" e manter "Fiquem na paz do Senhor!" como fecho depois do convite, para não terminar a gravação no link. A partir daqui é só gravar e escutar.
- **Ferramenta de voz (autora buscou gratuita para clonar a voice da Laura e gerar 1:00+):**
  - Quasar Voice (`https://qwen3-tts.ai`) é uma opção online gratuita de clonagem e TTS (Qwen3-TTS), com clonagem a partir de 3 a 10 segundos, controles de emoção e narração longa; pede conta/sign in. **Atenção:** o plano gratuito geralmente tem limite mensal de caracteres (aprox. 10k), então para 27 áudios de ~1:50 convém gerar um por dia e acompanhar o limite. Verificar no site antes de adotar.
  - Alternativas locais gratuitas e sem limite de caracteres: OmniVoice Studio e Voicebox (rodam no computador, sem conta/API; exigem instalação, chance menor de o autor conseguir sozinho).
  - Se o limite dificultar, o autor pode usar a voz masculina que já usou hoje, ou contratar um plano pequeno da ferramenta que mais gostar.
- **Não tentar usar site que não esteja mais funcionando. Não depender de outro número/celular para a voz.**

## GOOGLE SEARCH CONSOLE E SITEMAP (estado em 03/09/2026)

- Sitemap enviado: **`https://missaocomdeus.com.br/sitemap.xml`**.
- No painel aparece **Sucesso**, última leitura **02/09/2026**, **9 páginas** enviadas, **90 páginas descobertas**.
- As 9 páginas do `sitemap.xml` são: `/`, `/livro04`, `/livro05`, `/livro06`, `/livro07`, `/livro09`, `/livro11`, `/livro12`, `/guia-pais-filhos`.
- `/palavra`, `/stats` e `enquete.php` **não estão** no sitemap e têm `noindex, nofollow`. Mantê-los assim.
- Depois que `APLICAR_IDENTIDADE_MISSAO.py` rodar no servidor: submeter o sitemap de novo, usar **Inspecionar URL** nas 9 páginas para pedir indexação, e usar **Remoções** só para URLs antigas que realmente saíram (ex.: `/livro01` … `/livro12` antigos, páginas-ponte antigas, etc.).
- Não remover do índice sem necessidade. Para páginas que sumiram de verdade, o Google entende 404/301 sozinho; a remoção manual é só quando for urgente.

## ATUALIZAÇÃO URGENTE — 03/09/2026 (consultoria)

- Bônus 1 e 4 no ar: **`/ebooks/livro11-o-n-t.pdf`** (NT) e **`/ebooks/livro12-a-d-o.pdf`** (Afirmações). O nome antigo `livro11-onovotestamenento.pdf` **retorna 404**. Não usar.
- Bônus 4 (Afirmações) no obrigado: **`/ebooks/livro12-a-d-o.pdf`** (existe e está no ar).
- Home / FAQ e oferta ajustadas no espelho para **4 bônus**: NT, Devocional 30 dias, Jesus e Afirmações em PDF. Módulos 1 a 3 grátis.
- Banner fixo da Home NÃO deve mais prometer "código de acesso grátis à Laura" nem pedir "código grátis". O convite certo é sobre o acesso completo.
- Caixa de código das pontes: dizer **"Liberar os módulos restantes (4 a 7)"**, não "Liberar Módulos 5, 6 e 7".
- O `gerar_estatisticas.py` do GitHub já foi sincronizado com o do servidor (v4/v6, inclui Origem e Termômetro). Se aparecer diferença, conferir no `/home/deploy/` antes de substituir. Não subir a versão v3 antiga em cima do v6.

## INFRA

- VPS Contabo `212.28.182.86` Ubuntu 22.04.5, Nginx, PHP 8.1.32, aaPanel, ~15 GB RAM.
- Produtos Kiwify antigos ainda Ativos (não usar na Home): Devocional R$ 9,90; Anestesia avulsa; Evolução avulsa.
- Página de obrigado da casa: `https://missaocomdeus.com.br/obrigado`
  Colar na Kiwify em **Cartão ou Pix aprovado** (iVfp2bi e NCAEVtO). Boleto/pix gerado = página padrão Kiwify.
- Presente no obrigado = **Baixar PDF** `/ebooks/livro11-onovotestamenento.pdf` (typo no nome, proposital).
- Presente no obrigado = **Baixar PDF** `/ebooks/livro11-o-n-t.pdf` (confirmado no ar em 03/09. O nome antigo `livro11-onovotestamenento.pdf` retorna 404 e nao deve ser usado).
  Não é link `/livro11` (isso já é grátis).
- Não listar o NT como leitura exclusiva. Dois cursos no pacote R$ 37.

- Botão dourado: Começar o Devocional de 30 dias → `/livro04`
- Botão quieto: Ler as Afirmações → `/livro12`
- Arte: `https://i.ibb.co/zhH6FV9X/hero.jpg` · CSS `--navy` `#0e1a2e`
- Título oferta: Seja um Semeador da Missão e ganhe um Brinde Extra
- Brinde extra na lista: PDF O Novo Testamento como nunca lido (para guardar)
- Título oferta: Seja um Semeador da Missão e ganhe 4 bônus
- 4 bônus no acesso completo: NT, Devocional 30 dias, Jesus e Afirmações em PDF
- FAQ: «O que eu recebo no acesso completo?» · «Isso é doação?» (não)
- Banner `#cta-cursos`: ~45% scroll / mouseleave; `VALIDADE_HORAS = 6`; só Trilogia na Home
- Seção `#missao`: fé e a mente; Laura não é carne; Mt 18:20
- Motivo: 4 livres é mais da metade (filha de 13 anos). Autor concordou 3.
- Texto: isto é prévia; área de membros Kiwify tem explicações e exercícios.
- Um botão: **Quero o acesso completo — R$ 37,00** → iVfp2bi
- Linha dourada visível: brinde extra PDF NT
- Linha dourada visível: 4 bônus (NT, Devocional, Jesus e Afirmações)
- Modal: um preço. «Já tenho código de acesso»
- Mural vazio `display:none`. `/mural.html` no servidor, noindex, **sem link**
- Caixa de código: «Liberar os módulos restantes (4 a 7)». Não usar «Liberar Módulos 5, 6 e 7».
- Mural **eliminado**. Não existe mais funcionalidade pública de mural; não recriar, não colocar link.
- Plays: `tocarVideo` faz `fetch('/q-trilogia-m0N')` ou `/q-anestesia-m0N`
- Anestesia WhatsApp → `/q-codigo`; Kiwify → `/q-semeador`


## PDF / ebooks/

- **Fonte de verdade:** conferir a lista real do aaPanel no topo (03/09/2026). `livro11-onovotestamenento.pdf` **não existe** e nunca deve ser usado.
- Proteção pypdf (`permissions_flag`). Script `PROTEGER_PDFS.py`
- **LIVRES (sem evalma, quiz):** `Um-Segundo-com-Deus-Vol-01.pdf` · `jesus-quer-falar.pdf`
- **Com evalma (chute difícil):** `Anestesia-mental-evalma.pdf` · `Evolucao-da-alma-evalma.pdf`
- **Brinde NT (typo proposital, sem evalma):** `livro11-onovotestamenento.pdf`
- **LIVRES (sem evalma, quiz):** `Um-Segundo-com-Deus-Vol-01.pdf` · `jesus-quer-falar.pdf` · `jesus-quer-falar-com-seu-filho.pdf`
- **Com evalma (chute difícil):** `Anestesia-mental-evalma.pdf` · `Evolucao-da-alma-evalma.pdf` · `livro05-evalma.pdf` · `livro07-ocdespertar.pdf` · `livro09-amental.pdf` · `livro12-a-d-o.pdf`
- **Bônus 1 (nome real no ar):** `livro11-o-n-t.pdf`
- Dois «Jesus Quer Falar» no log antigo = dois arquivos (quiz curto × nome longo do livro). Não é duplicata.

---
- Script vivo do cron: `/home/deploy/gerar_estatisticas.py`
- Cópia nova (29/08) em `consultoria-redes/gerar_estatisticas.py`:
  - Aula grátis = soma dos plays módulos **1 a 3** (não o pixel morto `/q-aula-gratis`)
  - Tabela Downloads: evalma + nome antigo no mesmo balde; brinde NT; quiz livres; Palavra tocada
  - Tabela Downloads: evalma + nome antigo no mesmo balde; bônus NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O brinde é o GET de `livro11-onovotestamenento.pdf`
- `/obrigado` ≠ PDF baixado. O bônus 1 é o GET de `livro11-o-n-t.pdf`

---

- Não overlay YouTube. Não publicar Eu Sou.
- Não apagar apioficial / app / api compraoseu.
- Não zerar enquete_dados.json para limpar spam.
- Não usar `/ebooks/livro11-onovotestamenento.pdf` (404 no ar). O bônus 1 do NT é `/ebooks/livro11-o-n-t.pdf`.
- Não dizer "as quatro aulas no site", nem "código de acesso grátis à Laura", nem "Liberar Módulos 5, 6 e 7". O ar é: módulos 1 a 3 grátis, um acesso R$ 37, código libera módulos 4 a 7.

---

O que ficou registrado na memória do projeto
1. Segundo quiz dos pais (aprovado e no ar)

/guia-pais-filhos-espelho é um quiz interativo, como o primeiro.
Emoji da família 👨‍👩‍👧 no topo (sem aquele 🪞 vertical estranho).
Resposta obrigatória em todas as perguntas, nos dois quizzes. Ninguém mais pula nem pega o brinde sem responder.
Ao final, 📖 Baixar o Devocional (Um-Segundo-com-Deus-Vol-01.pdf) para os pais.
Envio da página completa por e-mail funcionando (enviar_guia_espelho.php).
2. Home final

Voltou à originalidade: bloco "Para famílias" com um card.
A segunda chamada para o Espelho aparece só no final do quiz dos filhos.
Registrar que o script de dois cards não deve ser usado como referência.
3. Janela de leitura livre (18/09 00:00)

Confirmada no servidor: os 4 livros abertos, com navegação funcionando.
Banner na Home: 📖 Comece hoje sua leitura, sem urgência, com convite carinhoso.
Após a data, os quatro voltam a abrir a primeira metade automaticamente.
Backup e reversão prontos: python3 ABRIR_JANELA_LIVROS.py --reverter.
Observação que deixei na memória
O resultado desse período livre (se as pessoas vão sentir o conteúdo e depois querer o acesso completo) ainda não sabemos. Vamos observar com calma e oração, como você disse. Se surgir algo bom ou negativo, a memória já está pronta para registrar a próxima decisão.

## ABERTO (não é urgente nesta noite)

1. Confirmar se `palavra.html` e o `gerar_estatisticas.py` novo já estão no servidor.
2. Colar `PROMPT_LAURA_V11_CASA.txt` no OpenAI do FlowOpenAi. Encerrar tickets do autor. Testar só com número novo.
1. Confirmar se `palavra.html` e o `gerar_estatisticas.py` novo já estão no servidor. O autor já confirmou: `/palavra` é só para ele ver os temas, noindex, sem menu.
2. **PROMPT_LAURA_V11_CASA.txt já foi colado no FlowOpenAi.** Pendência só: encerrar tickets do autor e testar com número novo.
3. Conferir Pix real na Kiwify vs cliques Semeador / obrigado.
4. Ads só com pixel no domínio missaocomdeus. Destino Home ou `/livro11`. Sem carrossel de preço.
5. Mural só com nome real + «pode publicar».
6. Share nas pontes / obrigado: ideia boa, **depois**. Um lugar de cada vez.
4. **Pixel de conversão:** planejar e ativar na Kiwify (Pixels de Conversão). Google Ads + GA4 são os mais seguros sem IG/FB. Meta só depois com conta nova em outro aparelho/notebook e outro e-mail.
5. **Google Search Console:** depois da identidade no ar, atualizar/subscrever `sitemap.xml` (9 páginas), pedir reindexação das páginas vivas e remoção das páginas saídas.
6. Share nas pontes / obrigado: ideia boa, depois. Um lugar de cada vez.
7. GitHub ≠ servidor. Espelho quando o autor puder, sem apagar o vivo.
8. Redes sociais: não depender de IG/FB enquanto as contas estiverem banidas. Voltar só com aparelho novo, e-mail novo e sem reutilizar número que já caiu.

---

- Produtos Kiwify antigos ainda Ativos (não usar na Home): Devocional R$ 9,90; Anestesia avulsa; Evolução avulsa.
- Página de obrigado da casa: `https://missaocomdeus.com.br/obrigado`
  Colar na Kiwify em **Cartão ou Pix aprovado** (iVfp2bi e NCAEVtO). Boleto/pix gerado = página padrão Kiwify.
- Presente no obrigado = **Baixar PDF** `/ebooks/livro11-onovotestamenento.pdf` (typo no nome, proposital).
- Presente no obrigado = **Baixar PDF** `/ebooks/livro11-o-n-t.pdf` (confirmado no ar em 03/09. O nome antigo `livro11-onovotestamenento.pdf` retorna 404 e nao deve ser usado).
  Não é link `/livro11` (isso já é grátis).
- Não listar o NT como leitura exclusiva. Dois cursos no pacote R$ 37.

- Botão dourado: Começar o Devocional de 30 dias → `/livro04`
- Botão quieto: Ler as Afirmações → `/livro12`
- Arte: `https://i.ibb.co/zhH6FV9X/hero.jpg` · CSS `--navy` `#0e1a2e`
- Título oferta: Seja um Semeador da Missão e ganhe um Brinde Extra
- Brinde extra na lista: PDF O Novo Testamento como nunca lido (para guardar)
- Título oferta: Seja um Semeador da Missão e ganhe 4 bônus
- 4 bônus no acesso completo: NT, Devocional 30 dias, Jesus e Afirmações em PDF
- FAQ: «O que eu recebo no acesso completo?» · «Isso é doação?» (não)
- Banner `#cta-cursos`: ~45% scroll / mouseleave; `VALIDADE_HORAS = 6`; só Trilogia na Home
- Seção `#missao`: fé e a mente; Laura não é carne; Mt 18:20
- Motivo: 4 livres é mais da metade (filha de 13 anos). Autor concordou 3.
- Texto: isto é prévia; área de membros Kiwify tem explicações e exercícios.
- Um botão: **Quero o acesso completo — R$ 37,00** → iVfp2bi
- Linha dourada visível: brinde extra PDF NT
- Linha dourada visível: 4 bônus (NT, Devocional, Jesus e Afirmações)
- Modal: um preço. «Já tenho código de acesso»
- Mural vazio `display:none`. `/mural.html` no servidor, noindex, **sem link**
- Mural **eliminado**. Não existe mais funcionalidade pública de mural; não recriar, não colocar link.
- Plays: `tocarVideo` faz `fetch('/q-trilogia-m0N')` ou `/q-anestesia-m0N`
- Anestesia WhatsApp → `/q-codigo`; Kiwify → `/q-semeador`


## PDF / ebooks/

- **Fonte de verdade:** conferir a lista real do aaPanel no topo (03/09/2026). `livro11-onovotestamenento.pdf` **não existe** e nunca deve ser usado.
- Proteção pypdf (`permissions_flag`). Script `PROTEGER_PDFS.py`
- **LIVRES (sem evalma, quiz):** `Um-Segundo-com-Deus-Vol-01.pdf` · `jesus-quer-falar.pdf`
- **Com evalma (chute difícil):** `Anestesia-mental-evalma.pdf` · `Evolucao-da-alma-evalma.pdf`
- **Brinde NT (typo proposital, sem evalma):** `livro11-onovotestamenento.pdf`
- **LIVRES (sem evalma, quiz):** `Um-Segundo-com-Deus-Vol-01.pdf` · `jesus-quer-falar.pdf` · `jesus-quer-falar-com-seu-filho.pdf`
- **Com evalma (chute difícil):** `Anestesia-mental-evalma.pdf` · `Evolucao-da-alma-evalma.pdf` · `livro05-evalma.pdf` · `livro07-ocdespertar.pdf` · `livro09-amental.pdf` · `livro12-a-d-o.pdf`
- **Bônus 1 (nome real no ar):** `livro11-o-n-t.pdf`
- Dois «Jesus Quer Falar» no log antigo = dois arquivos (quiz curto × nome longo do livro). Não é duplicata.

---
- Script vivo do cron: `/home/deploy/gerar_estatisticas.py`
- Cópia nova (29/08) em `consultoria-redes/gerar_estatisticas.py`:
  - Aula grátis = soma dos plays módulos **1 a 3** (não o pixel morto `/q-aula-gratis`)
  - Tabela Downloads: evalma + nome antigo no mesmo balde; brinde NT; quiz livres; Palavra tocada
  - Tabela Downloads: evalma + nome antigo no mesmo balde; bônus NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O brinde é o GET de `livro11-onovotestamenento.pdf`
- `/obrigado` ≠ PDF baixado. O bônus 1 é o GET de `livro11-o-n-t.pdf`

---


## ABERTO (não é urgente nesta noite)

1. Confirmar se `palavra.html` e o `gerar_estatisticas.py` novo já estão no servidor.
2. Colar `PROMPT_LAURA_V11_CASA.txt` no OpenAI do FlowOpenAi. Encerrar tickets do autor. Testar só com número novo.
1. Confirmar se `palavra.html` e o `gerar_estatisticas.py` novo já estão no servidor. O autor já confirmou: `/palavra` é só para ele ver os temas, noindex, sem menu.
2. **PROMPT_LAURA_V11_CASA.txt já foi colado no FlowOpenAi.** Pendência só: encerrar tickets do autor e testar com número novo.
3. Conferir Pix real na Kiwify vs cliques Semeador / obrigado.
4. Ads só com pixel no domínio missaocomdeus. Destino Home ou `/livro11`. Sem carrossel de preço.
5. Mural só com nome real + «pode publicar».
6. Share nas pontes / obrigado: ideia boa, **depois**. Um lugar de cada vez.
4. **Pixel de conversão:** planejar e ativar na Kiwify (Pixels de Conversão). Google Ads + GA4 são os mais seguros sem IG/FB. Meta só depois com conta nova em outro aparelho/notebook e outro e-mail.
5. **Google Search Console:** depois da identidade no ar, atualizar/subscrever `sitemap.xml` (9 páginas), pedir reindexação das páginas vivas e remoção das páginas saídas.
6. Share nas pontes / obrigado: ideia boa, depois. Um lugar de cada vez.
7. GitHub ≠ servidor. Espelho quando o autor puder, sem apagar o vivo.
8. Redes sociais: não depender de IG/FB enquanto as contas estiverem banidas. Voltar só com aparelho novo, e-mail novo e sem reutilizar número que já caiu.

---

- Script vivo do cron: `/home/deploy/gerar_estatisticas.py`
- Cópia nova (29/08) em `consultoria-redes/gerar_estatisticas.py`:
  - Aula grátis = soma dos plays módulos **1 a 3** (não o pixel morto `/q-aula-gratis`)
  - Tabela Downloads: evalma + nome antigo no mesmo balde; brinde NT; quiz livres; Palavra tocada
  - Tabela Downloads: evalma + nome antigo no mesmo balde; bônus NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O brinde é o GET de `livro11-onovotestamenento.pdf`
- `/obrigado` ≠ PDF baixado. O bônus 1 é o GET de `livro11-o-n-t.pdf`

## PONTES `/trilogia-da-alma` e `/anestesia-mental`

- Motivo: 4 livres é mais da metade (filha de 13 anos). Autor concordou 3.
- Texto: isto é prévia; área de membros Kiwify tem explicações e exercícios.
- Um botão: **Quero o acesso completo — R$ 37,00** → iVfp2bi
- Linha dourada visível: brinde extra PDF NT
- Linha dourada visível: 4 bônus (NT, Devocional, Jesus e Afirmações)
- Modal: um preço. «Já tenho código de acesso»
- Mural vazio `display:none`. `/mural.html` no servidor, noindex, **sem link**
- Mural **eliminado**. Não existe mais funcionalidade pública de mural; não recriar, não colocar link.
- Plays: `tocarVideo` faz `fetch('/q-trilogia-m0N')` ou `/q-anestesia-m0N`
- Anestesia WhatsApp → `/q-codigo`; Kiwify → `/q-semeador`
