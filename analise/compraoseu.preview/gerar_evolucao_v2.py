# -*- coding: utf-8 -*-
"""
Gera a página de leitura do "Evolução da Alma" (v2 — DOCX 27 correções).
Lê o JSON estruturado (evolucao_v2_dados.json).
Navegação como o livro01: rodapé com ← Anterior | Sumário | Próximo →
Proteção anti-cópia + impressão bloqueada.
"""
import json, re, html
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "evolucao_v2_preview.html"
DADOS = HERE / "evolucao_v2_dados.json"

TITULO = "Evolução da Alma"
SUBTITULO = "Caminhos para o Autoconhecimento, Fé e Transformação Pessoal"

def esc(t):
    return html.escape(t, quote=False)

def build():
    dados = json.loads(DADOS.read_text(encoding='utf-8'))
    estrutura = [(d["tipo"], d["texto"]) for d in dados["estrutura"]]

    # ---- Sumário ----
    toc = []
    parte_atual = ""
    cont_cap = 0
    for tipo, txt in estrutura:
        if tipo == "h1_parte":
            parte_atual = txt
            toc.append(f'<li class="toc-parte">{esc(txt)}</li>')
        elif tipo == "h1":
            cont_cap += 1
            # capítulo ou seção
            slug = f"sec-{cont_cap}"
            toc.append(f'<li><a href="#{slug}">{esc(txt[:70])}</a></li>')
    toc_html = "\n".join(toc)

    # ---- Corpo HTML com navegação ----
    secoes = []
    atual = []
    cont = 0

    def flush():
        nonlocal atual
        if atual:
            secoes.append("\n".join(atual))
            atual = []

    for tipo, txt in estrutura:
        if tipo == "h1_parte":
            flush()
            cont += 1
            if txt == "PREFÁCIO":
                atual.append(f'<section class="capitulo" id="sec-{cont}">')
                atual.append(f'<p class="cap-num">Abertura</p>')
                atual.append(f'<h2 class="cap-titulo">Prefácio</h2>')
            elif txt == "ORAÇÃO FINAL":
                atual.append(f'<section class="capitulo" id="sec-{cont}">')
                atual.append(f'<h2 class="cap-titulo">Oração Final</h2>')
            elif txt == "FRASE FINAL":
                atual.append(f'<section class="capitulo" id="sec-{cont}">')
                atual.append(f'<h2 class="cap-titulo">Frase Final</h2>')
            elif txt == "INÍCIO DO DESENVOLVIMENTO":
                atual.append(f'<section class="capitulo parte" id="sec-{cont}">')
                atual.append(f'<h2 class="cap-titulo parte-titulo">Desenvolvimento</h2>')
            else:
                atual.append(f'<section class="capitulo" id="sec-{cont}">')
                atual.append(f'<h2 class="cap-titulo">{esc(txt)}</h2>')
        elif tipo == "h1":
            flush()
            cont += 1
            # extrai número do capítulo se existir
            m = re.match(r'^Cap[ií]tulo\s*(\d+)[:\s]*(.*)$', txt, re.I)
            if m:
                num = m.group(1)
                titulo_cap = m.group(2).strip()
                atual.append(f'<section class="capitulo" id="sec-{cont}">')
                atual.append(f'<p class="cap-num">Capítulo {num}</p>')
                atual.append(f'<h2 class="cap-titulo">{esc(titulo_cap)}</h2>')
            else:
                atual.append(f'<section class="capitulo" id="sec-{cont}">')
                atual.append(f'<h2 class="cap-titulo">{esc(txt)}</h2>')
        elif tipo == "h2":
            atual.append(f'<h3 class="secao-titulo">{esc(txt)}</h3>')
        elif tipo == "p":
            atual.append(f'<p>{esc(txt)}</p>')
    flush()

    # navegação no rodapé de cada seção
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
        html_secoes.append(sec + "\n" + "\n".join(nav) + "\n</section>")
    corpo_html = "\n".join(html_secoes)

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
.secao-titulo{font-size:1.08rem; color:var(--navy); margin:1.4rem 0 .5rem}
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
      '© Coleção Oculta — Evolução da Alma. Todos os direitos reservados. Leitura online em compraoseu.com');
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
<title>{esc(TITULO)} — Leitura Online | Missão com Deus</title>
<meta name="description" content="Leia online {esc(TITULO)} — {esc(SUBTITULO)}. Guia prático com preces, orações e ensinamentos bíblicos. Leitura protegida.">
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
  <img class="capa-livro" src="https://i.ibb.co/4n4ZtWZJ/Evolucao-Alma.jpg" alt="Capa do livro Evolução da Alma">
  <p class="selo">Coleção Oculta</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">Leitura online · grátis</p>
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
  <h2>Que a luz de Deus o acompanhe</h2>
  <p>"Portanto, agora existem estas três coisas: a fé, a esperança e o amor. Mas a maior delas é o amor." — 1 Coríntios 13:13</p>
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
