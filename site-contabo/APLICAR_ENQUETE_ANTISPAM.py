# -*- coding: utf-8 -*-
"""Anti-spam da enquete. Voto segue. Comentario lixo nao grava.

  cd /www/wwwroot/missaocomdeus.com.br
  python3 APLICAR_ENQUETE_ANTISPAM.py
"""
import os, json, re

SITE = "/www/wwwroot/missaocomdeus.com.br"
PHP = os.path.join(SITE, "enquete.php")
JSONF = os.path.join(SITE, "enquete_dados.json")

FN = r'''
function comentario_e_lixo($t) {
    $t = trim($t);
    if ($t === '') return false;
    if (strpos($t, ' ') === false && preg_match('/^[A-Za-z0-9]{10,}$/', $t)) {
        return true;
    }
    $vogais = @preg_match_all('/[aeiouAEIOUáéíóúàâêôãõÁÉÍÓÚ]/u', $t);
    if ($vogais === false) { $vogais = 0; }
    if (strlen($t) >= 12 && strpos($t, ' ') === false && $vogais < 3) {
        return true;
    }
    return false;
}

'''


def lixo_py(t):
    t = (t or "").strip()
    if not t:
        return False
    if " " not in t and re.match(r"^[A-Za-z0-9]{10,}$", t):
        return True
    vog = len(re.findall(r"[aeiouAEIOUáéíóúàâêôãõÁÉÍÓÚ]", t))
    if len(t) >= 12 and " " not in t and vog < 3:
        return True
    return False


def main():
    t = open(PHP, encoding="utf-8").read()
    if "function comentario_e_lixo" not in t:
        t = t.replace("function resultado_json", FN + "function resultado_json", 1)
        print("OK funcao lixo")
    else:
        print("funcao lixo ja estava")

    if "comentario_e_lixo($comentario)" not in t:
        t = t.replace(
            "if ($comentario !== '') {\n        $novo['comentarios']",
            "if ($comentario !== '' && comentario_e_lixo($comentario)) { $comentario = ''; }\n    if ($comentario !== '') {\n        $novo['comentarios']",
            1,
        )
        print("OK filtro no save")
    else:
        print("filtro save ja estava")

    open(PHP, "w", encoding="utf-8").write(t)

    if os.path.isfile(JSONF):
        d = json.load(open(JSONF, encoding="utf-8"))
        com = d.get("comentarios") or []
        antes = len(com)
        d["comentarios"] = [c for c in com if not lixo_py((c or {}).get("texto", ""))]
        json.dump(d, open(JSONF, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        try:
            os.chmod(JSONF, 0o664)
        except Exception:
            pass
        print("comentarios:", antes, "->", len(d["comentarios"]))
    print("Pronto. Irmão vota e escreve. Robô de letras nao grava.")


if __name__ == "__main__":
    main()
