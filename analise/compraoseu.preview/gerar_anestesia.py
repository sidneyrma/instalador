# -*- coding: utf-8 -*-
"""
Gera a página de leitura de "Anestesia Mental e seus Algoritmos da Escravidão"
(Livro 09 da Coleção do Despertar) para a Vendd.

Padrão da coleção: capa com imagem, sumário clicável, capítulos com seções,
navegação ← Anterior | Sumário | Próximo → em cada bloco, proteção anti-cópia
e SEO completo no <head>.
"""
import json, re, html
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "paginas" / "livro09_preview.html"
DADOS = HERE / "anestesia_dados.json"

TITULO = "Anestesia Mental"
SUBTITULO = "e seus Algoritmos da Escravidão — o manual de retorno à sua versão original"
URL = "https://www.compraoseu.com/livro09"
CAPA = "https://i.ibb.co/MkL2DhsV/capa1080.png"

DESC = "Leia online Anestesia Mental e seus Algoritmos da Escravidão — 16 capítulos sobre como as correntes invisíveis dos algoritmos controlam sua mente e como se libertar em Cristo. Leitura gratuita e protegida."
KEYWORDS = "anestesia mental, algoritmos da escravidão, governo da mente, reset do shabat, detox da alma, libertação mental, autodomínio, livro cristão, leitura online grátis"


def esc(t):
    return html.escape(t, quote=False)


def slugify(txt):
    s = re.sub(r'[^a-z0-9]+', '-', txt.lower()).strip('-')
    return s[:60] or 'secao'


def build():
    dados = json.loads(DADOS.read_text(encoding='utf-8'))
    estrutura = dados["estrutura"]

    # ---- Divide em blocos (cada bloco = uma parte/capítulo) ----
    blocos = []  # lista de {tipo: 'parte'|'cap', num: int|None, titulo: str, itens: [(tipo,texto)]}
    atual = None
    for e in estrutura:
        t, txt = e["tipo"], e["texto"]
        if t == "h1_parte":
            atual = {"tipo": "parte", "num": None, "titulo": txt, "itens": []}
            blocos.append(atual)
        elif t == "h1":
            num = int(re.search(r'\d+', txt).group())
            atual = {"tipo": "cap", "num": num, "titulo": "", "itens": []}
            blocos.append(atual)
        elif t == "h2":
            if atual is not None:
                if atual["tipo"] == "cap" and not atual["titulo"]:
                    atual["titulo"] = txt  # primeiro h2 do capítulo é o título
                else:
                    atual["itens"].append(("h2", txt))
        elif t == "p":
            if atual is not None:
                atual["itens"].append(("p", txt))
    # garante título dos caps (fallback)
    TIT_CAP = {
        1: "O Algoritmo da Anestesia Mental", 2: "O Governo do Pensamento",
        3: "O Poder do Isolamento e o Casulo", 4: "Governo do Tempo e Disciplina",
        5: "O Autodomínio e o Governo da Vontade", 6: "O Legado da Maturidade e a Inteireza",
        7: "Detox da Alma e o Reset do Shabat", 8: "A Estética do Silêncio e o Comando Final",
        9: "A Engenharia do Algoritmo da Alma", 10: "Anestesia Mental e o Despertar Coletivo",
        11: "A Disciplina da Alma: O Algoritmo da Vitória", 12: "A Coragem de Ser Inteiro no Mundo Fragmentado",
        13: "Ansiedade Espiritual e Exaustão Digital", 14: "A Estética do Silêncio: Ouvindo a Voz no Vácuo Digital",
        15: "O Comando Final: Viva a Vida em Alta Definição", 16: "Checklist Final de Reprogramação Mental",
    }
    for b in blocos:
        if b["tipo"] == "cap" and not b["titulo"]:
            b["titulo"] = TIT_CAP.get(b["num"], f"Capítulo {b['num']}")

    # ---- IDs ----
    for b in blocos:
        if b["tipo"] == "cap":
            b["id"] = f"cap-{b['num']}"
        else:
            b["id"] = "parte-" + slugify(b["titulo"])

    # ---- Sumário ----
    toc = []
    for b in blocos:
        if b["tipo"] == "parte":
            toc.append(f'<li class="toc-parte">{esc(b["titulo"])}</li>')
        else:
            toc.append(f'<li><a href="#{b["id"]}">Capítulo {b["num"]} — {esc(b["titulo"])}</a></li>')
    toc_html = "\n".join(toc)

    # ---- Corpo ----
    corpo = []
    for i, b in enumerate(blocos):
        sec = [f'<section class="capitulo {"parte" if b["tipo"]=="parte" else ""}" id="{b["id"]}">']
        if b["tipo"] == "parte":
            sec.append(f'<p class="cap-num">Coleção do Despertar</p>')
            sec.append(f'<h2 class="cap-titulo parte-titulo">{esc(b["titulo"])}</h2>')
        else:
            sec.append(f'<p class="cap-num">Capítulo {b["num"]}</p>')
            sec.append(f'<h2 class="cap-titulo">{esc(b["titulo"])}</h2>')
        for tipo, txt in b["itens"]:
            if tipo == "h2":
                sec.append(f'<h3 class="secao-titulo">{esc(txt)}</h3>')
            else:
                sec.append(f'<p>{esc(txt)}</p>')
        # navegação
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
      '© Coleção do Despertar — Anestesia Mental. Todos os direitos reservados. Leitura online em compraoseu.com');
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
<meta property="og:description" content="16 capítulos sobre as correntes invisíveis dos algoritmos e como se libertar em Cristo. Leitura online gratuita e protegida.">
<meta property="og:image" content="{CAPA}">
<meta property="og:url" content="{URL}">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Missão com Deus — CompraOSeu">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(TITULO)} — {esc(SUBTITULO)}">
<meta name="twitter:description" content="16 capítulos sobre as correntes invisíveis dos algoritmos e como se libertar em Cristo. Leitura online gratuita e protegida.">
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
  <img class="capa-livro" src="{CAPA}" alt="Capa do livro Anestesia Mental e seus Algoritmos da Escravidão">
  <p class="selo">Coleção do Despertar</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">CompraOseu · Leitura online · grátis</p>
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
  <h2>O Sistema está em Conformidade</h2>
  <p>“O sistema caiu. O Reino chegou. E você é o agente dessa realidade.”</p>
  <p>Que a anestesia se rompa e que você viva a sua vida em Alta Definição — em Cristo, com propósito e liberdade.</p>
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


if __name__ == "__main__":
    build()
