# 📚 EDIÇÕES ABNT PROTEGIDAS — Coleção do Despertar

**Pasta:** `edicoes/abnt/`

Estas são as edições em PDF dos livros da Coleção do Despertar, formatadas segundo
o padrão ABNT de editoras brasileiras, **protegidas contra cópia e impressão**.

## 📄 Formato (padrão ABNT de livros físicos)

| Elemento | Especificação |
|---|---|
| **Página** | 16 x 23 cm (livro físico brasileiro) |
| **Margens** | 3 cm superior e esquerda · 2 cm inferior e direita |
| **Fonte** | Times New Roman 12 pt |
| **Entrelinha** | 1,5 (18 pt) |
| **Recuo** | 1,25 cm na primeira linha de cada parágrafo |
| **Estrutura** | Capa → Folha de rosto → Créditos → Sumário → Capítulos |

## 🛡️ Proteção

- **Cópia bloqueada** (seleção e extração de texto desativadas);
- **Impressão bloqueada**;
- **Modificação bloqueada**;
- O leitor consegue **apenas abrir e ler** o PDF.
- Senha de dono: `colegiododespertar2026` (para eventuais ajustes internos).

> ⚠️ Como qualquer PDF, leitores muito avançados podem tentar contornar a proteção.
> Este é um **deterrente** e um selo de zelo, não uma barreira absoluta.
> O uso pretendido é: **documentação das obras** e futura **doação** de materiais
> formatados, conforme permissão.

## 📖 Livros incluídos

| Arquivo | Livro | Páginas |
|---|---|---|
| `livro01.pdf` | O Ouro das Palavras (Joseph Murphy) | 45 |
| `livro02.pdf` | O Livro Proibido dos Mestres | 65 |
| `livro03.pdf` | A Mente de Cristo (Emmet Fox) | 59 |
| `livro05.pdf` | Evolução da Alma | 93 |
| `livro07.pdf` | O Caminho do Despertar | 45 |
| `livro08.pdf` | Você e o Universo | 105 |
| `livro09.pdf` | Anestesia Mental | 83 |
| `livro10.pdf` | O Despertar do Observador | 104 |

> **Não incluídos por pedido:** Devocional (livro04) e Jesus Quer Falar com Seu Filho
> (livro06) — possuem imagens e atividades que não fazem sentido em PDF de texto puro.

## 🔄 Regenerar

```bash
pyenv/bin/python analise/compraoseu.preview/gerar_pdfs_abnt.py
```

O script lê as páginas HTML já validadas (`paginas/livroXX_preview.html`) e gera os
PDFs com proteção. Qualquer atualização dos livros nas páginas se reflete nos PDFs
após rodar o script.

*Coleção do Despertar · Missão com Deus · CompraOSeu · 2026*
