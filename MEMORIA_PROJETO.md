## INFRA

- VPS Contabo `212.28.182.86` Ubuntu 22.04.5, Nginx, PHP 8.1.32, aaPanel, ~15 GB RAM.
- Vivo: `missaocomdeus.com.br` → `/www/wwwroot/missaocomdeus.com.br/`
- compraoseu.com: só 301 + SSL (GSC mudança de endereço aprovada 21/08). Não desligar. Não esvaziar o 301.
- PM2: `conectai-apioficial` :6000, `conectai-backend` :4000, `conectai-frontend` :3000.
- FormSubmit: `portalmissaocomdeus@gmail.com.
- Stats cron: `python3 /home/deploy/gerar_estatisticas.py` → `stats.html` + `leituras.json`
---
## CONTATOS E REDES (público)
- WhatsApp: `5528999111493`
- YouTube: `@vivaamissaocomdeus
- Instagram: https://www.instagram.com/vivaamissaocomdeus/ 
- TikTok da Missão: https://www.tiktok.com/@vivaamissaocomdeus (~4k)
- E-mail casa: portalmissaocomdeus@gmail.com

- # Memória da Missão com Deus

Atualizado em 24 de setembro de 2026, Brasília.

Site vivo: https://missaocomdeus.com.br

Este arquivo é o chão do próximo chat. Leia inteiro antes de escrever ou mexer no site. O que está aqui é o que está no ar hoje. Se um nome, um preço ou um produto não aparece neste texto, não use.

A honra é do Senhor.

Como começar o próximo chat:

Continuar a Missão com Deus. Site vivo missaocomdeus.com.br. Leia MEMORIA_PROJETO.md de 24/09/2026.

A verdade do site está no servidor, pasta `/www/wwwroot/missaocomdeus.com.br/`. O GitHub (sidneyrma/instalador) é espelho atrasado. Não trate o GitHub como o ar.

---

## 1. Quem é o autor e como servir

O autor é irmão em Cristo, dono da Missão. Não é técnico avançado. Fale em português do Brasil, com calma, um passo de cada vez. Trate-o por amado irmão, irmão em Cristo Jesus. Não se apresente como anjo. Você é servo que ajuda no site e nos textos.

Um pedido, um passo. Não empilhe tarefas. Não peça senha, token ou acesso ao GitHub.

No aaPanel, Terminal: só 2 linhas, digitadas. Se o Terminal mostrar o nome do script entre colchetes azuis, não clique. Isso gera `can't open file ... Errno 2`. Digite o nome do `.py`.

Nunca use `cat >>` em HTML. Envie o `.py` e os HTML que o script precisa antes de pedir para rodar. Script faz backup sozinho. Se a string não achar, não grava. Segunda execução diz que já estava.

Não substitua `index.html` nem o miolo de um livro inteiro no servidor. Isso apaga banner, quiz, enquete e player.

Antes de recarregar Nginx: `nginx -t`.

---

## 2. Padrão de linguagem da Missão

Isto não é “regra interna”. É o jeito de escrever para o público e para o autor.

- Português do Brasil, com acentos.
- Frase de gente. Curta. Clara. Como conversa franca.
- Não use travessão (o traço longo nem o médio) em copy nova, FAQ, botão, carrossel, WhatsApp ou explicação. Use vírgula, ponto ou dois pontos.
- Prefira “você”. Não use “sincera(o)”, “bem-vind(o)a”, nem pares com barra de gênero em texto novo.
- Sem depoimento inventado.
- Sem cura pronta. A Missão oferece caminho, no ritmo de cada um.
- A Palavra primeiro. Leitura grátis antes de falar de pagamento.
- A marca pública é **Missão com Deus**. O irmão lê “Missão”, “portal”, “livros”, “acesso completo”. Não use gíria de bastidor no texto que ele lê.
- No quiz da família, a frase “minha casa” (versículo e pergunta) permanece, porque é da Palavra e do roteiro.
- Sexualidade no quiz da família: um pingo. Ouça. Sem catálogo. Sem ato. Sem perguntar “você é o quê?”.

Se uma IA anterior usou outro vocabulário, ignore. Use só o deste arquivo.

---

## 3. O que a Missão é

A Missão com Deus oferece leitura cristã, áudio da Palavra, videoaulas e um caminho de estudo. Fé cristã no centro. A mente e o coração entram como cuidado, não como espetáculo.

Laura é figura criada para a Missão, com apoio de tecnologia. Não é pessoa de carne. Não é mentora humana. Não é anjo. Quando perguntarem quem ela é: a honra é do Senhor. História: https://missaocomdeus.com.br/nossa-missao

Não publicar a obra “Poder do Eu Sou”.

---

## 4. Funil e preço (o que está no ar)

1. Home e livros: Palavra e leitura.
2. Quem quer o conjunto vai para https://missaocomdeus.com.br/guardar
3. Quem confirma o pagamento vai para a Kiwify: https://pay.kiwify.com.br/iVfp2bi

Um pagamento: **R$ 57,00**. Pix na hora ou cartão em até 4x. Garantia de 7 dias pela Kiwify. Acesso vitalício. Chega por e-mail da Kiwify. Sem mensalidade.

O acesso completo reúne:

- as 8 obras em arquivos digitais
- 14 módulos em vídeo (7 da Trilogia, 7 da Anestesia)
- exercícios e comunidade
- 30 áudios das mensagens diárias
- conteúdos para Pais e Filhos
- novos conteúdos digitais no mesmo acesso, sem cobrança nova

Valores de referência na página `/guardar` (não são preço de venda avulso): Evolução 47, Anestesia 47, Um Segundo 19, Jesus Filho 19, Caminho 47, NT 49, Afirmações 19, Guia Pais e Filhos 37, cada curso 47, exercícios 15, comunidade 15, 30 áudios 27, lançamento futuro incluso. Soma de referência 435. Pagamento 57.

Códigos das aulas 1 a 3:

- Trilogia: `EVLTRLAM26` · https://missaocomdeus.com.br/trilogia-da-alma
- Anestesia: `NSTMNT26` · https://missaocomdeus.com.br/anestesia-mental

O código não abre os módulos 4 a 7. Esses ficam no acesso completo.

Página de obrigado: https://missaocomdeus.com.br/obrigado  
PDF do NT nessa página: `/ebooks/livro11-o-n-t.pdf`

Não receba cartão no site da Missão. Checkout só na Kiwify.

---

## 5. As oito obras

Ordem da biblioteca na Home:

| Rota | Obra | Leitura no site |
|---|---|---|
| `/livro11` | O Novo Testamento como nunca lido | janela (veja §6) |
| `/livro05` | Evolução da Alma | janela |
| `/livro09` | Anestesia Mental | janela |
| `/livro04` | Um Segundo com Deus | inteiro sempre |
| `/livro06` | Jesus Quer Falar com Seu Filho | inteiro sempre |
| `/livro07` | O Caminho do Despertar | janela |
| `/livro12` | Afirmações, Declarações e Orações | inteiro sempre |
| `/livro08` | Guia Pais e Filhos: Construindo um Futuro | janela, já no ar |

Capa pedida do 08: `https://i.ibb.co/b5XXwH4M/livro08.jpg`

O 08 público é o Guia Pais e Filhos. Não trate essa rota como outro título antigo.

Fora da Home (HTML pode existir no disco, sem card): 01, 02, 03, 10.

Não adulterar o miolo original do livro 08 sem pedido explícito do autor. Vestimenta (sumário, nav, proteção, trava, leitor) sim.

---

## 6. Leitura aberta e janela

A leitura gratuita continua. A quantidade aberta pode variar conforme o período.

Até 30/09/2026 00:00 Brasília, estas obras abrem por inteiro no site: Evolução da Alma, Anestesia Mental, O Caminho do Despertar, O Novo Testamento, Guia Pais e Filhos.

Quando a janela termina, voltam ao formato habitual: cerca de 40% livres, o restante no acesso completo. 04, 06 e 12 continuam inteiros.

Na copy pública, explique a regra de forma genérica (abertura temporária, retorno a cerca de 40%). A data da campanha atual pode aparecer no banner com a contagem. Não escreva “estão abertos agora” em texto que vai envelhecer sozinho. Não diga que a leitura gratuita some. Ela continua, em parte.

O acesso completo não depende dessas datas.

---

## 7. Home (como está)

Hero: “Começar o Devocional de 30 dias” (`/livro04`) e “Conhecer Pais e Filhos” (`/guia-pais-filhos`). Sem botão de preço na primeira dobra.

Player da Palavra de hoje: círculo 36px, anéis, sem autoplay. Não rodar `APLICAR_PLAYER_SHARE_BOTAO.py`.

WhatsApp flutuante: ícone próprio, ondas. Número `5528999111493`.

Biblioteca: uma grade, 8 cards, números de leitura via `/leituras.json` (só no ar, precisa de internet). Botões: Ler grátis ou Ler a prévia grátis, e Acesso completo por R$ 57 (`/guardar`). Card 08: Conversas vai para `#pais-filhos`.

Menu: sem o item duplicado “Livros”. Fica Biblioteca gratuita. Já tenho acesso: entrar no Portal (painel Kiwify). Ainda não tem acesso → `/guardar`. Ícones SVG.

FAQ próprio: diferença entre leitura gratuita e acesso completo.

Banner de cursos (`#cta-cursos`): texto curto, botão ouro para `/guardar`, aulas, Falar com a Laura. Não é o único caminho de compra.

Rodapé: Nossa Missão, e-mail, WhatsApp, TikTok `@portalmissaocomdeus`, Instagram https://www.instagram.com/vivamissaocomdeus, Facebook https://www.facebook.com/livrosmissaocomdeus

Página da Missão no Facebook: 60 dias sem anúncio. Link no rodapé pode ficar. Campanha paga, por agora, no Instagram.

Não turbinar post pelo app do Instagram com destino WhatsApp: a arte e a legenda grudam na conversa e a Laura não lê a pergunta. Anúncio de mensagem: Gerenciador de Anúncios, quebra-gelo em texto limpo.

Termômetro da Alma: 6 perguntas na Home (diagnóstico). Outra peça, não confundir com o quiz da família.

Enquete: `#enquete`. Não apagar `enquete_dados.json`.

---

## 8. Página /guardar

Preço 57. Checkout `iVfp2bi`. Animação do preço usa 57.

Oito cards de obras. Grade: 4 colunas no computador, 2 no celular.

Leitura aberta temporária explicada no FAQ e no aviso após os cards grátis e vitalício. Lista das obras que podem participar de período integral, em linguagem que não envelhece.

Perto do 57: o acesso completo permanece quando uma abertura temporária termina.

Último fecho: um só parágrafo no valor de referência (sem repetir embaixo). CTAs com chave SVG.

---

## 9. Pais e Filhos

Roteiro dos filhos: https://missaocomdeus.com.br/guia-pais-filhos e bloco na Home `#pais-filhos` (8 perguntas).

Espelho (pais): `/guia-pais-filhos-espelho` (8 perguntas, uma a uma).

Livro: `/livro08` já no ar, com leitor, sumário, trilha, trava 30/09/2026 00:00 Brasília (livre até o capítulo 4; do 5 em diante o portão leva a `/guardar` quando a janela fecha).

Quiz da Home para o guia: botão na capa do livro, linha no sumário, banner da Laura.

Não reescrever o texto original do autor no miolo do 08.

---

## 10. Laura (WhatsApp)

Número: 5528999111493

Flow: Início → OpenAI Permanente. Sem bloco “um momento” no meio. Sem Transferir / Setor por dúvida. Temp 0,7. Tokens 800.

Prompt no ar a usar: **V19** (`PROMPT_LAURA_V19.txt`). Encerrar tickets ao colar. Teste em conversa nova:

1. “Olá, quero saber mais sobre o Portal Missão com Deus.” → uma pergunta (já leu ou chegou agora). Sem panfleto.
2. “Sobre o guia pais e filhos Laura pode me dizer alguma coisa” → os dois links (`/guia-pais-filhos` e `/livro08`). Sem transferir.

Instagram que chega no WhatsApp com imagem: a pergunta vem presa na arte. A Laura muitas vezes não dispara. Abrir a conversa e responder o tema do post (quiz e Guia), não o panfleto do portal.

Não transfere por livro, guia, pais e filhos, preço, oração ou “pode me dizer”. Transfere só se pediram gente de carne, xingamento grave, CNPJ, ou três tentativas concretas e ainda pedem uma pessoa.

Bolhas curtas. Sem travessão. “Você”. Nome só se a pessoa disse o nome.

---

## 11. Contatos e redes

- WhatsApp: 5528999111493
- E-mail: portalmissaocomdeus@gmail.com
- Instagram: https://www.instagram.com/vivamissaocomdeus
- TikTok: https://www.tiktok.com/@portalmissaocomdeus
- YouTube: @portal.o.despertar (não embutir o vídeo `Ot6CRgd_nYY`)
- Facebook: https://www.facebook.com/livrosmissaocomdeus (página quieta para anúncio por 60 dias)

FormSubmit público: portalmissaocomdeus@gmail.com

---

## 12. Como aplicar mudança no site

A pasta pública do site é `/www/wwwroot/missaocomdeus.com.br/`. O GitHub não é o ar.

1. Backup automático no script.
2. Subir o `.py` e o HTML necessário.
3. Duas linhas no Terminal:

```
cd /www/wwwroot/missaocomdeus.com.br
python3 NOME_DO_SCRIPT.py
```

4. Conferir no ar (celular e notebook), não só no painel sem internet.

Não apague a enquete. Não mude URL de API ou webhook da Laura. Não publique overlay no YouTube.

Painel de números: https://missaocomdeus.com.br/stats.html  
`/palavra`, `/stats` e `enquete.php` ficam sem índice e sem menu.

---

## 13. Carrossel e anúncio

Copy de campanha: 8 obras, R$ 57, leitura grátis primeiro, Laura não é mentora de carne. Acentos. CTA ouro.

Arquivo de referência do carrossel Anestesia: `CARROSSEL_ANESTESIA_CORRIGIDO.md`

---

## 15. Frase de ouro da oferta

A leitura gratuita continua disponível. Em alguns períodos, determinadas obras podem ser abertas integralmente. Essa liberação é temporária. Quando ela termina, a leitura aberta volta a cerca de 40%. O acesso completo, por R$ 57, garante as oito obras inteiras, os módulos, os exercícios, os áudios, os conteúdos para Pais e Filhos e a comunidade, sem depender dessas datas.
