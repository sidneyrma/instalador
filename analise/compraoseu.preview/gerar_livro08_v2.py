# -*- coding: utf-8 -*-
"""
Gera a página de leitura do Livro 02 reescrito — "A Sabedoria dos Mestres"
a partir da obra original (obra_livro02_v2.md).

Padrão da coleção: capa, sumário clicável, partes/capítulos com navegação
← Anterior | Sumário | Próximo →, proteção anti-cópia e SEO.
"""
import re, html
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent / "livro08_reescrito" / "obra_livro08_v2.md"
OUT = HERE.parent.parent / "paginas" / "livro08_preview.html"

TITULO = "O Arquiteto da Realidade"
SUBTITULO = "O Poder da Mente que Cria o Mundo que Você Vive"
URL = "https://www.compraoseu.com/livro08"
CAPA = "https://sidneyrma.github.io/instalador/capas/livro08.png?v=4"

DESC = "Leia online O Arquiteto da Realidade — O Poder da Mente que Cria o Mundo que Você Vive. Uma obra original sobre crenças, mente profunda, rituais de transformação e o estado do criador. Leitura gratuita e protegida."
KEYWORDS = "arquiteto da realidade, poder da mente, crenças, subconsciente, reprogramação, visualização, rituais, identidade, transformação, livro espiritual, leitura online grátis"


def esc(t):
    return html.escape(t, quote=False)


def slugify(txt):
    s = re.sub(r'[^a-z0-9]+', '-', txt.lower()).strip('-')
    return s[:60] or 'secao'


def build():
    texto = SRC.read_text(encoding='utf-8')

    blocos = []
    atual = None
    num_cap = 0
    for linha in texto.split('\n'):
        linha = linha.strip()
        if not linha:
            continue
        if linha.startswith('### '):
            if atual is not None and atual['tipo'] == 'cap':
                atual['titulo'] = linha[4:].strip()
            elif atual is not None:
                atual['paras'].append(linha[4:].strip())
            continue
        if linha.startswith('## '):
            titulo = linha[3:].strip()
            if titulo.upper() in ('PRÓLOGO', 'PROLOGO', 'EPÍLOGO', 'EPILOGO'):
                atual = {'tipo': 'parte', 'titulo': titulo, 'paras': []}
                blocos.append(atual)
            elif titulo.upper().startswith('PARTE'):
                atual = {'tipo': 'parte', 'titulo': titulo, 'paras': []}
                blocos.append(atual)
            elif titulo.upper().startswith('CAPÍTULO'):
                num_cap += 1
                atual = {'tipo': 'cap', 'num': num_cap, 'titulo': titulo, 'paras': []}
                blocos.append(atual)
            else:
                if atual is not None:
                    atual['paras'].append(titulo)
            continue
        if linha.startswith('# '):
            continue
        if linha.startswith('---'):
            continue
        else:
            if atual is None:
                atual = {'tipo': 'parte', 'titulo': 'Abertura', 'paras': []}
                blocos.append(atual)
            atual['paras'].append(linha)

    for b in blocos:
        if b['tipo'] == 'cap':
            b['id'] = f"cap-{b['num']}"
        else:
            b['id'] = 'parte-' + slugify(b['titulo'])

    # Sumário
    toc = []
    for b in blocos:
        if b['tipo'] == 'parte':
            toc.append(f'<li class="toc-parte">{esc(b["titulo"])}</li>')
        else:
            nome_cap = re.sub(r'^CAP[IÍ]TULO\s+\d+\s*[-–:]?\s*', '', b['titulo'], flags=re.IGNORECASE).strip()
            toc.append(f'<li><a href="#{b["id"]}">Capítulo {b["num"]} — {esc(nome_cap)}</a></li>')
    toc_html = "\n".join(toc)

    # Corpo
    corpo = []
    for i, b in enumerate(blocos):
        sec = [f'<section class="capitulo {"parte" if b["tipo"]=="parte" else ""}" id="{b["id"]}">']
        if b['tipo'] == 'parte':
            sec.append('<p class="cap-num">Coleção do Despertar</p>')
            sec.append(f'<h2 class="cap-titulo parte-titulo">{esc(b["titulo"])}</h2>')
        else:
            sec.append(f'<p class="cap-num">Capítulo {b["num"]}</p>')
            nome_cap = re.sub(r'^CAP[IÍ]TULO\s+\d+\s*[-–:]?\s*', '', b['titulo'], flags=re.IGNORECASE).strip()
            sec.append(f'<h2 class="cap-titulo">{esc(nome_cap)}</h2>')
        for p in b['paras']:
            sec.append(f'<p>{esc(p)}</p>')
        nav = ['<nav class="cap-nav">']
        if i > 0:
            nav.append(f'<a href="#{blocos[i-1]["id"]}">← Anterior</a>')
        nav.append('<a href="#sumario">Sumário</a>')
        if i < len(blocos) - 1:
            nav.append(f'<a href="#{blocos[i+1]["id"]}">Próximo →</a>')
        else:
            nav.append('<a href="#fim">Fim</a>')
        nav.append('</nav>')
        sec.append("\n".join(nav))
        sec.append('</section>')
        corpo.append("\n".join(sec))
    corpo_html = "\n".join(corpo)

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

.topbar{background:var(--navy); border-bottom:3px solid var(--ouro); position:sticky; top:0; z-index:50}
.topbar .wrap{display:flex; align-items:center; justify-content:space-between; padding:.8rem 1.2rem; gap:10px}
.topbar .logo{color:#fff; font-size:1.05rem; text-decoration:none}
.topbar .logo span{color:var(--ouro)}
.topbar .ler{color:var(--ouro-claro); font-size:.78rem; letter-spacing:.2em; text-transform:uppercase}

.capa{min-height:82vh; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:3rem 1.2rem; color:#fff;
  background:radial-gradient(900px 500px at 70% -10%, rgba(201,162,75,.2), transparent 60%), linear-gradient(170deg,var(--navy) 0%,#120b18 100%);}
.capa .capa-livro{width:190px; height:auto; border:2px solid var(--ouro); border-radius:6px;
  box-shadow:0 18px 44px rgba(0,0,0,.6); margin-bottom:1.8rem; -webkit-user-drag:none}
.capa .selo{font-size:.78rem; letter-spacing:.4em; text-transform:uppercase; color:var(--ouro-claro); margin-bottom:1.6rem}
.capa h1{font-size:clamp(2rem,5.5vw,3.2rem); margin:0 0 .6rem; line-height:1.12}
.capa .sub{font-style:italic; color:#cfd6e2; font-size:1.1rem; margin-bottom:1.8rem; max-width:34rem}
.capa .autor{font-size:.9rem; letter-spacing:.3em; text-transform:uppercase; color:var(--ouro); margin-bottom:2.4rem}
.capa .inicio{display:inline-block; background:linear-gradient(180deg,#d4a83f,var(--cta)); color:#fff;
  font-weight:700; padding:14px 30px; border-radius:8px; text-decoration:none; font-size:1rem}
.capa .aviso{font-size:.78rem; color:#8fa0b8; margin-top:1.4rem; max-width:26rem; line-height:1.5}

#sumario{background:var(--navy2); color:#fff; padding:3rem 1.2rem}
#sumario h2{text-align:center; color:var(--ouro); font-size:1.4rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1.4rem}
#sumario ul{list-style:none; padding:0; margin:0 auto; max-width:34rem}
#sumario li{border-bottom:1px solid rgba(201,162,75,.25)}
#sumario li.toc-parte{color:var(--ouro); font-weight:700; padding:.9rem .4rem .4rem; letter-spacing:.08em; text-transform:uppercase; font-size:.85rem}
#sumario a{display:block; color:#e8ecf3; text-decoration:none; padding:.8rem .4rem; font-size:1rem}
#sumario a:hover{color:var(--ouro-claro); padding-left:.8rem}

.leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}
.leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:12px;
  padding:2.2rem 1.6rem; box-shadow:0 10px 30px rgba(0,0,0,.08)}
.capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha)}
.capitulo.parte{margin-top:4rem; padding-top:2.6rem; border-top:3px double var(--ouro)}
.cap-num{letter-spacing:.3em; text-transform:uppercase; font-size:.78rem; color:var(--ouro); margin:0 0 .5rem}
.cap-titulo{font-size:1.5rem; color:var(--navy); margin:0 0 1.2rem}
.cap-titulo.parte-titulo{color:var(--ouro); text-align:center; letter-spacing:.1em}
.secao-titulo{font-size:1.05rem; color:var(--navy); margin:1.2rem 0 .5rem}
.capitulo p{margin:0 0 1rem; text-align:justify}
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
      '© Coleção do Despertar — O Arquiteto da Realidade. Todos os direitos reservados. Leitura online em compraoseu.com');
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
<title>{esc(TITULO)} — {esc(SUBTITULO)}</title>
<meta name="description" content="{DESC}">
<meta name="keywords" content="{KEYWORDS}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(TITULO)} — {esc(SUBTITULO)}">
<meta property="og:description" content="Uma obra original sobre crenças, mente profunda, rituais de transformação e o estado do criador. Leitura online gratuita e protegida.">
<meta property="og:image" content="{CAPA}">
<meta property="og:url" content="{URL}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Missão com Deus — CompraOSeu">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(TITULO)} — {esc(SUBTITULO)}">
<meta name="twitter:description" content="Uma obra original sobre crenças, mente profunda, rituais de transformação e o estado do criador. Leitura online gratuita e protegida.">
<meta name="twitter:image" content="{CAPA}">
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
  <img class="capa-livro" src="{CAPA}" alt="Capa do livro {esc(TITULO)}">
  <p class="selo">Coleção do Despertar</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">Obra original da Coleção do Despertar · Leitura online · grátis</p>
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
  <h2>A Fênix em Voo</h2>
  <p>"O arquiteto despertou. A planta está pronta. E a obra, agora, é sua."</p>
  <p>Que a fênix, despertada nestas páginas, voe alto e construa, dia após dia, a vida que a sua alma veio viver.</p>
  <p class="cred">© Coleção do Despertar · Todos os direitos reservados.<br>Leitura protegida — não é permitido copiar, imprimir ou distribuir este conteúdo.</p>
</section>

<footer>
  <p>Missão com Deus · CompraOSeu — Desperte sua mente, fortaleça sua fé, transforme sua vida.</p>
</footer>

{js}
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_doc, encoding="utf-8")
    print("Gerado:", OUT, f"({OUT.stat().st_size:,} bytes)")
    print(f"Blocos: {len(blocos)} | Capítulos: {sum(1 for b in blocos if b['tipo']=='cap')}")


if __name__ == "__main__":
    build()
