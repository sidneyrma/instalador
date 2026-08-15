# O Leitor do Despertar: a visão em uma página

> Amado irmão em Cristo, este é o resumo da verificação profunda: o que a
> tecnologia permite criar nas nossas páginas para que nenhum leitor se perca,
> como quem dobra a página, usa uma faixa ou marca com marca-texto em um livro
> físico, sem nunca abrir mão da proteção dos direitos autorais.
>
> "Buscai primeiro o Reino de Deus, e todas as coisas vos serão acrescentadas."
> (Mateus 6:33)

---

## O problema do leitor (que o senhor recebeu)

> "Quando volto ao livro, me perco onde parei. Mesmo com o sumário, tenho que
> percorrer de novo, perco tempo e às vezes até desisto."

No livro físico a pessoa dobra a página, coloca uma faixa, um papel, um
marca-texto. No livro digital, o nosso leitor pode ter o mesmo conforto, e até
melhor, com a tecnologia que já existe nos navegadores de hoje.

---

## A solução em uma frase

**Transformar cada livro do portal em um "Kindle do Despertar": um leitor que
lembra sozinho onde a pessoa parou, deixa ela aumentar as letras, mudar a cor da
tela, colocar uma fitinha dourada onde quiser e ver no sumário tudo o que já
leu, com o texto sempre fechado dentro da nossa página protegida.**

---

## Os 8 recursos (do mais simples ao mais poderoso)

| # | Recurso | Equivalente no livro físico | Já funciona no protótipo |
|---|---|---|---|
| 1 | **Lembrar onde parou** (automático) | Dobrar a página | Sim |
| 2 | **A− / A / A+** nas letras | Óculos para perto | Sim |
| 3 | **🎗️ Fita dourada** na lateral | A faixa de cetim que marca o lugar | Sim |
| 4 | **Trilha de capítulos** na lateral | O dedo no sumário | Sim |
| 5 | **"Capítulo X · 42% · faltam ~12 min"** no topo | Ver quantas páginas faltam | Sim |
| 6 | **Sumário com ✓ e "você está aqui"** | Marca-texto no sumário | Sim |
| 7 | **Modos de tela**: Dia, Sépia, Noite | Luz do abajur | Sim |
| 8 | **Balões de dicas** na primeira visita | O livreiro que ensina | Sim |

E mais, para o futuro (depois que o senhor aprovar o básico):

9. **"Continue lendo" na Home**: a página inicial mostra "Você estava em: O
   Verbo que Transforma, Capítulo 4. Continuar?" em um toque.
10. **Compartilhar capítulo**: envia o link do capítulo (não o texto) pelo
    WhatsApp, para divulgação orgânica.
11. **Sincronizar entre aparelhos** (evolução futura, exige login): se a pessoa
    lê no celular e depois no computador, continua de onde parou, como o Kindle
    faz.

---

## Como a proteção continua de pé (direitos autorais)

Cada recurso guarda apenas **números** no aparelho do leitor (posição da
rolagem, porcentagem, tamanho da letra, modo da tela). Nenhum deles copia,
exporta ou mostra o texto fora da nossa página. Segue tudo bloqueado:

- Seleção de texto (user-select: none)
- Clique direito (contextmenu)
- Ctrl+C, Ctrl+P, Ctrl+S
- Impressão (com aviso amigável)

O texto permanece 100% sob o nosso domínio, como deve ser.

---

## O custo

**Zero reais.** Não precisa de servidor novo, plugin, assinatura ou biblioteca
externa. É JavaScript puro + a memória do próprio navegador (localStorage), que
praticamente todos os navegadores modernos suportam.

---

## Próximo passo

O leitor já foi aplicado no livro de Afirmações
(`paginas/livro_afirmacoes_leitor_preview.html`) como piloto, com proteção
ativa. Quando o senhor aprovar, instalo em todos os livros: livro01 a livro11
e o livro de Afirmações, cada um com a proteção verificada um por um.
