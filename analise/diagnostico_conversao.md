# 🔍 Diagnóstico de Conversão — CompraOSeu.com

**Data:** 05/08/2026 · **Analisado:** página principal, `/evolucaodaalma`, `/anestesiamental` (+ devocional "Um Segundo com Deus" sem página própria)

---

## 1. Resumo executivo

O material de vendas (copy, estrutura, ofertas) tem **boa base**, mas as páginas têm **erros técnicos e de consistência que destroem a confiança** e, principalmente, **não recebem tráfego qualificado**. Uma página só converte se houver visitantes. A reformulação é necessária em 3 frentes:

| Frente | Impacto | Esforço |
|---|---|---|
| 🔴 Corrigir erros críticos (quebram confiança) | Alto | Baixo (horas) |
| 🟠 Reestruturar ofertas e CTAs | Alto | Médio (1–2 dias) |
| 🟢 Gerar tráfego qualificado | **Essencial** | Contínuo |

---

## 2. O que já funciona bem ✅

- Copy emocional com linguagem de fé + ciência (diferencial da marca);
- Estrutura de página de vendas clássica (dor → solução → prova → oferta → urgência);
- Preços de entrada acessíveis (R$ 9,90 – R$ 19,90) — baixa fricção;
- Garantia de 7 dias mencionada no FAQ;
- Proposta de valor clara ("o trono não fica vazio: ou você governa, ou o algoritmo ocupa").

---

## 3. Os 10 problemas que estão matando as vendas 🔴

### 3.1 Ícones Material quebrados (aparecem como texto)
Em **todas** as páginas aparecem palavras soltas no meio do texto: `shopping_bag`, `play_circle`, `verified`, `timer`, `lock`, `auto_stories`, `psychology`, `history_edu`...
**Causa:** os ícones Material Symbols não estão carregando (fonte CSS ausente).
**Efeito:** aparência amadora imediata; o visitante vê lixo visual em cada botão.
**Correção:** adicionar a fonte do Material Icons no `<head>` OU trocar por SVGs/emojis.

### 3.2 Erro grave de consistência de preço na página Evolução da Alma
O botão do topo **"GARANTIR ACESSO À MINHA EVOLUÇÃO"** mostra a oferta **"De R$ 49,90 por R$ 19,90"**, mas o link leva para o checkout **iVfp2bi (combo Trilogia + Anestesia = R$ 49,00)**.
**Efeito:** o visitante clica esperando pagar R$ 19,90 e o checkout cobra R$ 49,00 → sensação de engano → abandono e desconfiança.
**Correção:** apontar esse botão para o checkout individual `ptH32K9` (R$ 19,90) ou mudar o texto/preço para R$ 49,00.

### 3.3 Urgência falsa (cronômetros que não zeram)
Toda visita mostra o mesmo "00:59:58" no topo e outro "00:29:59" no rodapé, que **sempre resetam**.
**Efeito:** visitante que retorna percebe a falsidade → perde toda a credibilidade. Urgência falsa é pior que não ter urgência.
**Correção:** usar **escassez real** (ex.: "restam X vagas no portal nesta semana" atualizado de verdade) ou **sem urgência**, focando em valor + garantia.

### 3.4 Prova social fabricada / sem substância
- Canal YouTube com **16 inscritos** embutido nas páginas (o visitante vê o número);
- Depoimentos com nomes genéricos ("João da Silva, 38 anos") e sem origem verificável;
- "10k+ Vidas Impactadas" sem nenhuma evidência.
**Efeito:** a maior objeção ("isso funciona?") fica sem resposta; autoridade zero.
**Correção:** remover o embute do YouTube (ou trocar por vídeo hospedado), usar **depoimentos reais com foto** (peça a alunos do portal), e trocar "10k+" por números reais (mesmo que pequenos: "300+ alunos").

### 3.5 Paradoxo da escolha na página principal
A home mistura **4 produtos diferentes** (Evolução da Alma, Anestesia Mental, Devocional, Casais Fortes da Hotmart) com CTAs distintos, sem hierarquia.
**Efeito:** o visitante não sabe o que clicar e clica em nada (paralisia de decisão).
**Correção:** a home deve ter **UMA oferta principal** (ex.: o Portal/Trilogia) + seções secundárias claras, ou virar um catálogo com filtro óbvio.

### 3.6 O devocional "Um Segundo com Deus" está invisível
Não tem página própria (confirmado). É o produto de **menor preço (R$ 9,90)** e **maior potencial de entrada** (compra por impulso), mas aparece só como card na home.
**Correção:** criar página dedicada `/umsegundocomdeus` com copy curta e CTA único; usar como **produto de entrada** para a Trilogia (upsell).

### 3.7 Marca confusa (3 nomes ao mesmo tempo)
A página alterna "Compraoseu", "Missão com Deus", "Portal: O Despertar da Alma" — inclusive com grafias inconsistentes ("Missão Com Deus" vs "Missão com Deus", "à Portal" sem crase correta).
**Efeito:** o visitante não guarda quem é você; perde memorização e busca.
**Correção:** definir **uma marca-mãe** (sugestão: "Missão com Deus" como marca, "CompraOSeu" como loja técnica, "Portal Missão com Deus" como produto).

### 3.8 Erros de português e ícones quebrados na copy
- "garante acesso à **Portal**" (falta crase/artigo);
- "ADQUIRE AQUI O SEU ACESSO\\" (barra invertida vazada);
- Texto com ícones Material não renderizados entre palavras.
**Efeito:** reforça impressão amadora.
**Correção:** revisão geral da copy + correção dos ícones.

### 3.9 Entrega vaga ("Receba no seu e-mail o acesso ao livro")
Não fica claro **o que exatamente** o comprador recebe: PDF? Link da área de membros? Aulas? Quantas?
**Efeito:** insegurança na compra ("vou receber mesmo?").
**Correção:** especificar: "Você recebe por e-mail: 📕 o livro em PDF + 🔗 link da Área do Aluno com 7 aulas + 🎁 bônus". Colocar isso em checklist logo abaixo de cada CTA.

### 3.10 Sem tráfego (o problema real)
16 inscritos no YouTube + sem sinais de anúncios/SEO/tráfego pago = **quase zero visitantes**.
**Efeito:** a melhor página do mundo não vende sem gente. Este é o ponto nº 1.
**Correção (ver seção 5):** definir canal de tráfego antes de tudo.

---

## 4. O que fazer primeiro (plano de 7 dias)

**Dia 1 — Corrigir os críticos (3.1, 3.2, 3.3):**
1. Consertar os ícones (fonte do Material Icons no head);
2. Corrigir o link do CTA de R$ 19,90 na página Evolução da Alma;
3. Remover/ajustar os cronômetros falsos.

**Dia 2 — Prova e clareza (3.4, 3.9):**
4. Remover embute do YouTube com 16 subs;
5. Colocar checklist de entrega abaixo de cada botão;
6. Substituir "10k+" por número real.

**Dia 3 — Estrutura (3.5, 3.6):**
7. Definir oferta principal da home;
8. Criar página do Devocional com CTA único.

**Dias 4–7 — Página reformulada:**
9. Redesenhar 1 página (sugestão: começar pelo Devocional ou pela Evolução da Alma) com layout profissional, hierarquia visual e CTAs consistentes (posso criar o modelo);
10. Instalar **pixel de conversão** (Meta/Google) + **analytics** para medir.

---

## 5. O problema nº 1: tráfego 🚦

Sem visitantes, nenhuma reformulação gera venda. Opções realistas, por ordem de custo:

| Canal | Custo | Quando |
|---|---|---|
| **YouTube (orgânico)** | R$ 0 | já tem canal; precisa conteúdo consistente + CTA no vídeo |
| **TikTok/Reels (orgânico)** | R$ 0 | melhor custo-benefício para livros/espiritualidade |
| **Google Ads (palavras-chave)** | R$ 300–600/mês | bom para "livro evolução da alma", intenção alta |
| **Meta Ads (Facebook/IG)** | R$ 300–600/mês | bom para cold traffic com criativo emocional |
| **Parcerias com canais de fé** | R$ 0 | divulgar para audiência já engajada |
| **WhatsApp/lista de e-mails** | R$ 0 | nutrir quem já demonstrou interesse |

**Sugestão inicial:** começar com **tráfego orgânico (TikTok/Reels + YouTube)** criando 1 vídeo/dia de 30–60s com os ganchos já existentes na copy ("Sua mente ainda pertence a você?"), com CTA para o link na bio. Quando houver 1ª prova de demanda, investir em anúncios.

---

## 6. O que NÃO fazer ⚠️

- ❌ Não criar urgência falsa (cronômetro que não zera);
- ❌ Não colocar números de prova social que não existem;
- ❌ Não misturar ofertas sem hierarquia na mesma página;
- ❌ Não usar o "Ouro das Palavras" na vitrine (direitos autorais de audiolivro do YouTube — risco legal real).

---

## 7. Próximos passos possíveis (me diga qual quer)

1. **Protótipo da página reformulada** — crio o modelo visual de uma das páginas (sugiro o Devocional ou Evolução da Alma) pronto para você replicar na Vendd;
2. **Copy reescrita** — reescrevo os textos das páginas com foco em conversão (ganchos, benefícios, objeções, garantia);
3. **Checklist técnico** — passo a passo exato dos consertos rápidos (ícones, links, cronômetros) para você aplicar no editor da Vendd;
4. **Plano de tráfego** — roteiro de 30 dias de conteúdo para TikTok/Reels/YouTube.
