# -*- coding: utf-8 -*-
"""
Gera a página de leitura do "Devocional Um Segundo com Deus Vol.01" para a Vendd.
Lê o JSON extraído (devocional_dados.json).
- 30 dias com versículo, mensagem, oração, prece e obra
- Proteção anti-cópia + impressão bloqueada
- Design de leitura + identidade da marca
"""
import json, re, html
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "devocional_preview.html"
DADOS = HERE / "devocional_dados.json"

TITULO = "Um Segundo com Deus"
SUBTITULO = "Devocional Vol. 01 — 30 dias de conexão diária com Deus"

def esc(t):
    return html.escape(t, quote=False)

def build():
    dados = json.loads(DADOS.read_text(encoding='utf-8'))
    dias = dados["dias"]
    apresentacao = dados["apresentacao"]
    encerramento = dados["encerramento"]

    # ---- Sumário (30 dias) ----
    toc = []
    for d in dias:
        toc.append(f'<li><a href="#dia-{d["num"]}">Dia {d["num"]} — {esc(d["titulo"])}</a></li>')
    toc_html = "\n".join(toc)

    # ---- Apresentação (primeiros parágrafos) ----
    intro_pars = []
    for par in apresentacao.split('\n\n'):
        p = re.sub(r'\s+', ' ', par).strip()
        if p:
            intro_pars.append(f'<p>{esc(p)}</p>')
    intro_html = "\n".join(intro_pars[:5])  # primeiros 5 blocos da apresentação

    # ---- Dias ----
    secoes = []
    for d in dias:
        num = d["num"]
        blocos = [
            f'<section class="capitulo dia" id="dia-{num}">',
            f'<p class="cap-num">Dia {num}</p>',
            f'<h2 class="cap-titulo">{esc(d["titulo"])}</h2>',
        ]
        if d["versiculo"]:
            blocos.append(f'<div class="versiculo"><span class="rotulo">📖 Versículo-Chave</span><p class="versiculo-texto">{esc(d["versiculo"])}</p></div>')
        if d["mensagem"]:
            blocos.append(f'<h3 class="secao">Mensagem Inspirada</h3><p>{esc(d["mensagem"])}</p>')
        if d["oracao"]:
            blocos.append(f'<h3 class="secao">Oração do Dia</h3><p class="oracao">{esc(d["oracao"])}</p>')
        if d["prece"]:
            blocos.append(f'<div class="prece"><span class="rotulo">🕊️ Um Segundo com Deus</span><p>{esc(d["prece"])}</p></div>')
        if d["obra"]:
            blocos.append(f'<h3 class="secao">Obra Prática do Dia</h3><p>{esc(d["obra"])}</p>')
        # navegação
        nav = ['<nav class="cap-nav">']
        if num > 1:
            nav.append(f'<a href="#dia-{num-1}">← Dia {num-1}</a>')
        nav.append('<a href="#sumario">Sumário</a>')
        if num < 30:
            nav.append(f'<a href="#dia-{num+1}">Dia {num+1} →</a>')
        nav.append('</nav>')
        blocos.append("\n".join(nav))
        blocos.append('</section>')
        secoes.append("\n".join(blocos))
    dias_html = "\n".join(secoes)

    # ---- Encerramento ----
    encer_pars = []
    for par in encerramento.split('\n\n'):
        p = re.sub(r'\s+', ' ', par).strip()
        if p and 'Conheça Também' not in p and 'Evolução da Alma' not in p:
            encer_pars.append(f'<p>{esc(p)}</p>')
    encer_html = "\n".join(encer_pars[:4])

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
.capa .capa-livro{width:178px; height:auto; border:2px solid var(--ouro); border-radius:6px;
  box-shadow:0 18px 44px rgba(0,0,0,.6); margin-bottom:1.8rem; -webkit-user-drag:none}
.capa .selo{font-size:.78rem; letter-spacing:.4em; text-transform:uppercase; color:var(--ouro-claro); margin-bottom:1.6rem}
.capa h1{font-size:clamp(1.9rem,5.5vw,3.2rem); margin:0 0 .6rem; line-height:1.12}
.capa .sub{font-style:italic; color:#cfd6e2; font-size:1.05rem; margin-bottom:1.8rem; max-width:34rem}
.capa .autor{font-size:.9rem; letter-spacing:.3em; text-transform:uppercase; color:var(--ouro); margin-bottom:2.4rem}
.capa .inicio{display:inline-block; background:linear-gradient(180deg,#d4a83f,var(--cta)); color:#fff;
  font-weight:700; padding:14px 30px; border-radius:8px; text-decoration:none; font-size:1rem}
.capa .aviso{font-size:.78rem; color:#8fa0b8; margin-top:1.4rem; max-width:26rem; line-height:1.5}

#sumario{background:var(--navy2); color:#fff; padding:3rem 1.2rem}
#sumario h2{text-align:center; color:var(--ouro); font-size:1.4rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1.4rem}
#sumario ul{list-style:none; padding:0; margin:0 auto; max-width:34rem}
#sumario li{border-bottom:1px solid rgba(201,162,75,.25)}
#sumario a{display:block; color:#e8ecf3; text-decoration:none; padding:.8rem .4rem; font-size:1rem}
#sumario a:hover{color:var(--ouro-claro); padding-left:.8rem}

.leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}
.leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:12px;
  padding:2.2rem 1.6rem; box-shadow:0 10px 30px rgba(0,0,0,.08)}
.capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha)}
.cap-num{letter-spacing:.3em; text-transform:uppercase; font-size:.78rem; color:var(--ouro); margin:0 0 .5rem}
.cap-titulo{font-size:1.6rem; color:var(--navy); margin:0 0 1.2rem}
.secao{font-size:1rem; color:var(--navy); margin:1.4rem 0 .5rem; letter-spacing:.02em}
.capitulo p{margin:0 0 1rem; text-align:justify}
.versiculo{background:var(--claro, #f6f1e7); border-left:4px solid var(--ouro); border-radius:0 10px 10px 0;
  padding:14px 18px; margin:0 0 1.2rem}
.rotulo{display:block; font-size:.75rem; letter-spacing:.18em; text-transform:uppercase; color:var(--ouro); font-weight:700; margin-bottom:6px}
.versiculo-texto{font-style:italic; margin:0}
.oracao{background:#fbf7ee; border:1px solid var(--linha); border-radius:10px; padding:14px 16px;}
.prece{background:linear-gradient(135deg, rgba(201,162,75,.08), transparent); border:1px solid rgba(201,162,75,.3);
  border-radius:10px; padding:14px 16px; margin:1rem 0}
.cap-nav{display:flex; justify-content:space-between; gap:.6rem; flex-wrap:wrap; margin-top:2.4rem;
  font-size:.88rem; font-family:system-ui,sans-serif}
.cap-nav a{color:var(--navy2); text-decoration:none; border-bottom:1px dotted var(--ouro)}
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
  .cap-titulo{font-size:1.35rem}
}
"""

    js = """<script>
document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
document.addEventListener('copy', function(e){
  e.preventDefault();
  if (e.clipboardData){
    e.clipboardData.setData('text/plain',
      '© Coleção Oculta — Um Segundo com Deus (Devocional Vol. 01). Todos os direitos reservados. Leitura online em compraoseu.com');
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
<title>{esc(TITULO)} — Devocional Vol. 01 · Leitura Online | Missão com Deus</title>
<meta name="description" content="Leia online o devocional {esc(TITULO)} — 30 dias de conexão diária com Deus. Leitura protegida, sem impressão e sem cópia.">
<meta name="robots" content="index, follow">
<style>{css}</style>
</head>
<body>

<div id="print-block">
  <h1>{esc(TITULO)}</h1>
  <p style="font-style:italic">{esc(SUBTITULO)}</p>
  <p>Impressão desabilitada para proteger os direitos autorais desta obra.</p>
  <p>© Coleção Oculta — Todos os direitos reservados.</p>
</div>

<header class="topbar">
  <div class="wrap">
    <a class="logo" href="#">Missão <span>com Deus</span></a>
    <span class="ler">Leitura online</span>
  </div>
</header>

<section class="capa">
  <img class="capa-livro" src="https://i.ibb.co/Kx1mKFv6/umsegundocdeusjpg.jpg" alt="Capa do devocional Um Segundo com Deus">
  <p class="selo">Coleção Oculta</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">Leitura online · grátis</p>
  <a class="inicio" href="#sumario">Começar a leitura →</a>
  <p class="aviso">🔒 Leitura protegida: não é possível copiar, imprimir ou baixar este conteúdo.</p>
</section>

<section id="sumario">
  <h2>Sumário — 30 Dias</h2>
  <ul>
{toc_html}
  </ul>
</section>

<main class="leitura">
  <div class="wrap">
    <section class="capitulo" id="apresentacao">
      <p class="cap-num">Apresentação</p>
      <h2 class="cap-titulo">Comece sua jornada</h2>
{intro_html}
      <nav class="cap-nav">
        <a href="#sumario">Sumário</a>
        <a href="#dia-1">Dia 1 →</a>
      </nav>
    </section>

{dias_html}
  </div>
</main>

<section id="fim">
  <h2>Missão Cumprida</h2>
{encer_html}
  <p class="cred">© Coleção Oculta · Todos os direitos reservados.<br>Leitura protegida — não é permitido copiar, imprimir ou distribuir este conteúdo.</p>
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
