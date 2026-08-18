# 📚 EDIÇÕES ABNT PROTEGIDAS — Coleção do Despertar

> **Status (13/08/2026):** os PDFs ABNT **foram removidos do repositório** para
> deixá-lo mais leve (o usuário mantém cópias locais). Eles podem ser **regenerados
> a qualquer momento** com o script abaixo — as páginas HTML continuam no repositório.

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

- Cópia bloqueada (seleção e extração de texto desativadas);
- Impressão bloqueada;
- Modificação bloqueada;
- O leitor consegue apenas abrir e ler o PDF.
- Senha de dono: `colegiododespertar2026` (para eventuais ajustes internos).

> ⚠️ Como qualquer PDF, leitores muito avançados podem tentar contornar a proteção.
> É um deterrente e um selo de zelo, não uma barreira absoluta.

## 📖 Livros gerados (antes da remoção)

| Arquivo | Livro |
|---|---|
| `livro01.pdf` | O Verbo que Transforma |
| `livro02.pdf` | A Sabedoria dos Mestres |
| `livro03.pdf` | A Mente Renovada |
| `livro05.pdf` | Evolução da Alma |
| `livro07.pdf` | O Caminho do Despertar |
| `livro08.pdf` | O Arquiteto da Realidade |
| `livro09.pdf` | Anestesia Mental |
| `livro10.pdf` | O Despertar do Observador |

> **Não incluídos:** Devocional (livro04) e Jesus Quer Falar com Seu Filho
> (livro06) — possuem imagens/atividades que não fazem sentido em PDF de texto puro.

## 🔄 Regenerar (quando precisar)

```bash
pyenv/bin/python analise/compraoseu.preview/gerar_pdfs_abnt.py
```

O script lê as páginas HTML (`paginas/livroXX_preview.html`) e gera os PDFs com
proteção. Qualquer atualização dos livros se reflete nos PDFs após rodar o script.

*Coleção do Despertar · Missão com Deus · CompraOSeu · 2026*
