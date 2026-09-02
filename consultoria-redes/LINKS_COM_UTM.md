# Links marcados (UTM) para saber de onde o irmão veio

WhatsApp, Instagram e TikTok **não avisam** ao site de onde a pessoa clicou.
Sem marcação, ela entra no painel como «Direto».

Com a marcação, o painel `/stats` mostra a origem certinha. É só copiar e colar.

> Regra: use estes links **para compartilhar** (bio, stories, grupos, descrição do vídeo).
> Dentro do site, os links continuam limpos, sem marcação.

---

## Instagram (bio e stories)

```
https://missaocomdeus.com.br/?utm_source=instagram&utm_medium=social&utm_campaign=bio
```

Devocional de 30 dias (o botão dourado da Home):

```
https://missaocomdeus.com.br/livro04?utm_source=instagram&utm_medium=social&utm_campaign=bio
```

O Novo Testamento como nunca lido:

```
https://missaocomdeus.com.br/livro11?utm_source=instagram&utm_medium=social&utm_campaign=nt
```

---

## TikTok (bio e vídeos)

```
https://missaocomdeus.com.br/?utm_source=tiktok&utm_medium=social&utm_campaign=bio
```

```
https://missaocomdeus.com.br/livro11?utm_source=tiktok&utm_medium=social&utm_campaign=nt
```

---

## WhatsApp (grupos, listas, status)

```
https://missaocomdeus.com.br/?utm_source=whatsapp&utm_medium=social&utm_campaign=grupos
```

```
https://missaocomdeus.com.br/livro04?utm_source=whatsapp&utm_medium=social&utm_campaign=grupos
```

---

## YouTube (descrição dos vídeos e comentário fixado)

```
https://missaocomdeus.com.br/?utm_source=youtube&utm_medium=social&utm_campaign=descricao
```

```
https://missaocomdeus.com.br/livro11?utm_source=youtube&utm_medium=social&utm_campaign=nt
```

---

## E-mail e formulário (FormSubmit)

```
https://missaocomdeus.com.br/?utm_source=newsletter&utm_medium=email&utm_campaign=casa
```

---

## Pontes (aulas)

```
https://missaocomdeus.com.br/trilogia-da-alma?utm_source=instagram&utm_medium=social&utm_campaign=trilogia
```

```
https://missaocomdeus.com.br/anestesia-mental?utm_source=whatsapp&utm_medium=social&utm_campaign=anestesia
```

---

## Como trocar a marcação

O que vale para o painel é só este pedaço: `utm_source=`

| O senhor escreve | O painel mostra como |
|---|---|
| `utm_source=instagram` | Instagram / Facebook |
| `utm_source=facebook` | Instagram / Facebook |
| `utm_source=tiktok` | TikTok |
| `utm_source=youtube` | YouTube |
| `utm_source=whatsapp` | WhatsApp |
| `utm_source=google` | Google (busca / SEO) |
| `utm_source=compraoseu` | Site antigo compraoseu.com |
| `utm_source=newsletter` | E-mail / lista |

As outras duas partes (`utm_medium` e `utm_campaign`) pode deixar como estão.
`utm_campaign` serve para separar, por exemplo, `bio` de `stories`.

---

## Cuidado bom de ter

Antes de sair compartilhando links marcados, rode o `APLICAR_CANONICAL.py`
(está explicado no `COMO_ATIVAR_ORIGEM.md`, passo 6). Ele diz ao Google qual é o
endereço oficial de cada página, e aí os links marcados não viram «página repetida».

Se não rodar, também não é o fim do mundo: os links continuam funcionando,
só fica menos arrumado para o SEO.
