#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purifica os livros 03, 07 e 10: remove travessões (—), asteriscos (*),
reticências (…) e setas (→) do CONTEÚDO, mantendo a pontuação suave
(vírgulas, dois-pontos, parênteses) e preservando:
  - a navegação HTML (← Anterior | Próximo →)
  - o JavaScript do Leitor do Despertar
  - o JSON-LD (dados estruturados) — também purificado

Regras:
  1. " — NomeLivro cap:vers" (referência bíblica)  ->  " (NomeLivro cap:vers)"
  2. "CAPÍTULO N — X" / "PARTE I — X" / "APRESENTAÇÃO — X" / etc. -> "CAPÍTULO N: X"
  3. Títulos de capa/JSON com o nome do livro     ->  "Título: Subtítulo"
  4. "Missão com Deus — ..."                       ->  "Missão com Deus · ..."
  5. "© Coleção do Despertar — Todos os direitos reservados" -> "© Coleção do Despertar. Todos os direitos reservados"
  6. Fallback " — " em prosa                       ->  ", "
  7. "**texto**" (markdown)                        ->  "<strong>texto</strong>"

Uso: python3 purificar_livros_03_07_10.py
"""
import re
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]

ARQUIVOS = [
    "paginas/livro03_preview.html",
    "paginas/livro07_preview.html",
    "paginas/livro10_preview.html",
    "paginas/livro03_leitor_preview.html",
    "paginas/livro07_leitor_preview.html",
    "paginas/livro10_leitor_preview.html",
    "site-contabo/livro03.html",
    "site-contabo/livro07.html",
    "site-contabo/livro10.html",
]

# Títulos de capa/JSON por livro (travessão -> dois-pontos)
TITULOS_CAPA = [
    ("A Mente Renovada — O Pensar com Cristo que Transforma a Vida",
     "A Mente Renovada: O Pensar com Cristo que Transforma a Vida"),
    ("O Caminho do Despertar — A Jornada Solitária da Alma",
     "O Caminho do Despertar: A Jornada Solitária da Alma"),
    ("O Despertar do Observador — As Leis Invisíveis que Moldam a Realidade",
     "O Despertar do Observador: As Leis Invisíveis que Moldam a Realidade"),
]

# Referência bíblica: " — Nome cap:vers" (opcional 1/2/3 antes do nome)
RE_REF = re.compile(r'"\s*—\s*((?:1|2|3)\s*)?([A-Za-zÁÉÍÓÚÂÊÔÃÕÇ][A-Za-zÁÉÍÓÚÂÊÔÃÕÇ]*)\s*(\d+):(\d+)(?:-(\d+))?')

def sub_ref(m):
    num = (m.group(1) or "").strip()
    nome = m.group(2)
    cap, ver = m.group(3), m.group(4)
    fim = "-" + m.group(5) if m.group(5) else ""
    ref = (num + " " if num else "") + nome + " " + cap + ":" + ver + fim
    return '" (' + ref + ')'

# Títulos de seções: "CAPÍTULO 1 — X" -> "CAPÍTULO 1: X"
RE_TITULO = re.compile(r'\b(CAPÍTULO\s+\d+|Capítulo\s+\d+|PARTE\s+[IVX]+|APRESENTAÇÃO|EPÍLOGO|PRÓLOGO|BÔNUS)\s*—\s*')
def sub_titulo(m):
    return m.group(1) + ": "

# Fallback de prosa: " — " -> ", "
def sub_prosa(texto):
    return texto.replace(" — ", ", ")

def purificar_texto(texto):
    """Aplica as regras de texto (usado no corpo HTML e no JSON-LD)."""
    for antigo, novo in TITULOS_CAPA:
        texto = texto.replace(antigo, novo)
    texto = texto.replace("Missão com Deus — Coleção do Despertar", "Missão com Deus · Coleção do Despertar")
    texto = texto.replace("Missão com Deus — CompraOSeu", "Missão com Deus · CompraOSeu")
    texto = texto.replace("© Coleção do Despertar — Todos os direitos reservados",
                          "© Coleção do Despertar. Todos os direitos reservados")
    texto = RE_REF.sub(sub_ref, texto)
    texto = RE_TITULO.sub(sub_titulo, texto)
    texto = sub_prosa(texto)
    texto = texto.replace("…", ".")
    # marcação markdown **texto** -> <strong>texto</strong> (apenas no corpo)
    texto = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', texto)
    return texto

def purificar_html(html):
    """Purifica o HTML preservando <script> (JS) e <style>, mas purificando o JSON-LD."""
    partes = []
    pos = 0
    for m in re.finditer(r'<script(?:\s[^>]*)?>.*?</script>|<style>.*?</style>', html, re.S):
        partes.append(purificar_texto(html[pos:m.start()]))
        bloco = m.group(0)
        if 'application/ld+json' in bloco:
            # purifica o conteúdo JSON (mantém as tags <script ...> ... </script>)
            interno = re.sub(r'^<script[^>]*>(.*)</script>$', r'\1', bloco, flags=re.S)
            bloco = re.sub(r'^(<script[^>]*>)(.*)(</script>)$',
                           lambda mm: mm.group(1) + purificar_texto(mm.group(2)) + mm.group(3),
                           bloco, flags=re.S)
        partes.append(bloco)
        pos = m.end()
    partes.append(purificar_texto(html[pos:]))
    return "".join(partes)

def main():
    for rel in ARQUIVOS:
        f = RAIZ / rel
        html = f.read_text(encoding="utf-8")
        novo = purificar_html(html)
        if novo != html:
            f.write_text(novo, encoding="utf-8")
            print("PURIFICADO:", rel)
        else:
            print("sem mudanças:", rel)

if __name__ == "__main__":
    main()
    print("Concluído.")
