# ✅ Relatório de Auditoria — Páginas do Claude (`analise/compraoseu.preview`)

**Data:** 05/08/2026 · **Auditado:** home, evolucao, anestesia, devocional (cada uma com `_HEAD.html` + `_BODY.html` + `_preview.html`)

---

## 🏁 Veredito final

# ✅ APROVADAS PARA PUBLICAR NA VENDD

As 4 páginas geradas pelo Claude **seguem corretamente a fórmula de alta conversão** e corrigem todos os problemas críticos das páginas atuais. **Não há erros de checkout, ícones quebrados ou urgência falsa.**

---

## 📊 Resultado da auditoria por página

| Critério (regra de alta conversão) | Home | Evolução | Anestesia | Devocional |
|---|---|---|---|---|
| 🔗 **Checkout = preço exibido** (regra nº 1) | ✅ | ✅ | ✅ | ✅ |
| 🎯 **CTAs repetidos** (3–5×) | ✅ (10 botões) | ✅ (5) | ✅ (6) | ✅ (4) |
| 📦 **Bloco "o que você recebe"** | ✅ | ✅ | ✅ | ✅ |
| 🛡️ **Garantia 7 dias visível** | ✅ | ✅ | ✅ | ✅ |
| 👤 **Depoimentos com placeholder claro** | ✅ | ✅ | ✅ | ✅ |
| 🚫 **Sem "10k+" inventado** | ✅ | ✅ | ✅ | ✅ |
| 😀 **Emojis no lugar de ícones quebrados** | ✅ (20) | ✅ (19) | ✅ (16) | ✅ (13) |
| ⏳ **Sem cronômetro falso** | ✅ | ✅ | ✅ | ✅ |
| 🎨 **Cores da marca** (#0e1a2e + #c9a24b) | ✅ | ✅ | ✅ | ✅ |
| 📱 **Responsivo** (@media) | ✅ | ✅ | ✅ | ✅ |
| 💬 **WhatsApp** | ✅ | ✅ | ✅ | ✅ |
| 📄 **Meta description + viewport** | ✅ | ✅ | ✅ | ✅ |

**Checkouts confirmados corretos em cada página:**
- **Home:** Portal `iVfp2bi` (R$ 49,00) · Evolução `ptH32K9` (R$ 19,90) · Anestesia `NCf1jh4` (R$ 19,90) · Devocional `CF9nhFx` (R$ 9,90) · Casais Fortes (Hotmart)
- **Evolução:** livro `ptH32K9` (R$ 19,90) + upsell Portal `iVfp2bi` (R$ 49,00) em bloco separado ✅
- **Anestesia:** livro `NCf1jh4` (R$ 19,90) + upsell Portal `iVfp2bi` (R$ 49,00) ✅
- **Devocional:** `CF9nhFx` (R$ 9,90) ✅

---

## ⚠️ Única ação necessária antes de publicar (2 minutos)

**Adicionar o Meta Pixel** — nenhuma das 4 páginas tem o código do seu Pixel (necessário para medir conversões e criar públicos para anúncios).

**Como fazer:** no `_HEAD.html` de cada página, cole seu código de Pixel logo após o `<meta name="viewport"...>`:

```html
<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'SEU_PIXEL_ID');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=SEU_PIXEL_ID&ev=PageView&noscript=1"/></noscript>
<!-- fim Meta Pixel -->
```

*(Substitua `SEU_PIXEL_ID` pelo ID do seu pixel — está em business.facebook.com → Configurações do pixel.)*

---

## 📋 Como publicar na Vendd (por página)

1. Abra a página na Vendd (ex.: a Home);
2. Copie o conteúdo do `home_HEAD.html` → **caixa HEAD** (cabeçalho) da página;
3. Copie o conteúdo do `home_BODY.html` → **caixa BODY** (corpo);
4. Publique e teste no celular e no PC;
5. Repita para `evolucao`, `anestesia` e `devocional`.

> 💡 **Dica:** o `files.zip` da pasta contém todos os 12 arquivos juntos — baixe e descompacte para ter tudo em um lugar.

---

## 🎯 Ordem de publicação sugerida

1. **Devocional** (R$ 9,90 — caixa, receita parada, página nova) — publicar e linkar na Home;
2. **Evolução da Alma** (R$ 19,90 — substitui a página atual com o erro de checkout);
3. **Anestesia Mental** (R$ 19,90 — substitui a atual);
4. **Home** (por último — depois que as páginas de produto existirem, para os links baterem).

---

## 🔗 Onde estão os arquivos (GitHub)

**Pasta:** `https://github.com/sidneyrma/instalador/tree/arena/019fcd27-instalador/analise/compraoseu.preview`

| Página | HEAD | BODY | Preview |
|---|---|---|---|
| Home | home_HEAD.html | home_BODY.html | home_preview.html |
| Evolução | evolucao_HEAD.html | evolucao_BODY.html | evolucao_preview.html |
| Anestesia | anestesia_HEAD.html | anestesia_BODY.html | anestesia_preview.html |
| Devocional | devocional_HEAD.html | devocional_BODY.html | devocional_preview.html |

---

*Relatório gerado automaticamente pelos scripts `auditoria_preview.py` e `auditoria_precos.py` (pasta `analise/`).*
