# -*- coding: utf-8 -*-
"""
Gera a página HTML de estudos com TODAS as afirmações 'EU SOU' dos livros
10, 08, 07, 03, 02, 01, organizadas por livro, no padrão da coleção.
"""
import json, html, re
from pathlib import Path

ROOT = Path('/home/user/instalador')
JSON = ROOT/'analise/livro_afirmacoes/afirmacoes_eusou_por_livro.json'
OUT = ROOT/'paginas'/'eusou_estudos_preview.html'

def esc(t):
    return html.escape(t, quote=False)

def build():
    dados = json.loads(JSON.read_text(encoding='utf-8'))

    # Ordem dos livros
    ordem = ['livro01', 'livro02', 'livro03', 'livro07', 'livro08', 'livro10']
    livros_ord = [(k, dados[k]) for k in ordem if k in dados]

    total = sum(len(v['afirmacoes']) for _, v in livros_ord)

    # Sumário
    toc = []
    for slug, info in livros_ord:
        n = len(info['afirmacoes'])
        toc.append(f'<li><a href="#{slug}">{esc(info["titulo"])} <span class="qtd">({n})</span></a></li>')
    toc_html = '\n'.join(toc)

    # Corpo
    corpo = []
    # Abertura
    corpo.append('''<section class="capitulo" id="abertura">
      <p class="cap-num">Coleção do Despertar</p>
      <h2 class="cap-titulo">Sobre esta compilação</h2>
      <p>Esta página reúne, para estudo, todas as afirmações e declarações que envolvem o "EU SOU" encontradas nas obras: O Verbo que Transforma (01), A Sabedoria dos Mestres (02), A Mente Renovada (03), O Caminho do Despertar (07), O Arquiteto da Realidade (08) e O Despertar do Observador (10).</p>
      <div class="box aviso"><h3>Fundamento bíblico</h3><p>O nome "EU SOU" é o nome sagrado de Deus (Êxodo 3:14). Quando declaramos, declaramos quem somos em Cristo, não uma autossuficiência vazia. A morte e a vida estão no poder da língua (Provérbios 18:21).</p></div>
      <nav class="cap-nav"><a href="#sumario">Sumário</a><a href="#livro01">Primeiro livro →</a></nav>
    </section>''')

    # Livros
    for idx, (slug, info) in enumerate(livros_ord):
        sec = [f'<section class="capitulo" id="{slug}">']
        sec.append(f'<p class="cap-num">Livro {slug.replace("livro","")} · Estudo</p>')
        sec.append(f'<h2 class="cap-titulo">{esc(info["titulo"])}</h2>')
        sec.append('<div class="lista-afirmacoes">')
        for af in info['afirmacoes']:
            sec.append(f'<p class="afirmacao">✨ {esc(af)}</p>')
        sec.append('</div>')
        nav = ['<nav class="cap-nav">']
        if idx > 0:
            nav.append(f'<a href="#{livros_ord[idx-1][0]}">← Anterior</a>')
        else:
            nav.append('<a href="#abertura">← Início</a>')
        nav.append('<a href="#sumario">Sumário</a>')
        if idx < len(livros_ord) - 1:
            nav.append(f'<a href="#{livros_ord[idx+1][0]}">Próximo →</a>')
        else:
            nav.append('<a href="#fim">Fim</a>')
        nav.append('</nav>')
        sec.append('\n'.join(nav))
        sec.append('</section>')
        corpo.append('\n'.join(sec))

    corpo_html = '\n'.join(corpo)

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
}
.wrap{max-width:46rem; margin:0 auto}
.topbar{background:var(--navy); border-bottom:3px solid var(--ouro); position:sticky; top:0; z-index:50}
.topbar .wrap{display:flex; align-items:center; justify-content:space-between; padding:.8rem 1.2rem; gap:10px}
.topbar .logo{color:#fff; font-size:1.05rem; text-decoration:none}
.topbar .logo span{color:var(--ouro)}
.topbar .ler{color:var(--ouro-claro); font-size:.78rem; letter-spacing:.2em; text-transform:uppercase}
.capa{min-height:60vh; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:3rem 1.2rem; color:#fff;
  background:radial-gradient(900px 500px at 70% -10%, rgba(201,162,75,.2), transparent 60%), linear-gradient(170deg,var(--navy) 0%,#120b18 100%);}
.capa .selo{font-size:.78rem; letter-spacing:.4em; text-transform:uppercase; color:var(--ouro-claro); margin-bottom:1.6rem}
.capa h1{font-size:clamp(1.8rem,5vw,2.8rem); margin:0 0 .6rem; line-height:1.12}
.capa .sub{font-style:italic; color:#cfd6e2; font-size:1.1rem; margin-bottom:1.8rem; max-width:34rem}
.capa .autor{font-size:.9rem; letter-spacing:.3em; text-transform:uppercase; color:var(--ouro); margin-bottom:2.4rem}
.capa .inicio{display:inline-block; background:linear-gradient(180deg,#d4a83f,var(--cta)); color:#fff;
  font-weight:700; padding:14px 30px; border-radius:8px; text-decoration:none; font-size:1rem}
.capa .aviso2{font-size:.78rem; color:#8fa0b8; margin-top:1.4rem; max-width:26rem; line-height:1.5}
#sumario{background:var(--navy2); color:#fff; padding:3rem 1.2rem}
#sumario h2{text-align:center; color:var(--ouro); font-size:1.4rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1.4rem}
#sumario ul{list-style:none; padding:0; margin:0 auto; max-width:34rem}
#sumario li{border-bottom:1px solid rgba(201,162,75,.25)}
#sumario a{display:flex; justify-content:space-between; align-items:center; color:#e8ecf3; text-decoration:none; padding:.8rem .4rem; font-size:1rem}
#sumario a:hover{color:var(--ouro-claro); padding-left:.8rem}
#sumario .qtd{color:var(--ouro); font-size:.85rem}
.leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}
.leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:12px;
  padding:2.2rem 1.6rem; box-shadow:0 10px 30px rgba(0,0,0,.08)}
.capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha)}
.cap-num{letter-spacing:.3em; text-transform:uppercase; font-size:.78rem; color:var(--ouro); margin:0 0 .5rem}
.cap-titulo{font-size:1.5rem; color:var(--navy); margin:0 0 1.2rem}
.capitulo p{margin:0 0 1rem; text-align:justify}
.afirmacao{background:#fdf6e3; border-left:4px solid var(--ouro); border-radius:8px;
  padding:.8rem 1rem; margin:.6rem 0; text-align:left; font-size:1.02rem;}
.box{border-radius:10px; padding:1rem 1.2rem; margin:1.2rem 0}
.box h3{margin:0 0 .4rem; font-size:1rem; letter-spacing:.05em}
.box p{margin:0; text-align:justify}
.box.aviso{background:#fdecea; border-left:4px solid #c0392b}
.box.aviso h3{color:#a93226}
.cap-nav{display:flex; justify-content:space-between; gap:.6rem; flex-wrap:wrap; margin-top:2.4rem;
  padding-top:1rem; border-top:1px dashed var(--linha); font-size:.9rem; font-family:system-ui,sans-serif}
.cap-nav a{color:var(--navy2); text-decoration:none; border-bottom:1px dotted var(--ouro); padding:2px 4px}
.cap-nav a:hover{color:var(--cta)}
#fim{background:var(--navy); color:#fff; text-align:center; padding:4rem 1.2rem}
#fim h2{font-size:1.5rem; margin-bottom:.8rem}
#fim p{color:#c4cdda; max-width:32rem; margin:0 auto 1.6rem}
#fim .cred{font-size:.82rem; color:#8fa0b8; margin-top:1.6rem; line-height:1.6}
footer{background:#0a1322; color:#7f8ca1; text-align:center; padding:1.6rem 1.2rem; font-size:.8rem}
@media (max-width:560px){
  body{font-size:17px}
  .leitura .wrap{padding:1.4rem 1rem}
  .cap-titulo{font-size:1.3rem}
}
"""

    html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Estudo das Afirmações EU SOU — Livros 01, 02, 03, 07, 08 e 10</title>
<meta name="description" content="Compilação para estudo de todas as afirmações e declarações EU SOU encontradas nos livros O Verbo que Transforma, A Sabedoria dos Mestres, A Mente Renovada, O Caminho do Despertar, O Arquiteto da Realidade e O Despertar do Observador.">
<style>{css}</style>
</head>
<body>

<header class="topbar">
  <div class="wrap">
    <a class="logo" href="#">Missão <span>com Deus</span></a>
    <span class="ler">Estudo EU SOU</span>
  </div>
</header>

<section class="capa">
  <p class="selo">Coleção do Despertar</p>
  <h1>Estudo das Afirmações EU SOU</h1>
  <p class="sub">As declarações poderosas do eu interior na natureza de Deus, extraídas dos livros 01, 02, 03, 07, 08 e 10</p>
  <p class="autor">{total} afirmações compiladas · Versão de estudo</p>
  <a class="inicio" href="#sumario">Começar o estudo →</a>
  <p class="aviso2">✨ Compilação para estudo e reflexão pessoal.</p>
</section>

<section id="sumario">
  <h2>Sumário por livro</h2>
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
  <h2>O Poder do EU SOU</h2>
  <p>"E disse Deus a Moisés: EU SOU O QUE SOU." (Êxodo 3:14)</p>
  <p>Quando declaramos quem somos em Cristo, as nossas palavras se tornam sementes de vida.</p>
  <p class="cred">© Coleção do Despertar · Missão com Deus · CompraOSeu<br>
  Versão de estudo — para uso pessoal e avaliação.</p>
</section>

<footer>
  <p>Missão com Deus · CompraOSeu — Desperte sua mente, fortaleça sua fé, transforme sua vida.</p>
</footer>

</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_doc, encoding='utf-8')
    print("Gerado:", OUT, f"({OUT.stat().st_size:,} bytes)")
    print(f"Livros: {len(livros_ord)} | Afirmações: {total}")

if __name__ == '__main__':
    build()
