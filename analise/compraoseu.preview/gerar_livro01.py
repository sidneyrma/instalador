# -*- coding: utf-8 -*-
"""
Gera a página de leitura do livro (livro01) pronta para a Vendd:
- Conteúdo limpo (correções aplicadas) de "O Ouro das Palavras"
- Proteção anti-cópia (seleção, botão direito, clipboard)
- Impressão bloqueada (mostra aviso)
- Design de leitura (papel) + identidade da marca
- Sumário clicável + navegação entre capítulos
"""
import sys, re, html
from pathlib import Path

# build_livro.py fica em livro/ (raiz do repo) — sobe 2 pastas a partir de compraoseu.preview
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "livro"))
import build_livro as bl

HERE = Path(__file__).parent
PAGINAS = HERE.parent.parent / "paginas"
OUT = PAGINAS / "livro01_preview.html"

TITULO = "O Ouro das Palavras"
AUTOR = "Joseph Murphy"
SUBTITULO = "O poder criador da palavra"

def esc(t):
    return html.escape(t, quote=False)

def rich(t):
    t = esc(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    return t

def build():
    conteudo = bl.montar_conteudo()
    intro = conteudo["introducao"]   # [("h1","Introdução"), ("p",...)]
    caps = conteudo["capitulos"]     # lista de listas de blocos

    # ---- SUMÁRIO ----
    toc = ['<li><a href="#intro">Introdução</a></li>']
    for i in range(1, len(caps) + 1):
        tit = bl.CAPITULOS[i-1][3]
        toc.append(f'<li><a href="#cap{i}">Capítulo {i} — {esc(tit)}</a></li>')
    toc_html = "\n".join(toc)

    # ---- INTRODUÇÃO ----
    intro_pars = [f'<p>{rich(txt)}</p>' for tipo, txt in intro if tipo == "p"]
    intro_html = "\n".join(intro_pars)

    # ---- CAPÍTULOS ----
    secoes = []
    for i, blocos in enumerate(caps, 1):
        tit = bl.CAPITULOS[i-1][3]
        partes = [f'<section class="capitulo" id="cap{i}">',
                  f'<p class="cap-num">Capítulo {i}</p>',
                  f'<h2 class="cap-titulo">{esc(tit)}</h2>']
        for tipo, txt in blocos:
            if tipo in ("h1num", "h1"):
                continue
            if tipo == "h2":
                partes.append(f'<h3 class="sub">{esc(txt)}</h3>')
            else:
                partes.append(f'<p>{rich(txt)}</p>')
        # navegação
        nav = ['<nav class="cap-nav">']
        if i > 1:
            nav.append(f'<a href="#cap{i-1}">← Capítulo {i-1}</a>')
        else:
            nav.append('<a href="#intro">← Introdução</a>')
        nav.append('<a href="#sumario">Sumário</a>')
        if i < len(caps):
            nav.append(f'<a href="#cap{i+1}">Capítulo {i+1} →</a>')
        else:
            nav.append('<a href="#fim">Fim</a>')
        nav.append('</nav>')
        partes.append("".join(nav))
        partes.append('</section>')
        secoes.append("\n".join(partes))
    capitulos_html = "\n".join(secoes)

    css = """
:root{
  --navy:#0e1a2e; --navy2:#16283f;
  --ouro:#c9a24b; --ouro-claro:#e3c877;
  --papel:#faf6ee; --tinta:#2b2620; --tinta2:#6b6255;
  --linha:#e4dccb; --cta:#b8860b;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--navy); color:var(--tinta);
  font-family:Georgia,'Times New Roman',Times,serif; line-height:1.75;
  -webkit-user-select:none; -moz-user-select:none; -ms-user-select:none; user-select:none;
}
img{-webkit-user-drag:none; -webkit-touch-callout:none}
.wrap{max-width:46rem; margin:0 auto}

/* TOPO */
.topbar{background:var(--navy); border-bottom:3px solid var(--ouro); position:sticky; top:0; z-index:50}
.topbar .wrap{display:flex; align-items:center; justify-content:space-between; padding:.8rem 1.2rem; gap:10px}
.topbar .logo{color:#fff; font-size:1.05rem; text-decoration:none}
.topbar .logo span{color:var(--ouro)}
.topbar .ler{color:var(--ouro-claro); font-size:.78rem; letter-spacing:.2em; text-transform:uppercase}

/* CAPA */
.capa{min-height:82vh; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:3rem 1.2rem; color:#fff}
.capa .capa-livro{width:178px; height:auto; border:2px solid var(--ouro); border-radius:6px;
  box-shadow:0 18px 44px rgba(0,0,0,.6); margin-bottom:1.8rem; -webkit-user-drag:none}
.capa .selo{font-size:.78rem; letter-spacing:.4em; text-transform:uppercase; color:var(--ouro-claro); margin-bottom:1.6rem}
.capa h1{font-size:clamp(2rem,6vw,3.4rem); margin:0 0 .6rem; line-height:1.1}
.capa .sub{font-style:italic; color:#cfd6e2; font-size:1.1rem; margin-bottom:1.8rem}
.capa .autor{font-size:1rem; letter-spacing:.3em; text-transform:uppercase; color:var(--ouro); margin-bottom:2.4rem}
.capa .inicio{display:inline-block; background:linear-gradient(180deg,#d4a83f,var(--cta)); color:#fff;
  font-weight:700; padding:14px 30px; border-radius:8px; text-decoration:none; font-size:1rem}
.capa .aviso{font-size:.78rem; color:#8fa0b8; margin-top:1.4rem; max-width:26rem; line-height:1.5}

/* SUMÁRIO */
#sumario{background:var(--navy2); color:#fff; padding:3rem 1.2rem}
#sumario h2{text-align:center; color:var(--ouro); font-size:1.4rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1.4rem}
#sumario ul{list-style:none; padding:0; margin:0 auto; max-width:32rem}
#sumario li{border-bottom:1px solid rgba(201,162,75,.25)}
#sumario a{display:block; color:#e8ecf3; text-decoration:none; padding:.8rem .4rem; font-size:1rem}
#sumario a:hover{color:var(--ouro-claro); padding-left:.8rem}

/* LEITURA */
.leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}
.leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:12px;
  padding:2.2rem 1.6rem; box-shadow:0 10px 30px rgba(0,0,0,.08)}
#intro .cap-titulo{color:var(--navy)}
.capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha)}
.cap-num{letter-spacing:.3em; text-transform:uppercase; font-size:.78rem; color:var(--ouro); margin:0 0 .5rem}
.cap-titulo{font-size:1.6rem; color:var(--navy); margin:0 0 1.6rem}
.capitulo p{margin:0 0 1.1rem; text-align:justify}
.capitulo p strong{color:#8a6d1f}
.sub{margin:2rem 0 1rem; font-size:1.05rem; color:var(--navy)}
.cap-nav{display:flex; justify-content:space-between; gap:.6rem; flex-wrap:wrap; margin-top:2.4rem;
  font-size:.88rem; font-family:system-ui,sans-serif}
.cap-nav a{color:var(--navy2); text-decoration:none; border-bottom:1px dotted var(--ouro)}
.cap-nav a:hover{color:var(--cta)}

/* FIM */
#fim{background:var(--navy); color:#fff; text-align:center; padding:4rem 1.2rem}
#fim h2{font-size:1.5rem; margin-bottom:.8rem}
#fim p{color:#c4cdda; max-width:32rem; margin:0 auto 1.6rem}
#fim .cred{font-size:.82rem; color:#8fa0b8; margin-top:1.6rem; line-height:1.6}

/* RODAPÉ */
footer{background:#0a1322; color:#7f8ca1; text-align:center; padding:1.6rem 1.2rem; font-size:.8rem}

/* IMPRESSÃO BLOQUEADA */
#print-block{display:none; text-align:center; padding:4rem 1.5rem; font-family:Georgia,serif; color:var(--tinta)}
#print-block h1{font-size:1.5rem; margin:.8rem 0}
#print-block p{color:var(--tinta2); font-size:.95rem}
@media print{
  .topbar,.capa,#sumario,.leitura,footer{display:none}
  #print-block{display:block}
}

@media (max-width:560px){
  body{font-size:17px}
  .leitura .wrap{padding:1.4rem 1rem}
  .cap-titulo{font-size:1.35rem}
}
"""

    js = """<script>
/* Proteção contra cópia (deterrente — não é infalível) */
document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
document.addEventListener('copy', function(e){
  e.preventDefault();
  if (e.clipboardData){
    e.clipboardData.setData('text/plain',
      '© Coleção do Despertar — O Ouro das Palavras, de Joseph Murphy. Todos os direitos reservados. Leitura online em compraoseu.com');
  }
});
document.addEventListener('keydown', function(e){
  if ((e.ctrlKey||e.metaKey) && (e.key==='p'||e.key==='P'||e.key==='s'||e.key==='S')){
    e.preventDefault();
  }
});
</script>"""

    html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>O Ouro das Palavras — Joseph Murphy · Leitura Online | Missão com Deus</title>
<meta name="description" content="Leia online o livro O Ouro das Palavras, baseado nos ensinamentos de Joseph Murphy. Leitura protegida, sem impressão e sem cópia.">
<meta name="robots" content="index, follow">
<style>{css}</style>
</head>
<body>

<div id="print-block">
  <h1>O Ouro das Palavras</h1>
  <p style="font-style:italic">Joseph Murphy</p>
  <p>Impressão desabilitada para proteger os direitos autorais desta obra.</p>
  <p>© Coleção do Despertar — Todos os direitos reservados.</p>
</div>

<header class="topbar">
  <div class="wrap">
    <a class="logo" href="#">Missão <span>com Deus</span></a>
    <span class="ler">Leitura online</span>
  </div>
</header>

<section class="capa">
  <img class="capa-livro" src="https://sidneyrma.github.io/instalador/capas/livro01.png" alt="Capa do livro O Ouro das Palavras">
  <p class="selo">Coleção do Despertar</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">{esc(AUTOR)}</p>
  <a class="inicio" href="#intro">Começar a leitura →</a>
  <p class="aviso">🔒 Leitura protegida: não é possível copiar, imprimir ou baixar este conteúdo.</p>
</section>

<section id="sumario">
  <h2>Sumário</h2>
  <ul>
{toc_html}
  </ul>
</section>

<main class="leitura">
  <div class="wrap">
    <section class="capitulo" id="intro">
      <p class="cap-num">Prefácio</p>
      <h2 class="cap-titulo">Introdução</h2>
{intro_html}
      <nav class="cap-nav">
        <a href="#sumario">Sumário</a>
        <a href="#cap1">Capítulo 1 →</a>
      </nav>
    </section>

{capitulos_html}
  </div>
</main>

<section id="fim">
  <h2>Aqui termina sua jornada…</h2>
  <p>…mas começa sua transformação. O Ouro das Palavras, baseado nos ensinamentos de Joseph Murphy, editado e publicado por Coleção do Despertar.</p>
  <p class="cred">© Coleção do Despertar · Todos os direitos reservados.<br>Leitura protegida — não é permitido copiar, imprimir ou distribuir este conteúdo.</p>
</section>

<footer>
  <p>Missão com Deus · CompraOSeu — Desperte sua mente, fortaleça sua fé, transforme sua vida.</p>
</footer>

{js}
</body>
</html>
"""
    OUT.write_text(html_doc, encoding="utf-8")
    print("Gerado:", OUT, f"({OUT.stat().st_size:,} bytes)")

if __name__ == "__main__":
    build()
