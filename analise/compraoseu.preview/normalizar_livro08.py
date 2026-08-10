# -*- coding: utf-8 -*-
"""
Normaliza "Você e o Universo — O Inconsciente e as suas Criações" (livro08).
- Remove 212 timestamps [00:00] etc.
- Remove chamada final do canal YouTube
- Corrige "Partil" (erro de transcrição)
- Estrutura: Prólogo + 20 capítulos
- Gera JSON estruturado para a página de leitura
"""
import re, json
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "livro" / "Livro08.txt"
OUT_JSON = HERE / "livro08_dados.json"

TITULO = "Você e o Universo"
SUBTITULO = "O Inconsciente e as suas Criações"

# Mapa de capítulos (do texto)
TITULOS_CAP = {
    1: "O Sistema que Quase Ninguém Percebe",
    2: "O Erro de Pedir ao Universo",
    3: "A Linguagem que o Universo Entende",
    4: "O Poder das Crenças",
    5: "Neuroplasticidade",
    6: "A Psicologia da Expectativa",
    7: "O Campo de Possibilidades",
    8: "A Frequência da Convicção",
    9: "O Portal do Subconsciente",
    10: "O Ritual do Comando Matinal",
    11: "O Ritual do Espelho",
    12: "O Ritual da Visualização Dirigida",
    13: "O Ritual Noturno de Reprogramação",
    14: "O Diário de Identidade",
    15: "O Efeito Dominó da Mente",
    16: "O Sistema Invisível da Realidade",
    17: "A Mudança de Identidade",
    18: "O Ponto de Virada",
    19: "O Estado do Criador",
}

def main():
    t = SRC.read_text(encoding='utf-8').replace('\r\n', '\n')
    
    # 1) Remove timestamps [00:00] / [00:00:00] em qualquer posição
    t = re.sub(r'\s*\[\d{1,3}:\d{2}(?::\d{2})?\]\s*', ' ', t)
    t = re.sub(r'\s{2,}', ' ', t)
    
    # 2) Remove chamada final do canal
    t = re.sub(r'Se alguma ideia deste vídeo fez você refletir.*?jornada de consciência\. M\.', '', t, flags=re.S)
    
    # 3) Corrige "Partil" -> "Parte 1" (provavelmente parte 1 da obra)
    t = t.replace('Partil, o código invisível da realidade', 'Parte 1. O código invisível da realidade')
    t = re.sub(r'\bPartil\b', 'Parte 1', t)
    
    # 4) Fluxo contínuo
    t = re.sub(r'\s+([,.;:!?])', r'\1', t)
    
    # 5) Estruturar por capítulos
    estrutura = []
    linhas = t.split('\n')
    fluxo = ' '.join(l.strip() for l in linhas if l.strip())
    
    # Prólogo (antes do cap 1)
    m_cap1 = re.search(r'Cap[ií]tulo 1[.,]', fluxo)
    if m_cap1:
        prologo = fluxo[:m_cap1.start()].strip()
        estrutura.append(("h1_parte", "PRÓLOGO"))
        estrutura.append(("p", prologo))
        resto = fluxo[m_cap1.start():]
    else:
        resto = fluxo
    
    # Divide em capítulos
    # padrão: "Capítulo N, titulo." ou "Capítulo N. titulo" ou "Capítulo N titulo"
    caps = list(re.finditer(r'Cap[ií]tulo\s+(\d+)[.,]?\s*([A-ZÀ-Úa-zà-ú][^.]{0,60})', resto))
    
    # corrige a ordem e extrai corpo
    segmentos = []
    for i, m in enumerate(caps):
        num = int(m.group(1))
        inicio = m.start()
        fim = caps[i+1].start() if i+1 < len(caps) else len(resto)
        corpo = resto[m.end():fim].strip()
        segmentos.append((num, corpo))
    
    # Renumera: os capítulos originais são 1,3,4,...,20 (faltou o 2 na transcrição)
    # Mapa: original -> novo
    renumerar = {}
    nova_seq = 1
    for m_orig in sorted({seg[0] for seg in segmentos}):
        renumerar[m_orig] = nova_seq
        nova_seq += 1

    # Ordena e monta
    for num_orig, corpo in sorted(segmentos):
        num = renumerar[num_orig]
        # remove o título repetido no início do corpo
        titulo = TITULOS_CAP.get(num, "")
        if titulo:
            corpo = re.sub(r'^\s*' + re.escape(titulo) + r'[.,]?\s*', '', corpo, flags=re.I)
            corpo = re.sub(r'^\s*[A-ZÀ-Ú][^.]{0,60}[.,]\s*', '', corpo)  # remove refrão do título
        estrutura.append(("h1", f"CAPÍTULO {num}"))
        estrutura.append(("h2", titulo))
        # divide em parágrafos
        for par in re.split(r'(?<=[.!?])\s+', corpo):
            if par.strip():
                estrutura.append(("p", par.strip()))
    
    # Salvar JSON
    dados = {
        "titulo": TITULO,
        "subtitulo": SUBTITULO,
        "estrutura": [{"tipo": t2, "texto": x} for t2, x in estrutura],
    }
    OUT_JSON.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding='utf-8')
    
    total_pal = sum(len(x.split()) for t2, x in estrutura if t2 == "p")
    print(f"Blocos: {len(estrutura)} | Palavras: {total_pal}")
    print(f"Capítulos: {len(segmentos)}")
    print(f"JSON: {OUT_JSON}")
    
    print("\n=== ESTRUTURA ===")
    for t2, x in estrutura:
        if t2 in ("h1", "h1_parte"):
            print(f"  {x[:60]}")
    
    print("\n=== AMOSTRA PRÓLOGO ===")
    for t2, x in estrutura[:3]:
        print(f"  [{t2}] {x[:120]}")

if __name__ == "__main__":
    main()
