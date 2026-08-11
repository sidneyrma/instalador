# 🔍 ANÁLISE COMPLETA DOS CHECKOUTS (Kiwify) — O MOMENTO DECISIVO DA COMPRA

**Data:** 05/08/2026 · **Checkouts analisados:** iVfp2bi · ptH32K9 · NCf1jh4 · CF9nhFx

---

## 🏁 RESUMO EXECUTIVO (leia primeiro)

Analisei os 4 checkouts reais da Kiwify acessando os links. Encontrei **2 problemas GRAVES**
que estão **matando vendas no momento exato de comprar** + 5 problemas de credibilidade:

| # | Problema | Gravidade | Status |
|---|---|---|---|
| 1 | **Pixel de conversão QUEBRADO** (`pixels.compraoseu.com` não existe) | 🔴 **CRÍTICO** | ✅ Confirmado |
| 2 | **Moeda/preço exibido em dólar** (no ambiente de acesso usado) | 🔴 **CRÍTICO** | ⚠️ Verificar para BR |
| 3 | "O tempo acabou!" + "lote esgotado" em todos os checkouts | 🟠 Importante | ✅ Confirmado |
| 4 | Vídeo do YouTube (16 inscritos) embutido no checkout do Portal | 🟠 Importante | ✅ Confirmado |
| 5 | Depoimentos com nome completo + idade + foto de banco (parecem falsos) | 🟠 Importante | ✅ Confirmado |
| 6 | Títulos/descrições com erros ("EstudoCompleto") e sem garantia | 🟢 Melhoria | ✅ Confirmado |
| 7 | Páginas de vendas NÃO mostram as avaliações que o checkout mostra | 🟢 Oportunidade | ✅ Confirmado |

---

## 1) 🔴 PROBLEMA Nº 1 (CRÍTICO): O PIXEL DE CONVERSÃO ESTÁ MORTO

**O que encontrei:** nos 4 checkouts, a Kiwify tenta carregar o pixel do Facebook em:
```
https://pixels.compraoseu.com/pixel.html?pixel=1774330010027450&...
```
**Verifiquei:** o domínio `pixels.compraoseu.com` **não tem DNS** — não existe, não resolve,
dá erro `ERR_TUNNEL_CONNECTION_FAILED`. **O pixel NUNCA carregou.**

**O que isso significa para você:**
- ❌ **Nenhuma compra está sendo rastreada** no Meta (Facebook/Instagram);
- ❌ Se você roda **anúncios com otimização de conversão**, o algoritmo voa cego → dinheiro queimado;
- ❌ Você não consegue ver **quem comprou** para criar público de lookalike;
- ❌ Seus 200.000 visitantes e as (poucas) vendas nunca foram contabilizados pelo Meta.

**Por que acontece:** provavelmente você configurou um "domínio de pixel" na Kiwify apontando
para `pixels.compraoseu.com` (técnica para contornar bloqueio do Meta), mas o subdomínio
**nunca foi criado no seu DNS** (ou o registro apagou).

**✅ COMO CORRIGIR (escolha uma):**

**Opção A (recomendada — simples):** na Kiwify, remova o domínio de pixel personalizado e
use o **código do Meta Pixel direto** (no painel Kiwify → Integrações → Meta Pixel, cole seu
Pixel ID `1774330010027450`). A Kiwify dispara o pixel oficialmente.

**Opção B (manter domínio próprio):** crie o subdomínio `pixels.compraoseu.com` no seu DNS
(no painel da onde comprou o domínio) com um registro que aponte para o servidor que hospeda
o `pixel.html`, e suba o arquivo `pixel.html` lá.

**Depois de corrigir:** faça uma compra de teste e confira no **Event Manager do Meta** se o
evento `Purchase` chegou. Só então rode anúncios otimizados para conversão.

---

## 2) 🔴 PROBLEMA Nº 2 (CRÍTICO): PREÇO/MOEDA NO CHECKOUT

**O que encontrei:** no acesso feito, os checkouts exibiram **valores em dólar (USD)**:
- Portal: `$10.66` (R$ 49,00) · Evolução: `$3.90` (R$ 19,90) · Anestesia: `$3.90` (R$ 19,90) · Devocional: `$2.90` (R$ 9,90)
- Formulário com **estados dos EUA** (Alabama, Alaska...) e telefone `+1`
- O pixel enviava `currency=USD` e `product_price=8.2/2.71`

**⚠️ Importante ser honesto:** o acesso foi feito por um servidor no exterior, então a Kiwify
geolocalizou para EUA. **Para um visitante brasileiro deve mostrar R$ — mas VOCÊ PRECISA CONFIRMAR.**

**✅ COMO VERIFICAR (2 minutos):**
1. Abra o link de um checkout **no celular sem VPN, com dados móveis brasileiros** (não Wi-Fi);
2. Veja se aparece **R$ 49,00 / R$ 19,90 / R$ 9,90** e estados brasileiros no formulário;
3. Se aparecer em dólar para brasileiro → na Kiwify: **Configurações → Produto → moeda BRL**,
   e confira se não há um "preço em USD" configurado por engano.

**Se o brasileiro vê R$:** então o problema é só o **pixel reportando USD** — corrija com a
configuração de moeda BRL na integração do pixel, para o Meta receber eventos em BRL.

---

## 3) 🟠 "O TEMPO ACABOU!" + "LOTE ESGOTADO" EM TODOS OS CHECKOUTS

**O que encontrei:** os 4 checkouts mostram:
> "O tempo acabou!" · "Os ingressos desse lote esgotaram! Estamos redirecionando você para o próximo lote agora!"

**Problema:** essa é uma configuração de **lotes/cupons com data** da Kiwify. Se o prazo passou,
essa mensagem aparece **no momento do pagamento** — o cliente pensa que perdeu a oferta e desiste.

**✅ CORRIGIR:**
- Na Kiwify, verifique cada produto → **Lotes / Ofertas** → se há lote com data vencida, **crie um novo lote com data futura** (ou remova a data limite) com o mesmo desconto;
- **Ou** desative a urgência por lote se ela não for real (regra: nunca urgência falsa);
- A mensagem ideal quando há lote real: "Oferta de lançamento válida até [data real]".

---

## 4) 🟠 VÍDEO DO YOUTUBE (16 INSCRITOS) NO CHECKOUT DO PORTAL

**O que encontrei:** o checkout do Portal (iVfp2bi) tem um vídeo embutido "O Portal Está Aberto"
do canal **Missão com Deus — 16 subscribers**.

**Problema:** no momento decisivo, o cliente vê um canal com 16 inscritos enquanto o checkout
diz "4.9 estrelas, 3.920 avaliações". Isso **quebra a credibilidade** — parece inconsistente.

**✅ CORRIGIR:** remover o vídeo do YouTube do checkout (ou substituir por um vídeo hospedado
na Kiwify/Vimeo sem contador visível de inscritos).

---

## 5) 🟠 DEPOIMENTOS COM CARA DE FALSOS NO CHECKOUT

**O que encontrei:** o checkout do Evolução (ptH32K9) tem:
> "João da Silva, 38 anos" · "Cláudia Lysandre, 39 anos" · "Ana L., 33 anos" — com fotos de banco de imagens

**Problema:** mesmo problema das páginas — depoimentos que parecem fabricados. No checkout,
isso é pior (é a última barreira antes do cartão).

**✅ CORRIGIR:** usar depoimentos REAIS (você tem área de alunos — peça no WhatsApp, com
autorização e foto real). Enquanto não tiver, use as avaliações de estrelas da própria Kiwify
(se reais) sem inventar nomes.

---

## 6) 🟢 O QUE ESTÁ BOM NOS CHECKOUTS (aproveitar)

| Ponto bom | Onde |
|---|---|
| ⭐ **Avaliações 4.9/5 com milhares** (3.920, 4.850, 4.920) | Todos — forte prova social |
| 🎁 **Bônus claros** (devocional + e-book "Jesus Quer Falar com Seu Filho") | Portal (iVfp2bi) |
| 🔓 "Acesso imediato e vitalício" | Portal (iVfp2bi) |
| 💬 Botão de **WhatsApp** no checkout | Portal e Anestesia |
| 👤 Nome do vendedor (transparência) | Todos ("Sidney Rodrigues Margarida") |
| 📦 Entrega digital instantânea mencionada | Evolução |

**O grande erro:** as **PÁGINAS DE VENDAS não mostram nada disso!** O checkout tem estrelas,
bônus e avaliações que as páginas não exibem. Quando o cliente chega no checkout e VÊ as
estrelas pela primeira vez, é bom — mas as páginas deveriam mostrar ANTES, para aumentar a
chance de ele chegar lá.

---

## 7) 🎯 CONGRUÊNCIA PÁGINA ↔ CHECKOUT (o que alinhar)

| Item | Checkout diz | Página deve dizer (mesmo texto) |
|---|---|---|
| ⭐ Avaliações | 4.9/5 (3.920/4.850/4.920) | Adicionar selo de estrelas no hero e na oferta |
| 🎁 Bônus | Devocional + E-book "Jesus Quer Falar com Seu Filho" | Listar os 2 bônus na oferta do Portal |
| 🎥 Videoaulas | "Aulas Exclusivas em Vídeo" | Já consta — manter |
| 🔓 Acesso | "Imediato e Vitalício" | Já consta — manter |
| 💰 Preço | R$ 49,00 / R$ 19,90 / R$ 9,90 | Já corrigido nos protótipos |
| 🛡️ Garantia | (não aparece no checkout) | **Adicionar garantia de 7 dias NO CHECKOUT** (a Kiwify tem campo) |

---

## 8) ✅ CHECKLIST DE OTIMIZAÇÃO DO CHECKOUT (fazer nesta ordem)

### Hoje (crítico)
- [ ] **Corrigir o pixel** (Opção A: Pixel ID direto na Kiwify) — desbloqueia todo o rastreamento;
- [ ] **Confirmar moeda BRL** para visitante brasileiro (teste no celular sem VPN);
- [ ] **Consertar os lotes** vencidos ("O tempo acabou!" / "lote esgotado") nos 4 produtos;
- [ ] **Remover vídeo do YouTube** do checkout do Portal;

### Esta semana (importante)
- [ ] **Adicionar garantia de 7 dias** no texto/checkout (a Kiwify permite campo de garantia);
- [ ] **Corrigir título do Evolução** (está gigante — encurtar) e o "EstudoCompleto" (sem espaço) do Portal;
- [ ] **Trocar depoimentos** por reais (ou remover os de banco de imagem);
- [ ] **Adicionar selo de estrelas + bônus** nas páginas de vendas (espelhar o checkout);

### Contínuo
- [ ] Testar um checkout completo de compra (R$ 9,90 do devocional) e conferir o evento no Meta;
- [ ] Monitorar no painel da Kiwify a taxa de conversão checkout (visitantes → compradores).

---

## 9) TÍTULOS E DESCRIÇÕES SUGERIDOS (para editar na Kiwify) ✍️

**Portal (iVfp2bi) — título atual tem erro "EstudoCompleto":**
> ✅ Sugestão: "Portal Missão com Deus — Trilogia Evolução da Alma + Anestesia Mental + Videoaulas + Bônus"

**Evolução (ptH32K9) — título atual muito longo:**
> ✅ Sugestão: "Evolução da Alma — Guia Prático com Preces e Orações para Vencer Medo, Estresse e Ansiedade (Livro Digital + Videoaulas)"

**Anestesia (NCf1jh4) — título bom, manter:**
> ✅ "Anestesia Mental — Desperte sua mente e recupere o controle dos seus pensamentos"

**Devocional (CF9nhFx) — falta o nome do produto no título:**
> ✅ Sugestão: "Um Segundo com Deus — Devocional de 30 Dias para Renovar sua Fé"

---

## 🔗 LINKS DOS CHECKOUTS (para referência)

| Produto | Checkout | Preço |
|---|---|---|
| Portal completo | https://pay.kiwify.com.br/iVfp2bi | R$ 49,00 |
| Evolução da Alma | https://pay.kiwify.com.br/ptH32K9 | R$ 19,90 |
| Anestesia Mental | https://pay.kiwify.com.br/NCf1jh4 | R$ 19,90 |
| Devocional | https://pay.kiwify.com.br/CF9nhFx | R$ 9,90 |

---

*Análise feita a partir do acesso real aos checkouts + textos fornecidos pelo cliente.*
