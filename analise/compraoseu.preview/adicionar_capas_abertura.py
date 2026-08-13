# -*- coding: utf-8 -*-
"""
Adiciona a capa do livro na seção de abertura (.capa) de todas as páginas de leitura,
mantendo o padrão do livro08/mente_cristo:
  <img class="capa-livro" src="..." alt="...">
  <p class="selo">Coleção do Despertar</p> ...

Aplica a mesma mudança nos geradores (.py) para que a regeneração preserve a capa.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
PAGINAS = HERE.parent.parent / "paginas"
OBRA = HERE / "obra"

CSS_CAPA = (".capa .capa-livro{width:178px; height:auto; border:2px solid var(--ouro); border-radius:6px;\n"
            "  box-shadow:0 18px 44px rgba(0,0,0,.6); margin-bottom:1.8rem; -webkit-user-drag:none}")

# (página, gerador, url da capa, alt)
CONFIG = [
    ("livro01_preview.html", "gerar_livro01.py",
     "https://i.ibb.co/b52wmSGm/livro01jpg.jpg",
     "Capa do livro O Ouro das Palavras"),
    ("livro02_preview.html", "gerar_livro02.py",
     "https://i.ibb.co/W42S6bX0/livro02jpg.jpg",
     "Capa do livro O Livro Proibido dos Mestres"),
    ("livro03_preview.html", "gerar_livro03.py",
     "https://i.ibb.co/20jLgxZN/livro03jpg.jpg",
     "Capa do livro O Caibalion"),
    ("devocional_preview.html", "gerar_devocional.py",
     "https://i.ibb.co/Kx1mKFv6/umsegundocdeusjpg.jpg",
     "Capa do devocional Um Segundo com Deus"),
    ("evolucao_v2_preview.html", "gerar_evolucao_v2.py",
     "https://i.ibb.co/4n4ZtWZJ/Evolucao-Alma.jpg",
     "Capa do livro Evolução da Alma"),
    ("jesus_preview.html", "gerar_jesus.py",
     "https://i.ibb.co/8DLT57DZ/jesusfalarfilho.jpg",
     "Capa do livro Jesus Quer Falar com Seu Filho", ".capa .emoji-grande{"),
]


def aplica_em(conteudo, capa, alt, css_ancora=".capa .selo{"):
    # 1) CSS
    if ".capa .capa-livro{" not in conteudo:
        assert css_ancora in conteudo, f"âncora CSS não encontrada: {css_ancora}"
        conteudo = conteudo.replace(css_ancora, CSS_CAPA + "\n" + css_ancora, 1)
    # 2) <img class="capa-livro" ...> após <section class="capa">
    if '<img class="capa-livro"' not in conteudo:
        assert '<section class="capa">' in conteudo
        img = f'  <img class="capa-livro" src="{capa}" alt="{alt}">\n'
        conteudo = conteudo.replace('<section class="capa">\n',
                                    '<section class="capa">\n' + img, 1)
    return conteudo


def main():
    for item in CONFIG:
        pagina, gerador, capa, alt = item[0], item[1], item[2], item[3]
        css_ancora = item[4] if len(item) > 4 else ".capa .selo{"
        alvo_pag = PAGINAS / pagina
        alvo_ger = HERE / gerador
        for alvo in (alvo_pag, alvo_ger):
            txt = alvo.read_text(encoding="utf-8")
            novo = aplica_em(txt, capa, alt, css_ancora)
            if novo != txt:
                alvo.write_text(novo, encoding="utf-8")
                print(f"✔ {alvo.relative_to(HERE)} atualizado")
            else:
                print(f"· {alvo.relative_to(HERE)} já ok")

    # --- livro07 (despertar): padroniza capa-img -> capa-livro ---
    for alvo in (PAGINAS / "livro07_preview.html", OBRA / "gerar_despertar.py"):
        txt = alvo.read_text(encoding="utf-8")
        if ".capa .capa-livro{" not in txt:
            # substitui a regra capa-img pela padrão
            txt2 = re.sub(r'\.capa \.capa-img\{[^}]*\}', CSS_CAPA.replace('\n', '\n  '), txt)
            # remove <img class="capa-img" ...> (vai ser reinserido como capa-livro)
            txt2 = re.sub(r'\s*<img class="capa-img"[^>]*>', '', txt2)
            if '<img class="capa-livro"' not in txt2:
                img = ('  <img class="capa-livro" src="https://i.ibb.co/NdPkM40C/capa-despertar.png" '
                       'alt="Capa do livro O Caminho do Despertar">\n')
                txt2 = txt2.replace('<section class="capa">\n',
                                    '<section class="capa">\n' + img, 1)
            if txt2 != txt:
                alvo.write_text(txt2, encoding="utf-8")
                print(f"✔ {alvo.relative_to(HERE)} (despertar) atualizado")
            else:
                print(f"· {alvo.relative_to(HERE)} (despertar) já ok")


if __name__ == "__main__":
    main()
