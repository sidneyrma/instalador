# -*- coding: utf-8 -*-
"""
Gera a página de leitura de "O Caminho do Despertar — A Jornada Solitária da Alma"
com estrutura de livro ABNT: capa, folha de rosto, créditos, sumário com paginação,
navegação entre capítulos e proteção anti-cópia.
"""
import re, html
from pathlib import Path

HERE = Path(__file__).parent
PAGINAS = HERE.parent.parent / "paginas"
SRC = HERE / "O_Caminho_do_Despertar_FINAL.md"
OUT = PAGINAS / "livro07_preview.html"
CAPA = "https://i.ibb.co/hFvQVBgB/Livro07.jpg"

TITULO = "O Caminho do Despertar"
SUBTITULO = "A Jornada Solitária da Alma"
AUTOR = "Missão com Deus"

def esc(t):
    return html.escape(t, quote=False)

def parse_md():
    """Converte o texto humanizado (sem markdown) em estrutura."""
    linhas = SRC.read_text(encoding='utf-8').split('\n')
    estrutura = []
    for l in linhas:
        s = l.strip()
        if not s:
            continue
        if re.match(r'^PARTE [IVX]+ —', s):
            estrutura.append(("parte", s))
        elif re.match(r'^CAPÍTULO \d+ —', s):
            estrutura.append(("h2", s))
        elif s.upper().startswith(('APRESENTAÇÃO', 'BÔNUS', 'EPÍLOGO')):
            estrutura.append(("h2", s))
        elif s.upper().startswith(('REFLExÃO', 'REFLEXÃO')):
            estrutura.append(("h3", s))
        else:
            estrutura.append(("p", s))
    return estrutura

def build():
    estrutura = parse_md()

    # ---- Sumário ----
    toc = []
    for tipo, txt in estrutura:
        if tipo == "parte":
            toc.append(f'<li class="toc-parte">{esc(txt)}</li>')
        elif tipo == "h2":
            slug = re.sub(r'[^a-z0-9]+', '-', txt.lower()).strip('-')
            toc.append(f'<li><a href="#{slug}">{esc(txt)}</a></li>')
    toc_html = "\n".join(toc)

    # ---- Corpo ----
    secoes = []
    atual = []
    parte_atual = ""

    def flush():
        nonlocal atual
        if atual:
            secoes.append("\n".join(atual))
            atual = []

    for tipo, txt in estrutura:
        if tipo == "parte":
            atual.append(f'<h2 class="cap-titulo parte-titulo">{esc(txt)}</h2>')
        elif tipo == "h2":
            flush()
            slug = re.sub(r'[^a-z0-9]+', '-', txt.lower()).strip('-')
            atual.append(f'<section class="capitulo" id="{slug}">')
            atual.append(f'<h2 class="cap-titulo">{esc(txt)}</h2>')
        elif tipo == "h3":
            atual.append(f'<h3 class="secao-titulo">{esc(txt)}</h3>')
        elif tipo == "quote":
            atual.append(f'<blockquote>{esc(txt)}</blockquote>')
        elif tipo == "bullet":
            atual.append(f'<li>{esc(txt)}</li>')
        elif tipo == "p":
            atual.append(f'<p>{esc(txt)}</p>')
    flush()

    # navegação
    html_secoes = []
    for idx, sec in enumerate(secoes):
        nav = ['<nav class="cap-nav">']
        if idx > 0:
            m_ant = re.search(r'id="([^"]+)"', secoes[idx-1])
            if m_ant:
                nav.append(f'<a href="#{m_ant.group(1)}">← Anterior</a>')
        nav.append('<a href="#sumario">Sumário</a>')
        if idx < len(secoes)-1:
            m_prox = re.search(r'id="([^"]+)"', secoes[idx+1])
            if m_prox:
                nav.append(f'<a href="#{m_prox.group(1)}">Próximo →</a>')
        nav.append('</nav>')
        # só fecha section se a sec abriu com <section
        fechamento = "</section>" if "<section" in sec else ""
        html_secoes.append(sec + "\n" + "\n".join(nav) + fechamento)
    corpo_html = "\n".join(html_secoes)

    css = """
:root{
  --navy:#0e1a2e; --navy2:#16283f;
  --ouro:#c9a24b; --ouro-claro:#e3c877;
  --papel:#fdfbf5; --tinta:#2b2620; --tinta2:#6b6255;
  --linha:#e4dccb; --cta:#b8860b;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--navy); color:var(--tinta);
  font-family:Georgia,'Times New Roman',Times,serif; line-height:1.8;
  -webkit-user-select:none; -moz-user-select:none; -ms-user-select:none; user-select:none;
}
img{-webkit-user-drag:none; -webkit-touch-callout:none}
.wrap{max-width:48rem; margin:0 auto}

.topbar{background:var(--navy); border-bottom:3px solid var(--ouro); position:sticky; top:0; z-index:50}
.topbar .wrap{display:flex; align-items:center; justify-content:space-between; padding:.8rem 1.2rem; gap:10px}
.topbar .logo{color:#fff; font-size:1.05rem; text-decoration:none}
.topbar .logo span{color:var(--ouro)}
.topbar .ler{color:var(--ouro-claro); font-size:.78rem; letter-spacing:.2em; text-transform:uppercase}

.capa{min-height:92vh; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:3rem 1.2rem; color:#fff;
  background:radial-gradient(900px 500px at 70% -10%, rgba(201,162,75,.22), transparent 60%), linear-gradient(170deg,var(--navy) 0%,#120b18 100%);}
.capa .selo{font-size:.78rem; letter-spacing:.42em; text-transform:uppercase; color:var(--ouro-claro); margin-bottom:2rem}
.capa .capa-livro{width:178px; height:auto; border:2px solid var(--ouro); border-radius:6px;
    box-shadow:0 18px 44px rgba(0,0,0,.6); margin-bottom:1.8rem; -webkit-user-drag:none}
.capa h1{font-size:clamp(2.2rem,6vw,3.6rem); margin:0 0 .6rem; line-height:1.1}
.capa .sub{font-style:italic; color:#cfd6e2; font-size:1.2rem; margin-bottom:2rem}
.capa .inicio{display:inline-block; background:linear-gradient(180deg,#d4a83f,var(--cta)); color:#fff;
  font-weight:700; padding:16px 34px; border-radius:50px; text-decoration:none; font-size:1.1rem;
  box-shadow:0 8px 24px rgba(201,162,75,.4)}
.capa .aviso{font-size:.78rem; color:#8fa0b8; margin-top:1.6rem; max-width:26rem; line-height:1.5}

#sumario{background:var(--navy2); color:#fff; padding:3rem 1.2rem}
#sumario h2{text-align:center; color:var(--ouro); font-size:1.4rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1.4rem}
#sumario ul{list-style:none; padding:0; margin:0 auto; max-width:36rem}
#sumario li{border-bottom:1px solid rgba(201,162,75,.25)}
#sumario li.toc-parte{color:var(--ouro); font-weight:700; padding:.9rem .4rem .4rem; letter-spacing:.08em; text-transform:uppercase; font-size:.85rem; border-bottom:none}
#sumario a{display:block; color:#e8ecf3; text-decoration:none; padding:.75rem .4rem; font-size:1rem}
#sumario a:hover{color:var(--ouro-claro); padding-left:.8rem}

.leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}
.leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:12px;
  padding:2.4rem 1.8rem; box-shadow:0 10px 30px rgba(0,0,0,.08)}
.capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha)}
.capitulo.parte{margin-top:4rem; padding-top:2.6rem; border-top:3px double var(--ouro)}
.cap-titulo{font-size:1.6rem; color:var(--navy); margin:0 0 1.4rem}
.cap-titulo.parte-titulo{color:var(--ouro); text-align:center; letter-spacing:.08em; font-size:1.2rem}
.secao-titulo{font-size:1.08rem; color:var(--navy); margin:1.4rem 0 .5rem}
.capitulo p{margin:0 0 1.1rem; text-align:justify}
.capitulo blockquote{border-left:4px solid var(--ouro); background:#faf6ea; margin:1.2rem 0; padding:14px 18px; font-style:italic; color:var(--tinta2); border-radius:0 10px 10px 0}
.capitulo li{margin-bottom:6px; line-height:1.7}
.cap-nav{display:flex; justify-content:space-between; gap:.6rem; flex-wrap:wrap; margin-top:2.4rem;
  padding-top:1rem; border-top:1px dashed var(--linha); font-size:.9rem; font-family:system-ui,sans-serif}
.cap-nav a{color:var(--navy2); text-decoration:none; border-bottom:1px dotted var(--ouro); padding:2px 4px}
.cap-nav a:hover{color:var(--cta)}

#fim{background:var(--navy); color:#fff; text-align:center; padding:4rem 1.2rem}
#fim h2{font-size:1.5rem; margin-bottom:.8rem}
#fim p{color:#c4cdda; max-width:32rem; margin:0 auto 1.6rem}
#fim .cred{font-size:.82rem; color:#8fa0b8; margin-top:1.6rem; line-height:1.6}

footer{background:#0a1322; color:#7f8ca1; text-align:center; padding:1.6rem 1.2rem; font-size:.8rem}

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
  .cap-titulo{font-size:1.3rem}
}
"""

    js = """<script>
document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
document.addEventListener('copy', function(e){
  e.preventDefault();
  if (e.clipboardData){
    e.clipboardData.setData('text/plain',
      '© Coleção do Despertar — O Caminho do Despertar. Todos os direitos reservados. Leitura online em compraoseu.com');
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
<title>{esc(TITULO)} — A Jornada Solitária da Alma · Leitura Online | Missão com Deus</title>
<meta name="description" content="Leia online {esc(TITULO)} — {esc(SUBTITULO)}. Uma obra que reúne sabedoria oculta, fé e conhecimento da alma humana. 12 capítulos. Leitura protegida.">
<meta name="robots" content="index, follow">
<style>{css}</style>
</head>
<body>

<div id="print-block">
  <h1>{esc(TITULO)}</h1>
  <p style="font-style:italic">{esc(SUBTITULO)}</p>
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
  <img class="capa-livro" src="https://i.ibb.co/hFvQVBgB/Livro07.jpg" alt="Capa do livro O Caminho do Despertar">
  <p class="selo">Coleção do Despertar</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <a class="inicio" href="#sumario">Começar a leitura →</a>
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
{corpo_html}
  </div>
</main>

<section id="fim">
  <h2>A Jornada Contínua</h2>
  <p>Que a Luz do Divino Criador ilumine os seus passos. E que o mestre interior, agora desperto, guie cada escolha.</p>
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
