# -*- coding: utf-8 -*-
"""
Protege TODOS os livro01..12.html (inclui Devocional e Jesus).
Selecionar sim. Copiar, colar, imprimir, botao direito nao.
NAO mexe nos PDF (Devocional e Jesus em ebooks continuam abertos no quiz).

  cd /www/wwwroot/missaocomdeus.com.br
  python3 APLICAR_PROTECAO_TODOS_LIVROS.py
"""
import os, glob, re

SITE = "/www/wwwroot/missaocomdeus.com.br"
JS = r"""
<script>
(function(){
  document.addEventListener('copy', function(e){ e.preventDefault(); });
  document.addEventListener('cut', function(e){ e.preventDefault(); });
  document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
  document.addEventListener('keydown', function(e){
    var k = (e.key||'').toLowerCase();
    if((e.ctrlKey||e.metaKey) && (k==='p'||k==='s'||k==='u')) e.preventDefault();
  });
})();
</script>
"""


def main():
    n = 0
    for path in sorted(glob.glob(os.path.join(SITE, "livro*.html"))):
        nome = os.path.basename(path)
        if "antes" in nome or nome.endswith(".bak"):
            continue
        t = open(path, encoding="utf-8", errors="ignore").read()
        orig = t
        t = t.replace(
            "-webkit-user-select:none; -moz-user-select:none; -ms-user-select:none; user-select:none;",
            "-webkit-user-select:text; -moz-user-select:text; -ms-user-select:text; user-select:text;",
        )
        t = re.sub(r"user-select\s*:\s*none", "user-select:text", t, flags=re.I)
        if "document.addEventListener('copy'" not in t:
            if "</body>" in t:
                t = t.replace("</body>", JS + "\n</body>", 1)
            else:
                t += JS
        if t != orig:
            open(path, "w", encoding="utf-8").write(t)
            n += 1
            print("OK", nome)
        else:
            print("ja estava", nome)
    print("Alterados:", n)
    print("HTML: marcar sim, copiar/imprimir nao. PDF do quiz (Devocional e Jesus) nao mexi.")


if __name__ == "__main__":
    main()
