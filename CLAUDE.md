# CLAUDE.md — Projeto Missão com Deus / CompraOSeu

> Arquivo de instruções para o **Claude Code**. O Claude lê este arquivo automaticamente
> ao trabalhar neste repositório e leva estas diretrizes em conta em todos os comandos.
> (Versão adaptada de `analise/prompt_claude.md`, que contém o prompt completo para o
> Claude.ai — personalização global.)

---

## 1) Contexto do projeto

Atuo no mercado digital com venda de infoprodutos e livros autorais. Ecossistema:
**compraoseu.com** (páginas de vendas hospedadas na plataforma Vendd, editor Elementor).

- **Figura central / autora:** Laura — escritora e mentora cuja marca une **Fé Cristã à
  Neurociência** e ao estudo do comportamento humano.
- **Marca:** "Missão com Deus" (marca-mãe) · "CompraOSeu" (loja) · "Portal Missão com
  Deus" (área de membros).

## 2) Produtos e checkouts (não inventar outros links)

| Produto | Preço | Checkout |
|---|---|---|
| Portal Missão com Deus (aulas + comunidade + Trilogia + Anestesia Mental) | R$ 49,00 (de R$ 98,00) | `https://pay.kiwify.com.br/iVfp2bi` |
| Livro Evolução da Alma | R$ 19,90 (de R$ 49,90) | `https://pay.kiwify.com.br/ptH32K9` |
| Livro Anestesia Mental | R$ 19,90 (de R$ 49,90) | `https://pay.kiwify.com.br/NCf1jh4` |
| Devocional Um Segundo com Deus | R$ 9,90 (de R$ 19,90) | `https://pay.kiwify.com.br/CF9nhFx` |
| Parceria (não autoral): E-book Casais Fortes, Andréa Vermont | R$ 97,00 | `https://go.hotmart.com/F106343306J?dp=1` |

- **Pagamento:** Kiwify (Pix imediato / cartão até 12x).
- **Contato em CTAs:** WhatsApp `wa.me/5528999111493` · e-mail `compraoseu.com@gmail.com`.

## 3) Referências no repositório (pasta `analise/`)

- `diagnostico_conversao.md` — diagnóstico de conversão das páginas (problemas e correções).
- `prototipo_home.html` — protótipo da página principal (Portal + catálogo + trilogia + quiz + mentora + depoimentos + oferta).
- `prototipo_evolucao.html` — protótipo da página do livro Evolução da Alma.
- `prototipo_anestesia.html` — protótipo da página do livro Anestesia Mental (com quiz funcional).
- `prototipo_devocional.html` — protótipo da página do Devocional Um Segundo com Deus.
- `guia_vendd.md` — guia de aplicação dos protótipos na plataforma Vendd (seção a seção).
- `prompt_claude.md` — prompt completo de personalização para o Claude.ai.

**Ao criar ou editar páginas, seguir o padrão visual e estrutural desses protótipos.**

## 4) Identidade visual (páginas/layouts/código)

- Cores da marca:
  - Fundo azul-marinho: `#0e1a2e` · cartões: `#16283f` · hover: `#1d3350`
  - Dourado: `#c9a24b` · dourado claro: `#e3c877` · botões: `#b8860b`
  - Fundo claro: `#f6f1e7` · cartões claros: `#efe7d6`
  - Texto: `#20242b` / secundário `#5c615c` · sucesso: `#2e7d32`
- Tipografia: títulos em **Georgia (serifada)**; corpo em sans-serif.
- Estrutura de página (padrão): hero → barra de confiança → dor/solução → benefícios →
  prova → oferta → garantia → FAQ → CTA final.
- Botões de conversão grandes e destacados; usar **emojis** no lugar de ícones externos
  (nunca deixar ícones quebrados); layout responsivo (celular 1 coluna, desktop múltiplas).

## 5) Regras de conversão (obrigatórias)

1. **O preço exibido em qualquer página/copy deve ser EXATAMENTE o do checkout vinculado.**
   Nunca divergir (foi o erro crítico encontrado na página atual).
2. Nunca inventar números de vendas, depoimentos, avaliações ou prova social. Usar
   placeholders claros e sugerir como obter provas reais.
3. Nunca usar urgência falsa (ex.: cronômetro que nunca zera). Preferir escassez real,
   garantia e valor.
4. Toda página de vendas deve conter: oferta principal única e clara, CTA repetido
   (3 a 5 vezes), checklist do que o comprador recebe, garantia de 7 dias, selos de
   segurança (Kiwify, Pix, cartão).
5. Honestidade sempre: anúncios persuasivos, nunca enganosos.

## 6) Tom de voz

- Sempre **português do Brasil**.
- Profundo, reflexivo, persuasivo e empático — mas firme no convite ao despertar e ao
  governo da mente em Cristo.
- Ancorar a comunicação na fusão entre **autoridade espiritual (Fé)** e **desenvolvimento
  cognitivo/neurociência**.
- Vocabulário da marca: despertar, governo da mente, soberania da alma, Reset do Shabat,
  maturidade, propósito, clareza.

## 7) Formato de entrega

- Respostas diretas, em tópicos/marcadores/negritos, prontas para executar.
- **Anúncio/copy:** Título (até ~40 caracteres), Texto principal, Roteiro de vídeo
  (gancho de 3s, desenvolvimento, CTA) e 2–3 variações (formato Meta Ads).
- **Página/landing:** HTML autocontido funcional OU guia de blocos seção a seção para a
  Vendd (editor Elementor), seguindo a identidade visual acima.
- **Estratégia de vendas:** considerar LTV e ticket médio (order bumps, upsells,
  recuperação de carrinho, sequência de e-mails); propor o caminho mais simples primeiro.
- Se faltar informação importante (orçamento, público, objetivo), **perguntar antes de assumir**.

## 8) Limites

- Sempre PT-BR, salvo pedido explícito.
- Não inventar dados, links ou números; pedir confirmação quando houver dúvida.
- Respeitar as diretrizes de uso da Anthropic (sem manipulação enganosa, desinformação
  ou conteúdo proibido).
