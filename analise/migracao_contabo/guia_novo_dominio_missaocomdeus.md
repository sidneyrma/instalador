# 🌐 GUIA: NOVO DOMÍNIO missaocomdeus.com.br (site pronto no aaPanel)

**Criado em:** 17/08/2026
**Registrar:** HostGator Brasil (R$ 41,99; renovação R$ 70,99/ano em 17/08/2027)
**Status:** ✅ **LIBERADO pela HostGator em 18/08/2026!** Pronto para os passos abaixo.

---

## 1. O que já está pronto

- ✅ Domínio registrado na HostGator (aguardando liberação)
- ✅ Site **missaocomdeus.com.br** criado no aaPanel (visto na lista de sites)
- ✅ DNS apontado? ⏳ (ver passo 2)
- ✅ Arquivos do site prontos no repositório (site-contabo/, 3,9 MB; zip 2,8 MB)

## 2. Passos quando a HostGator liberar

1. **DNS no painel da HostGator:** criar/editar o registro A:
   - `missaocomdeus.com.br` → `212.28.182.86`
   - `www.missaocomdeus.com.br` → `212.28.182.86`
   - Pode levar alguns minutos/horas para propagar (verificar em
     https://dnschecker.org depois).

2. **SSL no aaPanel:** Site `missaocomdeus.com.br` → **SSL** → Let's Encrypt →
   marcar o domínio + www → aplicar. (Só funciona depois do DNS propagar.)

3. **Copiar os arquivos:** enviar o `site-contabo.zip` (ou a pasta site-contabo/)
   para `/www/wwwroot/missaocomdeus.com.br/` e extrair por cima.
   ⚠️ NÃO copiar `enquete_dados.json` / `enquete_ips.json` (a enquete do novo
   domínio começa do zero, com votos 0 — isso é o esperado; ou copiar se
   quiser manter os votos atuais).

4. **Nginx (URLs bonitas):** em Sites → missaocomdeus.com.br → Configuração →
   no `location /`, usar:
   ```
   try_files $uri $uri.html $uri/index.html =404;
   ```
   Salvar + Reload.

5. **Redirecionamento (decisão):**
   - **Opção A (recomendada):** redirecionar `compraoseu.com` → `missaocomdeus.com.br`
     com **301** (permanente, preserva SEO). No aaPanel: Sites → compraoseu.com →
     Redirect → `https://missaocomdeus.com.br/$request_uri` (permanente).
   - **Opção B:** manter os dois sites funcionando (sem redirect).
   - ⚠️ Decisão: o autor precisa escolher. A sugestão de consultor é a Opção A
     (domínio .com.br passa mais confiança no Brasil e o nome "Missão com Deus"
     é o coração da obra).

6. **Sitemap/SEO:** atualizar o `sitemap.xml` para o novo domínio e adicionar a
   propriedade `missaocomdeus.com.br` no Google Search Console (depois da
   publicação).

7. **Testar:** abrir https://missaocomdeus.com.br (home + livro01..12 + enquete
   + e-book do quiz).

## 3. Ajustes de conteúdo para o novo nome (opcional)

Quando o novo domínio estiver no ar, considerar trocar nos títulos/textos:
- "Portal O Despertar" → "Portal Missão com Deus" (ou manter ambos)
- Títulos das páginas (title), meta description, manifest.json (nome do PWA)
- Isso pode ser feito depois, sem pressa; o conteúdo dos livros não muda.

---

## 4. 💾 SOBRE BACKUPS (resposta honesta do autor)

**Pergunta:** "Backup vai gerar arquivos grandes? Temos espaço? Vai comprometer
a VPN/desempenho do servidor?"

**Resposta com honestidade técnica:**

### a) Quanto espaço cada backup ocupa

| O que é | Tamanho típico |
|---|---|
| Site compraoseu.com (HTML/JS/PHP/PNG) | ~4 MB (2,8 MB zipado) |
| Site missaocomdeus.com.br (igual) | ~4 MB |
| app/api/apioficial (chatbot Conectaí) | depende (código + dados) |
| Banco de dados (se houver) | depende |

**Conclusão:** os sites são LEVES (4 MB cada). Mesmo com 5 sites, o backup
completo fica em torno de **20–100 MB** — pequeno para qualquer servidor.

### b) Espaço do servidor Contabo

O servidor Contabo costuma ter **muito espaço** (normalmente 200 GB+ de disco
SSD). Para confirmar, no **Terminal** do aaPanel:
```
df -h
```
(Vai mostrar o espaço total, usado e livre. Se o uso estiver abaixo de 80%,
está tranquilo.)

### c) Vai comprometer o desempenho?

- **Gerar backup** usa CPU/disco por alguns segundos/minutos, mas o aaPanel faz
  isso em segundo plano; não derruba o site.
- **Recomendação:** agendar backups em horário de pouco movimento (ex.: 04h da
  manhã) e manter **no máximo 2–3 backups antigos** por site (o aaPanel tem a
  opção de "reter X backups" — assim o disco não acumula).
- A pasta de backup padrão do aaPanel é `/www/backup`.

### d) IMPORTANTE — backups que NÃO estão no aaPanel

O aaPanel faz backup dos **sites** (arquivos em /www/wwwroot). Mas o **chatbot
Conectaí** está em `/home/deploy/conectai` — pode NÃO estar incluído no backup
automático do painel. Recomendo:
1. Fazer um backup manual da pasta `/home/deploy/conectai` (zipar e baixar,
   ou copiar para outro lugar);
2. Guardar uma cópia do `site-contabo.zip` (já temos no GitHub — o repositório
   É o nosso backup externo, o que é uma grande vantagem!);
3. O que o senhor atualizou no aaPanel e "não lembra o quê": se o site está
   funcionando, provavelmente foi algo simples (ex.: atualização do painel ou
   do Nginx). Não precisa se preocupar — os arquivos do site estão seguros no
   GitHub.

### e) Sugestão de rotina de backup

| Frequência | O quê | Onde |
|---|---|---|
| Diário (automático) | Sites do aaPanel (2-3 retidos) | /www/backup |
| A cada atualização | site-contabo.zip | GitHub (já feito automaticamente) |
| Semanal | /home/deploy/conectai (manual) | Baixar para o PC |

> **Conclusão:** o senhor TEM espaço de sobra, os backups dos sites são
> pequenos e não vão comprometer o desempenho. O mais importante é que o
> repositório GitHub já é o backup externo de todo o código — e o senhor pode
> baixar o zip do site a qualquer momento.
