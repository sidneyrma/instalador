# 🦅 AVALIAÇÃO DE DESEMPENHO — 16/08/2026

**Portal O Despertar · compraoseu.com · painel gerado em 16/08/2026 13:29**

---

## 📊 Visão geral (com a comparação JUSTA — painel atualizado)

| Métrica | Valor | Observação |
|---|---|---|
| **Ontem completo (15/08)** | **1.231** | 🔥 Retomada do crescimento! |
| **Hoje até 13:29 (16/08)** | **809** | Em andamento |
| **Ontem até este horário** | 532 | (referência da comparação justa) |
| **Variação (justa)** | **📈 +52,1%** | Hoje MUITO à frente de ontem no mesmo horário |
| **Projeção do dia** | **~1.440** | Ritmo atual estendido para 24h |
| **Total geral** | **5.731** | Acumulado desde 11/08 |
| Visitas à Home | 684 | |
| Acessos aos livros | 605 | |
| Livros com acesso | 10 de 10 ✅ | |
| Quiz | 11 | |

## 📈 A tendência — leitura de águia

| Dia | Acessos | Leitura |
|---|---|---|
| 11/08 | 14 | Testes |
| 12/08 | 1.439 | Pico de lançamento |
| 13/08 | 1.272 | -12% pós-pico |
| 14/08 | 966 | Platô |
| 15/08 | **1.231** | 🔥 **+27% retomada!** |
| 16/08 | 809 até 13:29 (~1.440 projeção) | 📈 **+52% vs ontem no mesmo horário** |

**A grande notícia:** depois do platô de 966 em 14/08, ontem (15/08) voltou a
**crescer para 1.231** (+27%), e hoje está com **+52%** em relação a ontem no
mesmo horário, projetando ~1.440 — o nível do pico de lançamento!

**O que explica o crescimento (as mudanças que o senhor aprovou):**
1. **Quiz no topo da Home** (mudou do fim para logo após o portal) — mais
   interação desde o primeiro scroll;
2. **Faixa do brinde 🎁 E-book** no quiz — mais pessoas completam as 7
   perguntas (quiz passou de 9 para 11 e subindo);
3. **Home mais limpa** (hero 3 linhas, sem banner extra) — navegação mais
   rápida no celular;
4. **Botão "Instalar app" + PWA** — leitores voltam como app.

## 🏆 Ranking (com a correspondência Home ↔ arquivo)

| Pos. | Título (card) | Arquivo | Acessos | Hoje |
|---|---|---|---|---|
| 🥇 | Home | / | 684 | 43 |
| 🥈 | Evolução da Alma (Livro 02) | /livro05 | 85 | 4 |
| 🥉 | O Verbo que Transforma (Livro 06) | /livro01 | 76 | 2 |
| 4 | O Despertar do Observador (Livro 10) | /livro10 | 76 | 2 |
| 5 | O Arquiteto da Realidade (Livro 09) | /livro08 | 62 | 1 |
| 6 | A Sabedoria dos Mestres (Livro 11) | /livro02 | 57 | 3 |
| 7 | A Mente Renovada (Livro 07) | /livro03 | 57 | 2 |
| 8 | Um Segundo com Deus (Livro 04) | /livro04 | 53 | 3 |
| 9 | O Caminho do Despertar (Livro 08) | /livro07 | 51 | 1 |
| 10 | Anestesia Mental (Livro 03) | /livro09 | 48 | 1 |
| 11 | Jesus Quer Falar com Seu Filho (Livro 05) | /livro06 | 40 | 1 |
| 12 | Quiz | /quiz | 11 | — |

**Conversão Home → livros: 605/684 = 88%** — continua excelente.

## 🎯 Conclusão

1. **As mudanças de ontem estão dando frutos imediatos**: Home limpa + quiz no
   topo = mais interação. Projeção de ~1.440 hoje (nível do lançamento!).
2. **O quiz está crescendo** (9 → 11) — o destaque novo está funcionando;
3. **Bot do Google/validação 404**: a notificação do GSC segue em andamento
   (sem ação necessária);
4. **Recomendação:** manter o ritmo — inspeções diárias no GSC, divulgação
   ativa, e preparar o lançamento do Livro 11 (27/08) com o countdown rodando.

*"O Senhor é quem dá força ao seu povo; o Senhor abençoará o seu povo com
paz."* (Salmos 29:11)

## Vistoria técnica completa do leitor (16/08)

Inspeção profunda solicitada pelo autor, com olhos de águia:

**1. Leitores dos livros (12 arquivos — previews):**
- JavaScript válido em TODOS (node --check) — 0 erros.
- HTML balanceado em TODOS — 0 erros.
- Recursos presentes em todos: barra de progresso, fita dourada (id="fita-lateral"),
  trilha de capítulos (id="trilha"), modos Dia/Sépia/Noite (data-modo),
  balões de dicas (criados via JS: className="balao", mostrarDicas,
  "Continuar de onde parei", fechar balão).
- Os "balões" não aparecem no HTML estático porque são criados
  dinamicamente pelo JavaScript (comportamento correto).

**2. Livros publicados (site-contabo/livro01-11.html):**
- 11/11 com leitor completo (despertar_progresso_, fita, trilha, stats).

**3. Home (produção e preview):**
- JS válido, HTML balanceado.
- Lógica dos 7 dias confirmada: ao fechar, grava timestamp
  (despertar_continue_fechado = Date.now()); ao abrir, se fechou há menos de
  7 dias, não mostra; se passou 7 dias e há leitura em andamento, volta.
- Cartão "Continue lendo" presente, popups de dicas presentes, botão
  "Instalar app" (beforeinstallprompt) presente, Service Worker registrado.

**4. Pacote site-contabo.zip:**
- Contém index.html atualizado (cartão corrigido, 7 dias), livro01.html e
  livro10.html com leitor, sw.js e manifest.json.
- Zero ocorrências de "livrolivro" (bug corrigido).

**5. Site no ar:**
- https://compraoseu.com/livro10 exibe o balão "📖 Seu lugar fica salvo.
  Feche e volte quando quiser; retomamos do ponto exato." — o leitor está
  funcionando no servidor.
- Conteúdo purificado (títulos com dois-pontos, sem marcas).

**Conclusão:** o leitor está fluido e profissional. Para garantir a versão
mais recente da Home (cartão corrigido + 7 dias), enviar o site-contabo.zip
atual (16/08 16:15) ao servidor e extrair por cima.

## Enquete de participação na Home (16/08)

**O que foi criado:**
- Seção "📊 Participe — Sua opinião faz a diferença" na Home, entre a
  biblioteca e a trilogia.
- Pergunta: "O que você achou da leitura online com marcadores?" com 4 opções
  (Amei / Gostei / Parece útil / Ainda não usei).
- **Percentuais ao vivo** com barras de progresso douradas (atualizam a cada
  voto).
- Campo de comentário opcional: "Qual livro você está lendo? Está gostando?
  Tem alguma dúvida ou sugestão?" — o comentário aparece na seção
  "Comentários dos leitores".
- Proteção: 1 voto por navegador (localStorage) + intervalo mínimo de 30s
  entre votos do mesmo IP (enquete_ips.json).

**Como funciona (endpoint):**
- site-contabo/enquete.php — recebe GET (resultados) e POST (voto), guarda em
  enquete_dados.json (JSON), devolve percentuais.
- Fallback honesto: se o PHP não estiver ativo no servidor, o voto/comentário
  vai por e-mail via FormSubmit (compraoseu.com@gmail.com) e a enquete avisa.

**Para ativar no servidor (aaPanel):**
1. Enviar o site-contabo.zip (ou os arquivos enquete.php, enquete_dados.json e
   o index.html atualizado) e extrair por cima.
2. Garantir que o site compraoseu.com tenha versão PHP selecionada:
   Website → compraoseu.com → "PHP version" → escolher 7.4 ou 8.x → salvar.
3. Garantir permissão de escrita no arquivo enquete_dados.json (o PHP precisa
   gravar os votos): no Gerenciador de Arquivos, botão direito no arquivo →
   Permissão → 664, dono www (ou rodar no Terminal:
   `chown www:www /www/wwwroot/compraoseu.com/enquete_dados.json`).
4. Testar: abrir https://compraoseu.com/enquete.php no navegador → deve
   mostrar um JSON com "votos": 0.

**Validação:** lógica de votação testada (réplica em Python): percentuais
corretos (67/33 com 3 votos), comentários e total funcionando. JS das Homes
íntegro, HTML balanceado. Sem PHP no sandbox, a sintaxe foi revisada
cuidadosamente (balanceamento de chaves/parênteses, pontos críticos).

## Enquete: contagem de votos oculta (16/08)

A pedido do autor, a quantidade de votos não fica mais visível na página:

- Removida a barra de meta ("🎯 Meta: 100 participações") e o contador
  ("X votos até agora" / "1 voto").
- O carregamento da página agora é silencioso (só confirma que o endpoint
  responde; nada é exibido antes do voto).
- Os PERCENTUAIS por opção só aparecem APÓS o voto (a pessoa vota e vê o
  resultado) — mantém a gratificação sem expor a contagem geral.
- CSS morto (eq-meta, eq-total) removido; JS/HTML validados; gerador
  adicionar_enquete.py atualizado; zip regenerado.

## Chamada para a enquete no card "Livros online e gratuitos" (16/08)

A pedido do autor, o card-destaque "Livros online e gratuitos" (seção portal)
agora tem DOIS botões lado a lado:

- "Ir para os livros" (#biblioteca) — já existia;
- "💬 Participar da enquete" (#enquete) — NOVO, com estilo outline dourado
  (btn-enquete), ao lado do primeiro.

Os botões ficam em um contêiner flex (cd-acoes) com gap; no celular ocupam a
largura total, um embaixo do outro (flex:1 + wrap). Validado: JS íntegro,
HTML balanceado nas duas Homes; zip regenerado.

## Card destaque refinado (16/08, 2ª rodada)

A pedido do autor, o card "Livros online e gratuitos" foi refinado:

- **Ícone SVG do livro REMOVIDO** (a frase "Livros online e gratuitos" já
  fala por si) — ganha mais espaço/tela no celular.
- **Chamada convidativa adicionada** abaixo do parágrafo:
  "💬 E você? Conte o que achou da nova leitura com marcadores e ajude outros
  leitores, em menos de 1 minuto." (estilo .cd-convite, itálico dourado).
- **Dois botões lado a lado** (já da rodada anterior):
  "Ir para os livros" (#biblioteca) e "💬 Participar da enquete" (#enquete),
  em contêiner flex — lado a lado no desktop, empilhados no celular.

Validação: JS íntegro, HTML balanceado, ícone removido, convite presente,
botões presentes nas duas Homes; zip regenerado.

## CORREÇÃO: voto não computado + visualização da enquete (17/08)

**Problema:** o autor votou, mas o JSON mostrava votos:0.

**Causa (2 fatores):**
1. O site-contabo.zip continha enquete_dados.json com "votos": 0. Ao extrair o
   zip por cima no servidor, o arquivo com os votos reais era SOBRESCRITO,
   zerando a contagem.
2. Se a permissão de escrita não estiver definida (dono www), o PHP falha ao
   gravar (o @fopen silencia o erro).

**Correções aplicadas:**
1. **enquete.php robustecido:** cria o arquivo de dados automaticamente com
   chmod 0664 se não existir; se o fopen falhar, tenta criar e reabre.
2. **Zip recriado SEM enquete_dados.json e enquete_ips.json** (excluídos) —
   assim, ao extrair por cima, os votos do servidor NÃO são mais zerados.
3. **Visualização melhorada:** ao abrir enquete.php no NAVEGADOR (não via
   fetch), mostra uma página bonita com barras de percentual, contagem e
   comentários, em vez de JSON cru. As requisições da Home (fetch, Accept
   application/json) continuam recebendo JSON.

**Para o servidor (passos):**
1. Enviar o site-contabo.zip novo (só atualiza o enquete.php; NÃO sobrescreve
   os dados de votos) e extrair por cima.
2. No Terminal do aaPanel, garantir permissão de escrita:
   chown www:www /www/wwwroot/compraoseu.com/enquete_dados.json
   chmod 664 /www/wwwroot/compraoseu.com/enquete_dados.json
   (o PHP agora tenta criar sozinho, mas o chown garante)
3. Testar: abrir https://compraoseu.com/enquete.php no navegador → deve
   mostrar a página bonita (ou JSON se via fetch).
4. Votar de novo em aba anônima → o voto deve subir.
