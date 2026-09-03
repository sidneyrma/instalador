# MEMÓRIA DO PROJETO — MISSÃO COM DEUS
## Atualizado em: 03/09/2026 (Brasília)
## Site vivo: https://missaocomdeus.com.br
## Próximo chat: «Continuar a Missão com Deus. Site vivo missaocomdeus.com.br. Leia consultoria-redes/MEMORIA_PROJETO.md»

A Arca anda sobre as águas. O que está neste arquivo é o que está no ar. O GitHub (sidneyrma/instalador) está ATRÁS do servidor. Nunca trate o GitHub como verdade.

## ATUALIZAÇÃO URGENTE — 03/09/2026 (consultoria)

- Bônus 1 e 4 no ar: **`/ebooks/livro11-o-n-t.pdf`** (NT) e **`/ebooks/livro12-a-d-o.pdf`** (Afirmações). O nome antigo `livro11-onovotestamenento.pdf` **retorna 404**. Não usar.
- Bônus 4 (Afirmações) no obrigado: **`/ebooks/livro12-a-d-o.pdf`** (existe e está no ar).
- Home / FAQ e oferta ajustadas no espelho para **4 bônus**: NT, Devocional 30 dias, Jesus e Afirmações em PDF. Módulos 1 a 3 grátis.
- Banner fixo da Home NÃO deve mais prometer "código de acesso grátis à Laura" nem pedir "código grátis". O convite certo é sobre o acesso completo.
- Caixa de código das pontes: dizer **"Liberar os módulos restantes (4 a 7)"**, não "Liberar Módulos 5, 6 e 7".
- O `/stats` vivo hoje é **v6** e NÃO é o `site-contabo/gerar_estatisticas.py` do GitHub (que é v3). Antes de atualizar/sobrescrever, retirar o script v6 do servidor, senão o painel volta.

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
- Presente no obrigado = **Baixar PDF** `/ebooks/livro11-o-n-t.pdf` (confirmado no ar em 03/09. O nome antigo `livro11-onovotestamenento.pdf` retorna 404 e nao deve ser usado).
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
- Título oferta: Seja um Semeador da Missão e ganhe 4 bônus
- 4 bônus no acesso completo: NT, Devocional 30 dias, Jesus e Afirmações em PDF
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
- Linha dourada visível: 4 bônus (NT, Devocional, Jesus e Afirmações)
- Modal: um preço. «Já tenho código de acesso»
- Caixa de código: «Liberar os módulos restantes (4 a 7)». Não usar «Liberar Módulos 5, 6 e 7».
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
- **Bônus 1 (nome real no ar):** `livro11-o-n-t.pdf`
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
  - Tabela Downloads: evalma + nome antigo no mesmo balde; bônus NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O bônus 1 é o GET de `livro11-o-n-t.pdf`

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
- Não usar `/ebooks/livro11-onovotestamenento.pdf` (404 no ar). O bônus 1 do NT é `/ebooks/livro11-o-n-t.pdf`.
- Não dizer "as quatro aulas no site", nem "código de acesso grátis à Laura", nem "Liberar Módulos 5, 6 e 7". O ar é: módulos 1 a 3 grátis, um acesso R$ 37, código libera módulos 4 a 7.

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

# MEMÓRIA DO PROJETO — MISSÃO COM DEUS
## Atualizado em: 29/08/2026 (Brasília)
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
- Presente no obrigado = **Baixar PDF** `/ebooks/livro11-o-n-t.pdf` (confirmado no ar em 03/09. O nome antigo `livro11-onovotestamenento.pdf` retorna 404 e nao deve ser usado).
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
- Título oferta: Seja um Semeador da Missão e ganhe 4 bônus
- 4 bônus no acesso completo: NT, Devocional 30 dias, Jesus e Afirmações em PDF
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
- Linha dourada visível: 4 bônus (NT, Devocional, Jesus e Afirmações)
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
- **Bônus 1 (nome real no ar):** `livro11-o-n-t.pdf`
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
  - Tabela Downloads: evalma + nome antigo no mesmo balde; bônus NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O bônus 1 é o GET de `livro11-o-n-t.pdf`

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
  - Tabela Downloads: evalma + nome antigo no mesmo balde; bônus NT; quiz livres; Palavra tocada
  - `/obrigado` e `/palavra` no ranking
  - `/trilogia` e `/anestesia` (1 hit) = URL curta, não as pontes. Alias para as pontes de verdade
  - `.well-known` (SSL) some da lista
- Se o card «Aula grátis» ainda mostrar 0 no ar, o `/home/deploy/` ainda não recebeu essa cópia. Enviar e rodar `python3 /home/deploy/gerar_estatisticas.py`
- Conversão 1,5% = clique/pessoas, não Pix. Conferir vendas reais na Kiwify.
- `/obrigado` ≠ PDF baixado. O bônus 1 é o GET de `livro11-o-n-t.pdf`

## PONTES `/trilogia-da-alma` e `/anestesia-mental`

- **3 aulas livres** (1–3). Módulos **4–7 cadeado**. Barra 3 de 7.
- Motivo: 4 livres é mais da metade (filha de 13 anos). Autor concordou 3.
- Texto: isto é prévia; área de membros Kiwify tem explicações e exercícios.
- Um botão: **Quero o acesso completo — R$ 37,00** → iVfp2bi
- Linha dourada visível: 4 bônus (NT, Devocional, Jesus e Afirmações)
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
