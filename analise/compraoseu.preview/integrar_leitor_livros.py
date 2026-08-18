#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integra o Leitor do Despertar em todos os livros do Portal.

Modo de uso:
  python3 integrar_leitor_livros.py

Gera (previews, novos arquivos) e atualiza (site-contabo, no lugar):
  paginas/livro01..10_leitor_preview.html   (protegidos, como no site)
  paginas/livro11_leitor_preview.html       (sem proteção, versão do autor)
  site-contabo/livro01..11.html             (páginas publicadas, no lugar)

Recursos: lembrar onde parou, fita dourada, trilha de seções, A-/A/A+,
modos Dia/Sépia/Noite, balões de dicas, sumário com marcas, barra de
progresso e estatística de leitura. Proteção condicional por arquivo.
"""
import re
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]

CSS_LEITOR = """
  /* ===== Leitor do Despertar ===== */
  :root{--tamanho-fonte:100%}
  body{font-size:var(--tamanho-fonte)}
  body[data-modo="sepia"]{--fundo-leitura:#f1e6cd; --card-leitura:#faf3e0; --tinta-leitura:#4a3a20; --titulo-leitura:#3a2d15; --linha-leitura:#d8c69d; --destaque:#f6ecd2}
  body[data-modo="noite"]{--fundo-leitura:#0d1520; --card-leitura:#17202f; --tinta-leitura:#c9d4e3; --titulo-leitura:#e3c877; --linha-leitura:#2a3a52; --destaque:#1c2940}
  body[data-modo="sepia"] .leitura{background:var(--fundo-leitura); color:var(--tinta-leitura)}
  body[data-modo="sepia"] .leitura .wrap{background:var(--card-leitura); border-color:var(--linha-leitura)}
  body[data-modo="sepia"] .cap-titulo{color:var(--titulo-leitura)}
  body[data-modo="sepia"] .afirmacao, body[data-modo="sepia"] .box.versiculo{background:var(--destaque)}
  body[data-modo="noite"] .leitura{background:var(--fundo-leitura); color:var(--tinta-leitura)}
  body[data-modo="noite"] .leitura .wrap{background:var(--card-leitura); border-color:var(--linha-leitura)}
  body[data-modo="noite"] .cap-titulo{color:var(--titulo-leitura)}
  body[data-modo="noite"] .cap-num{color:#c9a24b}
  body[data-modo="noite"] .afirmacao, body[data-modo="noite"] .box.versiculo, body[data-modo="noite"] .box{background:var(--destaque)}
  body[data-modo="noite"] .ref{color:var(--ouro-claro)}
  body[data-modo="noite"] .cap-nav a{color:#9fb0c9}
  body[data-modo="noite"] .cap-nav a:hover{color:var(--ouro-claro)}
  body[data-modo="noite"] .faq-item{background:var(--fundo-leitura); border-color:var(--linha-leitura)}
  body[data-modo="noite"] .faq-q{background:var(--destaque); color:var(--titulo-leitura)}
  body[data-modo="noite"] .faq-a{background:var(--card-leitura); color:var(--tinta-leitura)}
  #barra-progresso{
    position:fixed; top:0; left:0; height:4px; width:0%;
    background:linear-gradient(90deg,#c9a24b,#e3c877);
    z-index:100; border-radius:0 3px 3px 0; transition:width .15s linear;
  }
  .topbar .wrap{flex-wrap:wrap; gap:6px}
  .linha1{display:flex; align-items:center; justify-content:space-between; gap:10px; width:100%}
  #stats-leitura{color:var(--ouro-claro); font-size:.7rem; letter-spacing:.05em; font-family:system-ui,sans-serif; white-space:nowrap; text-align:right}
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
  @media (max-width:560px){
    .controles button{min-width:30px; padding:0 6px}
    #trilha{right:3px}
    #stats-leitura{font-size:.62rem}
    #baloes .balao{width:94%}
  }
"""

CSS_PROTECAO = """
  @media print{
    body::before{
      content:"Livro protegido. A impressão não está disponível nesta obra. Obrigado pela compreensão.";
      display:block; position:fixed; inset:0; background:#fff; color:#333;
      font-size:18px; text-align:center; padding-top:40vh; z-index:9999;
    }
    .topbar,.capa,#sumario,.leitura,#fim,footer,#baloes,#trilha,#fita-lateral,#botao-marcador,#barra-progresso{display:none !important}
  }
"""

# %CHAVE% é substituído pelo slug do livro (ex.: livro05)
SCRIPT = """<script>
(function(){
  "use strict";
  var CHAVE_PROGRESSO = "despertar_progresso_%CHAVE%";
  var CHAVE_FONTE     = "despertar_fonte_%CHAVE%";
  var CHAVE_DICAS     = "despertar_dicas_%CHAVE%";
  var CHAVE_MARCADOR  = "despertar_marcador_%CHAVE%";
  var CHAVE_FITA      = "despertar_fita_%CHAVE%";
  var CHAVE_MODO      = "despertar_modo_%CHAVE%";

  function guardar(chave, valor){ try{ localStorage.setItem(chave, JSON.stringify(valor)); }catch(e){} }
  function ler(chave){ try{ var v = localStorage.getItem(chave); return v ? JSON.parse(v) : null; }catch(e){ return null; } }
  function remover(chave){ try{ localStorage.removeItem(chave); }catch(e){} }

  var baloes = document.getElementById("baloes");
  var capitulos = Array.prototype.slice.call(document.querySelectorAll(".capitulo, .mandamento"));
  var NOMES = {};
  capitulos.forEach(function(c, i){
    var t = c.querySelector(".cap-titulo") || c.querySelector(".mand-titulo");
    var nome = t ? t.textContent.trim() : (c.id || ("secao" + i));
    NOMES[c.id || ("sec" + i)] = nome;
  });

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
%PROTECAO_JS%
  /* ============ Início ============ */
  mostrarDicas();
  atualizarFita();
  setTimeout(oferecerContinuacao, 900);
})();
</script>
"""

PROTECAO_JS = """
  /* ============ Proteção de direitos autorais ============ */
  document.addEventListener("contextmenu", function(e){ e.preventDefault(); });
  document.addEventListener("keydown", function(e){
    if((e.ctrlKey || e.metaKey) && ["c","p","s","u","a"].indexOf(String(e.key).toLowerCase()) >= 0){ e.preventDefault(); }
  });
"""

TOPBAR_NOVO = """<header class="topbar">
  <div class="wrap">
    <div class="linha1">
      %LOGO%
      <span id="stats-leitura">Início da leitura</span>
    </div>
    <div class="controles">
      <button id="btn-menos" title="Diminuir letras">A−</button>
      <button id="btn-padrao" title="Tamanho original" class="ativo">A</button>
      <button id="btn-mais" title="Aumentar letras">A+</button>
      <span class="sep"></span>
      <button id="btn-fita" title="Colocar ou remover a fita dourada">🎗️ Fita</button>
      <button id="btn-modo" title="Mudar a cor da tela (Dia, Sépia, Noite)">🎨 Dia</button>
      <button id="btn-dicas" title="Ver dicas de leitura">💡</button>
    </div>
  </div>
</header>"""


def aplicar(origem, destino, slug, proteger, sobrescrever=False):
    html = origem.read_text(encoding="utf-8")
    if "despertar_progresso_" in html:
        print("  (já tem leitor, pulando):", origem.name)
        return

    # 1. CSS do leitor (+ proteção de impressão)
    css = CSS_LEITOR + (CSS_PROTECAO if proteger else "")
    assert "</style>" in html, "sem </style> em " + origem.name
    html = html.replace("</style>", css + "\n</style>", 1)

    # 2. id="capa" na capa
    html = html.replace('<section class="capa">', '<section class="capa" id="capa">', 1)

    # 3. Topbar com controles (preserva o logo original)
    m = re.search(r'<header class="topbar">\s*<div class="wrap">(.*?)</div>\s*</header>', html, re.S)
    if m:
        logo = re.search(r'<a class="logo"[^>]*>.*?</a>', m.group(1), re.S)
        logo_html = logo.group(0) if logo else '<a class="logo" href="#">Missão <span>com Deus</span></a>'
        novo = TOPBAR_NOVO.replace("%LOGO%", logo_html)
        html = html.replace(m.group(0), novo, 1)

    # 4. body com data-modo + barra de progresso
    html = re.sub(r'(<body[^>]*>)', r'\1\n<div id="barra-progresso"></div>', html, count=1)
    if 'data-modo=' not in html.split("</head>")[1][:200]:
        html = html.replace("<body", '<body data-modo="dia"', 1)

    # 5. Balões, trilha e fita após o topbar
    html = html.replace("</header>",
                        "</header>\n\n<div id=\"baloes\"></div>\n<div id=\"trilha\"></div>\n<div id=\"fita-lateral\"></div>", 1)

    # 6. ids nas li do sumário + span de marca de leitura
    def _marca_li(m):
        return '<li id="li-' + m.group(1) + '"><a href="#' + m.group(1) + '">'
    html = re.sub(r'<li><a href="#([a-z0-9-]+)">', _marca_li, html)
    html = re.sub(r'(<li id="li-[a-z0-9-]+"><a href="#[a-z0-9-]+">.*?)</li>',
                  r'\1<span class="marca"></span></li>', html, flags=re.S)

    # 7. Botão marcador + script do leitor
    script = SCRIPT.replace("%CHAVE%", slug).replace("%PROTECAO_JS%", PROTECAO_JS if proteger else "")
    bloco = '\n<button id="botao-marcador" title="Guardar ponto de leitura">📍 Marcar ponto</button>\n' + script + '\n'
    assert "</body>" in html, "sem </body> em " + origem.name
    html = html.replace("</body>", bloco + "\n</body>", 1)

    destino.write_text(html, encoding="utf-8")
    print("  OK:", origem.name, "->", destino.name or "(no lugar)", "| proteger:", proteger)


def main():
    trabalhos = []
    # Previews: gerar novos arquivos _leitor_preview
    for i in range(1, 11):
        n = f"livro{i:02d}"
        origem = RAIZ / "paginas" / f"{n}_preview.html"
        destino = RAIZ / "paginas" / f"{n}_leitor_preview.html"
        if origem.exists():
            trabalhos.append((origem, destino, n, True))
    # Livro 11: versão do autor (sem proteção)
    origem11 = RAIZ / "paginas" / "livro11_preview.html"
    destino11 = RAIZ / "paginas" / "livro11_leitor_preview.html"
    if origem11.exists():
        trabalhos.append((origem11, destino11, "livro11", False))
    # site-contabo: atualizar no lugar
    for i in range(1, 12):
        n = f"livro{i:02d}"
        arquivo = RAIZ / "site-contabo" / f"{n}.html"
        if arquivo.exists():
            proteger = i < 11  # livro11 ainda é versão do autor em avaliação
            trabalhos.append((arquivo, arquivo, n, proteger))

    # Página de Estudos EU SOU: gerar versão com leitor (sem proteção, do autor)
    eusou = RAIZ / "paginas" / "eusou_estudos_preview.html"
    eusou_dest = RAIZ / "paginas" / "eusou_estudos_leitor_preview.html"
    if eusou.exists():
        trabalhos.append((eusou, eusou_dest, "eusou_estudos", False))

    for origem, destino, slug, proteger in trabalhos:
        aplicar(origem, destino, slug, proteger)


if __name__ == "__main__":
    main()
    print("Concluído.")
