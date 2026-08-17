# MEMÓRIA DO PROJETO — MISSÃO COM DEUS
## Atualizado em: 17/08/2026

---

## 🖥️ INFRAESTRUTURA DO SERVIDOR

- **Provedor:** Contabo VPS
- **IP:** 212.28.182.86
- **OS:** Ubuntu 22.04.5 LTS
- **Nginx:** 1.18.0
- **PHP:** 8.1.32
- **RAM:** 15GB (14% uso)
- **Disco:** 194GB (8% uso)
- **Painel:** aaPanel

---

## 🌐 DOMÍNIOS E ESTRUTURA

| Domínio | Pasta no Servidor | Função |
|---------|-------------------|--------|
| compraoseu.com | /www/wwwroot/compraoseu.com/ | Site principal |
| missaocomdeus.com.br | /www/wwwroot/missaocomdeus.com.br/ | Novo domínio |
| app.compraoseu.com | /www/wwwroot/app.compraoseu.com/ | Frontend Laura |
| api.compraoseu.com | /www/wwwroot/api.compraoseu.com/ | Backend API |
| apioficial.compraoseu.com | /www/wwwroot/apioficial.compraoseu.com/ | Webhooks WhatsApp |

---

## 📁 ESTRUTURA DO SITE PRINCIPAL (compraoseu.com)

### Tecnologia
- HTML puro + PHP (SEM WordPress)
- Nginx 1.18.0
- PHP 8.1.32

### Arquivos Principais
- index.html — Página principal (86KB)
- leitor.html — Leitor de livros online
- enquete.php — Sistema de enquetes
- enquete_dados.json — Dados das enquetes
- livro01.html até livro11.html — 11 livros online
- manifest.json — PWA configurado
- robots.txt — SEO configurado
- sitemap.xml — Mapa do site
- sw.js — Service Worker (PWA)

### Pastas
- /capas/ — Imagens das capas dos livros
- /ebooks/ — Arquivos dos livros
- /icones/ — Ícones do site
- /nginx/ — Configurações extras Nginx

### Backup
- site-contabo.zip (2.9MB) na pasta raiz

---

## 🔐 SEGURANÇA NGINX (compraoseu.com)

- Bloqueio de bots maliciosos ativo
- Limite de requisições: 20r/s (burst 40)
- SSL TLS 1.1/1.2/1.3 ativo
- HSTS configurado (31536000s)
- Arquivos sensíveis bloqueados (444)

---

## 🤖 CHATBOX LAURA

- **Frontend:** app.compraoseu.com
- **Backend:** api.compraoseu.com
- **Webhooks:** apioficial.compraoseu.com
- **Integração:** WhatsApp Business + OpenAI
- **IMPORTANTE:** Não alterar URLs das APIs!
  Os webhooks do WhatsApp dependem
  dessas URLs estáticas.

---

## 🆕 NOVO DOMÍNIO — missaocomdeus.com.br

- **Registrado em:** 17/08/2026
- **Registrar:** HostGator Brasil
- **Valor pago:** R$ 41,99
- **Renovação:** R$ 70,99/ano em 17/08/2027
- **Site criado no aaPanel:** ✅ Sim
- **DNS apontado:** ⏳ Aguardando HostGator
- **SSL ativo:** ⏳ Aguardando DNS

### Passos Pendentes
- [ ] HostGator liberar domínio (até 24h)
- [ ] Apontar DNS para 212.28.182.86
- [ ] Ativar SSL (Let's Encrypt) no aaPanel
- [ ] Copiar arquivos do compraoseu.com
- [ ] Ajustar títulos e textos para novo nome
- [ ] Configurar redirecionamento 301
- [ ] Atualizar sitemap.xml
- [ ] Testar todos os 11 livros no novo domínio

---

## 📌 COMO INICIAR NOVO CHAT

Ao abrir novo chat, informe:
1. Link deste arquivo no GitHub
2. Diga: "Continuar do ponto onde paramos"
3. Informe o status atual das pendências

**GitHub do Projeto:**
https://github.com/sidneyrma/instalador

---

## 🙏 PROPÓSITO DA MISSÃO

Site de livros evangélicos gratuitos online.
Conteúdo espiritual acessível a todos.
Integrado com Chatbox Laura (WhatsApp).
Construído com fé, persistência e amor.
"Até a consumação" — Mateus 28:20
