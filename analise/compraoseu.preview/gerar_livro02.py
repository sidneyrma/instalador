# -*- coding: utf-8 -*-
"""
Gera a página de leitura do livro02 ("O Livro Proibido dos Mestres") para a Vendd:
- Conteúdo limpo (normalizado) com os 10 capítulos
- Proteção anti-cópia + impressão bloqueada
- Design de leitura + identidade da marca
- Sumário clicável + navegação entre capítulos
"""
import sys, re, html
from pathlib import Path

HERE = Path(__file__).parent
PAGINAS = HERE.parent.parent / "paginas"
OUT = PAGINAS / "livro02_preview.html"

TITULO = "A Sabedoria dos Mestres"
SUBTITULO = "O Despertar do Conhecimento que Liberta a Alma"

def esc(t):
    return html.escape(t, quote=False)

def build():
    # reusa o normalizador para obter a estrutura (tipo, texto)
    sys.path.insert(0, str(HERE))
    from normalizar_livro02 import SRC, TITULOS_CAP, NUM_MAP, corrigir_capitalizacao, capitalizar_sentencas
    import re as _re

    # recalcula a estrutura (mesma lógica do normalizador)
    fluxo = ' '.join(l.strip() for l in SRC.read_text(encoding='utf-8').replace('\r\n','\n').split('\n') if l.strip())
    fluxo = _re.sub(r'\s+([,.;:!?])', r'\1', fluxo)
    correcoes = {
        "Lautsé": "Lao-Tsé", "Padma Sambava": "Padmasambhava", "Ipatia": "Hipátia",
        "Hipátia De Alexandria": "Hipátia de Alexandria",
        "sobre seu peso das Palavras": "sobre o peso das palavras",
        "sobre seu peso das palavras": "sobre o peso das palavras",
    }
    for a, b in correcoes.items():
        fluxo = fluxo.replace(a, b)

    caps = list(_re.finditer(r'Cap[ií]tulo\s+(um|dois|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|\d+)[,.]?\s*', fluxo))
    segmentos = []
    for i, m in enumerate(caps):
        num = NUM_MAP.get(m.group(1).lower()) or int(m.group(1))
        fim_prox = caps[i+1].start() if i+1 < len(caps) else len(fluxo)
        segmentos.append((num, fluxo[m.end():fim_prox].strip()))
    pre_cap1 = fluxo[:caps[0].start()].strip() if caps else fluxo.strip()

    def dividir_paragrafos(texto, alvo=110):
        texto = _re.sub(r'\s+', ' ', texto).strip()
        sentencas = _re.findall(r'[^.!?]+[.!?]?', texto)
        paragrafos, atual = [], ""
        for s in sentencas:
            s = s.strip()
            if not s: continue
            if len(atual.split()) + len(s.split()) > alvo and atual.strip():
                paragrafos.append(_re.sub(r'\s{2,}', ' ', atual.strip()))
                atual = s
            else:
                atual = (atual + ' ' + s).strip()
        if atual.strip():
            paragrafos.append(_re.sub(r'\s{2,}', ' ', atual.strip()))
        final = []
        for p in paragrafos:
            if p and p[0].islower():
                p = p[0].upper() + p[1:]
            final.append(p)
        return final

    estrutura = []
    if pre_cap1:
        for p in dividir_paragrafos(corrigir_capitalizacao(pre_cap1)):
            estrutura.append(("p", capitalizar_sentencas(p)))
    for num, texto in segmentos:
        estrutura.append(("h1", f"CAPÍTULO {num}"))
        estrutura.append(("h2", TITULOS_CAP[num]))
        texto_corrigido = corrigir_capitalizacao(texto)
        titulo_limpo = TITULOS_CAP[num]
        texto_corrigido = _re.sub(r'^\s*' + _re.escape(titulo_limpo) + r'[.!]?\s*', '', texto_corrigido, flags=_re.I)
        prim = _re.match(r'^([^.!?]+[.!?]?)', texto_corrigido)
        if prim:
            s = prim.group(1).strip()
            s_limpo = _re.sub(r'[.!]', '', s).lower().strip()
            t_limpo = _re.sub(r'[.!]', '', titulo_limpo).lower().strip()
            if s_limpo == t_limpo or t_limpo in s_limpo:
                texto_corrigido = texto_corrigido[len(s):].strip()
        texto_corrigido = _re.sub(r'\s{2,}', ' ', texto_corrigido)
        for p in dividir_paragrafos(texto_corrigido):
            estrutura.append(("p", capitalizar_sentencas(p)))

    # ---- SUMÁRIO ----
    toc = ['<li><a href="#intro">Introdução</a></li>']
    for i in range(1, 11):
        toc.append(f'<li><a href="#cap{i}">Capítulo {i} — {esc(TITULOS_CAP[i])}</a></li>')
    toc_html = "\n".join(toc)

    # ---- CORPO ----
    secoes = []
    atual_secao = []
    def flush():
        nonlocal atual_secao
        if atual_secao:
            secoes.append("\n".join(atual_secao))
            atual_secao = []

    for tipo, txt in estrutura:
        if tipo == "h1":
            flush()
            num = txt.split()[-1]
            atual_secao.append(f'<section class="capitulo" id="cap{num}">')
            atual_secao.append(f'<p class="cap-num">Capítulo {num}</p>')
        elif tipo == "h2":
            atual_secao.append(f'<h2 class="cap-titulo">{esc(txt)}</h2>')
        elif tipo == "p":
            # primeira seção = introdução
            if not secoes and not atual_secao:
                atual_secao.append('<section class="capitulo" id="intro">')
                atual_secao.append('<p class="cap-num">Prefácio</p>')
                atual_secao.append('<h2 class="cap-titulo">Introdução</h2>')
            atual_secao.append(f'<p>{esc(txt)}</p>')
    # fecha a última seção com navegação
    flush()

    # adiciona navegação em cada seção
    html_secoes = []
    for i, sec in enumerate(secoes):
        nav = ['<nav class="cap-nav">']
        if i == 0:
            nav.append('<a href="#sumario">Sumário</a>')
            nav.append('<a href="#cap1">Capítulo 1 →</a>')
        else:
            num_sec = re.search(r'id="cap(\d+)"', sec)
            if num_sec:
                n = int(num_sec.group(1))
                nav.append(f'<a href="#cap{n-1}">← Capítulo {n-1}</a>' if n > 1 else '<a href="#intro">← Introdução</a>')
                nav.append('<a href="#sumario">Sumário</a>')
                nav.append(f'<a href="#cap{n+1}">Capítulo {n+1} →</a>' if n < 10 else '<a href="#fim">Fim</a>')
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
#sumario ul{list-style:none; padding:0; margin:0 auto; max-width:32rem}
#sumario li{border-bottom:1px solid rgba(201,162,75,.25)}
#sumario a{display:block; color:#e8ecf3; text-decoration:none; padding:.8rem .4rem; font-size:1rem}
#sumario a:hover{color:var(--ouro-claro); padding-left:.8rem}

.leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}
.leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:12px;
  padding:2.2rem 1.6rem; box-shadow:0 10px 30px rgba(0,0,0,.08)}
.capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha)}
.cap-num{letter-spacing:.3em; text-transform:uppercase; font-size:.78rem; color:var(--ouro); margin:0 0 .5rem}
.cap-titulo{font-size:1.6rem; color:var(--navy); margin:0 0 1.6rem}
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
      '© Coleção do Despertar — O Livro Proibido dos Mestres. Todos os direitos reservados. Leitura online em compraoseu.com');
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
  <p>© Coleção do Despertar — Todos os direitos reservados.</p>
</div>

<header class="topbar">
  <div class="wrap">
    <a class="logo" href="#">Missão <span>com Deus</span></a>
    <span class="ler">Leitura online</span>
  </div>
</header>

<section class="capa">
  <img class="capa-livro" src="https://i.ibb.co/yBNkHB7q/livro02.jpg" alt="Capa do livro O Livro Proibido dos Mestres">
  <p class="selo">Coleção do Despertar</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">Leitura online · grátis</p>
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
{corpo_html}
  </div>
</main>

<section id="fim">
  <h2>A Jornada termina aqui…</h2>
  <p>…mas o mestre permanece com você para sempre, dentro, vivo, presente, silencioso, eterno.</p>
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
