# Limpeza da biblioteca — passo a passo (com rede de segurança)

**Objetivo:** tirar do ar os 5 livros que não são de autoria da casa
(risco de direito autoral), sem derrubar nada do que funciona.

**Livros que saem:** O Verbo que Transforma · A Sabedoria dos Mestres ·
A Mente Renovada · O Arquiteto da Realidade · O Despertar do Observador

**Livros que ficam (7):** O Novo Testamento · Evolução da Alma ·
Anestesia Mental · Um Segundo com Deus · Jesus Quer Falar com Seu Filho ·
O Caminho do Despertar · Comece o dia com Afirmações

---

## Antes de tudo: o que o script NÃO faz

- ❌ Não mexe no player da Palavra de hoje
- ❌ Não mexe na enquete
- ❌ Não mexe no quiz
- ❌ Não mexe no banner dos cursos
- ❌ Não mexe no formulário (FormSubmit)
- ❌ Não mexe no compartilhar

E tem três travas: se a Home perder enquete, quiz, banner, biblioteca ou
formulário, **ele mesmo desfaz tudo e avisa**. Nada é gravado.

---

## Passo 1 — Enviar o script

aaPanel → **Files** → `/home/deploy/` → **Upload** →
escolher `APLICAR_LIMPEZA_LIVROS.py` (da pasta consultoria-redes).

## Passo 2 — Simular (só ver o que vai acontecer)

aaPanel → **Terminal** → colar:

```
python3 /home/deploy/APLICAR_LIMPEZA_LIVROS.py --simular
```

Ele mostra tudo o que faria e **não grava nada**.
Leia com calma. Se concordar, vá ao passo 3.

## Passo 3 — Executar de verdade

```
python3 /home/deploy/APLICAR_LIMPEZA_LIVROS.py
```

Vai aparecer uma lista assim:

```
[1/6] Preparando backup ...
[2/6] Removendo os cards da Home
[3/6] Conferindo se a Home continua inteira
[4/6] Limpando o sitemap.xml
[5/6] Limpando o cache do app (sw.js)
[6/6] Movendo os arquivos para fora da pasta publica
```

## Passo 4 — Conferir no navegador

Abra **https://missaocomdeus.com.br** e veja:

- [ ] A biblioteca tem **7 livros**, numerados 01 a 07
- [ ] Os botões dourados continuam lá
- [ ] A enquete continua no pé da página
- [ ] O player da Palavra continua tocando
- [ ] O quiz continua abrindo

Se algo saiu do lugar, vá direto ao **Passo 6** (desfazer).

## Passo 5 — Pedir ao Google para esquecer (feito à mão)

Google Search Console → **Remoções** → **Nova solicitação** → colar estes
endereços, um por um:

```
https://missaocomdeus.com.br/livro01
https://missaocomdeus.com.br/livro02
https://missaocomdeus.com.br/livro03
https://missaocomdeus.com.br/livro08
https://missaocomdeus.com.br/livro10
```

Isso faz o Google tirá-los da busca em poucos dias.

## Passo 6 — Se precisar desfazer (Deus o livre, mas tem)

O script guarda tudo numa pasta com a data. Dentro dela tem um arquivo
**LEIA-ME.txt** com as linhas prontas para copiar e colar. Exemplo:

```
cp /home/deploy/_limpeza-20260902-130000/index.html.bak /www/wwwroot/missaocomdeus.com.br/index.html
```

*(o nome da pasta muda conforme a data e a hora; use a que apareceu no fim
da execução do script)*

---

## Por que mexer no sw.js?

O site é um app (PWA). Quando o irmão instala, o celular **baixa os livros
para o cache**. Se a gente só apagar os arquivos do servidor, quem já
instalou continua abrindo os livros pelo celular, mesmo fora do ar.

Por isso o script tira os 5 endereços do `sw.js` e sobe a versão do cache
(v3 → v4). Assim o celular é obrigado a buscar a lista nova.

---

## Observação honesta sobre os contadores

Os números de "leituras" dos cards estavam inflados por causa desse mesmo
app: cada instalação baixava os 12 livros de uma vez, somando +1 em cada um.
Por isso todos apareciam com números parecidos (285 a 296).

Com a limpeza, os contadores passam a ser mais verdadeiros daqui para frente.

---

## Fica pendente (sem pressa, mas com sinceridade)

**O Caminho do Despertar** e **Comece o dia com Afirmações** ficaram no ar,
mas na memória da casa eles também estão marcados como "fora do selo Da
Missão". Vale o senhor confirmar, com calma, se são escritos pela casa ou se
têm trechos de outros autores. Se tiverem, a mesma limpeza se aplica.

---

«Se o Senhor não edificar a casa, em vão trabalham os que a edificam.» (Salmo 127:1)
