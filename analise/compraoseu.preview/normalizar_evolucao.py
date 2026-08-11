# -*- coding: utf-8 -*-
"""
Normaliza "Evolução da Alma" (livro) — texto já é de boa qualidade.
Estrutura:
- Prefácio + Abertura + Prece
- Seções introdutórias (Sabedoria, Pensamentos, Luz, Perdão, Propósito, Mindfulness, Ansiedade)
- INÍCIO DO DESENVOLVIMENTO + Capítulos 1-11 (com subseções X.Y)
- Oração Final + Frase Final
Faz: junta quebras, limpa espaços, corrige "sabedora", preserva a estrutura.
"""
import re
import json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "livro" / "evolucaodaalma.txt"
OUT_JSON = HERE / "evolucao_dados.json"

TITULOS_CAP = {
    1: "Descobrindo a Essência Divina",
    2: "A Profundidade do Autoconhecimento",
    3: "Superação das Dificuldades Emocionais",
    4: "Vencendo o Stress",
    5: "Vencendo a Depressão",
    6: "A Persistência no Caminho da Evolução",
    7: "Maturidade Espiritual e Resiliência",
    8: "Buscando Apoio",
    9: "Planejando o Futuro com Propósito",
    10: "O Poder da Persistência e Consistência",
    11: "Conectando-se com o Futuro",
}

def main():
    t = SRC.read_text(encoding='utf-8').replace('\r\n', '\n')
    linhas = [l.strip() for l in t.split('\n')]

    # 1) Localizar marcos
    # corpo real começa no 2º "INÍCIO DO DESENVOLVIMENTO" ou 2º "Capítulo 1:"
    pos_cap1 = [i for i, l in enumerate(linhas) if re.match(r'^Cap[ií]tulo\s*1:', l, re.I)]
    corpo_inicio = pos_cap1[1] if len(pos_cap1) > 1 else 641

    # 2) Prefácio (linhas 0 até o SUMÁRIO)
    pos_sumario = next((i for i, l in enumerate(linhas) if l.strip().upper() == 'SUMÁRIO'), None)
    prefacio = linhas[:pos_sumario] if pos_sumario else linhas[:corpo_inicio]

    # 3) Seções introdutórias (entre sumário e corpo)
    intro = linhas[pos_sumario+1:corpo_inicio] if pos_sumario else []

    # 4) Corpo (capítulos)
    corpo = linhas[corpo_inicio:]

    # 5) Corrigir "sabedora"
    def limpar_texto(lista):
        return [re.sub(r'\b[sS]abedora\b', 'sabedoria', l) for l in lista]

    prefacio = limpar_texto(prefacio)
    intro = limpar_texto(intro)
    corpo = limpar_texto(corpo)

    # 6) Estruturar corpo em capítulos
    estrutura = []  # (tipo, texto)
    # prefácio
    estrutura.append(("h1_parte", "PREFÁCIO"))
    par_atual = []
    def flush_par(pars):
        if pars:
            texto = re.sub(r'\s+', ' ', ' '.join(pars)).strip()
            if texto:
                estrutura.append(("p", texto))
            pars.clear()

    for l in prefacio:
        if not l:
            flush_par(par_atual)
        else:
            par_atual.append(l)
    flush_par(par_atual)

    # seções introdutórias
    estrutura.append(("h1_parte", "INTRODUÇÃO"))
    for l in intro:
        if not l:
            flush_par(par_atual)
        elif re.match(r'^(INÍCIO DO DESENVOLVIMENTO|O que é Ansiedade\?|Fatores comuns)', l, re.I):
            continue
        elif len(l) < 60 and not l.endswith(('.', ',')) and '\t' not in l and re.match(r'^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]', l):
            flush_par(par_atual)
            estrutura.append(("h2", l.strip()))
        else:
            par_atual.append(l)
    flush_par(par_atual)

    # capítulos
    for i, l in enumerate(corpo):
        m_cap = re.match(r'^Cap[ií]tulo\s*(\d+):\s*(.*)$', l, re.I)
        if m_cap:
            flush_par(par_atual)
            num = int(m_cap.group(1))
            estrutura.append(("h1", f"CAPÍTULO {num}"))
            estrutura.append(("h2", TITULOS_CAP.get(num, m_cap.group(2).strip())))
            continue
        m_sub = re.match(r'^(\d+\.\d+)\s*:?\s*(.*)$', l)
        if m_sub:
            flush_par(par_atual)
            estrutura.append(("h3", m_sub.group(2).strip()))
            continue
        if not l:
            flush_par(par_atual)
        elif l.strip().upper() in ('ORAÇÃO FINAL', 'FRASE FINAL'):
            flush_par(par_atual)
            estrutura.append(("h1_parte", l.strip().upper()))
        else:
            par_atual.append(l)
    flush_par(par_atual)

    # 7) Salvar JSON
    dados = {
        "titulo": "Evolução da Alma",
        "subtitulo": "Fé e Transformação Pessoal — Guia Prático com Preces, Orações e Ensinamentos Bíblicos",
        "estrutura": [{"tipo": t, "texto": x} for t, x in estrutura],
    }
    OUT_JSON.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')

    # Estatísticas
    total_pal = sum(len(x.split()) for t, x in estrutura if t == "p")
    caps = sum(1 for t, _ in estrutura if t == "h1")
    print(f"Blocos: {len(estrutura)} | Palavras: {total_pal} | Capítulos (h1): {caps}")
    print(f"JSON salvo: {OUT_JSON}")

    # amostra da estrutura
    print("\n=== ESTRUTURA (títulos) ===")
    for t, x in estrutura:
        if t in ("h1", "h1_parte"):
            print(f"  {x[:60]}")

if __name__ == "__main__":
    main()
