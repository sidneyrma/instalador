# 📊 GUIA: ESTATÍSTICAS DE ACESSO + SEO NO GOOGLE

**Portal O Despertar · compraoseu.com · Atualizado 12/08/2026**

---

## 1. 📊 Painel de Estatísticas de Acesso

O servidor Nginx **já registra todos os acessos** no log `/www/wwwlogs/compraoseu.com.log`.
O script `gerar_estatisticas.py` lê esse log e gera **`stats.html`** com:
- Total de acessos (páginas) e **visitas à Home** (a ponte para os livros);
- **Ranking completo: Home + 10 livros + quiz** (o mais acessado no topo 🥇), com % e barra;
- Acessos por dia (últimos 7);
- Outras páginas acessadas.

### Instalar no servidor (aaPanel) — 5 minutos
1. **Suba o script:** aaPanel → Files → `/home/deploy/` → envie
   `analise/compraoseu.preview/gerar_estatisticas.py` (do repositório no GitHub);
2. **Teste no Terminal:** `python3 /home/deploy/gerar_estatisticas.py`;
3. **Acesse:** `https://compraoseu.com/stats.html`;
4. **Atualização automática (opcional):** aaPanel → **Cron** → Shell → a cada 1 hora
   (ou a cada 30 min, se quiser leitura mais fresca):
   `python3 /home/deploy/gerar_estatisticas.py`
   (o script sobrescreve o mesmo stats.html; não acumula arquivos. Só o log do
   Nginx cresce — o aaPanel faz rotação; opcional: cron mensal
   `find /www/wwwlogs -name "*.log" -mtime +30 -delete`).

### 📊 Sobre a "Variação" do painel (comparação justa)

Desde a versão atualizada, o painel compara **hoje (parcial) contra ontem até o
mesmo horário**, e ainda mostra a **projeção do dia** (ritmo atual estendido
para 24h). Isso evita a leitura enganosa de "queda" no meio do dia (comparar
parcial com o dia inteiro de ontem sempre mostra queda de manhã).

### 🔧 Se o stats.html der 404 (solução — causa: redirect para www)

**Sintoma:** `curl -I https://compraoseu.com/stats.html` responde **301** com
`location: http://www.compraoseu.com/stats.html` e o navegador dá 404.

**Causa:** existe um **redirect** de `compraoseu.com` → `www.compraoseu.com` (em http),
e o `www` não serve os arquivos com https.

**Solução (aaPanel):**
1. Site `compraoseu.com` → **Redirect** → remover qualquer regra que envie
   `compraoseu.com` → `www.compraoseu.com` (o correto é não ter redirect, ou ter o inverso);
2. **Website** → se existir um site **separado** `www.compraoseu.com`, **excluir**;
3. Site `compraoseu.com` → **Domain Manager** → confirmar que `www.compraoseu.com` está na lista;
4. **Reload** no Nginx;
5. Testar: `curl -I https://compraoseu.com/stats.html` → deve responder **200**.

---
### 🔒 Proteção
A página já tem `noindex` (não aparece no Google). Se quiser senha, use auth básico no Nginx
ou renomeie para um nome difícil.

> **Dica:** para dados ricos (cidade, dispositivo, origem), instale depois o **Google Analytics**
> (grátis) com o código no `<head>` da Home.

---

## 2. 🚀 SEO — Google Search Console

### 2.1 Verificar o site
1. `search.google.com/search-console` → **Adicionar propriedade** → **Domínio** → `compraoseu.com`;
2. Verificação por **TXT** (HostGator → Zona DNS) ou **HTML** (Files na raiz do site);
3. Confirmar.

### 2.2 Sitemap
1. O `sitemap.xml` já está no ar (`https://compraoseu.com/sitemap.xml`);
2. GSC → **Sitemaps** → `sitemap.xml` → Enviar;
3. Exclua sitemaps antigos da Vendd (com erro).

### 2.3 Solicitar indexação
1. GSC → **Inspeção de URL** → `https://compraoseu.com/` → Solicitar indexação;
2. Repita para `/livro01` ... `/livro10`, `/quiz` (limite ~10/dia, faça em 2 dias).

### 2.4 Configurações
- `robots.txt` já permite tudo (bloqueia só `/quiz`);
- Páginas públicas: `noindex` **desmarcado**;
- `stats.html`: `noindex` (como já está).

---

## 3. 🧭 Arquivos
| Arquivo | Função |
|---|---|
| `analise/compraoseu.preview/gerar_estatisticas.py` | Gera o painel (rodar no servidor) |
| `stats.html` (gerado) | `/stats.html` |
| `docs/sitemap.xml` / `site-contabo/sitemap.xml` | Sitemap |
| `docs/robots.txt` / `site-contabo/robots.txt` | Regras para buscadores |
| `analise/seo/kit_seo_completo.md` | Metadados (PÁGINAS 1–12) |

*"A sabedoria é a coisa principal; adquire, pois, a sabedoria"* (Provérbios 4:7).
