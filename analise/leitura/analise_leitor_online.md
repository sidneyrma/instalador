# Análise: Tecnologias para o Leitor Online dos Livros (sem abrir mão da proteção)

> Amado irmão em Cristo, esta análise responde ao pedido de melhorar a leitura dos
> nossos livros na web: marcar onde o leitor parou, aumentar e diminuir as letras,
> e mostrar dicas de leitura em balões pequenos no topo, tudo isso **mantendo a
> proteção dos direitos autorais** (bloqueio de cópia, seleção e impressão).
>
> "Examinai tudo; retende o que é bom." (1 Tessalonicenses 5:21)

---

## 1. Resumo em uma frase

Todas as três funcionalidades podem ser feitas com **HTML5, CSS3 e JavaScript
puro (vanilla)**, sem depender de nenhum servidor, nenhum plugin e nenhuma
biblioteca externa. Os dados do leitor ficam salvos **no próprio aparelho do
leitor** (localStorage), o que é rápido, privado e gratuito.

---

## 2. As tecnologias disponíveis hoje

| Tecnologia | O que é | Suporte | Papel no nosso leitor |
|---|---|---|---|
| **Web Storage API (localStorage)** | Guarda pequenos dados no navegador do usuário, mesmo depois de fechar a página | 100% dos navegadores modernos (Chrome, Safari, Edge, Firefox, navegadores de celular) | Salva a posição de leitura, o tamanho da letra e as dicas já vistas |
| **sessionStorage** | Igual ao localStorage, mas apaga ao fechar a aba | 100% | Opcional: lembrar só da sessão atual |
| **IntersectionObserver** | Detecta qual trecho da página está visível na tela, sem travar o navegador | 100% dos navegadores desde 2019 | Descobre em qual capítulo o leitor está para salvar a posição |
| **Evento scroll + scrollTo** | Percebe a rolagem e pode mover a página até um ponto exato | 100% | Salva o ponto exato e devolve o leitor a ele ao reabrir |
| **CSS Custom Properties (variáveis)** | Define valores como `--tamanho-fonte` e troca com um clique | 100% | Aumenta e diminui a letra instantaneamente, em todo o texto |
| **CSS `clamp()` + `rem`** | Tamanhos de letra fluidos, que respeitam a tela | 100% | Base do conforto de leitura no celular |
| **Toast / balão CSS+JS** | Pequena caixinha que aparece e some sozinha | 100% | Dicas de leitura no topo, sem incomodar |
| **Service Worker (PWA)** | Já usamos no site; permite abrir os livros offline | 100% dos navegadores modernos | O livro continua abrindo sem internet, e o marcador continua funcionando |

**Conclusão técnica:** nada de novo precisa ser comprado ou instalado. Tudo o que
pedimos já existe nos navegadores de hoje, e o custo de processamento é zero
(fica tudo no aparelho do leitor).

---

## 3. As três funcionalidades, uma a uma

### 3.1. Marcador de leitura (voltar de onde parou)

**Como funciona:**
1. Enquanto o leitor rola a página, o navegador percebe em qual capítulo ele está
   (IntersectionObserver) e qual é a altura exata da rolagem (evento scroll).
2. A cada poucos segundos, isso é guardado no aparelho do leitor (localStorage),
   com uma chave por livro, por exemplo: `despertar_progresso_livro05`.
3. Quando o leitor reabre a página, um **balão aparece no topo**: "Você parou no
   Capítulo 3. Continuar de onde parei?".
4. Ao tocar, a página desce exatamente para o ponto salvo.
5. O leitor também pode tocar em um marcador manual, se quiser guardar um trecho
   específico (marcador de livro de verdade).

**O que é guardado (exemplo real):**
```
despertar_progresso_livro05 = {
  "secao": "capitulo-3",
  "titulo": "Capítulo 3: A criança interior",
  "scrollY": 12480,
  "porcentagem": 42,
  "data": "2026-08-15T21:30:00-03:00"
}
```

**Observação importante:** a posição de leitura é um número (altura da rolagem),
**não é texto do livro**. Ou seja, o marcador não copia nem expõe conteúdo algum;
a proteção de direitos autorais permanece intacta.

**Limitações honestas:**
- O marcador fica no aparelho do leitor. Se ele trocar de celular ou limpar os
  dados do navegador, o progresso some. (Isso é uma vantagem para nós: nenhum
  texto sai do nosso site e nada é armazenado no nosso servidor.)
- Se o leitor usar o modo anônimo do navegador, o marcador dura só enquanto a
  aba estiver aberta (limitação do próprio navegador, sem solução, e é até bom
  para a proteção).

### 3.2. Aumentar e diminuir as letras

**Como funciona:**
1. No topo da página, dois botões discretos: **A−** e **A+** (e um botão de
   voltar ao tamanho original, "A").
2. O texto inteiro do livro usa uma variável CSS única, `--tamanho-fonte`.
   Ao tocar em A+, a variável cresce (ex.: 100% → 112% → 125% → 140%).
3. O navegador redesenha o texto na hora; não precisa recarregar a página.
4. O tamanho escolhido fica salvo no aparelho; na próxima visita, o livro já
   abre no tamanho que o leitor escolheu.
5. Limites seguros: de 90% até 160%, para nunca quebrar o desenho da página.

**Por que funciona bem no celular:** o texto do livro já usa medidas relativas
(rem), então a mudança de uma única variável altera tudo: título, parágrafo,
citações e versículos, todos juntos e proporcionais.

### 3.3. Dicas de leitura em balõezinhos no topo

**Como funciona:**
1. Na primeira vez que o leitor abre um livro, aparecem 2 ou 3 balões pequenos
   no topo, um depois do outro, cada um por alguns segundos:
   - "📖 Sua leitura fica salva aqui. Feche e volte quando quiser."
   - "🔍 Toque em A+ para aumentar as letras."
   - "📍 Use o marcador para não perder o ponto onde parou."
2. Cada balão some sozinho e pode ser fechado com um X.
3. Depois de mostrados, o sistema lembra (localStorage) e não mostra de novo,
   para não incomodar. Se o leitor quiser rever, há um botão "💡 Dicas" no topo.
4. No nosso caso, o balão de "Você parou no Capítulo X" também aparece no topo,
   junto com as dicas, sem disputar espaço.

---

## 4. Como isso se encaixa na proteção atual (direitos autorais)

A proteção existente continua de pé, sem nenhuma mudança:

| Proteção atual | Status |
|---|---|
| `user-select: none` (não seleciona texto) | Mantida |
| Bloqueio do menu do botão direito (contextmenu) | Mantido |
| Bloqueio de Ctrl+C, Ctrl+P, Ctrl+S | Mantido |
| Impressão bloqueada com aviso (media print) | Mantida |
| Conteúdo servido do nosso servidor (sem API pública de texto) | Mantido |

As novidades **não** copiam, exportam ou expõem o texto; elas apenas movem a
página e mudam o tamanho da letra, como um leitor de PDF faz. O texto em si
nunca é armazenado fora da nossa página.

---

## 5. Plano de implementação (quando o senhor aprovar)

1. **Criar o módulo compartilhado** (um único arquivo `leitor.js` + estilos):
   barra de progresso, marcador, A−/A+/A, dicas e balões. Fica igual em todos
   os livros, o que facilita a manutenção.
2. **Aplicar em um livro piloto** (sugestão: livro de Afirmações ou Livro 05),
   testar no celular e ajustar.
3. **Aplicar nos demais livros** (livro01 a livro10, livro11 e livro de
   Afirmações), um por um, conferindo que a proteção continua ativa.
4. **Na Home**, adicionar um pequeno aviso "Você estava lendo: O Verbo que
   Transforma, Capítulo 4. Continuar?" para o leitor voltar em um toque.
5. **Versões do autor** (sem proteção): podem receber o mesmo leitor, com a
   opção extra de marcar e anotar trechos.

---

## 6. Considerações finais e honestidade total

- **Custo:** zero reais. Não precisa de servidor novo, plugin ou assinatura.
- **Privacidade:** nada é enviado para nós; o progresso fica no aparelho do
  leitor. Isso é bom para o leitor e bom para a proteção da obra.
- **Simplicidade:** um único arquivo de JavaScript por livro, sem dependências.
  Se um dia quisermos sincronizar o progresso entre aparelhos (ex.: via login),
  aí sim precisaríamos de um pequeno serviço; mas para hoje, não é necessário.
- **Risco baixo:** as APIs usadas são estáveis desde 2019; funcionam no
  WhatsApp Web, Instagram, Chrome, Safari e navegadores de celular.

> "O coração do sábio ensina a sua boca, e acrescenta doutrina aos seus lábios."
> (Provérbios 16:23)

---

## 7. Próximo passo

O protótipo funcional está em `paginas/leitor_demo_preview.html`. Nele o senhor
pode testar, no celular e no computador:

1. Rolar até um capítulo, fechar a página e reabrir: aparece "Continuar de onde
   parei".
2. Tocar em A+ e A−: a letra cresce e diminui, e o tamanho fica lembrado.
3. Ver os balões de dicas na primeira abertura.
4. Ver a barrinha de progresso dourada no topo.

---

## 8. Verificação vasta e profunda: o que os grandes leitores fazem

A pedido do nosso leitor, fiz uma verificação aprofundada do que a tecnologia de
leitura usa hoje para ninguém se perder. Os grandes leitores digitais (Kindle,
KOReader e outros) mostram o caminho:

| Recurso | Kindle | KOReader | O que é, em linguagem simples |
|---|---|---|---|
| **Porcentagem e minutos restantes** | Sim | Sim | "Você leu 42% do livro, faltam cerca de 12 minutos" [1](https://www.reddit.com/r/kindle/comments/1arherk/how_to_make_the_minutes_left_and_percentage_show/) |
| **Barra de progresso com marcas de capítulo** | Sim | Sim | Uma barrinha fina no rodapé ou na lateral, com pontinhos para cada capítulo; tocar em um pontinho salta até ele [2](https://koreader.rocks/user_guide/pt_BR.html) |
| **Voltar para a localização anterior** | Sim | Sim | Se o leitor pulou para outro capítulo e quis voltar, um toque o devolve ao ponto exato [2](https://koreader.rocks/user_guide/pt_BR.html) |
| **Marcador de livro (bookmark)** | Sim | Sim | Equivale a dobrar a página ou colocar uma faixa; fica gravado e pode ser acessado depois |
| **Sincronização entre aparelhos** | Sim | Parcial | O Kindle guarda no servidor: se a pessoa lê no celular e depois abre no tablet, continua de onde parou [3](https://gizmodo.com/download/amazon-kindle) |
| **Notas e marca-texto** | Sim | Sim | O leitor grifa um trecho com a cor e pode até escrever uma anotação |

**Tradução para a nossa realidade:** tudo isso, exceto a sincronização entre
aparelhos (que exige login e servidor), pode ser feito com **JavaScript puro +
localStorage**, sem custo e sem abrir mão da proteção. A sincronização entre
aparelhos é o único recurso que exigiria criar uma conta para o leitor; fica
como evolução futura, se o senhor quiser.

## 9. O Leitor do Despertar (visão completa do que podemos criar)

Resumo em uma frase: **transformar cada livro em um "Kindle do Despertar", com
todos os recursos de conforto de leitura, mas com o texto sempre fechado dentro
da nossa página protegida.**

Recursos propostos, em ordem de prioridade:

1. **Lembrar onde parou** (automático): ao reabrir, balão "Continuar de onde
   parei". Já implementado no protótipo.
2. **A− / A / A+**: tamanho da letra ajustável e lembrado. Já implementado.
3. **Fita dourada (🎗️)**: equivalente a dobrar a página. O leitor toca no
   botão e uma fitinha dourada fica na lateral; ao voltar, toca na fita e salta
   direto para aquele trecho.
4. **Trilha de capítulos na lateral**: pontinhos dourados, um para cada
   capítulo; o ponto do capítulo atual brilha, os já lidos ficam cheios, e tocar
   em um pontinho salta até ele (igual à barra do KOReader).
5. **Estatística de leitura no topo**: "Capítulo 3 · 42% · faltam ~12 minutos".
6. **Sumário com marcas**: cada capítulo do sumário ganha um ✓ quando é lido e
   "você está aqui" no capítulo atual (como marcar com marca-texto no sumário de
   um livro físico).
7. **Modos de tela**: Dia (papel claro), Sépia (amarelado, conforto noturno) e
   Noite (fundo escuro), para a vista do leitor.
8. **Balões de dicas** na primeira visita, sem incomodar depois. Já
   implementado.
9. **"Continue lendo" na Home**: a página inicial mostra um cartãozinho
   "Você estava em: O Verbo que Transforma, Capítulo 4. Continuar?" (evolução
   futura, depois dos itens 1 a 8).
10. **Compartilhar capítulo**: botão que envia o link com o capítulo (não o
    texto) para WhatsApp, usando a API de compartilhamento do celular. Ótimo
    para divulgação orgânica.

**Como a proteção permanece intacta:** nenhum desses recursos copia, exporta ou
expõe o texto. Eles guardam apenas números (posição da rolagem, porcentagem,
tamanho da letra) no aparelho do leitor. O texto continua 100% dentro da nossa
página, com seleção, clique direito, atalhos e impressão bloqueados.

**Tecnologia resumida em uma palavra: localStorage.** É a memória do navegador
que guarda pequenos dados por site; suportada por praticamente todos os
navegadores modernos, com limite em torno de 5 MB por domínio, mais do que
suficiente para posições de leitura [4](https://codigofacil.com.br/localstorage-e-o-sessionstorage/). Para anotações longas no futuro,
existe o IndexedDB (banco de dados dentro do navegador) e, para sincronizar
entre aparelhos, um pequeno serviço com login. Nada disso é necessário agora.

## 10. Protótipo avançado (v2)

O arquivo `paginas/leitor_demo2_preview.html` implementa os itens 1 a 8 desta
visão. O senhor pode testar no celular:

1. Role, feche a página e reabra: "Continuar de onde parei".
2. Toque em **🎗️ Fita** no meio da leitura: a fitinha dourada aparece na
   lateral; role para longe e toque na fita: você volta.
3. Veja a **trilha de capítulos** na lateral direita: pontinhos para cada
   capítulo; toque em um para pular; o capítulo atual fica dourado.
4. Veja no topo: "Capítulo X · Y% · ~Z min restantes".
5. No sumário, os capítulos lidos ganham ✓ e o atual mostra "você está aqui".
6. Toque em **🎨** para alternar Dia / Sépia / Noite (fica lembrado).
7. A− / A+ continuam funcionando, com a letra lembrada.
8. Toda a proteção continua ativa (sem seleção, sem clique direito, sem
   imprimir).

## 11. Aplicado no livro de Afirmações (piloto)

O leitor foi integrado ao **livro de Afirmações**, gerando o arquivo
`paginas/livro_afirmacoes_leitor_preview.html` pelo script
`analise/compraoseu.preview/integrar_leitor_afirmacoes.py`.

O que o piloto inclui, em cima do conteúdo já purificado:

- 14 seções de leitura (Abertura, Gratidão, 8 categorias, Orações do dia,
  Versículos, Como usar e Orações de Fé em FAQ).
- Lembrar onde parou, com balão "Continuar de onde parei" ao reabrir.
- Fita dourada lateral, trilha de seções (14 pontinhos), A− / A / A+,
  modos Dia / Sépia / Noite, balões de dicas e sumário com ✓ e "aqui".
- Barra de progresso dourada no topo e estatística "Seção · % · faltam ~min".
- **Proteção ativada**, como ficará no site: sem seleção, sem clique direito,
  sem Ctrl+C/P/S e impressão bloqueada com aviso.
- FAQ das 10 Orações de Fé preservado (toca para abrir e fechar).

A versão original `paginas/livro_afirmacoes_preview.html` (avaliação, sem
proteção) permanece intacta para o senhor marcar e copiar à vontade.

Quando o senhor aprovar, aplicamos o mesmo leitor aos demais livros
(livro01 a livro11), sempre conferindo a proteção um por um.

## 12. Aplicado em todos os livros (atualização geral)

Com a aprovação do piloto, o Leitor do Despertar foi aplicado em **todos os
livros** do Portal:

- `paginas/livro01` a `livro10_leitor_preview.html` — versões com leitor e
  proteção ativa (como ficará no site), para conferência.
- `paginas/livro11_leitor_preview.html` — versão com leitor, **sem proteção**
  (versão do autor em avaliação, para marcar e copiar).
- `site-contabo/livro01.html` a `livro11.html` — páginas publicadas atualizadas
  no lugar, prontas para envio ao servidor.
- O livro de Afirmações já havia recebido o leitor
  (`paginas/livro_afirmacoes_leitor_preview.html`).

Gerador: `analise/compraoseu.preview/integrar_leitor_livros.py` (processa
previews e site-contabo em um único comando).

Verificações finais (23 arquivos):

- JavaScript válido em todos (node --check).
- Trilha de seções por livro: 14 (livro01), 13 (livro02), 22 (livro03),
  31 (livro04), 33 (livro05), 15 (livro06, incluindo os 10 mandamentos),
  15 (livro07), 17 (livro08), 30 (livro09), 40 (livro10), 23 (livro11).
- Sumário com marcas ✓/▶ em todos.
- Proteção conforme o estado de cada arquivo: livros 01 a 10 e Afirmações
  protegidos; livro 11 sem proteção (versão do autor).

Observação honesta: alguns livros (03, 07 e 10) ainda contêm travessões e
asteriscos herdados da formatação original do conteúdo (não introduzidos pelo
leitor). A limpeza dessas marcas é uma tarefa à parte, a combinar com o autor
antes de tocar no conteúdo.

## 13. Home com "Continue lendo" e página EU SOU

- **Home** (`paginas/home_preview.html` e `site-contabo/index.html`): adicionado
  o cartão dourado **"Continue lendo"** abaixo do hero. Ele lê o progresso
  salvo em cada livro (localStorage `despertar_progresso_livroXX`) e mostra o
  livro, a seção, a posição percentual e o botão "Continuar lendo →", levando o
  leitor direto à página. Aparece somente quando há progresso salvo; sem
  progresso, a Home permanece igual.
- **Estudos EU SOU** (`paginas/eusou_estudos_leitor_preview.html`): gerada a
  versão com leitor (7 seções), sem proteção (versão de estudo do autor).
- Correção importante aplicada nos dois geradores: os itens do sumário agora
  recebem o `<span class="marca">` e o JavaScript ficou defensivo (não lança
  erro se o marcador não existir), garantindo o funcionamento da marcação
  "✓ lido" e "▶ aqui" em todas as páginas.
