# -*- coding: utf-8 -*-
"""
Gera a página de leitura do "Jesus Quer Falar Com Seu Filho" para a Vendd.
Design infantil acolhedor: cores suaves, cantos arredondados, emojis.
Proteção anti-cópia + impressão bloqueada.
"""
import json, re, html
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "jesus_preview.html"
DADOS = HERE / "jesus_dados.json"

TITULO = "Jesus Quer Falar com Seu Filho"
SUBTITULO = "Uma obra infantil de amor, fé e ensinamentos bíblicos"

def esc(t):
    return html.escape(t, quote=False)

def paragrafos(texto):
    """Converte texto em parágrafos HTML (robusto: divide por quebras)."""
    blocos = []
    # divide por parágrafos vazios ou linhas
    partes = re.split(r'\n\s*\n|(?<=\.)\s*\n(?=[A-ZÀ-Ú"\u201c])', texto)
    for par in partes:
        p = re.sub(r'\s+', ' ', par).strip()
        if p:
            blocos.append(f'<p>{esc(p)}</p>')
    return "\n".join(blocos)

def build():
    dados = json.loads(DADOS.read_text(encoding='utf-8'))

    # ---- Apresentação ----
    intro_html = paragrafos(dados["apresentacao"])[:2500]  # primeiros parágrafos

    # ---- Corpo (Jesus te ama, Oração) ----
    corpo_html = ""
    for bloco in dados["corpo"]:
        corpo_html += paragrafos(bloco) + "\n"

    # ---- Mandamentos ----
    mands_html = []
    for i, m in enumerate(dados["mandamentos"], 1):
        # extrai título (primeira linha) e conteúdo
        linhas = [l.strip() for l in m.split('\n') if l.strip()]
        titulo = linhas[0] if linhas else f"Mandamento {i}"
        conteudo = "\n".join(linhas[1:]) if len(linhas) > 1 else ""
        mands_html.append(f'''
        <div class="mandamento" id="mand-{i}">
          <div class="mand-num">{i}</div>
          <div class="mand-corpo">
            <h3 class="mand-titulo">{esc(titulo)}</h3>
            {paragrafos(conteudo)}
          </div>
        </div>''')
    mands_html_str = "\n".join(mands_html)

    # ---- Atividades ----
    ativ_html = paragrafos(dados["atividades"])

    # ---- Final ----
    final_html = paragrafos(dados["final"])[:2000]

    css = """
:root{
  --navy:#0e1a2e; --navy2:#16283f;
  --ouro:#c9a24b; --ouro-claro:#e3c877;
  --papel:#fdf9f0; --tinta:#3a2f28; --tinta2:#7a6a58;
  --linha:#eadfc8; --cta:#b8860b;
  --doce:#ff9e5e; --ceu:#87ceeb; --verde:#8bc34a;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--navy); color:var(--tinta);
  font-family:Georgia,'Times New Roman',Times,serif; line-height:1.8;
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
  background:radial-gradient(900px 500px at 70% -10%, rgba(135,206,235,.3), transparent 60%),
             radial-gradient(700px 400px at 20% 90%, rgba(201,162,75,.25), transparent 60%),
             linear-gradient(170deg,var(--navy) 0%,#123a5e 100%);}
.capa .emoji-grande{font-size:4.5rem; margin-bottom:1.2rem}
.capa h1{font-size:clamp(2rem,6vw,3.4rem); margin:0 0 .6rem; line-height:1.12}
.capa .sub{font-style:italic; color:#d8e6f2; font-size:1.1rem; margin-bottom:1.8rem; max-width:34rem}
.capa .versiculo-capa{font-size:.95rem; color:#c9a24b; font-style:italic; margin-bottom:2rem; max-width:28rem}
.capa .inicio{display:inline-block; background:linear-gradient(180deg,#ff9e5e,#e07b2f); color:#fff;
  font-weight:700; padding:16px 34px; border-radius:50px; text-decoration:none; font-size:1.1rem;
  box-shadow:0 8px 24px rgba(255,158,94,.4)}
.capa .aviso{font-size:.78rem; color:#8fa0b8; margin-top:1.4rem; max-width:26rem; line-height:1.5}

#sumario{background:var(--navy2); color:#fff; padding:3rem 1.2rem}
#sumario h2{text-align:center; color:var(--ouro); font-size:1.4rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1.4rem}
#sumario ul{list-style:none; padding:0; margin:0 auto; max-width:34rem}
#sumario li{border-bottom:1px solid rgba(201,162,75,.25)}
#sumario a{display:block; color:#e8ecf3; text-decoration:none; padding:.8rem .4rem; font-size:1rem}
#sumario a:hover{color:var(--ouro-claro); padding-left:.8rem}

.leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}
.leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:16px;
  padding:2.2rem 1.6rem; box-shadow:0 10px 30px rgba(0,0,0,.08)}
.capitulo{margin-top:2.5rem; padding-top:1.8rem; border-top:1px solid var(--linha)}
.cap-titulo{font-size:1.5rem; color:var(--navy); margin:0 0 1.2rem}
.cap-titulo.centro{text-align:center}
.capitulo p{margin:0 0 1rem; text-align:justify}

.mandamento{display:flex; gap:14px; align-items:flex-start; background:#fdf6e9;
  border:1px solid var(--linha); border-radius:14px; padding:16px; margin:0 0 14px}
.mand-num{flex:0 0 auto; width:38px; height:38px; border-radius:50%; background:var(--ouro);
  color:#fff; font-weight:800; font-size:1.1rem; display:flex; align-items:center; justify-content:center}
.mand-titulo{font-size:1.05rem; color:var(--navy); margin:0 0 6px}
.mand-corpo p{margin:0 0 8px; font-size:.98rem}
.mand-corpo p:last-child{margin:0}

.atividades{background:#eef7ee; border:2px dashed var(--verde); border-radius:14px; padding:18px}
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
  .cap-titulo{font-size:1.3rem}
  .mandamento{flex-direction:column}
}
"""

    js = """<script>
document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
document.addEventListener('copy', function(e){
  e.preventDefault();
  if (e.clipboardData){
    e.clipboardData.setData('text/plain',
      '© Coleção Oculta — Jesus Quer Falar com Seu Filho. Todos os direitos reservados. Leitura online em compraoseu.com');
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
<meta name="description" content="Leia online {esc(TITULO)} — uma obra infantil cristã que ensina os Mandamentos e o amor de Jesus às crianças. Leitura protegida.">
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
    <span class="ler">Leitura infantil</span>
  </div>
</header>

<section class="capa">
  <div class="emoji-grande">👶✨</div>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="versiculo-capa">"Deixem vir a mim as criancinhas, pois delas é o Reino de Deus." — Lucas 18:16</p>
  <a class="inicio" href="#introducao">Começar a leitura →</a>
  <p class="aviso">🔒 Leitura protegida: não é possível copiar, imprimir ou baixar este conteúdo.</p>
</section>

<section id="sumario">
  <h2>Sumário</h2>
  <ul>
    <li><a href="#introducao">Apresentação</a></li>
    <li><a href="#corpo">Jesus te ama</a></li>
    <li class="toc-parte" style="color:var(--ouro);font-weight:700;padding:.9rem .4rem .4rem;">Os 10 Mandamentos</li>
    <li><a href="#mand-1">1. Ame a Deus sobre todas as coisas</a></li>
    <li><a href="#mand-2">2. Adore somente a Deus</a></li>
    <li><a href="#mand-3">3. Fale o nome de Deus com respeito</a></li>
    <li><a href="#mand-4">4. Guarde o dia de descanso para Deus</a></li>
    <li><a href="#mand-5">5. Honre seu pai e sua mãe</a></li>
    <li><a href="#mand-6">6. Não machuque ninguém</a></li>
    <li><a href="#mand-7">7. Seja fiel, verdadeiro e respeite</a></li>
    <li><a href="#mand-8">8. Não pegue nada que não é seu</a></li>
    <li><a href="#mand-9">9. Não minta nem fale mal dos outros</a></li>
    <li><a href="#mand-10">10. Não deseje o que é dos outros</a></li>
    <li><a href="#atividades">Atividades</a></li>
    <li><a href="#final">Oração Final</a></li>
  </ul>
</section>

<main class="leitura">
  <div class="wrap">
    <section class="capitulo" id="introducao">
      <h2 class="cap-titulo centro">Apresentação 🌈</h2>
{intro_html}
      <nav class="cap-nav"><a href="#sumario">Sumário</a><a href="#corpo">Próximo →</a></nav>
    </section>

    <section class="capitulo" id="corpo">
      <h2 class="cap-titulo centro">Jesus te ama 💛</h2>
{corpo_html}
      <nav class="cap-nav"><a href="#introducao">← Anterior</a><a href="#mand-1">Os Mandamentos →</a></nav>
    </section>

    <section class="capitulo" id="mandamentos">
      <h2 class="cap-titulo centro">Os 10 Mandamentos 📜</h2>
      <p style="text-align:center;color:var(--tinta2);margin-bottom:1.6rem">Contados com amor e histórias, do jeitinho que as crianças entendem.</p>
{mands_html_str}
      <nav class="cap-nav"><a href="#corpo">← Anterior</a><a href="#atividades">Atividades →</a></nav>
    </section>

    <section class="capitulo" id="atividades">
      <h2 class="cap-titulo centro">Atividades 🎨</h2>
      <div class="atividades">
{ativ_html}
      </div>
      <nav class="cap-nav"><a href="#mandamentos">← Anterior</a><a href="#final">Oração Final →</a></nav>
    </section>

    <section class="capitulo" id="final">
      <h2 class="cap-titulo centro">Oração Final 🙏</h2>
{final_html}
      <nav class="cap-nav"><a href="#atividades">← Anterior</a><a href="#sumario">Sumário</a></nav>
    </section>
  </div>
</main>

<section id="fim">
  <h2>Um abraço cheio de fé e paz! 🤗</h2>
  <p>Que Jesus, seu melhor amigo, esteja sempre pertinho de você, guiando seus passos com luz e proteção.</p>
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
