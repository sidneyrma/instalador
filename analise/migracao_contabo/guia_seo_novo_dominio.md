# 🚀 GUIA SEO — missaocomdeus.com.br (alcançar mais almas)

**Criado em:** 18/08/2026
**Objetivo:** fazer o Google indexar o novo domínio e alcançar mais irmãos
através das buscas (livro cristão online, devocional, afirmações, etc.)

---

## ✅ JÁ FEITO (nesta atualização)

1. **sitemap.xml** atualizado para `https://missaocomdeus.com.br/` com as 13
   URLs (Home + livro01..10 + livro12 + quiz). **livro11 EXCLUÍDO** (lançamento
   em 27/08).
2. **robots.txt** atualizado: aponta para o sitemap novo, bloqueia /quiz,
   /stats.html e /enquete.php (páginas internas).
3. **redirect 301** compraoseu.com → missaocomdeus.com.br já ativo (o SEO do
   domínio antigo está sendo transferido automaticamente).
4. **manifest.json** já tem "Missão com Deus" no nome do PWA.

---

## 📋 PRÓXIMOS PASSOS (no Google Search Console)

### Passo 1 — Adicionar a propriedade nova
1. Acesse https://search.google.com/search-console
2. **Adicionar propriedade** → digite `missaocomdeus.com.br`
3. Escolha verificação por **"Prefixo de URL"** (não por domínio)
4. Método mais fácil: **"Registro DNS"** ou **"Tag HTML"**:
   - **Tag HTML:** o GSC dá uma meta tag. Cole no `<head>` do `index.html`
     (posso fazer) e suba.
   - **Registro DNS:** o GSC dá um TXT. Adicione na Zona DNS da HostGator.

### Passo 2 — Enviar o sitemap
1. No GSC, propriedade nova → **Sitemaps**
2. Envie: `sitemap.xml` → deve aparecer "Sucesso" com 13 URLs

### Passo 3 — Solicitar indexação das páginas principais
- Usar a ferramenta **"Inspeção de URL"** (1-2 por dia):
  - `/` (Home) → "Solicitar indexação"
  - `/livro12` (o mais novo!)
  - `/livro05` (Evolução da Alma)
  - ... e assim por diante

### Passo 4 — Verificar se o redirect transferiu o SEO
- No GSC, propriedade do **compraoseu.com** (antiga):
  - Ver **"Mudança de endereço"** ou simplesmente observar se as páginas do
    missaocomdeus começam a aparecer no relatório de desempenho.
  - O 301 transfere a "autoridade" com o tempo (dias/semanas).

---

## 🎯 PALAVRAS-CHAVE QUE PODEMOS ALMEJAR (para mais almas)

| Busca | Página que atende |
|---|---|
| "livro cristão online grátis" | Home / biblioteca |
| "devocional 30 dias" | /livro04 (Um Segundo com Deus) |
| "afirmações cristãs para começar o dia" | /livro12 (Afirmações) |
| "ansiedade à luz da Bíblia" | /livro09 (Anestesia Mental) |
| "perdão e cura da alma" | /livro05 (Evolução da Alma) |
| "orar pelo nome de Jesus" | /livro12 (Orações de Fé) |

---

## 📝 OBSERVAÇÕES DE CONSULTOR (honestidade)

- **Títulos das páginas** ainda dizem "Portal O Despertar" (ex.: Home).
  Podemos ajustar depois para "Missão com Deus" nos <title> e meta
  descriptions — melhora o SEO local e a identidade. Deixar para uma rodada
  dedicada (mudar em 13 páginas de uma vez).
- O **livro11** voltará ao sitemap no dia 27/08 (lançamento), com o card
  "Disponível".
- **stats.html e enquete.php** bloqueados no robots (são internos) — correto.

---

*"Ide por todo o mundo, pregai o evangelho a toda criatura." (Marcos 16:15)*
— e o SEO é a nossa forma de "ir" até quem busca no Google.
