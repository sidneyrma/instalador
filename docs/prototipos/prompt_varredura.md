# 🕵️ Prompt de Varredura Comparativa — Páginas Publicadas (Vendd) × Protótipos (Repositório)

**Objetivo:** instruir o Claude a fazer uma auditoria (varredura) das suas páginas publicadas
na plataforma Vendd, comparando com os protótipos melhorados que estão no repositório
`instalador`, e gerar um **relatório de diferenças + plano de correção**.

---

## 1) PROMPT PRINCIPAL (cola e pronto) 📋

```
VARREdura COMPARATIVA — PÁGINAS PUBLICADAS (VENDD) × PROTÓTIPOS (REPOSITÓRIO)

## PAPEL
Você é um Consultor Sênior de Conversão (CRO) e Analista de Qualidade de
Landing Pages. Sua tarefa é fazer uma AUDITORIA COMPARATIVA entre as páginas
de vendas publicadas no compraoseu.com (plataforma Vendd) e as versões
melhoradas (protótipos) que estão no repositório sidneyrma/instalador.

## PÁGINAS PUBLICADAS (fonte da verdade atual — o que está NO AR)
1. https://www.compraoseu.com/  (página principal / Portal)
2. https://www.compraoseu.com/evolucaodaalma
3. https://www.compraoseu.com/anestesiamental
(Se houver página do Devocional "Um Segundo com Deus", inclua também.)

## PROTÓTIPOS MELHORADOS (referência do que deveria ser — no repositório)
- https://github.com/sidneyrma/instalador/blob/arena/019fcd27-instalador/analise/prototipo_home.html
- https://github.com/sidneyrma/instalador/blob/arena/019fcd27-instalador/analise/prototipo_evolucao.html
- https://github.com/sidneyrma/instalador/blob/arena/019fcd27-instalador/analise/prototipo_anestesia.html
- https://github.com/sidneyrma/instalador/blob/arena/019fcd27-instalador/analise/prototipo_devocional.html
- Guia de referência: https://github.com/sidneyrma/instalador/blob/arena/019fcd27-instalador/analise/guia_vendd.md

## O QUE COMPARAR (item por item)
Para CADA página publicada, compare com o protótipo correspondente e avalie:
1. PREÇOS: o preço exibido na página publicada é EXATAMENTE o do checkout
   vinculado? (checkouts reais: Portal R$ 49,00 pay.kiwify.com.br/iVfp2bi;
   Evolução da Alma R$ 19,90 pay.kiwify.com.br/ptH32K9; Anestesia Mental
   R$ 19,90 pay.kiwify.com.br/NCf1jh4; Devocional R$ 9,90
   pay.kiwify.com.br/CF9nhFx; Casais Fortes R$ 97,00 hotmart
   go.hotmart.com/F106343306J?dp=1)
2. CTAs e botões: há CTA repetido (3-5x)? Os botões abrem o checkout certo?
   O texto do botão diz o que o preço cobra?
3. ESTRUTURA: a página segue o padrão hero → confiança → dor/solução →
   benefícios → prova → oferta → garantia → FAQ → CTA final?
4. IDENTIDADE VISUAL: cores (azul-marinho #0e1a2e + dourado #c9a24b),
   fontes (títulos serifados), botões destacados, emojis no lugar de ícones
   externos?
5. ERROS TÉCNICOS: ícones quebrados (ex.: texto "shopping_bag" solto),
   cronômetros falsos (que nunca zeram), embutes de redes sociais com poucos
   seguidores, links mortos, erros de português?
6. PROVA SOCIAL: há números inventados (ex.: "10k+") ou depoimentos
   falsos/genéricos? A prova é real e verificável?
7. ENTREGA: fica claro O QUE o comprador recebe (PDF, área do aluno, aulas)?
8. RESPONSIVO: a página se adapta bem ao celular?

## FORMATO DE SAÍDA (obrigatório)
Entregue UM relatório organizado assim:

### 📄 RELATÓRIO DE VARREdura — [data]
1. RESUMO EXECUTIVO: 3-5 frases do estado geral.
2. TABELA COMPARATIVA por página:
   | Página publicada | Protótipo | Situação | Itens que divergem |
   (linha para cada página)
3. DETALHAMENTO por página (com trechos citados):
   - Página [nome]: o que está no ar vs. o que o protótipo propõe.
   - Lista de itens CORRIGIDOS no protótipo que AINDA faltam no ar.
   - Lista de itens que o protótipo NÃO cobre (se houver).
4. PRIORIDADES (ordem de impacto):
   🔴 Crítico (quebra confiança/compra) · 🟠 Importante (afeta conversão) ·
   🟢 Melhoria (visual/copy)
5. PLANO DE AÇÃO: passos concretos por página (o que copiar do protótipo
   para a Vendd, o que ajustar, o que remover).
6. CHECKLIST final de "pronto para publicar" por página.

## REGRAS
- Seja objetivo; não elogie apenas — aponte divergências concretas.
- Se não conseguir acessar uma página publicada, avise e siga com as demais.
- Não invente dados; baseie-se no que realmente está nas páginas.
- Compare TAMBÉM a copy (títulos, subtítulos, benefícios) e aponte qual
  versão é mais persuasiva.
```

---

## 2) VARIAÇÃO PARA O CLAUDE CODE (arquivo local) 💻

Se usar o **Claude Code** dentro do repositório (onde o `CLAUDE.md` já carrega o contexto), use este prompt:

```
Faça uma varredura comparativa entre:
(a) as páginas publicadas no compraoseu.com:
    https://www.compraoseu.com/ · https://www.compraoseu.com/evolucaodaalma ·
    https://www.compraoseu.com/anestesiamental
(b) os protótipos melhorados que estão neste repositório:
    analise/prototipo_home.html · analise/prototipo_evolucao.html ·
    analise/prototipo_anestesia.html · analise/prototipo_devocional.html

Compare: preços vs. checkouts (CLAUDE.md tem os links reais), CTAs,
estrutura de seções, identidade visual (cores #0e1a2e + #c9a24b, títulos
serifados, emojis), erros técnicos (ícones quebrados, cronômetro falso),
prova social, clareza da entrega e responsividade.

Gere um relatório em analise/relatorio_varredura.md com: resumo executivo,
tabela comparativa por página, detalhamento das divergências, prioridades
(🔴 🟠 🟢) e plano de ação por página. Seja objetivo e aponte o que falta
copiar do protótipo para a página publicada.
```

---

## 3) COMO EXECUTAR ⚙️

| Onde | Como |
|---|---|
| **Claude.ai (web)** | Cole o prompt principal no chat. Se o Claude.ai tiver acesso à web, ele abrirá as páginas e os arquivos do GitHub. Dica: peça *"use web search / browse"* se não abrir automaticamente. |
| **Claude Code** | Dentro do repositório local (`cd instalador`), rode: `claude` e cole a variação curta. Ele lê o `CLAUDE.md`, acessa os arquivos locais da pasta `analise/` e pode baixar as páginas publicadas para comparar. |

> ⚠️ **Nota sobre acesso:** para comparar as páginas publicadas, o Claude precisa
> conseguir acessar `compraoseu.com`. Se o Claude não conseguir abrir (bloqueio),
> você pode **copiar o conteúdo da página publicada** (Ctrl+A → Ctrl+C no navegador)
> e colar no chat junto com o prompt — o Claude compara mesmo sem acesso direto.

---

## 4) O QUE ESPERAR DO RELATÓRIO 📄

O Claude gerará um arquivo tipo `analise/relatorio_varredura.md` com:

1. **Resumo executivo** — estado geral das suas páginas no ar;
2. **Tabela comparativa** — página publicada × protótipo × situação × divergências;
3. **Detalhamento por página** — o que está no ar vs. o que falta (com trechos);
4. **Prioridades** — 🔴 crítico / 🟠 importante / 🟢 melhoria;
5. **Plano de ação** — o que copiar do protótipo para a Vendd;
6. **Checklist final** — "pronto para publicar" por página.

Esse relatório vira o seu **roteiro de execução**: você (ou o próprio Claude)
aplica as correções na plataforma Vendd usando o `guia_vendd.md` como manual.
