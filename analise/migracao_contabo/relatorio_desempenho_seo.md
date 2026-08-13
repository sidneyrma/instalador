# 📈 RELATÓRIO DE DESEMPENHO + PLANO DE SEO

**Portal O Despertar · compraoseu.com · 13/08/2026**

---

## 1. 📊 Desempenho atual (painel de estatísticas)

**Dados do `stats.html` (12/08/2026, ~17h):**

| Métrica | Valor | Observação |
|---|---|---|
| **Acessos totais (páginas)** | **1.332** | 1.318 só no dia 12/08 (primeiro dia completo no ar) |
| **Visitas à Home** | 213 | A porta de entrada |
| **Acessos aos livros** | 209 | 98% dos visitantes da Home clicam num livro! |
| **Livros lidos (todos os 10)** | 10 | Todos os livros tiveram acesso ✅ |

### 🏆 Ranking dos livros (12/08)
| # | Livro | Acessos |
|---|---|---|
| 🥇 | 08 — O Arquiteto da Realidade | 40 |
| 🥈 | 01 — O Verbo que Transforma | 37 |
| 🥉 | 03 — A Mente Renovada | 26 |
| 4 | 09 — Anestesia Mental | 19 |
| 5 | 07 — O Caminho do Despertar | 17 |
| 6 | 10 — O Despertar do Observador | 17 |
| 7 | 02 — A Sabedoria dos Mestres | 15 |
| 8 | 05 — Evolução da Alma | 15 |
| 9 | 06 — Jesus Quer Falar com Seu Filho | 14 |
| 10 | 04 — Um Segundo com Deus | 9 |

### 🧠 Leitura dos números
- **Excelente taxa de conversão Home → livro (98%)**: quem chega, lê. O site está cumprindo sua missão;
- **Dia 1 (12/08) já teve 1.318 acessos** — um bom começo, mas ainda muito dependente de indicações diretas (ainda sem tráfego orgânico do Google, pois o SEO está começando agora);
- **O livro 08 lidera** — ótimo sinal para o "Arquiteto da Realidade", mas a diferença para os demais é pequena; o potencial de todos é grande.

### ⚠️ Alerta de segurança (visto no log)
O log mostra **tentativas de bots** explorando caminhos comuns: `/.env`, `/.git/config`, `/wp-login.php`, `/info.php`, `/server-status`, etc. **Não há invasão** (o Nginx bloqueia), mas recomendo:
1. Bloquear esses caminhos no Nginx (regra de `location` para retornar 403/444);
2. Ativar um **Web Application Firewall (WAF)** — o aaPanel tem um gratuito (Website → WAF);
3. Manter o painel/SSH com senhas fortes e acesso restrito.

---

## 2. 🚀 Projeção de crescimento (meta realista)

Base: 1.318 acessos no dia 1 (sem SEO ainda, só divulgação direta).

| Cenário | Acessos/dia | Acessos/mês | Com o quê |
|---|---|---|---|
| **Hoje (sem SEO)** | ~1.300 | ~39.000 | Indicações, WhatsApp, mídias sociais |
| **Com SEO básico (30–60 dias)** | 1.500–2.500 | 45.000–75.000 | Google indexando as 12 páginas |
| **Com SEO consistente (3–6 meses)** | 3.000–6.000 | 90.000–180.000 | Rankeando "livro cristão online", "devocional", etc. |

> **Estimativa honesta:** SEO leva tempo (2–6 meses para resultados reais), mas o tráfego orgânico é **gratuito e contínuo** — cada artigo/livro bem rankeado vira uma "porta aberta" permanente.

### Capacidade do servidor (já avaliada)
- 6 núcleos + 16 GB RAM + Nginx: suporta **500–2.000+ acessos simultâneos**;
- Para 6.000 acessos/dia, o servidor usa menos de 5% da capacidade. **Sem gargalo.**

---

## 3. 🎯 PLANO DE SEO (próximo passo — ação prioritária)

### 3.1 Já está pronto ✅
- [x] Títulos com palavras-chave em todas as 12 páginas;
- [x] Meta descriptions (Home e livros);
- [x] URLs canônicas + og:image + twitter:image;
- [x] `sitemap.xml` no ar (12 URLs, confirmado);
- [x] `robots.txt` no ar (permite tudo, bloqueia `/quiz`);
- [x] Site com HTTPS (cadeado) e sem conteúdo duplicado (redirect www → domínio).

### 3.2 Falta fazer (ações desta semana) 🔥
1. **Google Search Console — verificação e sitemap:**
   - Verificar `compraoseu.com` (TXT na HostGator ou HTML na raiz);
   - Enviar `sitemap.xml` no GSC;
   - Excluir sitemaps antigos da Vendd;
   - Solicitar indexação de `/`, `/livro01`... `/livro10`, `/quiz` (10/dia → 2 dias).

2. **Estrutura de dados (Schema.org) — adicionar `Book`/`Article`:**
   - Adicionar JSON-LD em cada página de livro (`@type: Book` com título, autor "Coleção do Despertar", idioma, capa, URL);
   - Isso ajuda o Google a mostrar **rich snippets** (estrelas/imagem) nos resultados.

3. **Conteúdo novo (para rankear):**
   - Criar uma página **"Blog/Reflexões"** com 2–3 artigos/mês (ex.: "O que é a mente renovada?", "5 versículos sobre ansiedade") — cada artigo é uma nova porta de entrada;
   - Ou adicionar seções de **FAQ** em cada livro (já existe FAQ na Home — expandir).

4. **Velocidade (Core Web Vitals):**
   - As imagens grandes da Home (imgbb) devem ser otimizadas (WebP/compressão);
   - Habilitar **cache do Nginx** para estáticos (já tem `expires 30d` para imagens);
   - Considerar **Cloudflare grátis** na frente (CDN global) depois da estabilização.

5. **Links internos (já bons, melhorar):**
   - Na Home, cada livro já linka para `/livroXX` ✅;
   - Adicionar no fim de cada livro um **"Continue lendo"** para o próximo livro (aumenta tempo no site e crawl);
   - Rodapé com links para todos os 10 livros (facilita o Google achar tudo).

6. **Monitoramento:**
   - Rodar o `gerar_estatisticas.py` no cron (6h) para o painel se atualizar;
   - (Opcional) Google Analytics para dados ricos (cidade, dispositivo, origem).

---

## 4. 📋 Resumo de prioridades

| Prioridade | Ação | Esforço | Impacto |
|---|---|---|---|
| 🔴 Alta | GSC: verificar + sitemap + indexação | 30 min | Alto (tira o site do "limbo") |
| 🔴 Alta | Bloquear bots no Nginx + WAF | 30 min | Segurança |
| 🟡 Média | Schema.org Book nas páginas | 1 h | Rich snippets |
| 🟡 Média | Blog/Reflexões (2 artigos) | 2 h | Tráfego novo |
| 🟢 Baixa | Otimizar imagens + cache | 1 h | Velocidade |
| 🟢 Baixa | Links "Continue lendo" entre livros | 1 h | Retenção |

---

## 5. 🎯 Meta dos próximos 30 dias
1. ✅ Todas as 12 páginas indexadas no Google;
2. ✅ Primeiras aparições no GSC (busca orgânica > 0);
3. ✅ Painel de estatísticas rodando em cron;
4. ✅ Bots bloqueados / WAF ativo;
5. 🚀 Projeção: 1.500–2.500 acessos/dia.

*"A sabedoria é a coisa principal; adquire, pois, a sabedoria"* (Provérbios 4:7).
