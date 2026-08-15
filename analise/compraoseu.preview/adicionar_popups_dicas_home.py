#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona os balõezinhos de dicas (pop-ups) na Home do Portal, como os que
aparecem nos livros, despertando curiosidade e levando o visitante até a
biblioteca de leitura.

Aparecem apenas na primeira visita (localStorage), um de cada vez, e cada um
tem o botão "Ver livros" que rola suavemente até a seção #biblioteca.

Aplica em:
  paginas/home_preview.html
  site-contabo/index.html
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]

CSS_POPUPS = """
  /* ===== Balõezinhos de dicas na Home ===== */
  #popup-dicas{position:fixed;top:76px;left:0;right:0;z-index:75;display:flex;flex-direction:column;align-items:center;gap:8px;pointer-events:none;padding:0 14px}
  .pd-balao{
    pointer-events:auto;max-width:480px;width:100%;
    background:#fffdf5;border:1px solid var(--gold);border-left:5px solid var(--gold);
    border-radius:12px;padding:12px 14px;font-size:.88rem;line-height:1.5;
    color:var(--navy);font-family:var(--sans);
    box-shadow:0 14px 34px rgba(14,26,46,.35);
    display:flex;align-items:center;gap:11px;
    animation:pdEntra .4s ease;
  }
  .pd-balao .pd-emoji{font-size:1.3rem;flex-shrink:0}
  .pd-balao .pd-texto{flex:1;min-width:0}
  .pd-balao .pd-texto b{color:var(--gold-dark)}
  .pd-balao .pd-fechar{background:none;border:none;color:var(--muted);font-size:1.1rem;cursor:pointer;line-height:1;padding:4px;flex-shrink:0}
  .pd-balao .pd-fechar:hover{color:var(--gold-dark)}
  .pd-balao .pd-cta{
    background:linear-gradient(135deg,var(--gold-light),var(--gold-dark));color:var(--navy);
    border:none;border-radius:8px;padding:8px 13px;font-size:.78rem;font-weight:700;
    cursor:pointer;font-family:var(--sans);white-space:nowrap;flex-shrink:0;
    box-shadow:0 6px 16px -6px rgba(184,134,11,.6);
  }
  .pd-balao.saindo{animation:pdSai .35s ease forwards}
  @keyframes pdEntra{from{opacity:0;transform:translateY(-16px)}to{opacity:1;transform:translateY(0)}}
  @keyframes pdSai{from{opacity:1;transform:translateY(0)}to{opacity:0;transform:translateY(-12px)}}
  @media (max-width:560px){
    #popup-dicas{top:70px}
    .pd-balao{flex-wrap:wrap}
    .pd-balao .pd-cta{width:100%}
  }
"""

POPUP_DIV = """<div id="popup-dicas" aria-live="polite"></div>
"""

JS_POPUPS = """<script>
(function(){
  "use strict";
  var CHAVE = "despertar_dicas_home";
  try{
    if(localStorage.getItem(CHAVE) === "1"){ return; }
  }catch(e){ return; }
  var dicas = [
    { e:"📖", t:"Agora você pode ler <b>nossos livros online</b> e, ao voltar, continuar exatamente de onde parou." },
    { e:"🎗️", t:"A <b>fita dourada</b> marca o seu lugar na leitura, como a faixa de um livro físico." },
    { e:"🔍", t:"<b>Letras no seu tamanho</b> (A− e A+) e pontinhos dourados que pulam entre os capítulos." },
    { e:"🎨", t:"Tela confortável: <b>Dia, Sépia e Noite</b>, do jeito que faz bem aos seus olhos." }
  ];
  var cont = document.getElementById("popup-dicas");
  if(!cont){ return; }
  function fechar(b){
    if(!b.parentNode){ return; }
    b.classList.add("saindo");
    setTimeout(function(){ if(b.parentNode){ b.parentNode.removeChild(b); } }, 350);
  }
  function mostrar(d, i){
    var b = document.createElement("div");
    b.className = "pd-balao";
    b.innerHTML = '<span class="pd-emoji">' + d.e + '</span>' +
      '<span class="pd-texto">' + d.t + '</span>' +
      '<button class="pd-cta" type="button">Ver livros →</button>' +
      '<button class="pd-fechar" type="button" aria-label="Fechar dica">✕</button>';
    var cta = b.querySelector(".pd-cta");
    var fech = b.querySelector(".pd-fechar");
    cta.addEventListener("click", function(){
      fechar(b);
      var alvo = document.getElementById("biblioteca");
      if(alvo){ alvo.scrollIntoView({ behavior:"smooth", block:"start" }); }
      else{ window.scrollTo({ top: document.body.scrollHeight, behavior:"smooth" }); }
    });
    fech.addEventListener("click", function(){ fechar(b); });
    cont.appendChild(b);
    var t = setTimeout(function(){ fechar(b); }, 7000);
    b.addEventListener("mouseenter", function(){ clearTimeout(t); });
  }
  try{ localStorage.setItem(CHAVE, "1"); }catch(e){}
  dicas.forEach(function(d, i){
    setTimeout(function(){ mostrar(d, i); }, 1600 + i * 3600);
  });
})();
</script>
"""


def aplicar(arquivo):
    html = arquivo.read_text(encoding="utf-8")
    if "popup-dicas" in html:
        print("  (já tem pop-ups, pulando):", arquivo.name)
        return
    # CSS antes de </style>
    assert "</style>" in html
    html = html.replace("</style>", CSS_POPUPS + "\n</style>", 1)
    # Div logo após <body>
    html = html.replace("</head><body>", "</head><body>\n" + POPUP_DIV, 1)
    if "<body>\n" in html and "popup-dicas" not in html.split("</head>")[1][:300]:
        html = html.replace("<body>", "<body>\n" + POPUP_DIV, 1)
    # JS antes de </body>
    assert "</body>" in html
    html = html.replace("</body>", JS_POPUPS + "\n</body>", 1)
    arquivo.write_text(html, encoding="utf-8")
    print("  OK:", arquivo.name)


def main():
    aplicar(RAIZ / "paginas" / "home_preview.html")
    aplicar(RAIZ / "site-contabo" / "index.html")


if __name__ == "__main__":
    main()
    print("Concluído.")
