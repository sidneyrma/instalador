# 🔄 GUIA: ATUALIZAR O CHATBOT CONECTAI (LAURA) NO SERVIDOR

**Portal O Despertar · app.compraoseu.com · Atualizado 12/08/2026**

---

## 📦 Como transferir o código (50 MB) para o servidor

O limite de 25 MB é **só da interface web do GitHub** (botão "Add file").
Para 50 MB, use uma destas opções:

### Opção 1 — Upload direto no aaPanel (mais simples)
1. aaPanel → **Files** → `/home/deploy/` → **Upload** → arraste o `.zip`;
2. Se der erro de limite: **Software Store → PHP → Configuração → `upload_max_filesize`** → `100M` → reiniciar PHP;
3. Seguir os passos de atualização abaixo.

### Opção 2 — Dividir o zip em partes (~10 MB cada)
1. No PC: 7-Zip/WinRAR → "Split to volumes" (ou Linux: `split -b 10M conectai.zip parte_`);
2. Enviar as partes no File Manager;
3. No Terminal do servidor:
   ```
   cat parte_* > conectai.zip
   ```

### Opção 3 — Baixar direto no servidor (com link)
```
wget -O conectai.zip "LINK_DIRETO_AQUI"
```

### Opção 4 — Git (se o repositório da Conectai ainda existir)
```
cd /home/deploy/conectai && git pull origin main
```

---

## 🔄 Passos de atualização (sempre com BACKUP!)

### 1. Backup do atual
```
mv /home/deploy/conectai /home/deploy/conectai_backup_$(date +%Y%m%d)
```

### 2. Extrair o novo
```
unzip /home/deploy/conectai.zip -d /home/deploy/
```
(se a pasta extraída não se chamar `conectai`, renomear)

### 3. Dependências + build
```
cd /home/deploy/conectai/frontend && npm install && npm run build
cd /home/deploy/conectai/backend && npm install
cd /home/deploy/conectai/api_oficial && npm install
```
> Se o `build` do frontend falhar, copie a mensagem de erro.

### 4. Reiniciar PM2
```
pm2 restart all
pm2 save
```

### 5. Verificar portas e versão
```
ss -tulpn | grep -E ":3000|:4000|:6000"
grep '"version"' /home/deploy/conectai/frontend/package.json
grep '"version"' /home/deploy/conectai/backend/package.json
grep '"version"' /home/deploy/conectai/api_oficial/package.json
```

### 6. Testar
- `https://app.compraoseu.com` → login e menus funcionando;
- `https://api.compraoseu.com` e `https://apioficial.compraoseu.com` respondendo.

---

## 🔙 Se der problema (rollback em 1 minuto)
```
mv /home/deploy/conectai /home/deploy/conectai_problema
mv /home/deploy/conectai_backup_$(data) /home/deploy/conectai
pm2 restart all
```

---

## 🧭 Estrutura do Conectai (referência)
| Pasta | Porta | Função |
|---|---|---|
| `/home/deploy/conectai/frontend` | 3000 | Interface (com `build/`) |
| `/home/deploy/conectai/backend` | 4000 | Backend |
| `/home/deploy/conectai/api_oficial` | 6000 | API oficial WhatsApp |

*"Tudo o que fizerdes, fazei-o de todo o coração, como ao Senhor"* (Colossenses 3:23).
