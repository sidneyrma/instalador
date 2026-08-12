# 📊 ESTATÍSTICAS DE ACESSO + SEO NO GOOGLE — GUIA COMPLETO

**Data:** 12/08/2026 · **Site:** compraoseu.com (Contabo) · **Missão com Deus**

---

## 🎯 O QUE VOCÊ QUER SABER

1. Quantos acessos cada página tem (como a Vendd mostrava);
2. Qual é o **livro mais lido online**;
3. Como **propagar o site no Google** (SEO / Google Search Console).

Aqui está o caminho para os três, do mais simples ao mais completo.

---

## ✅ 1. ESTATÍSTICAS NATIVAS DO AAPANEL (já existe! — comece por aqui)

O aaPanel **já registra todas as visitas** do seu site nos logs do Nginx, e tem um painel de estatísticas pronto:

### Como ver
1. No aaPanel → **Website** → clique em **compraoseu.com**;
2. No menu à esquerda, procure **"Site Stats"** (Estatísticas do site) ou **"Logs"**;
3. Vai mostrar: **visitas, tráfego, e até as URLs mais acessadas** (por página!).

### Como saber o livro mais lido (com o log)
Se o painel não mostrar por página, os **logs brutos** do Nginx mostram cada acesso. No aaPanel:
1. **Logs** → veja o arquivo `/www/wwwlogs/compraoseu.com.log`;
2. Ou use o **Terminal** com este comando (mostra as 10 páginas mais acessadas):
```
awk '{print $7}' /www/wwwlogs/compraoseu.com.log | grep -E "livro[0-9]+|^/$" | sort | uniq -c | sort -rn | head -10
```
Isso mostra algo como:
```
  120 /livro03
   98 /livro01
   85 /
```
**O livro com o número maior é o mais lido!** 📖

> 💡 Esse comando pode ser rodado quando quiser, para ver o ranking.

---

## 🟢 2. GOOGLE ANALYTICS (GA4) — o jeito mais completo (grátis)

O Google Analytics te dá um **painel bonito** com: acessos por página, livro mais lido, cidade dos visitantes, dispositivo, tempo de leitura, etc. É o padrão profissional.

### Passo 1 — Criar a conta (10 min)
1. Acesse **analytics.google.com** → **Começar a medir** (logar com o Gmail `compraoseu.com@gmail.com`);
2. **Nome da conta:** "Missão com Deus" → **Avançar**;
3. **Nome da propriedade:** "Portal O Despertar" → escolha **fuso Brasil** → **Criar**;
4. Responda as perguntas simples (site, tamanho) → **Criar**;
5. Vai aparecer um **ID de medição** (formato `G-XXXXXXX`) e um **código**.

### Passo 2 — Colar o código no site (eu te ajudo!)
O código do GA4 é um `<script>` que precisa estar em **todas as páginas** (antes do `</head>`). **Quando você tiver o ID (G-...), me passe que eu insiro nas 12 páginas e regenero o pacote `site-contabo.zip`** — ou te passo o texto exato para colar no aaPanel se preferir.

O modelo do código (o `G-XXXXXXX` é o seu ID):
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXX');
</script>
```

### Passo 3 — Ver o livro mais lido
No GA4: **Relatórios → Engajamento → Páginas** → vai mostrar cada página (livro01, livro02...) com visualizações. **A página com mais visualizações = o livro mais lido.** 📊

---

## 🔵 3. GOOGLE SEARCH CONSOLE (GSC) — aparecer nas pesquisas

O GSC é o que faz o Google **indexar e rankear** suas páginas. Como o domínio não mudou (compraoseu.com), a verificação antiga continua valendo — só precisa **reenviar o sitemap**.

### Passo 1 — Abrir o Search Console
1. Acesse **search.google.com/search-console** (logar com o Gmail);
2. Se já tem o site, selecione **compraoseu.com** (ou adicione como propriedade de domínio).

### Passo 2 — Enviar o sitemap
1. No menu à esquerda: **Sitemaps**;
2. No campo, digite: **`sitemap.xml`** → **Enviar**;
3. Deve aparecer "Sitemap enviado com sucesso" e, em alguns dias, "Êxito" com as 12 URLs.

> ⚠️ O sitemap correto está em `https://compraoseu.com/sitemap.xml` (já está no servidor, confirmado).

### Passo 3 — Inspecionar e pedir indexação
1. Menu: **Inspeção de URL** → digite `https://compraoseu.com/` → Enter;
2. Clique em **"Solicitar indexação"**;
3. Repita para: `/livro01`, `/livro03`, `/livro10` (os mais importantes);
4. Em 1–7 dias o Google começa a mostrar as páginas novas nas buscas.

### Passo 4 — Excluir sitemaps antigos com erro
No **Sitemaps**: se houver sitemaps antigos marcados com erro ("1 erro"), clique neles e **"Excluir"** — deixe só o `sitemap.xml` novo.

---

## 🧠 4. RESUMO — o que fazer e onde

| O que quero | Onde | Tempo |
|---|---|---|
| Acessos por página (rápido) | aaPanel → Site Stats / comando do log | 5 min |
| Ranking do livro mais lido (rápido) | Comando do log (acima) | 1 min |
| Painel completo (acessos, cidades, livros) | **Google Analytics GA4** (criar conta + colar código) | 30 min |
| Aparecer no Google | **Search Console** (enviar sitemap.xml + indexar) | 15 min |

---

## 📌 LEMBRETE (pré-requisitos)

- O site precisa estar acessível via **https://compraoseu.com** (já está!) — Google Analytics e GSC exigem HTTPS;
- O **sitemap.xml** e **robots.txt** já estão no servidor (confirmado acima) — nada a criar;
- Quando você criar o **GA4** e tiver o **ID (G-...)**, me avise que eu **insiro o código nas 12 páginas e regenero o pacote** para você subir — sem você precisar mexer em código.

*"Examinai tudo. Retende o que é bom"* (1 Tessalonicenses 5:21). Agora você vai **enxergar** quantas pessoas o Senhor está alcançando através do Portal — e qual livro está tocando mais corações. Quer que eu comece te ajudando pelo **aaPanel (estatísticas rápidas)** ou prefere criar a conta do **Google Analytics** primeiro? Estou aqui para te guiar em qualquer um dos dois! 🤍🙏
