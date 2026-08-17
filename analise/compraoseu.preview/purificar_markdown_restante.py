#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purifica resquícios de markdown no conteúdo dos livros, convertendo-os para
destaque HTML limpo (negrito), conforme pedido do autor:

  "#### O Que Observar Hoje"  ->  <strong>O Que Observar Hoje</strong>

PROTEÇÃO: blocos <script> e <style> (e o JSON-LD) são preservados intactos.
As regras são aplicadas apenas em TEXTO PURO fora de tags HTML:

  1. #{1,6} Titulo  ->  <strong>Titulo</strong>
  2. **texto**      ->  <strong>texto</strong>
  3. __texto__      ->  <strong>texto</strong>
  4. *texto*        ->  <em>texto</em>  (apenas pares simples seguros)

Uso: python3 purificar_markdown_restante.py
"""
import re
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]

ARQUIVOS = []
for n in range(1, 12):
    nome = f"livro{n:02d}"
    ARQUIVOS += [f"paginas/{nome}_preview.html", f"paginas/{nome}_leitor_preview.html",
                 f"site-contabo/{nome}.html"]
ARQUIVOS += ["paginas/livro12_preview.html", "paginas/livro12_leitor_preview.html",
             "paginas/eusou_estudos_preview.html", "paginas/eusou_estudos_leitor_preview.html",
             "paginas/home_preview.html", "site-contabo/index.html"]

# Blocos protegidos: script (qualquer tipo) e style
RE_BLOCO = re.compile(r'<script(?:\s[^>]*)?>.*?</script>|<style>.*?</style>', re.S)

# Itálico seguro: *texto* sem * interno, sem espaço nas bordas, sem alfanumérico colado
RE_ITALICO = re.compile(r'(?<![A-Za-z0-9*])\*([^*\n]{2,}?)\*(?![A-Za-z0-9*])')


def limpar_texto(texto):
    """Converte markdown em texto puro para HTML de destaque."""
    texto = re.sub(r'#{1,6}\s+(.+)', r'<strong>\1</strong>', texto)
    texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)
    texto = re.sub(r'__(.+?)__', r'<strong>\1</strong>', texto)
    texto = RE_ITALICO.sub(r'<em>\1</em>', texto)
    return texto


def purificar_html(html):
    """Aplica limpeza apenas em texto puro; script/style ficam intactos."""
    blocos = []

    def guarda(m):
        blocos.append(m.group(0))
        return f"@@BLOCO{len(blocos) - 1}@@"

    html = RE_BLOCO.sub(guarda, html)
    partes = re.split(r'(<[^>]+>)', html)
    for i, parte in enumerate(partes):
        if parte.startswith("<"):
            continue  # tag HTML: preserva
        partes[i] = limpar_texto(parte)
    html = "".join(partes)
    for idx, b in enumerate(blocos):
        html = html.replace(f"@@BLOCO{idx}@@", b)
    return html


def main():
    mudou = 0
    for rel in ARQUIVOS:
        f = RAIZ / rel
        if not f.exists():
            continue
        html = f.read_text(encoding="utf-8")
        novo = purificar_html(html)
        if novo != html:
            f.write_text(novo, encoding="utf-8")
            print("PURIFICADO:", rel)
            mudou += 1
    print(f"\nArquivos alterados: {mudou}")


if __name__ == "__main__":
    main()
    print("Concluído.")
