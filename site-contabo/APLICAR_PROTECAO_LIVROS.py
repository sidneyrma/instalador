#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Protege a leitura dos livros: selecionar sim, copiar e imprimir nao.
Nao troca o miolo. Nao mexe na Home, Palavra, Guardar nem Black Friday.
Nao promete travar print de tela (o aparelho nao deixa o site fazer isso).

  cd /www/wwwroot/missaocomdeus.com.br
  python3 APLICAR_PROTECAO_LIVROS.py

Digite o nome. Nao clique se o Terminal mostrar colchete azul.
"""
import datetime
import re
import shutil
from pathlib import Path

SITE = Path("/www/wwwroot/missaocomdeus.com.br")
STAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
MARCA = 'id="js-protecao-leitura-missao"'
LIVROS = [
    "livro04.html",
    "livro05.html",
    "livro06.html",
    "livro07.html",
    "livro08.html",
    "livro09.html",
    "livro11.html",
    "livro12.html",
    "livro13.html",
]


def nome_obra(html, arquivo):
    m = re.search(r"<title>([^<]+)</title>", html, re.I)
    if m:
        n = m.group(1).split("|")[0].split("·")[0].strip()
        n = re.sub(r", Leitura Online.*", "", n, flags=re.I)
        n = re.sub(r": Leitura Online.*", "", n, flags=re.I)
        return n[:80]
    return arquivo.replace(".html", "")


def bloco(nome):
    nome_js = nome.replace("\\", "\\\\").replace("'", "\\'")
    return f"""
<style id="css-protecao-leitura-missao">
html,body{{-webkit-user-select:text !important;-moz-user-select:text !important;user-select:text !important}}
@media print{{
  body *{{visibility:hidden !important}}
  #print-block,#print-block *{{visibility:visible !important}}
  #print-block{{display:block !important;position:absolute;left:0;top:0;width:100%}}
}}
</style>
<script id="js-protecao-leitura-missao">
(function(){{
  var aviso = "© Coleção Missão com Deus. {nome_js}. Todos os direitos reservados. Leitura online em missaocomdeus.com.br";
  function trava(e){{
    e.preventDefault();
    if (e.clipboardData) e.clipboardData.setData("text/plain", aviso);
    return false;
  }}
  document.addEventListener("copy", trava, true);
  document.addEventListener("cut", trava, true);
  document.addEventListener("contextmenu", function(e){{ e.preventDefault(); }}, true);
  document.addEventListener("dragstart", function(e){{ e.preventDefault(); }}, true);
  document.addEventListener("keydown", function(e){{
    var k = String(e.key || "").toLowerCase();
    if ((e.ctrlKey || e.metaKey) && (k === "c" || k === "x" || k === "p" || k === "s" || k === "u")) {{
      e.preventDefault();
    }}
  }}, true);
}})();
</script>
"""


def print_block(nome):
    return (
        '<div id="print-block">'
        f"<h1>{nome}</h1>"
        "<p>Impressão desabilitada para proteger os direitos autorais desta obra.</p>"
        "<p>© Coleção Missão com Deus. Leitura online em missaocomdeus.com.br</p>"
        "</div>\n"
    )


def main():
    print("Arquivo: APLICAR_PROTECAO_LIVROS.py  (sem colchete)")
    if not SITE.exists():
        print("Pasta do site nao achei. Nao gravei.")
        return
    ok = 0
    pulou = 0
    for nome in LIVROS:
        arq = SITE / nome
        if not arq.exists():
            print("AVISO  nao achei", nome)
            continue
        t = arq.read_text(encoding="utf-8", errors="replace")
        if MARCA in t:
            print("Ja estava ", nome)
            pulou += 1
            continue
        if "</body>" not in t:
            print("Nao achei </body> em", nome, ". Nao gravei este.")
            continue
        obra = nome_obra(t, nome)
        extra = ""
        if 'id="print-block"' not in t and "id='print-block'" not in t:
            extra = print_block(obra)
        t2 = t.replace("</body>", extra + bloco(obra) + "</body>", 1)
        if t2 == t:
            print("Nada mudou em", nome, ". Nao gravei este.")
            continue
        bak = arq.with_name(arq.stem + "-antes-protecao-" + STAMP + arq.suffix)
        shutil.copy2(arq, bak)
        arq.write_text(t2, encoding="utf-8")
        print("OK ", nome, "| backup", bak.name)
        ok += 1
    print("Fim. Gravados:", ok, "| ja estavam:", pulou)
    print("Selecionar continua. Copiar e imprimir nao levam o texto. Print de tela o site nao trava.")


if __name__ == "__main__":
    main()
