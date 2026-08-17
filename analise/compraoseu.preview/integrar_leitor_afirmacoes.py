#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integra o Leitor do Despertar no livro de Afirmações, gerando:
  paginas/livro_afirmacoes_leitor_preview.html

Recursos: lembrar onde parou, fita dourada, trilha de capítulos,
A- / A / A+, modos Dia/Sépia/Noite, balões de dicas, sumário com marcas
e proteção de direitos autorais (user-select, contextmenu, teclas, print).
"""
import re
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]
ORIG = RAIZ / "paginas" / "livro12_preview.html"
DEST = RAIZ / "paginas" / "livro12_leitor_preview.html"

html = ORIG.read_text(encoding="utf-8")
original = html

# ============ 1. Regra do body: fonte ajustável + proteção de seleção ============
antes = "font-family:Georgia,'Times New Roman',Times,serif; line-height:1.75;\n}"
depois = ("font-family:Georgia,'Times New Roman',Times,serif; line-height:1.75;\n"
          "  font-size:var(--tamanho-fonte);\n"
          "  -webkit-user-select:none; -moz-user-select:none; -ms-user-select:none; user-select:none;\n"
          "}\n"
          ":root{--tamanho-fonte:100%}")
assert antes in html, "regra do body não encontrada"
html = html.replace(antes, depois, 1)

# ============ 2. Cores adaptadas aos modos de tela ============ #
REGS = [
    (".leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}",
     ".leitura{background:var(--fundo-leitura); padding:2.6rem 1.2rem 4rem; color:var(--tinta-leitura)}"),
    (".leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:12px;",
     ".leitura .wrap{background:var(--card-leitura); border:1px solid var(--linha-leitura); border-radius:12px;"),
    (".capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha)}",
     ".capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha-leitura)}"),
    (".cap-titulo{font-size:1.5rem; color:var(--navy); margin:0 0 1.2rem}",
     ".cap-titulo{font-size:1.5rem; color:var(--titulo-leitura); margin:0 0 1.2rem}"),
    (".afirmacao{background:#fdf6e3; border-left:4px solid var(--ouro); border-radius:8px;",
     ".afirmacao{background:var(--destaque); border-left:4px solid var(--ouro); border-radius:8px;"),
    (".box.versiculo{background:#fdf6e3; border-left:4px solid var(--ouro)}",
     ".box.versiculo{background:var(--destaque); border-left:4px solid var(--ouro)}"),
    (".faq-item{background:#faf6ee;border:1px solid #e4dccb;border-radius:10px;margin-bottom:10px;overflow:hidden;}",
     ".faq-item{background:var(--fundo-leitura);border:1px solid var(--linha-leitura);border-radius:10px;margin-bottom:10px;overflow:hidden;}"),
    (".faq-q{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;cursor:pointer;font-weight:700;color:#0e1a2e;font-size:1rem;background:#fdf6e3;}",
     ".faq-q{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;cursor:pointer;font-weight:700;color:var(--titulo-leitura);font-size:1rem;background:var(--destaque);}"),
    (".faq-a{display:none;padding:14px 18px;color:#2b2620;font-size:.95rem;line-height:1.7;background:#fff;}",
     ".faq-a{display:none;padding:14px 18px;color:var(--tinta-leitura);font-size:.95rem;line-height:1.7;background:var(--card-leitura);}"),
]
for a, d in REGS:
    assert a in html, "CSS não encontrado: " + a[:60]
    html = html.replace(a, d, 1)

# ============ 3. CSS do Leitor do Despertar ============ #
CSS_LEITOR = """
  /* ===== Leitor do Despertar ===== */
  body[data-modo="dia"]{--fundo-leitura:var(--papel); --card-leitura:#fff; --tinta-leitura:var(--tinta); --titulo-leitura:var(--navy); --linha-leitura:var(--linha); --destaque:#fdf6e3}
  body[data-modo="sepia"]{--fundo-leitura:#f1e6cd; --card-leitura:#faf3e0; --tinta-leitura:#4a3a20; --titulo-leitura:#3a2d15; --linha-leitura:#d8c69d; --destaque:#f6ecd2}
  body[data-modo="noite"]{--fundo-leitura:#0d1520; --card-leitura:#17202f; --tinta-leitura:#c9d4e3; --titulo-leitura:#e3c877; --linha-leitura:#2a3a52; --destaque:#1c2940}
  #barra-progresso{
    position:fixed; top:0; left:0; height:4px; width:0%;
    background:linear-gradient(90deg,#c9a24b,#e3c877);
    z-index:100; border-radius:0 3px 3px 0; transition:width .15s linear;
  }
  .topbar .linha1{display:flex; align-items:center; justify-content:space-between; gap:10px; width:100%}
  #stats-leitura{color:var(--ouro-claro); font-size:.7rem; letter-spacing:.05em; font-family:system-ui,sans-serif; white-space:nowrap}
  .controles{display:flex; align-items:center; gap:5px; flex-wrap:wrap; font-family:system-ui,sans-serif}
  .controles button{
    background:var(--navy2); color:#fff; border:1px solid rgba(201,162,75,.5);
    border-radius:6px; min-width:34px; height:30px; cursor:pointer;
    font-size:.8rem; font-weight:700; font-family:Georgia,serif; line-height:1; padding:0 8px;
  }
  .controles button:hover{background:var(--ouro); color:var(--navy)}
  .controles button.ativo{background:var(--ouro); color:var(--navy)}
  .controles .sep{width:1px; height:20px; background:rgba(201,162,75,.35); margin:0 3px}
  #trilha{
    position:fixed; right:6px; top:50%; height:60vh; transform:translateY(-50%);
    z-index:55; display:block;
    background:rgba(14,26,46,.85); border:1px solid rgba(201,162,75,.4); border-radius:12px;
    width:14px; box-shadow:0 4px 14px rgba(0,0,0,.3);
  }
  #trilha .ponto{
    position:absolute; left:50%; transform:translateX(-50%);
    width:8px; height:8px; border-radius:50%; background:rgba(201,162,75,.35);
    cursor:pointer; border:none; padding:0; transition:all .2s;
  }
  #trilha .ponto:hover{background:var(--ouro-claro); transform:translateX(-50%) scale(1.35)}
  #trilha .ponto.feito{background:rgba(201,162,75,.7)}
  #trilha .ponto.atual{background:var(--ouro); width:11px; height:11px; box-shadow:0 0 8px rgba(201,162,75,.9)}
  #fita-lateral{
    position:fixed; right:0; width:6px; height:52px; background:linear-gradient(180deg,#e3c877,#b8860b);
    border-radius:4px 0 0 4px; z-index:56; cursor:pointer;
    box-shadow:0 2px 8px rgba(0,0,0,.4); display:none;
  }
  #fita-lateral::after{content:"🎗️"; position:absolute; right:4px; top:-6px; font-size:14px}
  #fita-lateral:hover{width:10px}
  #botao-marcador{
    position:fixed; right:16px; bottom:16px; z-index:60;
    background:var(--navy); color:var(--ouro-claro); border:1px solid var(--ouro);
    border-radius:50px; padding:10px 16px; font-size:.8rem; cursor:pointer;
    font-family:system-ui,sans-serif; box-shadow:0 4px 14px rgba(0,0,0,.35);
  }
  #botao-marcador:hover{background:var(--ouro); color:var(--navy)}
  #baloes{position:fixed; top:10px; left:0; right:0; z-index:90; display:flex; flex-direction:column; align-items:center; gap:8px; pointer-events:none}
  .balao{
    pointer-events:auto; max-width:92%; width:430px;
    background:#fffdf5; border:1px solid var(--ouro); border-left:5px solid var(--ouro);
    border-radius:10px; padding:10px 14px; font-size:.86rem; line-height:1.45;
    color:var(--navy); font-family:system-ui,sans-serif;
    box-shadow:0 8px 24px rgba(0,0,0,.28);
    display:flex; align-items:center; gap:10px;
    animation:balaoEntra .35s ease;
  }
  .balao .emoji{font-size:1.15rem}
  .balao .texto{flex:1}
  .balao .texto b{color:var(--cta)}
  .balao .fechar{background:none; border:none; color:var(--tinta2); font-size:1.05rem; cursor:pointer; line-height:1; padding:4px}
  .balao .fechar:hover{color:var(--cta)}
  .balao .acao{
    background:linear-gradient(180deg,#d4a83f,var(--cta)); color:#fff; border:none;
    border-radius:6px; padding:7px 12px; font-size:.78rem; font-weight:700; cursor:pointer; font-family:system-ui,sans-serif; white-space:nowrap;
  }
  .balao.saindo{animation:balaoSai .3s ease forwards}
  @keyframes balaoEntra{from{opacity:0; transform:translateY(-14px)} to{opacity:1; transform:translateY(0)}}
  @keyframes balaoSai{from{opacity:1} to{opacity:0; transform:translateY(-10px)}}
  #sumario li.aqui a{color:var(--ouro-claro); font-weight:700}
  #sumario li.lido a{color:#9fb0c9}
  #sumario li .marca{color:var(--ouro-claro); font-size:.78rem; font-family:system-ui,sans-serif; white-space:nowrap; padding-right:.4rem}
  @media print{
    body::before{
      content:"Livro protegido. A impressão não está disponível nesta obra. Obrigado pela compreensão.";
      display:block; position:fixed; inset:0; background:#fff; color:#333;
      font-size:18px; text-align:center; padding-top:40vh; z-index:9999;
    }
    .topbar,.capa,#sumario,.leitura,#fim,footer,#baloes,#trilha,#fita-lateral,#botao-marcador,#barra-progresso{display:none !important}
  }
  @media (max-width:560px){
    .controles button{min-width:30px; padding:0 6px}
    .controles .bt-txt{display:none}
    #trilha{right:3px}
    #stats-leitura{display:none}
  }
"""
assert "</style>" in html
html = html.replace("</style>", CSS_LEITOR + "\n</style>", 1)

# ============ 4. Body: modo inicial + barra de progresso ============ #
assert "<body>\n\n<header" in html
html = html.replace("<body>\n\n<header", "<body data-modo=\"dia\">\n\n<div id=\"barra-progresso\"></div>\n\n<header", 1)

# ============ 5. Topbar com controles ============ #
TOPBAR_ANTIGO = """<header class="topbar">
  <div class="wrap">
    <a class="logo" href="#">Missão <span>com Deus</span></a>
    <span class="ler">Comece o dia</span>
  </div>
</header>"""
assert TOPBAR_ANTIGO in html, "topbar antigo não encontrado"
TOPBAR_NOVO = """<header class="topbar">
  <div class="wrap">
    <div class="linha1">
      <a class="logo" href="#capa">Missão <span>com Deus</span></a>
      <span id="stats-leitura">Início da leitura</span>
    </div>
    <div class="controles">
      <button id="btn-menos" title="Diminuir letras">A−</button>
      <button id="btn-padrao" title="Tamanho original" class="ativo">A</button>
      <button id="btn-mais" title="Aumentar letras">A+</button>
      <span class="sep"></span>
      <button id="btn-fita" title="Colocar ou remover a fita dourada"><span class="bt-ic">🎗️</span><span class="bt-txt"> Fita</span></button>
      <button id="btn-modo" title="Mudar a cor da tela (Dia, Sépia, Noite)"><span class="bt-ic">🎨</span><span class="bt-txt"> Dia</span></button>
      <button id="btn-dicas" title="Ver dicas de leitura">💡</button>
    </div>
  </div>
</header>"""
html = html.replace(TOPBAR_ANTIGO, TOPBAR_NOVO, 1)

# ============ 6. Balões, trilha e fita após o topbar ============ #
html = html.replace("</header>\n\n<section class=\"capa\">",
                    "</header>\n\n<div id=\"baloes\"></div>\n<div id=\"trilha\"></div>\n<div id=\"fita-lateral\"></div>\n\n<section class=\"capa\" id=\"capa\">", 1)

# ============ 7. ids nas li do sumário + span de marca de leitura ============ #
def marcar_li(m):
    return '<li id="li-' + m.group(1) + '"><a href="#' + m.group(1) + '">'
html = re.sub(r'<li><a href="#([a-z0-9-]+)">', marcar_li, html)
html = re.sub(r'(<li id="li-[a-z0-9-]+"><a href="#[a-z0-9-]+">.*?)</li>',
              r'\1<span class="marca"></span></li>', html, flags=re.S)

# ============ 8. Botão marcador + script antes de </body> ============ #
SCRIPT = """<script>
(function(){
  "use strict";
  var CHAVE_PROGRESSO = "despertar_progresso_afirmacoes";
  var CHAVE_FONTE     = "despertar_fonte_afirmacoes";
  var CHAVE_DICAS     = "despertar_dicas_afirmacoes";
  var CHAVE_MARCADOR  = "despertar_marcador_afirmacoes";
  var CHAVE_FITA      = "despertar_fita_afirmacoes";
  var CHAVE_MODO      = "despertar_modo_afirmacoes";

  var NOMES = {
    "abertura": "Sobre este guia",
    "gratidao": "Gratidão",
    "cat-1": "Saúde e Cura",
    "cat-2": "Rejuvenescimento",
    "cat-3": "Paz e Emoções",
    "cat-4": "Prosperidade",
    "cat-5": "Identidade em Cristo",
    "cat-6": "Proteção",
    "cat-7": "Força e Superação",
    "cat-8": "Relacionamentos",
    "oracoes": "Orações do dia",
    "versiculos": "Versículos",
    "como-usar": "Como usar",
    "oracoes-fe": "Orações de Fé",
    "mensagens-dia": "Mensagens de Fé"
  };

  function guardar(chave, valor){ try{ localStorage.setItem(chave, JSON.stringify(valor)); }catch(e){} }
  function ler(chave){ try{ var v = localStorage.getItem(chave); return v ? JSON.parse(v) : null; }catch(e){ return null; } }
  function remover(chave){ try{ localStorage.removeItem(chave); }catch(e){} }

  var baloes = document.getElementById("baloes");
  var capitulos = Array.prototype.slice.call(document.querySelectorAll(".capitulo"));

  /* ============ Balões no topo ============ */
  function mostrarBalao(html, duracao){
    var b = document.createElement("div");
    b.className = "balao";
    b.innerHTML = html + '<button class="fechar" aria-label="Fechar">✕</button>';
    b.querySelector(".fechar").addEventListener("click", function(){ fechar(b); });
    baloes.appendChild(b);
    if(duracao){ setTimeout(function(){ fechar(b); }, duracao); }
    return b;
  }
  function fechar(b){
    if(!b.parentNode) return;
    b.classList.add("saindo");
    setTimeout(function(){ if(b.parentNode) b.parentNode.removeChild(b); }, 300);
  }
  function mostrarDicas(){
    var dicas = [
      { e:"📖", t:"<b>Seu lugar fica salvo.</b> Feche e volte quando quiser; retomamos do ponto exato." },
      { e:"🎗️", t:"Toque em <b>Fita</b> no meio da leitura. A fitinha dourada marca o lugar, como faixa de livro físico." },
      { e:"🔍", t:"Os <b>pontinhos dourados</b> da lateral são as seções. Toque para pular; a atual brilha." },
      { e:"🎨", t:"Use <b>Dia, Sépia e Noite</b> para a tela, e <b>A− / A+</b> para o tamanho das letras." }
    ];
    var vistos = ler(CHAVE_DICAS);
    if(vistos && vistos.v === 1){ return; }
    guardar(CHAVE_DICAS, { v:1 });
    dicas.forEach(function(d, i){
      setTimeout(function(){ mostrarBalao('<span class="emoji">'+d.e+'</span><span class="texto">'+d.t+'</span>', 5200); }, i*3000);
    });
  }
  document.getElementById("btn-dicas").addEventListener("click", function(){
    mostrarBalao('<span class="emoji">📖</span><span class="texto">Dicas: <b>Fita</b> marca um lugar, <b>pontinhos</b> pulam as seções, <b>🎨</b> muda a tela e <b>A−/A+</b> muda as letras. Tudo fica salvo.</span>', 7000);
  });

  /* ============ Trilha de capítulos ============ */
  var trilha = document.getElementById("trilha");
  var pontos = [];
  capitulos.forEach(function(c, i){
    var p = document.createElement("button");
    p.className = "ponto";
    var id = c.id || ("sec" + i);
    p.title = NOMES[id] || "Ir para a seção";
    p.addEventListener("click", function(){
      var topo = c.getBoundingClientRect().top + window.scrollY - 70;
      window.scrollTo({ top: topo, behavior:"smooth" });
    });
    trilha.appendChild(p);
    pontos.push(p);
  });
  function posicionarTrilha(){
    var total = document.documentElement.scrollHeight - window.innerHeight;
    if(total <= 0) return;
    capitulos.forEach(function(c, i){
      var top = c.getBoundingClientRect().top + window.scrollY;
      var pct = Math.min(100, Math.max(0, (top / total) * 100));
      if(pontos[i]){ pontos[i].style.top = pct + "%"; }
    });
  }

  /* ============ Fita dourada ============ */
  var fitaEl = document.getElementById("fita-lateral");
  var fitaAtual = ler(CHAVE_FITA);
  function secaoAtualId(){
    var y = window.scrollY + window.innerHeight * 0.35;
    var idx = 0;
    capitulos.forEach(function(c, i){
      var top = c.getBoundingClientRect().top + window.scrollY;
      if(y >= top){ idx = i; }
    });
    return capitulos[idx].id || ("sec" + idx);
  }
  function atualizarFita(){
    if(fitaAtual && fitaAtual.pct !== undefined){
      fitaEl.style.display = "block";
      fitaEl.style.top = fitaAtual.pct + "%";
      document.getElementById("btn-fita").textContent = "🎗️ Remover fita";
    }else{
      fitaEl.style.display = "none";
      document.getElementById("btn-fita").textContent = "🎗️ Fita";
    }
  }
  document.getElementById("btn-fita").addEventListener("click", function(){
    if(fitaAtual){
      fitaAtual = null; remover(CHAVE_FITA);
      atualizarFita();
      mostrarBalao('<span class="emoji">🎗️</span><span class="texto">Fita removida. Sua leitura continua salva automaticamente.</span>', 3500);
    }else{
      var total = document.documentElement.scrollHeight - window.innerHeight;
      var pct = total > 0 ? Math.round((window.scrollY / total) * 100) : 0;
      var id = secaoAtualId();
      fitaAtual = { pct: pct, titulo: NOMES[id] || id, data: new Date().toISOString() };
      guardar(CHAVE_FITA, fitaAtual);
      atualizarFita();
      mostrarBalao('<span class="emoji">🎗️</span><span class="texto">Fita colocada em <b>' + fitaAtual.titulo + '</b>. Toque na fita dourada da lateral para voltar a este ponto.</span>', 5000);
    }
  });
  fitaEl.addEventListener("click", function(){
    if(fitaAtual){
      var total = document.documentElement.scrollHeight - window.innerHeight;
      window.scrollTo({ top: Math.round((fitaAtual.pct / 100) * total), behavior:"smooth" });
    }
  });

  /* ============ Progresso, estatísticas e sumário ============ */
  var barra = document.getElementById("barra-progresso");
  var stats = document.getElementById("stats-leitura");
  var totalPalavras = 0;
  capitulos.forEach(function(c){
    var txt = c.textContent || "";
    totalPalavras += txt.trim().split(/\\s+/).length;
  });
  var ultimoSalvamento = 0;

  function atualizarProgresso(){
    var total = document.documentElement.scrollHeight - window.innerHeight;
    var p = total > 0 ? Math.round((window.scrollY / total) * 100) : 0;
    p = Math.min(100, Math.max(0, p));
    barra.style.width = p + "%";
    var idAtual = secaoAtualId();
    var idxAtual = 0;
    capitulos.forEach(function(c, i){ if((c.id || ("sec" + i)) === idAtual){ idxAtual = i; } });
    var nomeAtual = NOMES[idAtual] || idAtual;

    capitulos.forEach(function(c, i){
      var top = c.getBoundingClientRect().top + window.scrollY;
      var fim = top + c.offsetHeight;
      var lido = window.scrollY + window.innerHeight >= fim - 30;
      var li = document.getElementById("li-" + (c.id || ("sec" + i)));
      if(li){
        var marca = li.querySelector(".marca");
        if(lido){ li.className = "lido"; if(marca){ marca.textContent = "✓ lido"; } }
        else{ li.className = ""; if(marca){ marca.textContent = ""; } }
      }
    });
    pontos.forEach(function(pt, i){
      pt.classList.remove("atual", "feito");
      if(i < idxAtual){ pt.classList.add("feito"); }
      if(i === idxAtual){ pt.classList.add("atual"); }
    });
    var liAtual = document.getElementById("li-" + idAtual);
    if(liAtual){
      liAtual.className = "aqui";
      var marcaAtual = liAtual.querySelector(".marca");
      if(marcaAtual && !marcaAtual.textContent){ marcaAtual.textContent = "▶ aqui"; }
    }

    var palavrasLidas = Math.round((p / 100) * totalPalavras);
    var restantes = Math.max(0, totalPalavras - palavrasLidas);
    var minRest = Math.max(0, Math.ceil(restantes / 200));
    if(p >= 99){ stats.textContent = "Concluído · 100%"; }
    else if(minRest <= 1){ stats.textContent = nomeAtual + " · " + p + "% · quase no fim"; }
    else{ stats.textContent = nomeAtual + " · " + p + "% · faltam ~" + minRest + " min"; }

    if(p > 98){ remover(CHAVE_PROGRESSO); return; }
    var agora = Date.now();
    if(agora - ultimoSalvamento > 1500){
      ultimoSalvamento = agora;
      guardar(CHAVE_PROGRESSO, {
        secao: idAtual,
        titulo: nomeAtual,
        scrollY: Math.round(window.scrollY),
        porcentagem: p,
        data: new Date().toISOString()
      });
    }
  }
  var rolagemAgendada = false;
  window.addEventListener("scroll", function(){
    if(!rolagemAgendada){
      rolagemAgendada = true;
      setTimeout(function(){ rolagemAgendada = false; atualizarProgresso(); }, 120);
    }
  }, { passive:true });
  window.addEventListener("resize", posicionarTrilha);
  posicionarTrilha();
  atualizarProgresso();

  /* ============ Continuar de onde parou ============ */
  function oferecerContinuacao(){
    var prog = ler(CHAVE_PROGRESSO);
    if(prog && prog.scrollY > 60){
      var b = mostrarBalao(
        '<span class="emoji">📖</span>' +
        '<span class="texto">Você parou em <b>' + prog.titulo + '</b> (posição ' + prog.porcentagem + '%).<br>' +
        '<button class="acao" id="acao-continuar">Continuar de onde parei</button></span>',
        15000
      );
      var botao = b.querySelector("#acao-continuar");
      if(botao){ botao.addEventListener("click", function(){
        window.scrollTo({ top: prog.scrollY, behavior:"smooth" });
        fechar(b);
      }); }
    }
  }

  /* ============ Marcador manual ============ */
  var btnMarcador = document.getElementById("botao-marcador");
  if(btnMarcador){
    btnMarcador.addEventListener("click", function(){
      var id = secaoAtualId();
      guardar(CHAVE_MARCADOR, { scrollY: Math.round(window.scrollY), titulo: NOMES[id] || id, data: new Date().toISOString() });
      mostrarBalao('<span class="emoji">📍</span><span class="texto">Ponto guardado em <b>' + (NOMES[id] || id) + '</b>. Toque de novo para atualizar.</span>', 4000);
      btnMarcador.textContent = "📍 Ponto guardado";
      setTimeout(function(){ btnMarcador.textContent = "📍 Marcar ponto"; }, 2500);
    });
  }

  /* ============ Tamanho das letras ============ */
  var niveis = [90, 100, 112, 125, 140, 160];
  var indice = 1;
  var fonteSalva = ler(CHAVE_FONTE);
  if(fonteSalva && niveis.indexOf(fonteSalva.n) >= 0){ indice = niveis.indexOf(fonteSalva.n); }
  aplicarFonte();
  function aplicarFonte(){
    document.documentElement.style.setProperty("--tamanho-fonte", niveis[indice] + "%");
    guardar(CHAVE_FONTE, { n: niveis[indice] });
    document.getElementById("btn-padrao").classList.toggle("ativo", niveis[indice] === 100);
  }
  document.getElementById("btn-mais").addEventListener("click", function(){
    if(indice < niveis.length - 1){ indice++; aplicarFonte(); }
    else{ mostrarBalao('<span class="emoji">🔍</span><span class="texto">Este é o maior tamanho disponível (160%).</span>', 3000); }
  });
  document.getElementById("btn-menos").addEventListener("click", function(){
    if(indice > 0){ indice--; aplicarFonte(); }
    else{ mostrarBalao('<span class="emoji">🔍</span><span class="texto">Este é o menor tamanho disponível (90%).</span>', 3000); }
  });
  document.getElementById("btn-padrao").addEventListener("click", function(){ indice = 1; aplicarFonte(); });

  /* ============ Modos de tela ============ */
  var modos = ["dia", "sepia", "noite"];
  var nomesModo = { dia:"Dia", sepia:"Sépia", noite:"Noite" };
  var iconesModo = { dia:"🎨", sepia:"🌅", noite:"🌙" };
  var modoAtual = "dia";
  var modoSalvo = ler(CHAVE_MODO);
  if(modoSalvo && modos.indexOf(modoSalvo.m) >= 0){ modoAtual = modoSalvo.m; }
  aplicarModo();
  function aplicarModo(){
    document.body.setAttribute("data-modo", modoAtual);
    guardar(CHAVE_MODO, { m: modoAtual });
    document.getElementById("btn-modo").textContent = iconesModo[modoAtual] + " " + nomesModo[modoAtual];
  }
  document.getElementById("btn-modo").addEventListener("click", function(){
    var idx = modos.indexOf(modoAtual);
    modoAtual = modos[(idx + 1) % modos.length];
    aplicarModo();
    mostrarBalao('<span class="emoji">' + iconesModo[modoAtual] + '</span><span class="texto">Modo de tela: <b>' + nomesModo[modoAtual] + '</b>. Fica salvo para as próximas visitas.</span>', 3500);
  });

  /* ============ Proteção de direitos autorais ============ */
  document.addEventListener("contextmenu", function(e){ e.preventDefault(); });
  document.addEventListener("keydown", function(e){
    if((e.ctrlKey || e.metaKey) && ["c","p","s","u","a"].indexOf(String(e.key).toLowerCase()) >= 0){ e.preventDefault(); }
  });

  /* ============ Início ============ */
  mostrarDicas();
  atualizarFita();
  setTimeout(oferecerContinuacao, 900);
})();
</script>
"""
BOTAO = '\n<button id="botao-marcador" title="Guardar ponto de leitura">📍 Marcar ponto</button>\n'
assert "</body>" in html
html = html.replace("</body>", BOTAO + SCRIPT + "\n</body>", 1)

DEST.write_text(html, encoding="utf-8")
print("Gerado:", DEST)
print("Tamanho original:", len(original), "-> novo:", len(html))
