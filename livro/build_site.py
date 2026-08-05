# -*- coding: utf-8 -*-
"""
Gera a página web do livro (site/index.html) a partir do mesmo conteúdo
usado no .docx/.pdf — reutiliza build_livro.py.
"""
import re, sys, html
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_livro as bl

HERE = Path(__file__).parent
# O GitHub Pages (deploy por branch) só serve a pasta /docs ou a raiz do repositório.
# Publicamos a página em /docs na raiz do repo (raiz = HERE.parent).
OUT = HERE.parent / "docs" / "index.html"
DOCX = HERE / "O_Ouro_das_Palavras.docx"
PDF = HERE / "O_Ouro_das_Palavras_previa.pdf"

TITULO = "O Ouro das Palavras"
AUTOR = "Joseph Murphy"
SUBTITULO = "O poder criador da palavra"

def esc(txt):
    return html.escape(txt, quote=False)

def rich(txt):
    t = esc(txt)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    return t

def build():
    conteudo = bl.montar_conteudo()
    paginas = conteudo.get("paginas", {})

    intro_blocos = conteudo["introducao"]       # [("h1","Introdução"), ("p", ...)]
    caps = conteudo["capitulos"]                 # lista de listas de blocos

    # ---------- TOC ----------
    itens_toc = []
    itens_toc.append(f'<li><a href="#intro"><span class="toc-num">I</span>Introdução'
                     f'<span class="toc-pg">p. {paginas.get("introducao", 1)}</span></a></li>')
    for i, _ in enumerate(caps, 1):
        tit = bl.CAPITULOS[i-1][3]
        itens_toc.append(
            f'<li><a href="#cap{i}"><span class="toc-num">{i:02d}</span>{esc(tit)}'
            f'<span class="toc-pg">p. {paginas.get(f"cap{i}", "")}</span></a></li>')
    toc_html = "\n".join(itens_toc)

    # ---------- INTRODUÇÃO ----------
    par_intro = []
    for tipo, txt in intro_blocos:
        if tipo == "p":
            cls = ' class="first-p"' if not par_intro else ""
            par_intro.append(f"<p{cls}>{rich(txt)}</p>")
    intro_html = "\n".join(par_intro)

    # ---------- CAPÍTULOS ----------
    secoes_html = []
    for i, blocos in enumerate(caps, 1):
        num_tit = bl.CAPITULOS[i-1][3]
        partes = [f'<section id="cap{i}" class="capitulo">',
                  f'<header class="cap-head">',
                  f'<p class="cap-num">CAPÍTULO {i}</p>',
                  f'<h2 class="cap-titulo">{esc(num_tit)}</h2>',
                  '</header>']
        primeiro_p = True
        for tipo, txt in blocos:
            if tipo == "h1num":
                continue  # já impresso no cabeçalho
            if tipo == "h1":
                continue
            if tipo == "h2":
                partes.append(f'<h3 class="subtitulo">{esc(txt)}</h3>')
            else:
                cls = ' class="first-p"' if primeiro_p else ""
                partes.append(f'<p{cls}>{rich(txt)}</p>')
                primeiro_p = False
        # navegação anterior/próximo
        nav = ['<nav class="cap-nav">']
        if i > 1:
            nav.append(f'<a class="prev" href="#cap{i-1}">← {esc(bl.CAPITULOS[i-2][3])}</a>')
        else:
            nav.append('<a class="prev" href="#intro">← Introdução</a>')
        nav.append('<a class="topo" href="#topo">↑ Topo</a>')
        if i < len(caps):
            nav.append(f'<a class="next" href="#cap{i+1}">{esc(bl.CAPITULOS[i][3])} →</a>')
        else:
            nav.append('<a class="next" href="#topo">Fim do livro →</a>')
        nav.append('</nav>')
        partes.append("\n".join(nav))
        # aviso de direitos autorais ao final de cada capítulo
        partes.append('<p class="copy-chap">© Coleção Oculta &middot; <em>O Ouro das Palavras</em>'
                      ' &middot; Joseph Murphy — Todos os direitos reservados</p>')
        partes.append('</section>')
        secoes_html.append("\n".join(partes))

    capitulos_html = "\n".join(secoes_html)

    css = """
:root{
  --papel:#f7f2e9; --tinta:#2b2620; --tinta2:#5c5347;
  --ouro:#a9832d; --ouro2:#c9a24b; --linha:#e2d9c8;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--papel); color:var(--tinta);
  font-family:Georgia,'Times New Roman',Times,serif;
  line-height:1.75; font-size:18px;
  /* ---- proteção leve contra cópia (deterrente) ----
     impede seleção de texto com o mouse na maioria dos navegadores.
     Não é infalível: ver fonte (Ctrl+U) e DevTools (F12) continuam expondo o texto. */
  -webkit-user-select:none; -moz-user-select:none; -ms-user-select:none; user-select:none;
}
img{-webkit-touch-callout:none; -webkit-user-drag:none}
#topo{position:absolute; top:0}
.wrap{max-width:46rem; margin:0 auto; padding:2.4rem 1.4rem 4rem}

/* ---------- CAPA ---------- */
.capa{
  min-height:88vh; display:flex; flex-direction:column;
  align-items:center; justify-content:center; text-align:center;
  border-bottom:1px solid var(--linha); padding:4rem 1rem;
}
.capa .selo{font-size:.8rem; letter-spacing:.42em; text-transform:uppercase;
  color:var(--tinta2); margin-bottom:2.2rem}
.capa h1{font-size:clamp(2.2rem,7vw,4rem); line-height:1.12; margin:.2rem 0;
  font-weight:700; letter-spacing:.01em}
.capa .regua{width:5rem; height:2px; background:var(--ouro); margin:1.8rem auto}
.capa .sub{font-style:italic; font-size:1.15rem; color:var(--tinta2)}
.capa .autor{margin-top:2.6rem; font-size:1.05rem; letter-spacing:.28em;
  text-transform:uppercase; color:var(--tinta)}
.capa .ano{margin-top:2.4rem; font-size:.85rem; color:var(--tinta2);
  letter-spacing:.18em}

/* ---------- SUMÁRIO ---------- */
h2.toc-titulo{text-align:center; font-size:1.5rem; letter-spacing:.3em;
  text-transform:uppercase; margin:4.5rem 0 2.2rem; color:var(--tinta)}
.toc{list-style:none; margin:0; padding:0}
.toc li{border-bottom:1px solid var(--linha)}
.toc a{display:flex; align-items:baseline; gap:.9rem; text-decoration:none;
  color:var(--tinta); padding:.85rem .2rem; transition:color .15s}
.toc a:hover{color:var(--ouro)}
.toc-num{font-variant-numeric:tabular-nums; color:var(--ouro); font-size:.95rem;
  min-width:2rem}
.toc-pg{margin-left:auto; color:var(--tinta2); font-size:.85rem}

/* ---------- CAPÍTULOS ---------- */
.capitulo{margin-top:5rem; padding-top:2rem; border-top:1px solid var(--linha)}
.cap-head{text-align:center; margin-bottom:2.6rem}
.cap-num{letter-spacing:.42em; text-transform:uppercase; font-size:.85rem;
  color:var(--ouro); margin:0 0 .6rem}
.cap-titulo{font-size:clamp(1.4rem,4vw,1.9rem); margin:0; font-weight:700}
.capitulo p{margin:0 0 1.15rem; text-align:justify}
.capitulo p.first-p::first-letter{font-size:3.2em; float:left; line-height:.85;
  padding-right:.14em; color:var(--ouro); font-weight:700}
.capitulo p strong{color:#8a6d1f}
.subtitulo{margin:2.2rem 0 1rem; font-size:1.08rem; font-weight:700;
  letter-spacing:.02em; color:var(--tinta)}
.cap-nav{display:flex; justify-content:space-between; gap:.6rem; margin-top:3rem;
  flex-wrap:wrap; font-size:.9rem}
.cap-nav a{color:var(--tinta2); text-decoration:none; border-bottom:1px dotted var(--ouro)}
.cap-nav a:hover{color:var(--ouro)}
.cap-nav .topo{color:var(--ouro)}

/* Aviso de direitos autorais ao final de cada capítulo */
.copy-chap{text-align:center; font-size:.78rem; color:var(--tinta2);
  margin:2.4rem 0 0; letter-spacing:.05em}
.copy-chap em{font-style:italic}

/* Página exibida quando alguém tenta imprimir */
#print-block{display:none; text-align:center; padding:4rem 1.5rem;
  font-family:Georgia,'Times New Roman',serif; color:var(--tinta)}
#print-block h1{font-size:1.5rem; margin:.8rem 0}
#print-block .selo{letter-spacing:.35em; text-transform:uppercase;
  font-size:.8rem; color:var(--tinta2)}
#print-block .regua{width:4rem; height:1px; background:var(--ouro); margin:1.4rem auto}
#print-block p{color:var(--tinta2); font-size:.95rem; margin:.45rem 0}

/* ---------- RODAPÉ ---------- */
footer{border-top:1px solid var(--linha); margin-top:5rem; padding:2rem 0 3rem;
  text-align:center; color:var(--tinta2); font-size:.85rem}
footer .regua{width:3.5rem; height:1px; background:var(--ouro); margin:0 auto 1.4rem}

@media print{
  /* Impressão desabilitada: mostra apenas um aviso de direitos autorais
     em vez do conteúdo do livro. (Deterrente — usuários técnicos podem
     desativar o CSS ou imprimir por outros meios.) */
  .capa, .wrap{display:none}
  #print-block{display:block}
}
@media (max-width:560px){
  body{font-size:16.5px; line-height:1.7}
  .toc a{flex-wrap:wrap; gap:.3rem}
  .toc-pg{margin-left:auto}
}
"""

    # Script de proteção leve contra cópia (fora do f-string para evitar
    # conflito de chaves {}). Deterrente: bloqueia menu de contexto e
    # intercepta cópia. Não é infalível (Ctrl+U / F12 continuam expondo o texto).
    js_protecao = """<script>
/* ---- proteção leve contra cópia (deterrente) ----
   Bloqueia o menu do botão direito e, se alguém copiar, o conteúdo
   copiado vira um aviso de direitos autorais (em vez do texto do livro).
   Não é infalível: ver fonte (Ctrl+U) e DevTools (F12) continuam expondo o texto. */
document.addEventListener('contextmenu', function (e) { e.preventDefault(); });
document.addEventListener('copy', function (e) {
  e.preventDefault();
  if (e.clipboardData) {
    e.clipboardData.setData('text/plain',
      '© Coleção Oculta — O Ouro das Palavras, de Joseph Murphy. Todos os direitos reservados.');
  }
});
</script>"""

    html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(TITULO)} — {esc(AUTOR)}</title>
<meta name="description" content="O Ouro das Palavras, de Joseph Murphy — o poder criador da palavra. Edição digital formatada segundo a ABNT NBR 6029.">
<style>{css}</style>
</head>
<body>
<div id="topo"></div>

<header class="capa">
  <p class="selo">Coleção Oculta</p>
  <h1>{esc(TITULO)}</h1>
  <div class="regua"></div>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">{esc(AUTOR)}</p>
  <p class="ano">EDIÇÃO DIGITAL · 2026</p>
</header>

<div id="print-block">
  <p class="selo">Coleção Oculta</p>
  <h1>O Ouro das Palavras</h1>
  <p style="font-style:italic">Joseph Murphy</p>
  <div class="regua"></div>
  <p>Impressão desabilitada para proteger os direitos autorais desta obra.</p>
  <p>© Coleção Oculta — Todos os direitos reservados.</p>
</div>

<div class="wrap">
  <h2 class="toc-titulo">Sumário</h2>
  <ul class="toc">
{toc_html}
  </ul>

  <section id="intro" class="capitulo">
    <header class="cap-head">
      <p class="cap-num">Prefácio</p>
      <h2 class="cap-titulo">Introdução</h2>
    </header>
{intro_html}
    <nav class="cap-nav">
      <a class="prev" href="#cap1">Capítulo 1 →</a>
      <a class="topo" href="#topo">↑ Topo</a>
    </nav>
  </section>

{capitulos_html}

  <footer>
    <div class="regua"></div>
    <p><strong>{esc(TITULO)}</strong> · {esc(AUTOR)}</p>
    <p>Baseado nos ensinamentos de Joseph Murphy. Editado e publicado por Coleção Oculta.</p>
    <p>Diagramação segundo a ABNT NBR 6029 — Apresentação de livros e folhetos.</p>
    <p>Todos os direitos reservados.</p>
  </footer>
</div>
{js_protecao}
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_doc, encoding="utf-8")
    # .nojekyll para o GitHub Pages não ignorar nada
    (OUT.parent / ".nojekyll").write_text("", encoding="utf-8")
    # Obs.: os arquivos .docx/.pdf NÃO são copiados para /docs de propósito —
    # a página não oferece download (proteção contra cópias).
    # As versões originais continuam em /livro no repositório.
    print("Site gerado:", OUT, f"({OUT.stat().st_size:,} bytes)")

if __name__ == "__main__":
    build()
