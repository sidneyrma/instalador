# -*- coding: utf-8 -*-
"""
Extrai o "Devocional Um Segundo com Deus Vol.01" (PDF) para texto estruturado.
Estrutura: Apresentação + 30 dias (Versículo, Mensagem, Oração, Prece, Obra) + Encerramento.
Estratégia robusta: processa página por página, junta títulos quebrados e
extrai cada seção com regex flexível.
"""
import re, json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "livro" / "E-book Devocional Um Segundo com Deus Vol.01.pdf"
OUT_JSON = HERE / "devocional_dados.json"

import pymupdf

def main():
    doc = pymupdf.open(SRC)
    paginas = [doc[i].get_text() for i in range(len(doc))]

    # ---- Apresentação (págs 1-8) ----
    apresentacao = "\n\n".join(p.strip() for p in paginas[:8] if p.strip())

    # ---- Dias (págs 9-38) ----
    dias = []
    dia_atual = None
    # percorre as páginas dos dias
    for pg_idx in range(8, 38):
        texto = paginas[pg_idx]
        linhas = [l.strip() for l in texto.split('\n') if l.strip()]

        # detecta início de dia: "Nº DIA - título..."
        m_dia = None
        for i, l in enumerate(linhas):
            m = re.match(r'^(\d{1,2})[º°]?\s*DIA\s*[-–—]\s*(.*)$', l, re.I)
            if m:
                m_dia = (i, m)
                break

        if m_dia:
            # salva o dia anterior
            if dia_atual:
                dias.append(dia_atual)
            i, m = m_dia
            num = int(m.group(1))
            titulo = m.group(2).strip()
            # junta a continuação do título (linha seguinte, se não for seção)
            resto = linhas[i+1:]
            if resto and not re.match(r'^(Vers[ií]culo|Mensagem|Ora)', resto[0], re.I):
                titulo += ' ' + resto[0]
                resto = resto[1:]
            dia_atual = {
                "num": num,
                "titulo": re.sub(r'\s+', ' ', titulo).strip(),
                "corpo": "\n".join(resto),
            }
        else:
            # continuação do dia atual
            if dia_atual:
                dia_atual["corpo"] += "\n" + texto

    if dia_atual:
        dias.append(dia_atual)

    # ---- Parse de cada dia ----
    def extrair(corpo, inicio, fim_marcadores):
        """Extrai texto entre 'inicio' e o primeiro dos 'fim_marcadores'."""
        m = re.search(re.escape(inicio) + r'\s*\n(.*?)(?=\n(?:' + '|'.join(re.escape(f) for f in fim_marcadores) + r')\b)', corpo, re.S)
        if m:
            return re.sub(r'\s+', ' ', m.group(1)).strip()
        m2 = re.search(re.escape(inicio) + r'\s*\n(.*?)$', corpo, re.S)
        if m2:
            return re.sub(r'\s+', ' ', m2.group(1)).strip()
        return ""

    def extrair_obra(corpo):
        """Extrai a obra prática (aceita variação: Obra Prática do Dia (Subtítulo))."""
        m = re.search(r'Obra\s+Pr[áa]tica\s+do\s+Dia(?:\s*\([^)]*\))?\s*\n(.*?)$', corpo, re.S | re.I)
        if m:
            return re.sub(r'\s+', ' ', m.group(1)).strip()
        return ""

    def extrair_ci(corpo, inicio, fim_marcadores):
        """Case-insensitive: extrai entre 'inicio' e fim_marcadores."""
        m = re.search(re.escape(inicio) + r'\s*\n(.*?)(?=\n(?:' + '|'.join(re.escape(f) for f in fim_marcadores) + r')\b)', corpo, re.S | re.I)
        if m:
            return re.sub(r'\s+', ' ', m.group(1)).strip()
        m2 = re.search(re.escape(inicio) + r'\s*\n(.*?)$', corpo, re.S | re.I)
        if m2:
            return re.sub(r'\s+', ' ', m2.group(1)).strip()
        return ""
        m = re.search(re.escape(inicio) + r'\s*\n(.*?)(?=\n(?:' + '|'.join(re.escape(f) for f in fim_marcadores) + r')\b)', corpo, re.S)
        if m:
            return re.sub(r'\s+', ' ', m.group(1)).strip()
        # fallback: até o fim
        m2 = re.search(re.escape(inicio) + r'\s*\n(.*?)$', corpo, re.S)
        if m2:
            return re.sub(r'\s+', ' ', m2.group(1)).strip()
        return ""

    dias_estruturados = []
    for d in dias:
        corpo = d["corpo"]
        sec = {
            "num": d["num"],
            "titulo": d["titulo"],
            "versiculo": extrair(corpo, "Versículo-Chave", ["Mensagem Inspirada", "Mensagem", "Oração do Dia"]),
            "mensagem": extrair(corpo, "Mensagem Inspirada", ["Oração do Dia", "Oração"]),
            "oracao": extrair(corpo, "Oração do Dia", ["Um Segundo com Deus", "Obra Prática"]),
            "prece": (extrair_ci(corpo, "Um Segundo com Deus", ["Obra Prática do Dia", "Obra Prática"])
                      or extrair_ci(corpo, "Minuto com Deus", ["Obra Prática do Dia", "Obra Prática"])),
            "obra": extrair_obra(corpo),
        }
        dias_estruturados.append(sec)

    # ---- Encerramento (págs 39-40) ----
    encerramento = "\n\n".join(p.strip() for p in paginas[38:40] if p.strip())

    # ---- Salvar ----
    dados = {
        "titulo": "Devocional Um Segundo com Deus",
        "subtitulo": "Vol. 01 — 30 dias de conexão diária com Deus",
        "apresentacao": apresentacao,
        "dias": dias_estruturados,
        "encerramento": encerramento,
    }
    OUT_JSON.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')

    completos = sum(1 for d in dias_estruturados if d["versiculo"] and d["mensagem"] and d["oracao"])
    print(f"Dias: {len(dias_estruturados)} | completos: {completos}")
    print(f"Com prece: {sum(1 for d in dias_estruturados if d['prece'])} | com obra: {sum(1 for d in dias_estruturados if d['obra'])}")
    print(f"JSON: {OUT_JSON}")

    print("\n=== TÍTULOS (verificar) ===")
    for d in dias_estruturados:
        flag = '' if d["versiculo"] and d["mensagem"] else ' ⚠️'
        print(f"  {d['num']:>2}º: {d['titulo'][:50]}{flag}")

if __name__ == "__main__":
    main()
