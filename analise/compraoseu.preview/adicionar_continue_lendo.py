#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona o cartão "Continue lendo" na Home do Portal.

Lê o progresso salvo pelos livros (localStorage despertar_progresso_livroXX)
e mostra um cartão dourado com o livro, a seção e o botão para continuar.

Aplica em:
  paginas/home_preview.html  (links relativos aos previews com leitor)
  site-contabo/index.html    (links /livroXX da produção)
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]

# slug -> título (conforme as páginas publicadas)
TITULOS = {
    "livro01": "O Verbo que Transforma",
    "livro02": "A Sabedoria dos Mestres",
    "livro03": "A Mente Renovada",
    "livro04": "Um Segundo com Deus",
    "livro05": "Evolução da Alma",
    "livro06": "Jesus Quer Falar com Seu Filho",
    "livro07": "O Caminho do Despertar",
    "livro08": "O Arquiteto da Realidade",
    "livro09": "Anestesia Mental",
    "livro10": "O Despertar do Observador",
    "livro11": "O Novo Testamento como nunca lido",
}

CSS = """
  #continue-lendo{max-width:50rem;margin:18px auto 0;padding:0 1.2rem;position:relative;z-index:5}
  .cl-cartao{display:flex;align-items:center;gap:12px;background:linear-gradient(180deg,#fffdf5,#fdf6e3);border:1px solid var(--gold);border-left:5px solid var(--gold);border-radius:12px;padding:8px 10px 8px 16px;color:var(--navy);box-shadow:0 10px 28px rgba(14,26,46,.22);font-family:var(--sans)}
  .cl-cartao:hover{transform:translateY(-1px);box-shadow:0 12px 30px rgba(14,26,46,.28)}
  .cl-cartao-link{display:flex;align-items:center;gap:12px;flex:1;min-width:0;text-decoration:none;color:inherit}
  .cl-icone{font-size:1.4rem;flex-shrink:0}
  .cl-texto{flex:1;min-width:0}
  .cl-titulo{display:block;font-weight:700;font-size:.92rem;margin-bottom:2px}
  .cl-detalhe{display:block;font-size:.78rem;color:var(--muted)}
  .cl-cta{background:linear-gradient(135deg,var(--gold-light),var(--gold-dark));color:var(--navy);font-weight:700;font-size:.8rem;padding:9px 14px;border-radius:8px;white-space:nowrap}
  .cl-fechar{background:none;border:none;color:var(--muted);font-size:1.1rem;cursor:pointer;line-height:1;padding:6px;flex-shrink:0}
  .cl-fechar:hover{color:var(--gold-dark)}
  @media (max-width:560px){.cl-cta{display:none}}
"""

JS_TEMPLATE = """<script>
(function(){
  var MAPA = {
%%ENTRADAS%%  };
  function melhorProgresso(){
    var melhor = null;
    for (var slug in MAPA){
      try{
        var raw = localStorage.getItem("despertar_progresso_" + slug);
        if(!raw){ continue; }
        var p = JSON.parse(raw);
        if(!p || !p.scrollY || p.scrollY <= 60){ continue; }
        if(p.porcentagem >= 99){
          // livro terminado: limpa o progresso e não sugere mais
          try{ localStorage.removeItem("despertar_progresso_" + slug); }catch(e){}
          continue;
        }
        if(!melhor || (p.data || "") > (melhor.data || "")){ melhor = {slug:slug, p:p}; }
      }catch(e){}
    }
    return melhor;
  }
  var fechado = false;
  try{
    var fechouEm = parseInt(localStorage.getItem("despertar_continue_fechado"), 10);
    if(fechouEm && Date.now() - fechouEm < 7 * 24 * 60 * 60 * 1000){
      fechado = true; // fechou há menos de 7 dias: não incomoda de novo
    }
  }catch(e){}
  var m = fechado ? null : melhorProgresso();
  var el = document.getElementById("continue-lendo");
  if(m && el){
    var info = MAPA[m.slug];
    var secao = (m.p.titulo || "a leitura");
    var pct = (m.p.porcentagem || 0);
    el.innerHTML = '<div class="cl-cartao">' +
      '<a class="cl-cartao-link" href="' + info.url + '">' +
      '<span class="cl-icone">📖</span>' +
      '<span class="cl-texto"><span class="cl-titulo">Você estava lendo: ' + info.titulo + '</span>' +
      '<span class="cl-detalhe">' + secao + ' · posição ' + pct + '% · continue sem se perder</span></span>' +
      '<span class="cl-cta">Continuar lendo →</span></a>' +
      '<button class="cl-fechar" id="cl-fechar" aria-label="Fechar sugestão" title="Fechar">✕</button></div>';
    var fechar = document.getElementById("cl-fechar");
    if(fechar){
      fechar.addEventListener("click", function(){
        var c = document.getElementById("continue-lendo");
        if(c){ c.style.display = "none"; }
        // Fechar esconde por 7 dias; depois volta a sugerir (a menos que o
        // livro esteja terminado). Assim o leitor não é incomodado agora,
        // mas também não perde a lembrança para sempre.
        try{ localStorage.setItem("despertar_continue_fechado", String(Date.now())); }catch(e){}
      });
    }
  }
})();
</script>
"""


def aplicar(arquivo, url_fmt):
    html = arquivo.read_text(encoding="utf-8")
    if "continue-lendo" in html:
        print("  (já tem o cartão, pulando):", arquivo.name)
        return
    # 1. CSS + div antes do portal
    bloco = "<style>" + CSS + "</style>\n<div id=\"continue-lendo\"></div>\n\n"
    assert '<section id="portal">' in html, "portal não encontrado em " + arquivo.name
    html = html.replace('<section id="portal">', bloco + '<section id="portal">', 1)
    # 2. JS antes de </body>
    # slug já é "livroXX"; o formato deve receber só o número (ex.: "05")
    entradas = "".join('    %s:{url:"%s",titulo:"%s"},\n' % (slug, url_fmt % slug[5:], TITULOS[slug]) for slug in TITULOS)
    js = JS_TEMPLATE.replace("%%ENTRADAS%%", entradas)
    assert "</body>" in html, "sem </body> em " + arquivo.name
    html = html.replace("</body>", js + "</body>", 1)
    arquivo.write_text(html, encoding="utf-8")
    print("  OK:", arquivo.name)


def main():
    aplicar(RAIZ / "paginas" / "home_preview.html", "livro%s_leitor_preview.html")
    aplicar(RAIZ / "site-contabo" / "index.html", "/livro%s")


if __name__ == "__main__":
    main()
    print("Concluído.")
