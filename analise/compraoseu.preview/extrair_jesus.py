# -*- coding: utf-8 -*-
"""
Extrai "Jesus Quer Falar Com Seu Filho Vol.01" (PDF infantil) para texto estruturado.
Estrutura: Apresentação + Introdução + Jesus te ama + Oração + 10 Mandamentos +
Atividades + Oração Final + Dedicatória.
"""
import re, json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "livro" / "E-book - Jesus Quer Falar Com Seu Filho Vol.01.pdf"
OUT_JSON = HERE / "jesus_dados.json"

import pymupdf

TITULOS_MAND = {
    1: "Ame a Deus sobre todas as coisas",
    2: "Adore somente a Deus",
    3: "Fale o nome de Deus com respeito e amor",
    4: "Guarde o dia de descanso para Deus",
    5: "Honre seu pai e sua mãe",
    6: "Não machuque ninguém",
    7: "Seja fiel, verdadeiro e respeite as pessoas",
    8: "Não pegue nada que não é seu",
    9: "Não minta nem fale mal dos outros",
    10: "Não deseje o que é dos outros",
}

def limpar(t):
    t = t.replace('\u001f', ' ')
    t = re.sub(r'[<>=]', '"', t)
    return t

def main():
    doc = pymupdf.open(SRC)
    paginas = [limpar(doc[i].get_text()) for i in range(len(doc))]
    print(f"PDF: {len(doc)} páginas")

    # ---- Apresentação (págs 1-11) ----
    apresentacao = "\n\n".join(p.strip() for p in paginas[1:11] if p.strip())

    # ---- Corpo: Jesus te ama + Oração + Mandamentos (págs 12-27) ----
    corpo = []
    # páginas 12-16 (introdução + oração)
    for pg in range(11, 17):
        if paginas[pg].strip():
            corpo.append(paginas[pg])

    # Mandamentos (págs 18-27)
    mandamentos = []
    for pg in range(17, 27):
        texto = paginas[pg].strip()
        if texto:
            mandamentos.append(texto)

    # ---- Atividades (págs 28-33) ----
    atividades = "\n\n".join(p.strip() for p in paginas[27:33] if p.strip() and len(p.strip()) > 40)

    # ---- Final (págs 34-37) ----
    final = "\n\n".join(p.strip() for p in paginas[33:37] if p.strip())

    dados = {
        "titulo": "Jesus Quer Falar com Seu Filho",
        "subtitulo": "Vol. 01 — Uma obra infantil cristã de amor, fé e ensinamentos bíblicos",
        "apresentacao": apresentacao,
        "corpo": corpo,
        "mandamentos": mandamentos,
        "atividades": atividades,
        "final": final,
    }
    OUT_JSON.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"Apresentação: {len(apresentacao)} chars")
    print(f"Corpo: {len(corpo)} blocos")
    print(f"Mandamentos: {len(mandamentos)}")
    print(f"Atividades: {len(atividades)} chars")
    print(f"Final: {len(final)} chars")
    print(f"JSON: {OUT_JSON}")

if __name__ == "__main__":
    main()
