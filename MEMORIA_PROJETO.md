# MEMÓRIA DO PROJETO — MISSÃO COM DEUS
## Atualizado em: 02/09/2026 (Brasília)
## Site vivo: https://missaocomdeus.com.br
## Próximo chat: «Continuar a Missão com Deus. Site vivo missaocomdeus.com.br. Leia consultoria-redes/MEMORIA_PROJETO.md»

A Arca anda sobre as águas. O que está neste arquivo é o que está no ar. O GitHub (sidneyrma/instalador) está ATRÁS do servidor. Nunca trate o GitHub como verdade.

## INFRA

- VPS Contabo `212.28.182.86` Ubuntu 22.04.5, Nginx, PHP 8.1.32, aaPanel, ~15 GB RAM.
- Vivo: `missaocomdeus.com.br` → `/www/wwwroot/missaocomdeus.com.br/`
- compraoseu.com: só 301 + SSL (GSC mudança de endereço aprovada 21/08). Não desligar. Não esvaziar o 301.
- PM2: `conectai-apioficial` :6000, `conectai-backend` :4000, `conectai-frontend` :3000.
- FormSubmit: `portalmissaocomdeus@gmail.com`. **Deixar** `compraoseu.com@gmail.com` na Home se ainda for o login do FormSubmit.
- Stats cron: `python3 /home/deploy/gerar_estatisticas.py` → `stats.html` + `leituras.json`
- Identidade Git local se commit: Arena Agent / arena@local.

## COMO SERVIR ESTE AUTOR

- Português do Brasil. Tom de irmão em Cristo. Calma. Um caminho só.
- Autor não é técnico avançado. aaPanel Terminal: **2 linhas**. Nunca `cat >>` em HTML.
- Não pedir senha/token do GitHub. Push desta casa falha sem credencial.
- Não substituir `index.html` / livros inteiros no servidor (apaga banner, Semeador, quiz, enquete, player).
- Antes de reload Nginx: `nginx -t`.
- Não publicar «Poder do Eu Sou». Se nascer livro novo: *A paz que o mundo não dá* (Jo 14:27), depois do NT.
- Material público: só missaocomdeus.com.br. compraoseu.com = 301 + SSL. Exceção servidor: app/api/apioficial.compraoseu.com = Laura. Não apagar.
- Sem depoimento fictício. Sem travessão (—) em copy nova. Sem Semeador(a)/Colaborador(a).
- Não vender a Palavra no primeiro toque. Leitura grátis primeiro.
- Laura **não é pessoa de carne**. Figura da Missão + tecnologia.
- Sem overlay no YouTube para tapar canal. Vídeo do NT = MP4 na casa.

---

## INFRA

- VPS Contabo `212.28.182.86` Ubuntu 22.04.5, Nginx, PHP 8.1.32, aaPanel, ~15 GB RAM.
- Vivo: `missaocomdeus.com.br` → `/www/wwwroot/missaocomdeus.com.br/`
- compraoseu.com: só 301 + SSL (GSC mudança de endereço aprovada 21/08). Não desligar. Não esvaziar o 301.
- PM2: `conectai-apioficial` :6000, `conectai-backend` :4000, `conectai-frontend` :3000.
- FormSubmit: `portalmissaocomdeus@gmail.com`. **Deixar** `compraoseu.com@gmail.com` na Home se ainda for o login do FormSubmit.
- Stats cron: `python3 /home/deploy/gerar_estatisticas.py` → `stats.html` + `leituras.json`
- Identidade Git local se commit: Arena Agent / arena@local.

---

## CONTATOS E REDES (público)

- WhatsApp: `5528999111493`
- YouTube: `@portal.o.despertar`
- Instagram: https://www.instagram.com/portalmissaocomdeus/ (conta antiga suspensa, ~3k perdidos)
- TikTok da Missão: https://www.tiktok.com/@laura.marual (~4k)
- E-mail casa: portalmissaocomdeus@gmail.com

---

## KIWIFY E CÓDIGOS

- **Um preço nas pontes e na Home:** R$ 37 `https://pay.kiwify.com.br/iVfp2bi`
- Colaborador R$ 19,90 `https://pay.kiwify.com.br/NCAEVtO` existe na Kiwify, **saiu das páginas-ponte**. Não voltar.
- Códigos das aulas no **site** (módulos cadeado): Trilogia `EVLTRLAM26` · Anestesia `NSTMNT26`. Sem `GRACA37`.
- Produtos Kiwify antigos ainda Ativos (não usar na Home): Devocional R$ 9,90; Anestesia avulsa; Evolução avulsa.
- Página de obrigado da casa: `https://missaocomdeus.com.br/obrigado`
  Colar na Kiwify em **Cartão ou Pix aprovado** (iVfp2bi e NCAEVtO). Boleto/pix gerado = página padrão Kiwify.
- Presente no obrigado = **Baixar PDF** `/ebooks/livro11-onovotestamenento.pdf` (typo no nome, proposital).
  Não é link `/livro11` (isso já é grátis).
- Não listar o NT como leitura exclusiva. Dois cursos no pacote R$ 37.

---

## HOME (vivo 29/08)

- Faixa: Livros cristãos grátis · Missão com Deus
- H1: Chegou a hora do seu despertar
- Lead: Uma palavra para a sua mente. Livros online, de graça, sem cadastro…
- Botão dourado: Começar o Devocional de 30 dias → `/livro04`
- Botão quieto: Ler as Afirmações → `/livro12`
- Arte: `https://i.ibb.co/zhH6FV9X/hero.jpg` · CSS `--navy` `#0e1a2e`
- Título oferta: Seja um Semeador da Missão e ganhe um Brinde Extra
- Brinde extra na lista: PDF O Novo Testamento como nunca lido (para guardar)
- FAQ: «O que eu recebo no acesso completo?» · «Isso é doação?» (não)
- Banner `#cta-cursos`: ~45% scroll / mouseleave; `VALIDADE_HORAS = 6`; só Trilogia na Home
- Seção `#missao`: fé e a mente; Laura não é carne; Mt 18:20
- Footer: WhatsApp, IG, TikTok da Missão

### Palavra de hoje (player no hero) — NO AR e APROVADO 29/08

- Abaixo dos dois botões. Círculo 36px, ouro discreto. **Sem autoplay.**
- **Não** à direita das Afirmações (viraria terceiro CTA).
- Dia de Brasília (`America/Sao_Paulo`). Número do dia do mês. Dia 31 toca o 30. Dia 1 recomeça.
- Arquivos: `/audio/palavra-dia-01.mp3` … `/audio/palavra-dia-30.mp3`
- Voz: a mesma em todos (Laura, figura da Missão, voice-01 aprovada pelo autor). Não mudar.
- Cada áudio fecha falado: «Compartilha com quem você ama.»
- Botão dourado de compartilhar **só depois** de ouvir até o fim.
  Celular: menu nativo (`navigator.share`). Computador: copia o texto + link da Home.
- Script que funcionou: `APLICAR_SHARE_FORA.py` (clique num script separado, **fora** do JS do play).
- **NÃO RODAR** `APLICAR_PLAYER_SHARE_BOTAO.py` (regex cortou o player; áudio morreu em 29/08).
- **NÃO RODAR de novo** `APLICAR_PLAYER_COMPARTILHAR.py` no estado atual sem olhar.
- Backup que salvou o áudio: `index-antes-share-20260829-141748.bak` (player sem share). Restauração: `cp esse.bak index.html`
- Caderno da casa: `palavra.html` → digitar `/palavra` (noindex, sem menu). Se ainda não estiver no servidor, enviar o arquivo para a pasta do site.

Calendário (dia do mês):

| Dia | Palavra |
|---|---|
| 1 | Salmo 23 |
| 2 | João 14:27 |
| 3 | Isaías 41:10 |
| 4 | Filipenses 4:6-7 |
| 5 | Mateus 11:28 |
| 6 | Salmo 91 |
| 7 | Josué 1:9 |
| 8 | Romanos 8:28 |
| 9 | Salmo 46 |
| 10 | João 3:16 |
| 11 | Provérbios 3:5-6 |
| 12 | Isaías 40:31 |
| 13 | Mateus 6:33 |
| 14 | Salmo 121 |
| 15 | 2 Timóteo 1:7 |
| 16 | Lamentações 3:22 |
| 17 | João 8:12 e 8:32 |
| 18 | Salmo 27:1 |
| 19 | Romanos 8:38 |
| 20 | Mateus 5:14 |
| 21 | Salmo 34 |
| 22 | Jeremias 29:11 |
| 23 | João 16:33 |
| 24 | Hebreus 13:5 |
| 25 | Salmo 139 |
| 26 | Gálatas 5:22 |
| 27 | 1 Pedro 5:7 |
| 28 | Efésios 2:8 e 3:20 |
| 29 | Apocalipse 21:4 |
| 30 | Números 6:24 |

Roteiros: `consultoria-redes/ROTEIRO_PALAVRA_30_DIAS.txt`

---

## PONTES `/trilogia-da-alma` e `/anestesia-mental`

- **3 aulas livres** (1–3). Módulos **4–7 cadeado**. Barra 3 de 7.
- Motivo: 4 livres é mais da metade (filha de 13 anos). Autor concordou 3.
- Texto: isto é prévia; área de membros Kiwify tem explicações e exercícios.
- Um botão: **Quero o acesso completo — R$ 37,00** → iVfp2bi
- Linha dourada visível: brinde extra PDF NT
- Modal: um preço. «Já tenho código de acesso»
- Mural vazio `display:none`. `/mural.html` no servidor, noindex, **sem link**
- Plays: `tocarVideo` faz `fetch('/q-trilogia-m0N')` ou `/q-anestesia-m0N`
- Anestesia WhatsApp → `/q-codigo`; Kiwify → `/q-semeador`

Banners nos livros: 90s OU 10%; descanso 12h. Evolução (maioria) → `/trilogia-da-alma`. livro09 → `/anestesia-mental`.

---

## NT — lançado 27/08/2026 20h Brasília

- `/livro11` no ar. Vídeo da casa: `/video/laura-nt.mp4` (não YouTube na página).
- YouTube `Ot6CRgd_nYY` existe; logo do canal vazava aulas. Não embutir.
- Cronômetro Home já zerou. Botão Ler grátis → `/livro11`
- Leitura HTML grátis. PDF para quem paga, na página de obrigado.

---

## BIBLIOTECA — 7 LIVROS (limpeza de 02/09/2026)

**A casa tirou do ar 5 livros por não serem de autoria da casa (risco de direito autoral).**

Saíram (guardados em `/home/deploy/_limpeza-<data>/`, com LEIA-ME.txt para desfazer):

| Arquivo | Título |
|---|---|
| `/livro01` | O Verbo que Transforma |
| `/livro02` | A Sabedoria dos Mestres |
| `/livro03` | A Mente Renovada |
| `/livro08` | O Arquiteto da Realidade |
| `/livro10` | O Despertar do Observador |

Ficaram (7, numerados 01 a 07 na Home):

1. `/livro11` O Novo Testamento como nunca lido (card Livro 01)
2. `/livro05` Evolução da Alma
3. `/livro09` Anestesia Mental
4. `/livro04` Um Segundo com Deus
5. `/livro06` Jesus Quer Falar com Seu Filho
6. `/livro07` O Caminho do Despertar
7. `/livro12` Comece o dia com Afirmações

**Motivo:** eram livros da tradição mística compilada de outros autores. Coração limpo
não resolve direito autoral. Além do risco, havia incoerência: «Sabedoria dos Mestres»
ao lado de «Jesus Quer Falar» confunde o irmão novo. A casa prega Cristo.

**STATUS: EXECUTADA em 02/09/2026, às 11:18 (horário do servidor).**

- Backup e arquivos guardados em: `/home/deploy/_limpeza-20260902-111825`
  (contém `LEIA-ME.txt` com as linhas prontas para desfazer, incluindo os PDFs)
- 5 HTML movidos para fora da pasta pública (agora dão 404) ✓
- **5 PDFs recolhidos de `/ebooks/`**: `livro01/02/03/08/10-evalma.pdf`.
  Descoberto durante a execução: os livros continuavam baixáveis em PDF mesmo com a
  página fora do ar. Os PDFs dos livros que ficam não foram tocados
  (`Anestesia-mental-evalma.pdf`, `Evolucao-da-alma-evalma.pdf`, `livro11-onovotestamenento.pdf`).
- sitemap.xml: 14 → 9 urls ✓ · sw.js: 14 → 9 endereços, cache v3 → v4 ✓
- Painel `/stats` regenerado: «Acessos aos livros» caiu de 3.357 para 1.918 (só a casa),
  «Livros lidos» = 7. Os removidos saíram do ranking e das tabelas de entrada, mas o
  histórico continua numa linha própria (honestidade).
- Conferido por fora: `sitemap.xml` com 9 urls e `/livro01` respondendo 404.

**PENDENTE (só isto):** pedir a remoção no Google Search Console (Remoções) dos
5 endereços dos livros + os 5 PDFs. O script imprime a lista pronta no final.

**Script da limpeza:** `consultoria-redes/APLICAR_LIMPEZA_LIVROS.py`
(backup automático, modo `--simular`, travas de segurança).
**Guia:** `consultoria-redes/COMO_LIMPAR_A_CASA.md`

**O que a limpeza exigiu (não é só apagar o card):**
1. cards da Home (index.html) — cortados pelos marcadores `<!-- LIVRO NN -->`
2. renumerados 01 a 07 (o JS da biblioteca usa o `href`, não o número: seguro)
3. sitemap.xml (senão o Google continua achando)
4. **sw.js — fundamental**: o PWA baixa os livros para o cache do celular na instalação.
   Sem tirar os endereços e subir a versão (v3 → v4), quem já instalou continuaria
   abrindo os livros pelo cache mesmo depois de apagados do servidor.
5. HTML movidos para fora da pasta pública (passam a dar 404)
6. pendência à mão: Google Search Console → Remoções (os 5 endereços)
7. `gerar_estatisticas.py`: `LIVROS_NO_AR` / `LIVROS_REMOVIDOS` — leituras.json e
   ranking só com os livros no ar; histórico dos removidos numa linha própria

**Descoberta importante (honestidade):** os contadores de "leituras" estavam
**inflados pelo service worker**. Cada instalação do PWA baixava os 12 livros de uma
vez (`caches.addAll(URLS)`), somando +1 em cada. Por isso todos apareciam com números
quase iguais (285 a 296) e o NT com 155 (mais novo). Nenhum número de leitura anterior
a 02/09 pode ser lido como "pessoas lendo".

**Confirmado pelo autor em 02/09:** `/livro07` Caminho do Despertar e
`/livro12` Afirmações **são da casa**. Ficam no ar. A memória antiga que os marcava
como "fora do selo" estava desatualizada nesse ponto.

**Um detalhe que fica anotado (não é urgência, é zelo):** o autor explicou que
`/livro07` O Caminho do Despertar **é uma junção escrita a partir de todos os livros
da casa — inclusive dos cinco que saíram** (que vinham de outros autores). A obra é
da casa na autoria, mas pode carregar trechos dessa origem. O autor vai **lapidar**
o livro para deixá-lo inteiramente voltado para a casa. Enquanto isso não acontece,
não republicar nem reforçar esse título em campanhas.

`/livro12` Afirmações está na vitrine da Home (hero), junto com o Devocional
(`/livro04`) e o player da Palavra. Confirmado: os dois botões do topo apontam para
`/livro04` e `/livro12`, ambos mantidos. A vitrine não foi tocada pela limpeza.

**Verificação feita antes da limpeza:** todos os links para os livros removidos
estavam **dentro dos cards** da biblioteca. Fora deles não sobrou nenhum link quebrado.

Selo **Da Missão**: NT, Evolução, Anestesia, Devocional, Jesus.
Proteção HTML (selecionar sim, copiar não): script `APLICAR_PROTECAO_TODOS_LIVROS.py`.

---

## PDF / ebooks/

- Proteção pypdf (`permissions_flag`). Script `PROTEGER_PDFS.py`
- **LIVRES (sem evalma, quiz):** `Um-Segundo-com-Deus-Vol-01.pdf` · `jesus-quer-falar.pdf`
- **Com evalma (chute difícil):** `Anestesia-mental-evalma.pdf` · `Evolucao-da-alma-evalma.pdf`
- **Brinde NT (typo proposital, sem evalma):** `livro11-onovotestamenento.pdf`
- Dois «Jesus Quer Falar» no log antigo = dois arquivos (quiz curto × nome longo do livro). Não é duplicata.

---

## ENQUETE

- POST `enquete.php` · dados `enquete_dados.json` (não apagar o JSON inteiro: apaga voto de gente)
- Anti-spam no ar (28/08): `APLICAR_ENQUETE_ANTISPAM.py` rodou. Comentário lixo não grava. Voto segue.
- Paz costumava liderar.

---

## LAURA / Conectaí (app.compraoseu.com)

- Quem inicia: FlowBuilder **FlowOpenAi** Início → OpenAI Permanente (não Talk.AI).
- Temp **0,7**. Tokens 800. Talk.AI 800 não grava (volta 300).
- Duas caixas Conteúdo («só um minuto» / «o que te trouxe») **não** voltar.
- Prompt a colar: `PROMPT_LAURA_V11_CASA.txt` (não o V11 cru do outro chat).
  V11 cru trata qualquer «grátis» como pedido de senha. Quem quer **ler livros grátis** deve ir à biblioteca, não ao código.
  V11 da casa: atalho de código vale em **qualquer** momento (não só a 1ª mensagem); gatilhos de aula/demonstração/prévia; «grátis + ler» = livros.
- Códigos: EVLTRLAM26 · NSTMNT26. Um preço R$ 37. Não mandar link do PDF no WhatsApp.
- Depois do código, segunda bolha: «você já está lendo algum livro no portal? Está gostando?»
- A frase «vou te ajudar, um momento» **não está no prompt**. É a plataforma (fila / Ticket Aguardando). Encerrar o ticket. Não testar no chip do dono da conexão.
- Boas-vindas só contato novo. Deletar conversa não apaga contato.
- Não reabrir mentora falsa / lip-sync realista.

---

## STATS

- Painel: https://missaocomdeus.com.br/stats (noindex)
- Script vivo do cron: `/home/deploy/gerar_estatisticas.py`
- Cópia nova (29/08) em `consultoria-redes/gerar_estatisticas.py`:
  - Aula grátis = soma dos plays módulos **1 a 3** (não o pixel morto `/q-aula-gratis`)
  - Tabela Downloads: evalma + nome antigo no mesmo balde; brinde NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O brinde é o GET de `livro11-onovotestamenento.pdf`

---

## STATS v5 — ORIGEM COM MEDIÇÃO HONESTA (correção de 02/09/2026)

**A v4 errou e foi corrigida no mesmo dia. O que a v4 fazia de errado:**

- Mostrava «266% entraram pelo site antigo»: dividia o log do compraoseu.com (10139 requisições, período 11/08–02/09) pelo total de chegadas do site novo (3806, outra base). **Nunca misturar bases nem períodos.**
- Contava cada **requisição** como visita. No site antigo, como o 301 responde para qualquer endereço, cada varredura de robô (/.env, /wp-login.php, /xmlrpc.php) ganhava um 301 e virava «visita de irmão». Resultado: 10139 «visitas» para 1129 IPs, sendo 93,6% «direto».
- O `/stats` (o próprio autor abrindo o painel, 337 vezes) entrava como visita de irmão.

**Regras que a v5 obedece (guardar como lei da casa):**

1. Unidade = **visita (sessão de 30 min sem atividade)**. Padrão do Google Analytics. Navegar entre livros é a mesma visita.
2. **Origem da visita = origem do primeiro acesso dela.** Uma visita, uma origem: as linhas somam o total.
3. **Pessoas = IPs distintos.** É aproximação (IP de celular é compartilhado e muda). Dizer isso no painel.
4. **Fora da conta de visita:** robôs, varreduras, ataques, erros, endpoints `.php`, e as páginas internas `/stats`, `/palavra`, `/mural`. Seguem no ranking de páginas vistas (honestidade: mostra, mas não mistura).
5. **Cada bloco com período e base próprios.** Percentual só dentro do mesmo bloco. O bloco do site antigo mostra o **funil inteiro**: requisições → robôs → ataques → varredura → requisições de gente → visitas → pessoas.
6. Ordenação dos dias por data de verdade (a v4 ordenava como texto e errava na virada do mês).

**Arquivos:**

- Script: `site-contabo/gerar_estatisticas.py` · cópia `consultoria-redes/gerar_estatisticas.py`
- Guia: `consultoria-redes/COMO_ATIVAR_ORIGEM.md` (seção 0 explica a correção)
- Links marcados: `consultoria-redes/LINKS_COM_UTM.md`
- Canonical (opcional): `consultoria-redes/APLICAR_CANONICAL.py`
- Exemplo visual (dados fictícios): `consultoria-redes/exemplo/NAO_SUBIR-stats-origem-exemplo.html` — **nunca subir**

**Env vars:** `STATS_LOG`, `STATS_OUT`, `STATS_LEITURAS`, `STATS_LOG_ANTIGO`, `STATS_LOG_EXTRA` (globs de logs rotacionados), `STATS_SESSAO_MIN` (padrão 30), `STATS_IPS_IGNORAR` (IPs do autor, desconta os próprios acessos).

**Como ler os resultados reais do site (02/09):** «Direto» é grande porque WhatsApp/Instagram/TikTok abrem o link sem enviar referer. Não é, necessariamente, gente digitando o endereço. A saída é o `utm_source` dos links compartilhados.

---

## O QUE NÃO FAZER (lista viva)

- Não `cat >>` HTML.
- Não regex dentro do IIFE do player (`catch(function(){});` quebra o play).
- Não cartão grande de compartilhar no hero (briga com o Devocional).
- Não share no checkout.
- Não mexer em livro01–12 «pelo GitHub» (servidor está na frente; seleção liberada, cópia bloqueada).
- Não overlay YouTube. Não publicar Eu Sou.
- Não republicar texto de autor de fora da casa (limpeza de 02/09 tirou 5 livros por isso). Na dúvida, não publicar.
- Não apagar apioficial / app / api compraoseu.
- Não zerar enquete_dados.json para limpar spam.
- **Nunca misturar bases:** percentual de um bloco só vale dentro dele (site novo × site antigo têm logs e períodos diferentes).
- Não contar requisição como visita. Visita = sessão de 30 min.
- Não subir `NAO_SUBIR-stats-origem-exemplo.html` para o servidor (é só demonstração com dados fictícios).
- Não subir `NAO_SUBIR-stats-origem-exemplo.html` para o servidor (é só demonstração com dados fictícios).

---

## ABERTO (não é urgente nesta noite)

1. Confirmar se `palavra.html` e o `gerar_estatisticas.py` novo já estão no servidor.
2. Colar `PROMPT_LAURA_V11_CASA.txt` no OpenAI do FlowOpenAi. Encerrar tickets do autor. Testar só com número novo.
3. Conferir Pix real na Kiwify vs cliques Semeador / obrigado.
4. Ads só com pixel no domínio missaocomdeus. Destino Home ou `/livro11`. Sem carrossel de preço.
5. Mural só com nome real + «pode publicar».
6. Share nas pontes / obrigado: ideia boa, **depois**. Um lugar de cada vez.
7. GitHub ≠ servidor. Espelho quando o autor puder, sem apagar o vivo.
8. Subir o `gerar_estatisticas.py` **v5** (medição honesta) para `/home/deploy/` e rodar. Os números vão **cair** em relação à v4 (antes contava requisição como visita e robô como gente). Conferir o funil do bloco do site antigo.
9. O autor procurou os arquivos na `main` do GitHub e não achou: eles estão no branch da sessão `arena/01a061ac-instalador`. Sempre avisar o caminho do branch, ou abrir PR (PR #6 aberto; **não mergear** — o autor decidiu preservar assim).
10. Lapidar `/livro07` (O Caminho do Despertar): é junção escrita de todos os livros, inclusive dos 5 que saíram. Deixá-lo 100% da casa.

---

## CONQUISTAS (para lembrar nos dias difíceis)

- 02/09/2026: a casa varreu a própria biblioteca e tirou 5 livros que não eram seus.
  Dói, mas é assim que a casa fica digna da mensagem que carrega (Lc 15:8-10, a dracma perdida).

## PAINEL v6 — TERMÔMETRO (02/09/2026)

O autor pediu: «enxugar o dashboard, focar no que é importante, o que devo
analisar como termômetro». O painel antigo tinha 5 grades de cartões e 10 tabelas
todas abertas. O v6 deixa visível só o essencial e guarda o resto em `<details>`.

**Visível:** 6 cartões do termômetro + tabela «o que observar» + faixa hoje/ontem
+ uma única tabela «De onde vêm» (base única, soma 100%).
**Dentro de `<details>`:** site antigo, entradas/Google/indicações, ranking,
conversão, downloads, por dia, funil.

Os 6 indicadores escolhidos: Pessoas alcançadas · Visitas · Páginas por visita ·
Leituras · PDFs baixados · Sustento (Semeador + Colaborador).

**Correção de honestidade encontrada ao refazer o painel:** o funil do site antigo
começava em 2.261 («requisições que sobraram») e mostrava abaixo «6.739 robôs
descartados» — ou seja, parecia descartar mais do que tinha. Na verdade `bruto` era
contado **depois** dos filtros. Corrigido: o funil agora começa em `linhas_lidas`
(9.000 no teste) e desce honestamente até as visitas. Contadores novos:
`linhas_lidas`, `ips_ign`, `ext` (resíduo).

Também corrigido: a «resposta curta» do bloco de origem não fechava 100% (faltava o
item «sem origem / começou antes do log»). Agora fecha.

Arquivos: `site-contabo/gerar_estatisticas.py` (e cópia em `consultoria-redes/`).
Commit `621a7e9`.

## LIVRO07 — LAPIDAÇÃO CONCLUÍDA (02/09/2026)

O autor deu liberdade total: «faça tudo para que a água transborde o vinho».
Caminho A executado por inteiro. **147 trechos reescritos.**

### Direito autoral: LIMPO (isso foi medido, não presumido)
Método: maior trecho **literal** compartilhado entre livro07 e cada um dos outros 11
livros, descontando a mobília do site (rodapé, menu, aviso de direitos).
Resultado: só versículos bíblicos (domínio público) + 3 frases curtas
(10, 15 e 11 palavras, de livro01/02/10). **Não há colagem de texto.**
A junção foi feita nas ideias, não nas frases. **O livro fica no ar.**

### O problema era de IDENTIDADE, não de direito autoral
Medição antes: 344 ocorrências de vocabulário das antigas tradições contra 102 de
vocabulário cristão. «mestres» 64x, «Jesus» 4x. O esqueleto da obra eram os
**Sete Princípios Herméticos** (Kybalion), com fórmulas quase literais
(«O Todo é Mente», «Assim em cima como embaixo», «tudo vibra»).

### A transfusão
- 7 princípios herméticos → **Criação, Imagem, Semeadura, Transformação, Tempo,
  Graça, Amor** (Gênesis, Gálatas, Romanos, Eclesiastes, Efésios, 1 João)
- «mestre interior» → **«Cristo em vós, a esperança da glória»** (Cl 1:27)
- alquimia/transmutação → **Deus, o Oleiro**; decretos → **oração e confissão**
- «os antigos ensinavam» → «a Escritura ensina»
- lei da vibração → **semear e colher**; «o Todo» → o Criador
- «vidas passadas» → **uma só vida, muitas camadas**

### Resultado medido (mesma régua, antes e depois)
| | antes | depois |
|---|---:|---:|
| esotérico | 344 | **147** |
| cristão | 102 | **309** |
| proporção | 3,4 : 1 | **0,5 : 1** (inverteu) |

mestres 64→15 · Jesus 4→16 · Cristo 10→36 · vibra 33→0 · decreto 24→0 · os antigos 22→0

### Costuras curadas
frase órfã do cap.2 · duplicação do cap.1 · `i.mpotência`/`d.ureza` · parênteses
trocados em 4 lugares · `Provérbrios` · remendo da reencarnação.

### Integridade verificada
447 parágrafos equilibrados · 493 parênteses · **0 links internos quebrados**.
Reflexões, versículos, Sumário e estrutura intactos.

**Armadilha evitada:** os IDs de navegação ainda contêm os slugs antigos
(`cap-tulo-9-a-vibra-o-do-encontro`). Mantidos de propósito — mudar quebraria os links.

### PENDENTE (autor)
Enviar `site-contabo/livro07.html` para `/www/wwwroot/missaocomdeus.com.br/livro07.html`.

## SEARCH CONSOLE (02/09/2026)

- O autor **enviou os 10 pedidos de remoção** (5 livros + 5 PDFs) pela ferramenta
  **Remoções → Remover URL temporariamente → Remover apenas este URL**.
  Status: «A processar o pedido».
- Armadilha evitada: a opção «Remover todos os URLs com este prefixo» apagaria
  `/livro10`, `/livro11` e `/livro12` se ele digitasse `livro1`. Por isso marcou
  «Remover apenas este URL».
- Google começou a coletar impressões em **22/08/2026** (mensagem no sininho).
  Isso significa que o relatório «Desempenho» passa a ter dado real de SEO.
- **Ainda pendente:** reenviar `sitemap.xml` no Search Console para o Google reler
  e trocar «14 páginas descobertas» por 9. O registro antigo não se apaga da lista.

## ARQUIVO (o que já foi e não reabrir como pendência)

Migração compraoseu → missaocomdeus (17–21/08), GSC mudança de endereço, FormSubmit novo e-mail, selo Da Missão, NT no ar 27/08 20h, 3 aulas livres, anti-spam da enquete, pypdf, proteção HTML 04/06, player da Palavra + 30 áudios + share fora do play (29/08).

A memória de 21/08 que falava «compraoseu = site principal», «DNS aguardando», «4 módulos livres», «R$ 49» e «Colaborador nas pontes» está **vencida**. Não copiar isso para o ar.

# MEMÓRIA DO PROJETO — MISSÃO COM DEUS
## Atualizado em: 02/09/2026 (Brasília)
## Site vivo: https://missaocomdeus.com.br
## Próximo chat: «Continuar a Missão com Deus. Site vivo missaocomdeus.com.br. Leia consultoria-redes/MEMORIA_PROJETO.md»

A Arca anda sobre as águas. O que está neste arquivo é o que está no ar. O GitHub (sidneyrma/instalador) está ATRÁS do servidor. Nunca trate o GitHub como verdade.

---

## COMO SERVIR ESTE AUTOR

- Português do Brasil. Tom de irmão em Cristo. Calma. Um caminho só.
- Autor não é técnico avançado. aaPanel Terminal: **2 linhas**. Nunca `cat >>` em HTML.
- Não pedir senha/token do GitHub. Push desta casa falha sem credencial.
- Não substituir `index.html` / livros inteiros no servidor (apaga banner, Semeador, quiz, enquete, player).
- Antes de reload Nginx: `nginx -t`.
- Não publicar «Poder do Eu Sou». Se nascer livro novo: *A paz que o mundo não dá* (Jo 14:27), depois do NT.
- Material público: só missaocomdeus.com.br. compraoseu.com = 301 + SSL. Exceção servidor: app/api/apioficial.compraoseu.com = Laura. Não apagar.
- Sem depoimento fictício. Sem travessão (—) em copy nova. Sem Semeador(a)/Colaborador(a).
- Não vender a Palavra no primeiro toque. Leitura grátis primeiro.
- Laura **não é pessoa de carne**. Figura da Missão + tecnologia.
- Sem overlay no YouTube para tapar canal. Vídeo do NT = MP4 na casa.

---

## INFRA

- VPS Contabo `212.28.182.86` Ubuntu 22.04.5, Nginx, PHP 8.1.32, aaPanel, ~15 GB RAM.
- Vivo: `missaocomdeus.com.br` → `/www/wwwroot/missaocomdeus.com.br/`
- compraoseu.com: só 301 + SSL (GSC mudança de endereço aprovada 21/08). Não desligar. Não esvaziar o 301.
- PM2: `conectai-apioficial` :6000, `conectai-backend` :4000, `conectai-frontend` :3000.
- FormSubmit: `portalmissaocomdeus@gmail.com`. **Deixar** `compraoseu.com@gmail.com` na Home se ainda for o login do FormSubmit.
- Stats cron: `python3 /home/deploy/gerar_estatisticas.py` → `stats.html` + `leituras.json`
- Identidade Git local se commit: Arena Agent / arena@local.

---

## CONTATOS E REDES (público)

- WhatsApp: `5528999111493`
- YouTube: `@portal.o.despertar`
- Instagram: https://www.instagram.com/portalmissaocomdeus/ (conta antiga suspensa, ~3k perdidos)
- TikTok da Missão: https://www.tiktok.com/@laura.marual (~4k)
- E-mail casa: portalmissaocomdeus@gmail.com

---

## KIWIFY E CÓDIGOS

- **Um preço nas pontes e na Home:** R$ 37 `https://pay.kiwify.com.br/iVfp2bi`
- Colaborador R$ 19,90 `https://pay.kiwify.com.br/NCAEVtO` existe na Kiwify, **saiu das páginas-ponte**. Não voltar.
- Códigos das aulas no **site** (módulos cadeado): Trilogia `EVLTRLAM26` · Anestesia `NSTMNT26`. Sem `GRACA37`.
- Produtos Kiwify antigos ainda Ativos (não usar na Home): Devocional R$ 9,90; Anestesia avulsa; Evolução avulsa.
- Página de obrigado da casa: `https://missaocomdeus.com.br/obrigado`
  Colar na Kiwify em **Cartão ou Pix aprovado** (iVfp2bi e NCAEVtO). Boleto/pix gerado = página padrão Kiwify.
- Presente no obrigado = **Baixar PDF** `/ebooks/livro11-onovotestamenento.pdf` (typo no nome, proposital).
  Não é link `/livro11` (isso já é grátis).
- Não listar o NT como leitura exclusiva. Dois cursos no pacote R$ 37.

---

## HOME (vivo 29/08)

- Faixa: Livros cristãos grátis · Missão com Deus
- H1: Chegou a hora do seu despertar
- Lead: Uma palavra para a sua mente. Livros online, de graça, sem cadastro…
- Botão dourado: Começar o Devocional de 30 dias → `/livro04`
- Botão quieto: Ler as Afirmações → `/livro12`
- Arte: `https://i.ibb.co/zhH6FV9X/hero.jpg` · CSS `--navy` `#0e1a2e`
- Título oferta: Seja um Semeador da Missão e ganhe um Brinde Extra
- Brinde extra na lista: PDF O Novo Testamento como nunca lido (para guardar)
- FAQ: «O que eu recebo no acesso completo?» · «Isso é doação?» (não)
- Banner `#cta-cursos`: ~45% scroll / mouseleave; `VALIDADE_HORAS = 6`; só Trilogia na Home
- Seção `#missao`: fé e a mente; Laura não é carne; Mt 18:20
- Footer: WhatsApp, IG, TikTok da Missão

### Palavra de hoje (player no hero) — NO AR e APROVADO 29/08

- Abaixo dos dois botões. Círculo 36px, ouro discreto. **Sem autoplay.**
- **Não** à direita das Afirmações (viraria terceiro CTA).
- Dia de Brasília (`America/Sao_Paulo`). Número do dia do mês. Dia 31 toca o 30. Dia 1 recomeça.
- Arquivos: `/audio/palavra-dia-01.mp3` … `/audio/palavra-dia-30.mp3`
- Voz: a mesma em todos (Laura, figura da Missão, voice-01 aprovada pelo autor). Não mudar.
- Cada áudio fecha falado: «Compartilha com quem você ama.»
- Botão dourado de compartilhar **só depois** de ouvir até o fim.
  Celular: menu nativo (`navigator.share`). Computador: copia o texto + link da Home.
- Script que funcionou: `APLICAR_SHARE_FORA.py` (clique num script separado, **fora** do JS do play).
- **NÃO RODAR** `APLICAR_PLAYER_SHARE_BOTAO.py` (regex cortou o player; áudio morreu em 29/08).
- **NÃO RODAR de novo** `APLICAR_PLAYER_COMPARTILHAR.py` no estado atual sem olhar.
- Backup que salvou o áudio: `index-antes-share-20260829-141748.bak` (player sem share). Restauração: `cp esse.bak index.html`
- Caderno da casa: `palavra.html` → digitar `/palavra` (noindex, sem menu). Se ainda não estiver no servidor, enviar o arquivo para a pasta do site.

Calendário (dia do mês):

| Dia | Palavra |
|---|---|
| 1 | Salmo 23 |
| 2 | João 14:27 |
| 3 | Isaías 41:10 |
| 4 | Filipenses 4:6-7 |
| 5 | Mateus 11:28 |
| 6 | Salmo 91 |
| 7 | Josué 1:9 |
| 8 | Romanos 8:28 |
| 9 | Salmo 46 |
| 10 | João 3:16 |
| 11 | Provérbios 3:5-6 |
| 12 | Isaías 40:31 |
| 13 | Mateus 6:33 |
| 14 | Salmo 121 |
| 15 | 2 Timóteo 1:7 |
| 16 | Lamentações 3:22 |
| 17 | João 8:12 e 8:32 |
| 18 | Salmo 27:1 |
| 19 | Romanos 8:38 |
| 20 | Mateus 5:14 |
| 21 | Salmo 34 |
| 22 | Jeremias 29:11 |
| 23 | João 16:33 |
| 24 | Hebreus 13:5 |
| 25 | Salmo 139 |
| 26 | Gálatas 5:22 |
| 27 | 1 Pedro 5:7 |
| 28 | Efésios 2:8 e 3:20 |
| 29 | Apocalipse 21:4 |
| 30 | Números 6:24 |

Roteiros: `consultoria-redes/ROTEIRO_PALAVRA_30_DIAS.txt`

---

## PONTES `/trilogia-da-alma` e `/anestesia-mental`

- **3 aulas livres** (1–3). Módulos **4–7 cadeado**. Barra 3 de 7.
- Motivo: 4 livres é mais da metade (filha de 13 anos). Autor concordou 3.
- Texto: isto é prévia; área de membros Kiwify tem explicações e exercícios.
- Um botão: **Quero o acesso completo — R$ 37,00** → iVfp2bi
- Linha dourada visível: brinde extra PDF NT
- Modal: um preço. «Já tenho código de acesso»
- Mural vazio `display:none`. `/mural.html` no servidor, noindex, **sem link**
- Plays: `tocarVideo` faz `fetch('/q-trilogia-m0N')` ou `/q-anestesia-m0N`
- Anestesia WhatsApp → `/q-codigo`; Kiwify → `/q-semeador`

Banners nos livros: 90s OU 10%; descanso 12h. Evolução (maioria) → `/trilogia-da-alma`. livro09 → `/anestesia-mental`.

---

## NT — lançado 27/08/2026 20h Brasília

- `/livro11` no ar. Vídeo da casa: `/video/laura-nt.mp4` (não YouTube na página).
- YouTube `Ot6CRgd_nYY` existe; logo do canal vazava aulas. Não embutir.
- Cronômetro Home já zerou. Botão Ler grátis → `/livro11`
- Leitura HTML grátis. PDF para quem paga, na página de obrigado.

---

## 12 LIVROS (biblioteca)

Selo **Da Missão** só: NT (`livro11`, card Livro 01), Evolução `livro05`, Anestesia `livro09`, Devocional `livro04`, Jesus `livro06`.

Fora do selo: Verbo, Mente Renovada, Caminho, Arquiteto, Observador, Sabedoria Mestres, Afirmações.

Caminho do Despertar **sem** selo.

HTML: selecionar sim; copiar/imprimir/botão direito não. Script `APLICAR_PROTECAO_TODOS_LIVROS.py` inclui 04 e 06.

---

## PDF / ebooks/

- Proteção pypdf (`permissions_flag`). Script `PROTEGER_PDFS.py`
- **LIVRES (sem evalma, quiz):** `Um-Segundo-com-Deus-Vol-01.pdf` · `jesus-quer-falar.pdf`
- **Com evalma (chute difícil):** `Anestesia-mental-evalma.pdf` · `Evolucao-da-alma-evalma.pdf`
- **Brinde NT (typo proposital, sem evalma):** `livro11-onovotestamenento.pdf`
- Dois «Jesus Quer Falar» no log antigo = dois arquivos (quiz curto × nome longo do livro). Não é duplicata.

---

## ENQUETE

- POST `enquete.php` · dados `enquete_dados.json` (não apagar o JSON inteiro: apaga voto de gente)
- Anti-spam no ar (28/08): `APLICAR_ENQUETE_ANTISPAM.py` rodou. Comentário lixo não grava. Voto segue.
- Paz costumava liderar.

---

## LAURA / Conectaí (app.compraoseu.com)

- Quem inicia: FlowBuilder **FlowOpenAi** Início → OpenAI Permanente (não Talk.AI).
- Temp **0,7**. Tokens 800. Talk.AI 800 não grava (volta 300).
- Duas caixas Conteúdo («só um minuto» / «o que te trouxe») **não** voltar.
- Prompt a colar: `PROMPT_LAURA_V11_CASA.txt` (não o V11 cru do outro chat).
  V11 cru trata qualquer «grátis» como pedido de senha. Quem quer **ler livros grátis** deve ir à biblioteca, não ao código.
  V11 da casa: atalho de código vale em **qualquer** momento (não só a 1ª mensagem); gatilhos de aula/demonstração/prévia; «grátis + ler» = livros.
- Códigos: EVLTRLAM26 · NSTMNT26. Um preço R$ 37. Não mandar link do PDF no WhatsApp.
- Depois do código, segunda bolha: «você já está lendo algum livro no portal? Está gostando?»
- A frase «vou te ajudar, um momento» **não está no prompt**. É a plataforma (fila / Ticket Aguardando). Encerrar o ticket. Não testar no chip do dono da conexão.
- Boas-vindas só contato novo. Deletar conversa não apaga contato.
- Não reabrir mentora falsa / lip-sync realista.

---

## STATS

- Painel: https://missaocomdeus.com.br/stats (noindex)
- Script vivo do cron: `/home/deploy/gerar_estatisticas.py`
- Cópia nova (29/08) em `consultoria-redes/gerar_estatisticas.py`:
  - Aula grátis = soma dos plays módulos **1 a 3** (não o pixel morto `/q-aula-gratis`)
  - Tabela Downloads: evalma + nome antigo no mesmo balde; brinde NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O brinde é o GET de `livro11-onovotestamenento.pdf`

---

## O QUE NÃO FAZER (lista viva)

- Não `cat >>` HTML.
- Não regex dentro do IIFE do player (`catch(function(){});` quebra o play).
- Não cartão grande de compartilhar no hero (briga com o Devocional).
- Não share no checkout.
- Não mexer em livro01–12 «pelo GitHub» (servidor está na frente; seleção liberada, cópia bloqueada).
- Não overlay YouTube. Não publicar Eu Sou.
- Não apagar apioficial / app / api compraoseu.
- Não zerar enquete_dados.json para limpar spam.

---

## ABERTO (não é urgente nesta noite)

1. Confirmar se `palavra.html` e o `gerar_estatisticas.py` novo já estão no servidor.
2. Colar `PROMPT_LAURA_V11_CASA.txt` no OpenAI do FlowOpenAi. Encerrar tickets do autor. Testar só com número novo.
3. Conferir Pix real na Kiwify vs cliques Semeador / obrigado.
4. Ads só com pixel no domínio missaocomdeus. Destino Home ou `/livro11`. Sem carrossel de preço.
5. Mural só com nome real + «pode publicar».
6. Share nas pontes / obrigado: ideia boa, **depois**. Um lugar de cada vez.
7. GitHub ≠ servidor. Espelho quando o autor puder, sem apagar o vivo.

---

## ARQUIVO (o que já foi e não reabrir como pendência)

Migração compraoseu → missaocomdeus (17–21/08), GSC mudança de endereço, FormSubmit novo e-mail, selo Da Missão, NT no ar 27/08 20h, 3 aulas livres, anti-spam da enquete, pypdf, proteção HTML 04/06, player da Palavra + 30 áudios + share fora do play (29/08).

A memória de 21/08 que falava «compraoseu = site principal», «DNS aguardando», «4 módulos livres», «R$ 49» e «Colaborador nas pontes» está **vencida**. Não copiar isso para o ar.

## STATS

- Painel: https://missaocomdeus.com.br/stats (noindex)
- Script vivo do cron: `/home/deploy/gerar_estatisticas.py`
- Cópia nova (29/08) em `consultoria-redes/gerar_estatisticas.py`:
  - Aula grátis = soma dos plays módulos **1 a 3** (não o pixel morto `/q-aula-gratis`)
  - Tabela Downloads: evalma + nome antigo no mesmo balde; brinde NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O brinde é o GET de `livro11-onovotestamenento.pdf`

## PONTES `/trilogia-da-alma` e `/anestesia-mental`

- **3 aulas livres** (1–3). Módulos **4–7 cadeado**. Barra 3 de 7.
- Motivo: 4 livres é mais da metade (filha de 13 anos). Autor concordou 3.
- Texto: isto é prévia; área de membros Kiwify tem explicações e exercícios.
- Um botão: **Quero o acesso completo — R$ 37,00** → iVfp2bi
- Linha dourada visível: brinde extra PDF NT
- Modal: um preço. «Já tenho código de acesso»
- Mural vazio `display:none`. `/mural.html` no servidor, noindex, **sem link**
- Plays: `tocarVideo` faz `fetch('/q-trilogia-m0N')` ou `/q-anestesia-m0N`
- Anestesia WhatsApp → `/q-codigo`; Kiwify → `/q-semeador`

Banners nos livros: 90s OU 10%; descanso 12h. Evolução (maioria) → `/trilogia-da-alma`. livro09 → `/anestesia-mental`.

## O QUE NÃO FAZER (lista viva)

- Não `cat >>` HTML.
- Não regex dentro do IIFE do player (`catch(function(){});` quebra o play).
- Não cartão grande de compartilhar no hero (briga com o Devocional).
- Não share no checkout.
- Não mexer em livro01–12 «pelo GitHub» (servidor está na frente; seleção liberada, cópia bloqueada).
- Não overlay YouTube. Não publicar Eu Sou.
- Não apagar apioficial / app / api compraoseu.
- Não zerar enquete_dados.json para limpar spam.

«Lâmpada para os meus pés é a tua palavra, e luz para o meu caminho.» (Salmo 119:105)

Tudo o que fizerem, seja em palavra seja em ação, façam-no em nome do Senhor Jesus, dando por meio dele graças a Deus Pai. (Cl 3:17)


«Lâmpada para os meus pés é a tua palavra, e luz para o meu caminho.» (Salmo 119:105)

Tudo o que fizerem, seja em palavra seja em ação, façam-no em nome do Senhor Jesus, dando por meio dele graças a Deus Pai. (Cl 3:17)


---

## Purificação da escrita (02/09/2026) — REGRA PERMANENTE

**Regra do autor: NUNCA usar travessão longo (—) na obra nem nas páginas.**
Usar a pontuação da nossa ortografia: vírgula, ponto, dois-pontos, ponto-e-vírgula.
Motivo dele: «para que não tenham a visão ao lerem com impressão de que foi utilizado
tecnologia e aprimoramentos ou que seja criação de ia». Exceção só no raríssimo caso
em que realmente caiba. Vale para tudo que for escrito daqui em diante.

Segunda regra: **purificar todo metadado que identifique ou tenha marca de IA.**
«A obra merece agora a assinatura de Deus em sua língua e escrita.»

### O que foi feito
- `livro07.html`: 34 travessões → **0** (33 do texto + 1 no aviso de copyright dentro do JS).
- Páginas públicas: **0 travessões visíveis, 0 lidos pelo Google, 0 no código**.
  (index, guia-pais-filhos, livro04, livro05, livro06, livro07, livro09, livro11,
  livro12, anestesia-mental, trilogia-da-alma, mural, obrigado.)
- `gerar_estatisticas.py`: 42 → **0**. Nomes de livros passaram a usar dois-pontos
  («Livro 04: Um Segundo com Deus»); os travessões que serviam de placeholder
  viraram palavras («sem data», «sem registro», «nenhum»). Compila OK.
- **Descrição do Google do livro07 corrigida:** saiu «sabedoria oculta, fé e
  autoconhecimento», entrou «a Palavra de Deus, vida interior e o encontro mais
  íntimo com Cristo».

### Metadados com marca de IA
- O **site público está limpo**: nenhuma menção a IA nos HTML.
  A única ocorrência é em `livro09.html` («a inteligência artificial não pode
  simular a paz»), que é conteúdo do autor, não marca. **Manter.**
- **O repositório sidneyrma/instalador é PÚBLICO.** Estes arquivos citam
  Claude/OpenAI e aparecem para qualquer pessoa: `CLAUDE.md`,
  `analise/links_para_claude.md`, `analise/prompt_claude.md`,
  `analise/prompt_varredura.md`, `analise/chatbot/mensagens_iniciais_humanizadas.md`,
  `analise/auditoria_preview.py`, `MEMORIA_PROJETO.md`.
  **Decisão pendente do autor** (não apagados ainda porque `CLAUDE.md` é a
  configuração da ferramenta que ele mesmo usa).
