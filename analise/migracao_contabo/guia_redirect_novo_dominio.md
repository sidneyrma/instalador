# 🔀 GUIA: REDIRECIONAR compraoseu.com → missaocomdeus.com.br (301)

**Criado em:** 18/08/2026
**Objetivo:** quando alguém digitar `compraoseu.com` (ou www), ser levado
automaticamente para o novo domínio `missaocomdeus.com.br`.

---

## ⚠️ ANTES DE FAZER (importante, honestidade total)

1. O **301 é permanente**: o navegador e o Google passam a guardar que o
   endereço antigo mudou. Isso **preserva o SEO** (a autoridade do
   compraoseu.com é transferida para o novo). É o recomendado.
2. Após aplicar, `https://compraoseu.com/stats.html` também redireciona —
   mas o stats agora é **copiado para o missaocomdeus** (gerar_estatisticas.py
   atualizado), então o painel continua acessível em
   `https://missaocomdeus.com.br/stats.html`.
3. Se preferir manter os dois no ar por um tempo, NÃO faça o redirect agora
   (decisão do autor).

## ✅ COMO FAZER (2 opções)

### Opção A — Pelo painel do aaPanel (mais segura)
1. aaPanel → **Sites** → `compraoseu.com`
2. Procure a opção **"Redirect"** (ou "Redirecionar")
3. Crie uma regra: **todos os domínios** de `compraoseu.com` e
   `www.compraoseu.com` → **https://missaocomdeus.com.br** com o sufixo
   `$request_uri` (para preservar o caminho: /livro01 → /livro01)
4. Tipo: **301** (permanente) → Salvar

### Opção B — No Terminal (adicionar ao config do compraoseu)
No aaPanel → Sites → compraoseu.com → Configuração, adicione no bloco `server`:

```nginx
# REDIRECT 301 para o novo domínio
if ($host = compraoseu.com) { return 301 https://missaocomdeus.com.br$request_uri; }
if ($host = www.compraoseu.com) { return 301 https://missaocomdeus.com.br$request_uri; }
```

Ou, se o server_name já tem os dois, simplesmente:

```nginx
return 301 https://missaocomdeus.com.br$request_uri;
```

Depois: Salvar → Reload (e `nginx -t` deve passar — agora está OK!).

## 🧪 TESTAR
- Abrir `https://compraoseu.com` → deve cair em `https://missaocomdeus.com.br`
- Abrir `https://compraoseu.com/livro05` → deve cair em
  `https://missaocomdeus.com.br/livro05`
- Usar janela anônima (cache do navegador pode segurar o antigo)

## 🔁 SE QUISER DESFAZER
- Remover a regra de redirect (Opção A: apagar a regra; Opção B: remover as
  linhas `return 301`) → Salvar → Reload.
- O Google pode demorar dias para "esquecer" o 301, mas o site volta a
  funcionar nos dois.
