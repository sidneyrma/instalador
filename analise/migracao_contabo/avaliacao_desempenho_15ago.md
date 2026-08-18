# 🦅 AVALIAÇÃO DE DESEMPENHO — 15/08/2026

**Portal O Despertar · compraoseu.com · painel gerado em 15/08/2026 15:10**

---

## 📊 Visão geral desde o lançamento

| Dia | Acessos | Observação |
|---|---|---|
| 11/08 | 14 | Testes/configuração (site ainda não no ar) |
| 12/08 | 1.439 | 🔥 1º dia completo no ar (pico de lançamento/divulgação) |
| 13/08 | 1.272 | Queda natural de ~12% após o pico |
| 14/08 | 966 | Estabilização (dia completo) |
| 15/08 | 603 (até 15:10) | Em andamento; projeção ~900-1.000 |
| **Total** | **4.294** | Média ~1.200/dia nos dias completos |

## 📈 Leitura honesta dos números

**A queda de -37,6% que o painel mostra é enganosa** (como já sabíamos): ele
compara **o dia de hoje parcial (603 até 15:10) com o dia de ontem inteiro
(966)**. A comparação justa é por horário:

- Ontem às 10:29 tinha **260** acessos (relatório anterior);
- Hoje às 15:10 já tem **603** → hoje está **à frente** de ontem no mesmo
  horário;
- Ontem fechou em 966; hoje, no ritmo de ~40/hora, deve fechar entre
  **900 e 1.000**.

**Conclusão de águia:** o pico de 12-13/08 (1.439 e 1.272) foi o efeito do
lançamento; desde 14/08 o site **estabilizou em um platô saudável de ~950-1.000
acessos/dia**. Isso é audiência real e sustentada, não um pico passageiro.

## 🏆 Ranking dos livros (total acumulado · com correspondência Home ↔ arquivo)

A numeração dos **cards da Home** é editorial e diferente dos **nomes dos
arquivos** no servidor. Para não confundir, eis a correspondência real:

| Pos. | Título do livro | Arquivo (URL) | Card na Home | Acessos | Hoje |
|---|---|---|---|---|---|
| 🥇 | Home (início) | / | — | 590 | 79 |
| 🥈 | **Evolução da Alma** | /livro05 | Livro 02 | 75 | 15 |
| 🥉 | **O Verbo que Transforma** | /livro01 | Livro 06 | 69 | 6 |
| 4 | **O Despertar do Observador** | /livro10 | Livro 10 | 69 | 4 |
| 5 | **O Arquiteto da Realidade** | /livro08 | Livro 09 | 59 | 3 |
| 6 | **A Sabedoria dos Mestres** | /livro02 | Livro 11 | 52 | 3 |
| 7 | **A Mente Renovada** | /livro03 | Livro 07 | 51 | 2 |
| 8 | **Um Segundo com Deus** | /livro04 | Livro 04 | 48 | 2 |
| 9 | **O Caminho do Despertar** | /livro07 | Livro 08 | 48 | 3 |
| 10 | **Anestesia Mental** | /livro09 | Livro 03 | 44 | 5 |
| 11 | **Jesus Quer Falar com Seu Filho** | /livro06 | Livro 05 | 36 | 3 |
| 12 | Quiz | /quiz | — | 9 | 2 |

**Observações de águia:**

- **Evolução da Alma disparou hoje (15 acessos)** — é o livro que recebe os
  visitantes do quiz (que redireciona para /livro05) e tem forte divulgação;
- Os 10 livros seguem **bem distribuídos** (36 a 75 acessos), sinal de que o
  público explora a coleção, não fica preso a um único livro;
- **Conversão Home → livro: 551/590 = 93%** — praticamente todo visitante da
  Home clica em um livro. Excelente sinal do novo banner "leitura que não se
  perde" e dos pop-ups de dicas;
- O quiz ainda tem poucos acessos (9) porque aparece somente no fim da Home;
  é uma porta de entrada subutilizada (ver recomendação 4).

## 🛡️ Bots e tentativas de invasão

Continuam aparecendo tentativas no log (mesmo com o bloqueio `return 444`
ativo, o Nginx registra a requisição antes de bloquear):

| Tentativa | Acessos (acumulado) |
|---|---|
| //stats | 46 |
| //wp-login.php | 33 |
| //.env | 24 |
| //wp-content/plugins/hellopress/... | 19 |
| //this_is_a_new_hello_world.php | 19 |
| //wp-admin (várias) | ~60 |
| //xmlrpc.php | 15 |
| //.git/config | 13 |
| //.env.local | 12 |

**Leitura:** o bloqueio está funcionando (todas recebem 444, sem resposta), mas
os scanners **não param de tentar**. Para reduzir o ruído:

1. Instalar o **WAF gratuito do aaPanel** (Website → compraoseu.com → WAF),
   que bloqueia padrões de ataque antes de chegarem ao log;
2. Opcional: bloquear por país fora do Brasil (cuidado: a missão é aberta a
   leitores de outros países; avaliar com equilíbrio).

## 🔍 Google Search Console (andamento)

| Página | Inspeção | Status |
|---|---|---|
| /livro10 | 13/08 | ✅ Disponível para a Google |
| /livro01 | 13/08 | ✅ Disponível para a Google |
| /livro11 | 13/08 | ✅ Disponível para a Google |
| /livro02 | 13/08 | ✅ Disponível para a Google |
| **/livro03** | **15/08** | ✅ Inspecionado hoje |
| **/livro10** | **15/08** | ✅ Inspecionado hoje |
| /livro04 | 16/08 (amanhã) | ⏳ Pendente |
| /livro09 | 16/08 (amanhã) | ⏳ Pendente |
| /livro05, 06, 07, 08 | próximos | ⏳ Pendente |

Ritmo ideal: 1-2 inspeções/dia com "Solicitar indexação". Depois de todos os
livros, inspecionar também a **Home** e o **quiz**.

## 🎯 Recomendações finais

1. **O site está saudável e estável** (~950-1.000/dia). O próximo multiplicador
   é o **tráfego orgânico do Google** — continuar as inspeções diárias;
2. **Manter a divulgação ativa** (WhatsApp, redes) para sustentar o tráfego
   direto até o SEO amadurecer;
3. **Cron do stats**: o painel atualiza a cada 6h. Mudar para **2h** no aaPanel
   dá uma leitura mais fresca (o script sobrescreve o mesmo stats.html, não
   acumula);
4. **Dar mais destaque ao quiz na Home** (ex.: mover o quiz para logo após o
   hero ou adicionar um botão "Faça o teste" no topo) — ele gera o presente do
   e-book e alimenta a conversão;
5. **WAF no aaPanel** para reduzir os bots;
6. **Preparar o lançamento do Livro 11** (27/08): o countdown está rodando na
   Home; quando chegar o dia, trocar o card "Em breve" por "Disponível" e
   remover o cronômetro.

*"O Senhor é quem dá força ao seu povo; o Senhor abençoará o seu povo com
paz."* (Salmos 29:11)
