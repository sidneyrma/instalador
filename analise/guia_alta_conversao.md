# 🚀 GUIA PRÁTICO — "O que é uma página de alta conversão" + como usar o Claude

**Pergunta que você fez:** "Essa nova página no GitHub é de alta conversão? Como explorar o Claude ou outra IA para criar páginas de alta conversão?"

---

## 1) O que é uma página de ALTA CONVERSÃO (na prática) 📈

Uma página de alta conversão **não é sorte nem mágica** — é uma **fórmula testada**. As páginas que vendem bem (de grandes vendedores de infoprodutos) seguem estas 7 regras. Compare com as nossas:

| # | Regra de alta conversão | Nosso protótipo tem? |
|---|---|---|
| 1 | **Oferta clara e única** — o visitante entende em 5s o que é e quanto custa | ✅ Hero com produto + preço + botão |
| 2 | **Preço = checkout** — nunca divergir (o erro crítico que matava suas vendas) | ✅ 100% corrigido |
| 3 | **CTA repetido 3–5x** — "Quero meu acesso" aparece várias vezes, sempre com preço | ✅ Hero, oferta, CTA final |
| 4 | **Checklist da entrega** — "o que você recebe" (PDF, área do aluno, etc.) | ✅ Seção "O que você recebe" |
| 5 | **Prova social REAL** — depoimentos de verdade, com nome/foto autorizados | ✅ Placeholder claro (falta o real) |
| 6 | **Garantia visível** — "7 dias, risco zero" logo abaixo do botão | ✅ Selo "7 DIAS GARANTIA" |
| 7 | **Identidade profissional** — cores coesas, sem erro visual, responsivo | ✅ Azul + dourado, emojis, mobile |

**Resposta honesta:** a página que criamos no GitHub **segue a fórmula de alta conversão** (regras 1–7). Mas alta conversão **depende também de:**
- **Tráfego certo** (pessoas com o problema que você resolve);
- **Depoimentos reais** (você ainda precisa coletar — você tem alunos!);
- **Teste e ajuste** (nenhuma página é perfeita na 1ª versão).

Então: a página está **pronta para o padrão profissional**. O que falta não é código — é **prova real e tráfego qualificado**.

---

## 2) Como usar o Claude (ou outra IA) para criar páginas de alta conversão 🤖

### O jeito CERTO (funciona):

**Passo 1 — Dê contexto à IA (uma vez):**
Cole o `prompt_claude.md` (versão curta) nas instruções do Claude. Ele contém: produtos, preços, links, cores, regras de conversão e tom de voz.

**Passo 2 — Peça o código no formato que a Vendd aceita:**
```
Gere o código completo da página do DEVOCIONAL (R$ 9,90), com:
- CAIXA HEAD: <title>, <meta>, e todo o <style> (CSS)
- CAIXA BODY: todo o <body> (HTML + botões + script)
Separe as duas partes com os marcadores [INÍCIO HEAD] / [FIM HEAD] e
[INÍCIO BODY] / [FIM BODY], como no arquivo devocional_vendd.html.
Use as cores #0e1a2e e #c9a24b, CTA repetido 3x, garantia 7 dias,
checklist "o que você recebe" e checkout https://pay.kiwify.com.br/CF9nhFx.
```

**Passo 3 — Cole na Vendd:**
- HEAD → caixa "HEAD" (cabeçalho) da página;
- BODY → caixa "BODY" (corpo);
- Publique e abra no celular para testar.

**Passo 4 — Teste e melhore (o que a maioria não faz):**
- Veja no Analytics onde as pessoas desistem;
- Peça ao Claude: *"reescreva o título do hero em 3 versões para testar A/B"*;
- Troque a cor do botão e compare.

### O jeito ERRADO (não funciona):
- ❌ "Crie minha página de vendas" sem contexto → a IA inventa preços, links e layout genérico;
- ❌ Pedir a página e não testar → uma página nunca converte de primeira;
- ❌ Achar que a IA vai "vender por você" → a IA faz o código e a copy; quem publica, testa e ajusta é você.

---

## 3) NOSSO PLANO AGORA (com foco no Devocional, seu caixa) 🎯

| Etapa | O que fazer | Onde |
|---|---|---|
| 1 | **Publicar a página do Devocional** (código pronto) | Na Vendd, usando `devocional_vendd.html` |
| 2 | **Adicionar link na Home** | Card do Devocional → apontar para a página nova |
| 3 | **Corrigir checkouts das 3 páginas** (5 min) | `plano_execucao_vendd.md` seção 1.1 |
| 4 | **Coletar depoimentos reais** | WhatsApp para quem já comprou (você tem alunos!) |
| 5 | **Medir** | Pixel do Meta + Analytics |

---

## 4) Arquivos prontos (clique e copie) 📁

| Página | Arquivo | Link direto |
|---|---|---|
| 🕊️ **Devocional (R$ 9,90)** — NOVO | `analise/vendd/devocional_vendd.html` | https://github.com/sidneyrma/instalador/blob/arena/019fcd27-instalador/analise/vendd/devocional_vendd.html |
| 🏠 Home (R$ 49,00 Portal) | `analise/vendd/home_vendd.html` | https://github.com/sidneyrma/instalador/blob/arena/019fcd27-instalador/analise/vendd/home_vendd.html |

> 💡 **Dica para achar no GitHub:** na pasta `analise/` clique na subpasta **`vendd`** (a que você viu na listagem) — os dois arquivos `home_vendd.html` e `devocional_vendd.html` estão lá dentro.

---

*Documento gerado em 05/08/2026 · Missão com Deus · CompraOSeu*
