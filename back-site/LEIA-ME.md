# 🔧 Correção — Códigos de Acesso das Videoaulas

**Data:** 24/08/2026
**Feito em:** repositório `instalador` (branch `arena/01a034ef-instalador`)

---

## 🩺 O que estava acontecendo (diagnóstico)

1. As páginas do **Menu interno** são:
   - `site-contabo/trilogia-da-alma.html` → area do aluno da **Trilogia da Alma** (7 módulos / 7 vídeos)
   - `site-contabo/anestesia-mental.html` → area do aluno da **Anestesia Mental** (7 módulos / 7 vídeos)

2. Os códigos de acesso corretos são **apenas dois**:
   - `EVLTRLAM26` → Trilogia da Alma
   - `NSTMNT26` → Anestesia Mental

3. Ao digitar o código, o usuário **não estava indo para a área do aluno** (as 7 videoaulas).
   Em vez disso, ele era levado a **outra página criada por outro agente** (que também criou um
   código extra chamado **`GRACA37`**).

4. **Por quê:** essas páginas quebradas do "outro agente" estão **apenas no servidor (aaPanel)**
   e **não foram enviadas para o GitHub** (aquele agente tinha apenas acesso de leitura). Ou seja:
   o que está no repositório já são as páginas corretas; o servidor é que ficou com uma versão
   diferente e quebrada.

> **Conclusão:** a correção precisa ser **aplicada no servidor (aaPanel)** substituindo as duas
> páginas quebradas pelas versões corrigidas que estão aqui no repositório.

---

## ✅ O que foi feito neste repositório

- **Credo do backup:** criada a pasta `back-site/` com **cópia de todos os arquivos** de
  `site-contabo/` (apenas os arquivos, sem as pastas internas) — para poder reverter qualquer coisa.

- **Páginas corrigidas** (`site-contabo/trilogia-da-alma.html` e `site-contabo/anestesia-mental.html`):
  - Agora mostram a **página de boas-vindas / Vitrine do Semeador** (texto motivacional +
    botão "🕊️ Quero Ser Semeador(a)" + "💛 Solicitar Código de Acesso" no WhatsApp).
  - Ao digitar o **código correto**, a **mesma página** libera os **7 módulos com os 7 vídeos**
    (sem redirecionar para fora — o bug do "levar para outra página" foi eliminado).
  - **Só** aceita o código daquele curso:
    - Trilogia da Alma → `EVLTRLAM26`
    - Anestesia Mental → `NSTMNT26`
  - O código `GRACA37` **não existe mais** — qualquer outro código (incluindo `GRACA37`) mostra
    "Código inválido". Logo, só ficam os dois códigos corretos.

- Os arquivos originais (antes da correção) estão preservados em `back-site/`.

---

## 🚀 Como aplicar a correção (aaPanel)

Como eu não tenho os acessos do servidor (o sandbox não tem rede para o aaPanel), você precisa
**subir os dois arquivos abaixo** substituindo os que estão no servidor em
`/www/wwwroot/missaocomdeus.com.br/`:

| Arquivo no repositório | Onde colocar no servidor |
|---|---|
| `site-contabo/trilogia-da-alma.html` | `/www/wwwroot/missaocomdeus.com.br/trilogia-da-alma.html` |
| `site-contabo/anestesia-mental.html` | `/www/wwwroot/missaocomdeus.com.br/anestesia-mental.html` |

**Passos (aaPanel → Arquivos):**
1. Abra o **aaPanel → Arquivos** e navegue até `/www/wwwroot/missaocomdeus.com.br/`.
2. **Baixe/renomeie** (como segurança) os arquivos atuais
   `trilogia-da-alma.html` e `anestesia-mental.html` (ex.: adicionar `.bak`).
3. **Faça upload** dos dois arquivos corrigidos deste repositório no lugar.
4. Acesse `https://missaocomdeus.com.br/trilogia-da-alma` e
   `https://missaocomdeus.com.br/anestesia-mental` para testar:
   - Deve aparecer a página de boas-vindas;
   - digitando `EVLTRLAM26` (na Trilogia) ou `NSTMNT26` (na Anestesia) devem abrir os **7 módulos**;
   - digitando `GRACA37` não deve liberar nada.

> Se preferir, também pode rodar via Terminal no próprio servidor: faça o download dos arquivos
> deste repositório e `cp` para a pasta. **Sempre rode `nginx -t` antes de recarregar.**

---

## ↩️ Como reverter (se algo der errado)

Todas as versões originais estão em `back-site/`. Para restaurar:

```bash
cp back-site/trilogia-da-alma.html site-contabo/trilogia-da-alma.html
cp back-site/anestesia-mental.html site-contabo/anestesia-mental.html
```

E no servidor, basta restaurar os arquivos `.bak` que você guardou no passo 2.

---

## 🎬 Títulos oficiais dos módulos (alinhados com o cronograma do autor)

### 🌱 Trilogia Evolução da Alma
1. Bem-vindo(a) ao nosso Portal
2. O Despertar da Alma
3. A Superação das dificuldades emocionais
4. O Perdão como libertação da alma
5. O Propósito em ação
6. A Persistência na evolução constante
7. Vivendo em Luz, Propósito e Liberdade

### 🧠 Anestesia Mental
1. Bem-vindo(a) ao nosso Portal
2. A Anestesia Mental
3. O Governo da Mente
4. O Impulso sem Consciência
5. O Despertar da Consciência
6. O Reset do Shabat
7. A Liberdade da Alma

### 🔒 Os vídeos NÃO saem da página
- Não existe nenhum link clicável para o YouTube fora dos players.
- Todos os iframes usam `sandbox="allow-scripts allow-same-origin allow-presentation"` e
  `youtube-nocookie.com` — o player bloqueia popups e navegação, então o aluno permanece
  na página (cadeado anti-YouTube já configurado).

---

## 🔑 Códigos válidos (resumo)

| Curso | Código | Página |
|---|---|---|
| Trilogia da Alma | `EVLTRLAM26` | /trilogia-da-alma |
| Anestesia Mental | `NSTMNT26` | /anestesia-mental |

*Qualquer outro código (incluindo `GRACA37`) é inválido.*
