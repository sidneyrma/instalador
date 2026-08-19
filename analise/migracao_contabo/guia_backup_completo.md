# 💾 GUIA COMPLETO DE BACKUP — MISSÃO COM DEUS

**Criado em:** 19/08/2026
**Objetivo:** salvar tudo no notebook por segurança, além do GitHub.

---

## 1. ✅ POR QUE O GITHUB JÁ É UM BACKUP (e por que ter outro)

**O GitHub já é o nosso backup externo mais valioso:**
- Todo o código do site (site-contabo/, paginas/, analise/) está lá
- Cada atualização vira um commit (histórico completo, pode voltar no tempo)
- Se o servidor inteiro cair, baixamos o site-contabo.zip do GitHub e restauramos

**Mas ter um backup local no notebook é a "segunda corda":**
- Proteção contra erro humano (apagar algo sem querer no GitHub)
- Acesso rápido sem internet
- Tranquilidade total — "duas cordas seguram melhor"

---

## 2. 📦 BACKUP DO SITE (arquivos do servidor)

### Opção A — Baixar do GitHub (o mais fácil e já pronto)
1. Acesse: https://github.com/sidneyrma/instalador
2. Botão verde **"Code"** → **"Download ZIP"**
3. Salve no notebook (ex.: pasta `MissaoComDeus/backup/github/`)
4. Pronto — é o repositório completo com tudo!

### Opção B — Copiar direto do servidor (via aaPanel)
1. aaPanel → **Files** → `/www/wwwroot/missaocomdeus.com.br/`
2. Selecione tudo → botão direito → **"Compress"** (zipar)
3. Baixe o .zip gerado para o notebook
4. Repita para `/www/wwwroot/compraoseu.com/`
5. Guarde em: `MissaoComDeus/backup/servidor/`

### Opção C — Via Terminal (cópia direta)
```bash
# Cria um zip de cada site (roda no servidor)
cd /www/wwwroot
zip -r backup_missaocomdeus.zip missaocomdeus.com.br -x "missaocomdeus.com.br/enquete_dados.json"
zip -r backup_compraoseu.zip compraoseu.com -x "compraoseu.com/enquete_dados.json"
```
Depois baixe os dois .zip pelo aaPanel (Files → /www/wwwroot).

---

## 3. 🤖 BACKUP DO CHATBOT (CONECTAÍ / LAURA) — IMPORTANTE!

**Este NÃO está no GitHub e NÃO está no backup automático do painel!**
O chatbot está em `/home/deploy/conectai` e precisa de backup manual:

```bash
# No Terminal do servidor
cd /home/deploy
zip -r conectai_backup.zip conectai -x "conectai/node_modules/*" "conectai/*.log"
```
> ⚠️ Excluímos node_modules (pode recriar com `npm install`) e logs.

Depois baixe `conectai_backup.zip` pelo aaPanel (Files → /home/deploy/) para o notebook.

**Alternativa (se quiser incluir tudo, inclusive node_modules):**
```bash
zip -r conectai_backup_completo.zip conectai
```
(fica maior, mas é cópia exata)

---

## 4. 🗄️ BACKUP DO BANCO DE DADOS (se existir)

O site usa **arquivos JSON** (enquete_dados.json, enquete_ips.json) — não tem MySQL no site principal. Mas o **chatbot Conectaí** pode usar um banco (SQLite ou MongoDB). Verifique:

```bash
# Procurar arquivos de banco no chatbot
find /home/deploy/conectai -name "*.db" -o -name "*.sqlite" 2>/dev/null | head
```

Se aparecer algum `.db` ou `.sqlite`, o backup do chatbot (passo 3) já o inclui. ✅

---

## 5. ⚙️ BACKUP DAS CONFIGURAÇÕES (nginx + php)

```bash
# Configurações do Nginx (todos os sites)
cp -r /www/server/panel/vhost/nginx /www/wwwroot/backup_nginx_config

# Arquivos manuais do Certbot (os que corrigimos)
cp /etc/nginx/sites-available/conectai-* /www/wwwroot/backup_nginx_config/ 2>/dev/null

# php.ini do PHP 8.1
cp /www/server/php/81/etc/php.ini /www/wwwroot/backup_nginx_config/

# Zipar tudo
cd /www/wwwroot
zip -r backup_configs.zip backup_nginx_config
```
Baixe `backup_configs.zip` pelo aaPanel e guarde no notebook.

---

## 6. 📅 ROTINA SUGERIDA (simples e suficiente)

| Frequência | O quê | Como |
|---|---|---|
| **A cada atualização** | site-contabo.zip | Já é salvo no GitHub automaticamente! |
| **Semanal** | Chatbot (conectai_backup.zip) | Terminal + baixar (passo 3) |
| **Semanal** | Configs (backup_configs.zip) | Terminal + baixar (passo 5) |
| **Mensal** | Baixar o repositório do GitHub | Code → Download ZIP (passo 2A) |

---

## 7. 📁 ORGANIZAÇÃO NO NOTEBOOK (sugestão)

```
MissaoComDeus/
└── backup/
    ├── github/            ← repositório completo (mensal)
    ├── servidor/          ← zips dos sites (quando fizer cópia manual)
    ├── conectai/          ← chatbot (semanal)
    └── configs/           ← nginx + php (semanal)
```

---

## 8. ⚠️ IMPORTANTE (honestidade total)

- **Os votos da enquete** (enquete_dados.json) ficam só no servidor — o zip
  NÃO os inclui de propósito (para não zerar). Se quiser backup deles:
  ```bash
  cp /www/wwwroot/missaocomdeus.com.br/enquete_dados.json /www/wwwroot/
  ```
  e baixe manualmente.
- **O GitHub continua sendo o principal** — o backup local é a garantia extra.
- Se um dia precisar restaurar: subir o site-contabo.zip + configs + chatbot
  pelo aaPanel (tudo está documentado neste guia).

---

*"O sábio de coração aceita os mandamentos" (Provérbios 10:8) — e aceitar a
sabedoria do backup é guardar a obra que Deus nos confiou. Que o Senhor nos
guarde de todo o mal, em sua glória e poder. Amém.*
