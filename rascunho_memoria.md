## 🎓 ÁREA DE ALUNOS (Trilogia e Anestesia Mental)

- **Arquivos:**
  - `site-contabo/trilogia-da-alma.html` (Trilogia da Alma)
  - `site-contabo/anestesia-mental.html` (Anestesia Mental)
- **Acesso:** Páginas protegidas por código de acesso via JavaScript (`EVLTRLAM26` e `NSTMNT26`). O estado de login é salvo no `localStorage` (`trilogia_acesso_ok` e `anestesia_acesso_ok`).
- **Conteúdo:** 7 videoaulas cada. Vídeos carregados via iframe do YouTube (nocookie), como "Não listados", para proteger o canal. Proporção 16:9, com `loading="lazy"` a partir da aula 02.
- **Progresso:** Sistema de marcação de aulas concluídas com botão "✓ Marcar aula como concluída", salvo no `localStorage` (`*_progresso`). Barra de progresso dourada fixa no topo.
- **Estatísticas (Sininhos):** O primeiro clique (pointerdown) no vídeo dispara uma requisição única por sessão para os marcadores `q-trilogia-m0X.html` e `q-anestesia-m0X.html` para registrar a visualização no log do Nginx.
- **Privacidade e SEO:** Áreas de alunos não indexadas (`<meta name="robots" content="noindex, nofollow">`) e ausentes no sitemap.

## 🏆 QUIZ DE AUTOAVALIAÇÃO (Home)

- **Novidade:** Adicionados "sininhos" de estatística para monitorar a conversão do quiz.
- **Início:** Ao selecionar a primeira resposta, é feito um fetch para `q-quiz-inicio.html`.
- **Fim:** Ao concluir o envio do e-mail, é feito um fetch para `q-quiz-fim.html`.
- **Registro:** Os dados são salvos no log do Nginx e processados pelo `gerar_estatisticas.py` para exibição no painel.
