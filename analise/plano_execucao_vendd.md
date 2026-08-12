# 🛠️ PLANO DE EXECUÇÃO — Aplicar correções na Vendd

**Base:** Relatório de Varredura (Claude) + Diagnóstico de Conversão
**Meta:** tirar as páginas publicadas do "crítico" para "pronto para publicar"

---

## 0) TABELA MESTRA DE CHECKOUTS (referência — nunca errar) 🔑

| Produto | Preço exato | Checkout (Kiwify/Hotmart) |
|---|---|---|
| Portal Missão com Deus (completo) | **R$ 49,00** | `https://pay.kiwify.com.br/iVfp2bi` |
| Livro Evolução da Alma | **R$ 19,90** | `https://pay.kiwify.com.br/ptH32K9` |
| Livro Anestesia Mental | **R$ 19,90** | `https://pay.kiwify.com.br/NCf1jh4` |
| Devocional Um Segundo com Deus | **R$ 9,90** | `https://pay.kiwify.com.br/CF9nhFx` |
| Parceria: Casais Fortes (Hotmart) | R$ 97,00 | `https://go.hotmart.com/F106343306J?dp=1` |

> **Regra de ouro:** o preço que aparece AO LADO de um botão deve ser SEMPRE o preço do checkout que o botão abre.

---

## 1) 🔴 FAZER HOJE (crítico — impacto direto em venda e confiança)

### 1.1 Corrigir links de checkout (as 3 páginas)

**Página Evolução da Alma (`/evolucaodaalma`)**
- [ ] Botão **"GARANTIR ACESSO À MINHA EVOLUÇÃO"** (hero, mostra R$ 19,90)
  - Trocar link de `iVfp2bi` → **`https://pay.kiwify.com.br/ptH32K9`**
  - Manter o texto "De R$ 49,90 por R$ 19,90" (agora bate com o checkout ✅)
- [ ] Botão **"QUERO MEU ACESSO AGORA"** (meio da página)
  - Trocar link de `iVfp2bi` → **`https://pay.kiwify.com.br/ptH32K9`**
- [ ] Deixar o `iVfp2bi` (R$ 49,00) APENAS no bloco "⭐ A Experiência Completa" (que já está correto)

**Página Anestesia Mental (`/anestesiamental`)**
- [ ] Botão de topo **"COMPRAR AGORA"** (primeiro botão que o visitante vê)
  - Trocar link de `iVfp2bi` → **`https://pay.kiwify.com.br/NCf1jh4`**
- [ ] Deixar `iVfp2bi` apenas no bloco da Experiência Completa

**Página Home (`/`)**
- [ ] Modal final "OFERTA ESPECIAL": preço **R$ 49,90 → R$ 49,00** (para bater com `iVfp2bi`)

> ✅ **Como testar:** abra cada página publicada e CLIQUE em cada botão. O checkout que abrir deve cobrar EXATAMENTE o preço que estava ao lado do botão. Qualquer divergência = corrigir.

### 1.2 Trocar ícones quebrados por emojis (as 3 páginas)

Os nomes soltos (`shopping_bag`, `expand_more`, `psychology_alt`, `key`, `timer`, `verified`...) são a fonte de ícones não carregando. A correção mais rápida no editor da Vendd:

- [ ] Opção A (rápida): trocar cada ícone quebrado por um **emoji** equivalente:
  - `shopping_bag` → 🛍️ · `play_circle` → ▶️ · `verified` → ✅ · `timer` → ⏳ ·
  - `lock` → 🔒 · `auto_stories` → 📖 · `psychology` → 🧠 · `key` → 🔑 ·
  - `check_circle` → ✅ · `expand_more` → ▾ (ou use texto)
- [ ] Opção B (definitiva): adicionar a **fonte do Material Icons** no `<head>` da página
  - `<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">`
  - Ou na Vendd: Configurações → CSS customizado/HTML head

> O padrão do projeto (e dos protótipos) é **usar emojis** — simples e nunca quebra.

### 1.3 Remover o cronômetro falso (as 3 páginas)

- [ ] Apagar o bloco **"O CRONÔMETRO ESTÁ RODANDO"** (00:00:00 fixo) das 3 páginas
- [ ] No lugar, reforçar a oferta com: desconto declarado ("De R$ 98,00 por R$ 49,00") + **bloco de garantia 7 dias** (ver 2.3)

> ⚠️ Se você quiser urgência de verdade no futuro, use **escassez real**: "Restam X vagas no Portal nesta semana" — atualizado de verdade, sem relógio fake.

### 1.4 Publicar a página do Devocional (oportunidade de receita parada)

- [ ] Criar página nova na Vendd: `/um-segundo-com-deus` (ou `/devocional`)
- [ ] Usar `prototipo_devocional.html` como base (já está com CTA correto `CF9nhFx`, R$ 9,90)
- [ ] Adicionar link para ela: no menu da Home e no rodapé das outras páginas

---

## 2) 🟠 FAZER NESTA SEMANA (importante — afeta conversão)

### 2.1 Depoimentos (as 3 páginas + Home)
- [ ] Substituir depoimentos "fabricados" (nome + idade + foto de banco) por **depoimentos reais autorizados** de alunos do Portal;
- [ ] Até ter os reais, usar o texto placeholder do protótipo: *"Depoimento ilustrativo — adicione aqui o depoimento real, com foto e nome autorizados"*;
- [ ] Se mantiver algum depoimento, adicionar origem verificável (ex.: "Aluna do Portal desde 2025").

### 2.2 Selo "10k+ Vidas Impactadas" (Home)
- [ ] Remover OU substituir por número real (ex.: "300+ alunos", "X vidas impactadas" se souber o real);
- [ ] Nunca inventar número.

### 2.3 Bloco de garantia visível (todas as páginas)
- [ ] Adicionar bloco **"7 DIAS GARANTIA"** FORA do FAQ, logo abaixo da oferta (como no protótipo):
  - Selo redondo "7 DIAS GARANTIA" + texto "Risco zero. Se em até 7 dias você sentir que não é para você, devolvemos 100% do investimento, sem perguntas."

### 2.4 Bloco "O que você recebe" (todas as páginas)
- [ ] Adicionar checklist visual logo abaixo do primeiro CTA:
  - 📕 Livro em PDF · 🔗 Acesso à Área do Aluno · ♾️ Acesso vitalício (adaptar por produto)

### 2.5 Quiz do Anestesia (manter + ressalva)
- [ ] Manter o quiz (bom como isca);
- [ ] Adicionar a ressalva: *"Autoavaliação ilustrativa, não substitui aconselhamento profissional"*.

---

## 3) 🟢 DESEJÁVEL (ajuste fino — quando sobrar tempo)

- [ ] **Confirmar visualmente** (captura de tela lado a lado) que as cores `#0e1a2e` / `#c9a24b` e fonte Georgia estão aplicadas nas páginas ao vivo;
- [ ] **Testar responsividade** em celular real (as 4 páginas, ao vivo e protótipo);
- [ ] **Padronizar o FAQ** entre as páginas (redação unificada);
- [ ] **Ofuscamento de e-mail**: o `compraoseu.com@gmail.com` está protegido via Cloudflare (`/cdn-cgi/l/email-protection`) — funciona, mas confirme que aparece para o visitante;
- [ ] Adicionar **pixel de conversão** (Meta/Google) para medir (ver `guia_vendd.md` seção 4.2).

---

## 4) COMO USAR ESTE PLANO COM O CLAUDE 🤖

**Opção 1 — Deixar o Claude te guiar na Vendd (um passo por vez):**
```
Use o plano de execução (analise/plano_execucao_vendd.md) e me guie
passo a passo para corrigir a página /evolucaodaalma na Vendd.
Comece pelos links de checkout. A cada passo, me diga exatamente o que
clicar e o que colar. Não pule etapas.
```

**Opção 2 — Pedir o texto pronto dos blocos novos (garantia / o que recebe):**
```
Gere o HTML pronto (com as cores #0e1a2e + #c9a24b) do bloco "7 DIAS
GARANTIA" e do bloco "O que você recebe" para a página do Anestesia
Mental, para eu colar no widget HTML da Vendd.
```

**Opção 3 — Depois de corrigir, rodar a varredura de novo:**
```
Refaça a varredura comparativa das páginas publicadas com os protótipos
e confirme se as divergências 🔴 foram resolvidas. Atualize o relatório.
```

---

## 5) CHECKLIST FINAL "PRONTO PARA PUBLICAR" ✅

Para CADA página (Home, Evolução, Anestesia, Devocional):
- [ ] Todos os botões → checkout com preço idêntico ao exibido;
- [ ] Zero ícones quebrados (só emojis);
- [ ] Zero cronômetro falso;
- [ ] Bloco de garantia 7 dias visível (fora do FAQ);
- [ ] Bloco "O que você recebe" visível;
- [ ] Depoimentos reais (ou placeholder claro);
- [ ] Sem números inventados;
- [ ] Funciona no celular (teste real);
- [ ] Pixel + Analytics ativos;
- [ ] Link do WhatsApp funcionando.

---

*Documento gerado em 05/08/2026 · Missão com Deus · CompraOSeu*
