# 🛠️ Guia de Aplicação na Vendd

Como transformar os protótipos HTML em páginas reais na plataforma **Vendd** (editor baseado no Elementor), seção por seção.

**Arquivos usados:**
- `prototipo_devocional.html` — Devocional "Um Segundo com Deus" (R$ 9,90)
- `prototipo_evolucao.html` — Livro "Evolução da Alma" (R$ 19,90 / combo R$ 49,00)
- `prototipo_anestesia.html` — Livro "Anestesia Mental" (R$ 19,90 / combo R$ 49,00)

---

## 1. Preparação (5 min)

1. **Baixe os protótipos** do GitHub (botão "Download raw file") e abra no navegador para ver o visual de referência.
2. **Tenha os links de checkout em mãos:**
   - Devocional → `https://pay.kiwify.com.br/CF9nhFx` (R$ 9,90)
   - Evolução da Alma (individual) → `https://pay.kiwify.com.br/ptH32K9` (R$ 19,90)
   - Anestesia Mental (individual) → `https://pay.kiwify.com.br/NCf1jh4` (R$ 19,90)
   - Combo Trilogia + Anestesia → `https://pay.kiwify.com.br/iVfp2bi` (R$ 49,00)
3. **Defina as cores da marca** (as variáveis CSS dos protótipos):
   - Azul-marinho (fundo): `#0e1a2e`
   - Azul cartão: `#16283f`
   - Dourado: `#c9a24b`
   - Dourado claro: `#e3c877`
   - Fundo claro: `#f6f1e7`
   - Botão (dourado escuro): `#b8860b`

---

## 2. Criar a página (5 min)

1. Na Vendd, clique em **Páginas → Nova página**.
2. Escolha um **template em branco** (ou "Em branco/Blank").
3. Dê um nome: `evolucao-da-alma`, `anestesia-mental`, `um-segundo-com-deus`.
4. Publique em um domínio/rota (ex.: `www.compraoseu.com/evolucao-da-alma`).

> 💡 **Se a Vendd tiver "Importar HTML"** (opção de colar HTML/CSS), você pode colar o arquivo inteiro do protótipo e pular a reprodução manual. Verifique em **Configurações da página → Importar**.

---

## 3. Reproduzir cada seção (editor de blocos)

Para cada bloco do editor, use esta tabela:

| Seção do protótipo | Bloco no editor | Conteúdo |
|---|---|---|
| **Topo** | Cabeçalho (Header) | Logo "Missão com Deus" + texto "Livro · CompraOSeu" |
| **Hero** | Colunas (2) + Texto + Imagem + Botão | Título grande (Georgia), subtítulo, botão dourado com o checkout, imagem da capa (hospede no i.ibb.co ou no gerenciador de mídia da Vendd) |
| **Barra de confiança** | 4 ícones/lista em linha | ✓ Acesso imediato · ✓ Kiwify · ✓ Garantia 7 dias · ✓ Multi-dispositivo |
| **A Dor / A Anestesia** | Colunas (3) + Cards | Ícone emoji + título + descrição |
| **Solução / Fluxo** | Colunas (4) + Cards (fundo escuro) | Números 1–4 + título + texto |
| **O que você domina/aprende** | Colunas (3) + Listas | Título + bullets (copie do protótipo) |
| **Sobre a autora** | Colunas (2): imagem + texto | Foto da Laura + texto da bio |
| **O que você recebe** | Colunas (3) + Cards com check | ✓ PDF · ✓ Área do Aluno · ✓ Acesso vitalício |
| **Depoimento** | Bloco de citação/testemunho | Quote + nome + origem |
| **Oferta** | Card + preço + botão | Preço riscado, preço grande, botão com checkout, selo de segurança |
| **Garantia** | Caixa destacada | Selo "7 DIAS GARANTIA" + texto |
| **Upgrade (Experiência Completa)** | Card (fundo escuro) + lista + botão | Benefícios + botão `iVfp2bi` |
| **FAQ** | Acordeão/FAQ | 4–5 perguntas (copie do protótipo) |
| **CTA final** | Bloco centralizado | Título + botão grande |
| **Rodapé** | Footer | Links + copyright |
| **WhatsApp flutuante** | Widget WhatsApp (a Vendd tem) | `wa.me/5528999111493` com mensagem pré-preenchida |

---

## 4. Configurações importantes

### 4.1 Botões de compra (CTAs)
- Cada botão deve abrir o **link do checkout da Kiwify** em **nova aba** (`target="_blank"`).
- **Não mude os preços nos textos** — o que está escrito na página deve ser EXATAMENTE o que o checkout cobra (o erro atual é justamente esse).

### 4.2 Pixels e rastreamento (essencial)
Na Vendd (configurações da página ou conta):
- **Facebook Pixel / Meta Pixel**: adicione seu pixel para medir conversões e criar públicos;
- **Google Analytics**: adicione a tag (G-XXXX);
- **Google Ads**: se for anunciar, use o rótulo de conversão na página de obrigado.

### 4.3 Lead capture
- O **quiz** do Anestesia Mental pode ser mantido em HTML (widget) ou substituído por um **formulário da Vendd** capturando nome + WhatsApp — os leads vão direto para o CRM da Vendd.

### 4.4 WhatsApp
- Ative o **widget de WhatsApp** nativo da Vendd apontando para `5528999111493`.

---

## 5. Antes de publicar — checklist final

- [ ] Preços da página batem com os checkouts da Kiwify;
- [ ] Ícones aparecem corretamente (sem `shopping_bag` etc. — use emojis);
- [ ] Sem cronômetros falsos;
- [ ] Depoimentos reais (com autorização) ou removidos;
- [ ] Botões abrem em nova aba;
- [ ] Página carrega no celular (teste o modo responsivo);
- [ ] Pixel + Analytics ativos;
- [ ] Link do WhatsApp funcionando;
- [ ] Garantia de 7 dias mencionada.

---

## 6. Ordem recomendada de publicação

1. **Devocional (R$ 9,90)** — produto de entrada, baixa fricção;
2. **Evolução da Alma (R$ 19,90)** — produto principal;
3. **Anestesia Mental (R$ 19,90)** — com o quiz;
4. Sempre oferecendo o **Upgrade para a Experiência Completa (R$ 49,00)** em todas.

---

## 7. Depois de publicar: medir e melhorar

- **Meta/Facebook Pixel** → veja quantos visitantes chegam ao checkout (taxa de abandono);
- **Google Analytics** → veja em qual seção o visitante desiste (tempo na página, scroll);
- Teste A/B simples: troque o título do hero ou a cor do botão e compare;
- Peça depoimentos a quem já comprou o portal;
- **Tráfego**: crie 1 vídeo/dia no TikTok/Reels/YouTube com os ganchos já existentes ("Sua mente ainda pertence a você?"), CTA para o link na bio.

---

*Documento gerado em 05/08/2026 · Missão com Deus · CompraOSeu*
