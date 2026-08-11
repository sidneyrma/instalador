# 🗂️ ORGANIZAÇÃO DO REPOSITÓRIO — COMPRAOSEU / MISSÃO COM DEUS

**Data da organização:** 11/08/2026

---

## ✅ Estrutura final (enxuta e organizada)

```
instalador/
├── paginas/                     → PÁGINAS OFICIAIS do site (prontas para publicar)
│   ├── home_preview.html        →   Home (Portal O Despertar)
│   ├── livro01_preview.html ... livro10_preview.html  →   os 10 livros
│   └── README.md
│
├── site-contabo/                → PACOTE DE MIGRAÇÃO (servidor Contabo/aaPanel)
│   ├── index.html + livro01-10.html   (links relativos)
│   ├── capas/  icones/  manifest.json  sw.js  robots.txt  sitemap.xml
│   └── nginx/                   →   compraoseu.conf + .htaccess
├── site-contabo.zip             → mesmo pacote compactado (pronto para upload)
│
├── docs/                        → GITHUB PAGES (publicado em sidneyrma.github.io/instalador)
│   ├── capas/                   →   capas oficiais dos livros
│   ├── icones/                  →   ícones PWA
│   ├── index.html  manifest.json  sitemap.xml  .nojekyll
│
├── livro/                       → FONTES ORIGINAIS das obras (textos, PDFs, DOCX)
│   └── fontes/                  →   fontes Tinos (usadas nas capas)
│
├── edicoes/abnt/                → PDFs ABNT protegidos (livros 01-10)
│
└── analise/                     → DOCUMENTAÇÃO E ARQUIVOS DE TRABALHO
    ├── migracao_contabo/        →   guia de migração + tutorial completo + análise Contabo vs Vendd
    ├── chatbot/                 →   prompt da Laura + mensagens humanizadas
    ├── livro01_reescrito/       →   obra original "O Verbo que Transforma"
    ├── livro02_reescrito/       →   obra original "A Sabedoria dos Mestres"
    ├── livro08_reescrito/       →   obra original "O Arquiteto da Realidade"
    ├── livro10/                 →   obra original "O Despertar do Observador"
    ├── seo/                     →   kit SEO, sitemap, robots, guias GSC/Vendd
    ├── compraoseu.preview/      →   scripts de geração (capas, páginas, PDFs, PWA)
    └── inspecao_publicacao.md, inspiracoes_escrituras.md, relatórios
```

---

## 🧹 O que foi REMOVIDO na limpeza (11/08/2026)

| Item removido | Motivo |
|---|---|
| `analise/config.jpg`, `index.jpg`, `vpn.jpg`, `site.jpg` | Screenshots enviados para análise (já analisados) |
| `livro/Screenshot_*.jpg` | Screenshot do YouTube (não usado) |
| `image-search/` | Imagens de referência da busca (não usadas no site) |
| `compraoseu` (arquivo vazio) | Sem conteúdo |
| `analise/compraoseu.preview/imgs/` (todas) | Imagens intermediárias/processo (artes rejeitadas, rascunhos) |
| `analise/compraoseu.preview/capa_trilogia_alma.png` | Não referenciada |
| `pwa/opcao_A/B/C_livro.png`, `comparacao_icones.png` | Mockups antigos (não usados) |
| `docs/capas/livro01_v5_*`, `v6_final` | Variantes de capa não aprovadas (a oficial é `livro01.png`) |
| `docs/prototipos/` | Protótipos antigos (o site real está em `paginas/`) |
| `analise/prototipo_*.html` | Protótipos antigos |
| `analise/vendd/` | Versões antigas da Vendd (desatualizadas) |
| `caibalion_preview.html`, `anestesia_preview.html`, `evolucao_preview.html` | Prévia antigas (oficiais em `paginas/`) |

> 💡 **Nada foi perdido definitivamente:** todos os arquivos removidos continuam no **histórico do Git**.
> Se um dia precisar de algum, é possível recuperar (`git log` / commit anterior).

---

## 📊 Números

- **Antes:** 289 arquivos · ~66 MB
- **Depois:** ~225 arquivos · ~43 MB
- **Redução:** ~22% em espaço, repositório mais limpo e com propósito claro.

---

## 🔒 Segurança

- **Nenhuma credencial** (senhas/endereços de acesso) está no repositório;
- Se algo sensível for enviado por engano no futuro, remover imediatamente e **rotacionar a senha** (trocar senha).

*"Tudo o que fizerdes, fazei-o de todo o coração, como ao Senhor"* (Colossenses 3:23).
