# MISSÃO COM DEUS — PRÓXIMOS PASSOS
## Atualizado em: 03/09/2026
## Site vivo: https://missaocomdeus.com.br

Este documento é a lista prática do que falta. É só seguir por ordem, com calma, sem mexer em muita coisa de uma vez.

---

## 1) O QUE JÁ ESTÁ CONFERIDO E SALVO

- Identidade única: **Missão com Deus** já aplicada no servidor. Home no ar já com a marca nova (autor confirmou).
- Aulas grátis corrigidas: `livro05` e `livro09` agora mostram **Módulo 03** (livre), não o Módulo 04.
- `ATUALIZAR_4_BONUS.py` já rodou no servidor.
- `PROMPT_LAURA_V11_CASA.txt` já foi colado no FlowOpenAi.
- Mural **eliminado** de vez. Não recriar.
- `gerar_estatisticas.py` ajustado: **Colaborador não conta mais como sustento**. Sustento = acesso completo R$ 37.
- `/palavra`, `/stats` e `enquete.php` são só do administrador: `noindex, nofollow`, fora do sitemap, sem link no menu.
- PDFs reais do aaPanel confirmados: a referência do Bônus 1 é **`/ebooks/livro11-o-n-t.pdf`**. O nome antigo não existe mais.

---

## 2) IDENTIDADE: JÁ APLICADA

- Autor confirmou que os comandos rodaram e a marca **Missão com Deus** já está no ar.
- Conferir em aba anônima se não aparece mais **Portal O Despertar** nem **Coleção do Despertar** como marca.

## 2B) AJUSTE DO /STATS (JÁ PRONTO NO ESPELHO)

O `/stats` no ar ainda dizia **"Sustento (Semeador + Colaborador)"** e mostrava **Colaborador R$ 19,90**. Como o Colaborador foi eliminado, o gerador já foi ajustado para:
- Sustento = somente **acesso completo R$ 37** (`/q-semeador`).
- Remover a linha de Colaborador dos cards ativos.
- Deixar nota de que Colaborador saiu do ar.

Para aplicar:
1. Subir o `site-contabo/gerar_estatisticas.py` atualizado para `/home/deploy/gerar_estatisticas.py`.
2. No Terminal do aaPanel, rodar:

```
cd /home/deploy
python3 gerar_estatisticas.py
```

3. Abrir `https://missaocomdeus.com.br/stats` e confirmar que não aparece mais Colaborador no sustento.

---

## 3) GOOGLE SEARCH CONSOLE

### Como está hoje
- Sitemap: `https://missaocomdeus.com.br/sitemap.xml`
- Status: **Sucesso**
- Última leitura: 02/09/2026
- Enviado: **9 páginas**
- Páginas descobertas: **90**

As 9 páginas do sitemap são:
`/`, `/livro04`, `/livro05`, `/livro06`, `/livro07`, `/livro09`, `/livro11`, `/livro12`, `/guia-pais-filhos`.

### O que fazer depois que a identidade entrar no ar
1. No Search Console, abrir **Sitemaps** e enviar de novo `sitemap.xml`.
2. Para cada uma das 9 páginas, usar **Inspecionar URL** → **Solicitar indexação**.
3. Não tirar do índice as páginas vivas. Só usar **Remoções** para URLs antigas que realmente não existem mais e que ainda aparecem como problema.
4. Não remover `/palavra`, `/stats` ou `enquete.php`: elas ficam fora do índice de propósito.

---

## 4) PIXEL DE CONVERSÃO NA KIWIFY

### Recomendação: começar com Google Ads + GA4
Motivo: Meta Pixel exige conta de Facebook/Instagram e hoje essas contas estão banidas. O caminho mais seguro agora é Google.

#### A) Criar a conversão no Google Ads
1. Entrar no Google Ads com um e-mail que **não seja** o das contas banidas.
2. Menu **Metas** → **Conversões**.
3. **Nova ação de conversão** → **Site** → domínio `missaocomdeus.com.br`.
4. **Configurar manualmente**.
5. Categoria: **Compra**. Nome: `Compra Missão com Deus`.
6. Valor: R$ 37,00.
7. Copiar o **ID de conversão** e o **label** (ficam no código `AW-XXXXXXX/XXXXXXXX`).

#### B) Colocar na Kiwify
1. Kiwify → **Produtos** → produto da oferta.
2. **Configurações** → **Pixels de Conversão**.
3. **Adicionar Pixel** → **Google Ads**.
4. Colar o **ID de conversão** e o **label**.
5. Marcar só o evento de compra aprovada. **Não** contar visita ao checkout como conversão.

#### C) GA4 (opcional, muito útil)
1. Criar uma propriedade Google Analytics 4.
2. Copiar o `Measurement ID` (`G-XXXXXXXXXX`).
3. Kiwify → **Pixels de Conversão** → **G Analytics** → colar o ID.
4. Salvar.

#### D) Meta Pixel (só depois)
Quando houver conta nova em **outro aparelho/notebook e outro e-mail**:
1. Criar Business Manager novo.
2. Gerenciador de Eventos → criar Pixel.
3. Copiar o ID do Pixel.
4. Kiwify → **Pixels de Conversão** → **Facebook/Meta** → colar o ID.
5. Não reutilizar e-mail, aparelho, número ou celular que já foi banido.

---

## 5) DEPOIS DO PIXEL

- Conferir na Kiwify as vendas reais (Cartão e Pix) contra os cliques do botão.
- Só depois pensar em anúncios.
- Regra atual: destino da campanha é **Home** ou **`/livro11`**, não carrossel de preço.
- Redes sociais: voltar só quando a nova conta estiver estável.

---

## ORDEM RECOMENDADA

1. Rodar `APLICAR_IDENTIDADE_MISSAO.py` no servidor.
2. Conferir as páginas no ar.
3. Atualizar e submeter o sitemap no Search Console.
4. Pedir indexação das 9 páginas.
5. Criar pixel Google Ads + GA4 e colar na Kiwify.
6. Acompanhar vendas reais vs cliques.
7. Só depois pensar em Meta/Instagram e anúncios.
