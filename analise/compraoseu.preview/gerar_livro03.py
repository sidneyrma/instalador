# -*- coding: utf-8 -*-
"""
Gera a página de leitura do livro03 ("O Caibalion / Kybalion") para a Vendd.
LÊ o texto limpo (livro03_limpo.txt) gerado pelo normalizador — a fonte da verdade.
- Proteção anti-cópia + impressão bloqueada
- Design de leitura + identidade da marca
- Sumário clicável + navegação entre capítulos
"""
import re, html
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "livro03_preview.html"
LIMPO = HERE / "livro03_limpo.txt"

TITULO = "O Caibalion"
SUBTITULO = "Edição Definitiva e Comentada — A Filosofia Hermética"

TITULOS_PARTE1 = {
    1: "A Filosofia Hermética", 2: "Os Sete Princípios Herméticos",
    3: "A Transmutação Mental", 4: "O Todo", 5: "O Universo Mental",
    6: "O Paradoxo Divino", 7: "O Todo em Tudo", 8: "Os Planos da Correspondência",
    9: "A Vibração", 10: "A Polaridade", 11: "O Ritmo", 12: "A Causalidade",
    13: "O Gênero", 14: "O Gênero Mental", 15: "Axiomas Herméticos",
}
TITULOS_PARTE2 = {
    1: "Introdução ao Livro", 2: "Lei Cósmica e Leis Cósmicas",
    3: "As Sete Leis Cósmicas", 4: "A Lei Cósmica da Unidade na Diversidade",
    5: "A Lei Cósmica da Atividade", 6: "A Lei Cósmica da Mudança",
    7: "A Lei Cósmica da Causalidade", 8: "A Lei Cósmica do Ritmo",
    9: "A Lei Cósmica da Polaridade", 10: "A Lei Cósmica do Equilíbrio",
}

def esc(t):
    return html.escape(t, quote=False)

def build():
    blocos = [b.strip() for b in LIMPO.read_text(encoding='utf-8').split('\n\n') if b.strip()]

    # ---- Sumário ----
    toc = ['<li><a href="#apresentacao">Apresentação</a></li>']
    for i in range(1, 16):
        toc.append(f'<li><a href="#p1-{i}">Capítulo {i} — {esc(TITULOS_PARTE1[i])}</a></li>')
    toc.append('<li class="toc-parte">PARTE II — As Sete Leis Cósmicas</li>')
    for i in range(1, 11):
        toc.append(f'<li><a href="#p2-{i}">Lei {i} — {esc(TITULOS_PARTE2[i])}</a></li>')
    toc.append('<li><a href="#comentarios">Comentários da Edição</a></li>')
    toc_html = "\n".join(toc)

    # ---- Corpo HTML a partir dos blocos ----
    secoes = []
    atual = []
    parte_atual = "apresentacao"
    num_part2 = 1  # contador para parte 2 (ordem fiel do texto)

    def flush():
        nonlocal atual
        if atual:
            secoes.append("\n".join(atual))
            atual = []

    for bloco in blocos:
        if bloco == "APRESENTAÇÃO":
            flush(); parte_atual = "apresentacao"
            atual.append('<section class="capitulo" id="apresentacao">')
            atual.append('<h2 class="cap-titulo">Apresentação</h2>')
        elif bloco == "PARTE I — O CAIBALION":
            flush(); parte_atual = "p1"
            atual.append('<section class="capitulo parte" id="parte1">')
            atual.append('<h2 class="cap-titulo parte-titulo">PARTE I — O Caibalion</h2>')
        elif bloco == "PARTE II — AS SETE LEIS CÓSMICAS":
            flush(); parte_atual = "p2"; num_part2 = 1
            atual.append('<section class="capitulo parte" id="parte2">')
            atual.append('<h2 class="cap-titulo parte-titulo">PARTE II — As Sete Leis Cósmicas</h2>')
        elif bloco == "COMENTÁRIOS DA EDIÇÃO":
            flush(); parte_atual = "comentarios"
            atual.append('<section class="capitulo" id="comentarios">')
            atual.append('<h2 class="cap-titulo">Comentários da Edição</h2>')
        else:
            m_cap = re.match(r'CAPÍTULO (\d+)', bloco)
            m_sub = re.match(r'^(A Filosofia Hermética|Os Sete Princípios|A Transmutação|O Todo|O Universo|'
                             r'O Paradoxo|Os Planos|A Vibração|A Polaridade|O Ritmo|A Causalidade|O Gênero|'
                             r'Axiomas|Introdução ao Livro|Lei Cósmica|As Sete Leis|A Lei Cósmica)', bloco)
            if m_cap:
                num = int(m_cap.group(1))
                flush()
                if parte_atual == "p1":
                    atual.append(f'<section class="capitulo" id="p1-{num}">')
                    atual.append(f'<p class="cap-num">Capítulo {num}</p>')
                elif parte_atual == "p2":
                    atual.append(f'<section class="capitulo" id="p2-{num_part2}">')
                    atual.append(f'<p class="cap-num">Capítulo {num}</p>')
                    num_part2 += 1
            elif m_sub and parte_atual in ("p1", "p2"):
                # é um subtítulo (título de capítulo) — pula pois já vem como parte do bloco anterior
                pass
            else:
                atual.append(f'<p>{esc(bloco)}</p>')
    flush()

    # adicionar navegação em cada seção
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
.cap-titulo{font-size:1.6rem; color:var(--navy); margin:0 0 1.6rem}
.cap-titulo.parte-titulo{color:var(--ouro); text-align:center; letter-spacing:.1em}
.cap-sub{font-size:1.05rem; color:var(--navy); margin:0 0 1rem}
.capitulo p{margin:0 0 1.1rem; text-align:justify}
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
      '© Coleção Oculta — O Caibalion (Kybalion). Todos os direitos reservados. Leitura online em compraoseu.com');
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
<meta name="description" content="Leia online {esc(TITULO)} — {esc(SUBTITULO)}. Leitura protegida, sem impressão e sem cópia.">
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
  <p class="selo">Coleção Oculta</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">Leitura online · grátis</p>
  <a class="inicio" href="#apresentacao">Começar a leitura →</a>
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
  <h2>Fim da obra</h2>
  <p>Que estes ensinamentos herméticos iluminem seus passos na busca pelo conhecimento e pela verdade.</p>
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
