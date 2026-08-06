# -*- coding: utf-8 -*-
"""
Normaliza "O Caibalion (Kybalion)" (livro03) — edição definitiva e comentada.
Estrutura: Apresentação → PARTE I (O Caibalion, 15 caps) → PARTE II (As Sete Leis
Cósmicas, 10 caps) → Comentários da edição.
Remove: timestamps de áudio, quebras aleatórias, capitalização indevida,
erros do nome "Caibalion", créditos finais do canal.
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "livro" / "Livro03.txt"
OUT_TXT = HERE / "livro03_limpo.txt"

EXCECOES = {
    "Deus", "Jesus", "Cristo", "Mestre", "Mestres", "Alma", "Universo",
    "Hermes", "Trismegisto", "Caibalion", "Kybalion", "William", "Walker",
    "Atkinson", "Egito", "Grécia", "Terra", "Capítulo", "Capítulos",
    "Mente", "Corpo", "Espírito", "Todo", "Lei", "Leis", "Parte",
}

TITULOS_PARTE1 = {
    1: "A Filosofia Hermética",
    2: "Os Sete Princípios Herméticos",
    3: "A Transmutação Mental",
    4: "O Todo",
    5: "O Universo Mental",
    6: "O Paradoxo Divino",
    7: "O Todo em Tudo",
    8: "Os Planos da Correspondência",
    9: "A Vibração",
    10: "A Polaridade",
    11: "O Ritmo",
    12: "A Causalidade",
    13: "O Gênero",
    14: "O Gênero Mental",
    15: "Axiomas Herméticos",
}

TITULOS_PARTE2 = {
    1: "Introdução ao Livro",
    2: "Lei Cósmica e Leis Cósmicas",
    3: "As Sete Leis Cósmicas",
    4: "A Lei Cósmica da Unidade na Diversidade",
    5: "A Lei Cósmica da Atividade",
    6: "A Lei Cósmica da Mudança",
    7: "A Lei Cósmica da Causalidade",
    8: "A Lei Cósmica do Ritmo",
    9: "A Lei Cósmica da Polaridade",
    10: "A Lei Cósmica do Equilíbrio",
}

NUM_MAP = {
    "um":1,"primeiro":1,"dois":2,"segundo":2,"três":3,"tres":3,"terceiro":3,
    "quatro":4,"quarto":4,"cinco":5,"quinto":5,"seis":6,"sexto":6,"sete":7,
    "sétimo":7,"setimo":7,"oito":8,"oitavo":8,"nove":9,"nono":9,"dez":10,
    "décimo":10,"decimo":10,"onze":11,"doze":12,"treze":13,"catorze":14,
    "quatorze":14,"quinze":15,
}

def corrigir_capitalizacao(texto):
    partes = re.split(r'(\s+)', texto)
    res, fim_frase = [], True
    for parte in partes:
        if not parte.strip():
            res.append(parte); continue
        m = re.match(r'^([A-ZÁÉÍÓÚÃÕÂÊÔÇ])([a-záéíóúãõâêôç]*)(.*)$', parte)
        if m:
            letra, resto, pont = m.group(1), m.group(2), m.group(3)
            base = (letra + resto).rstrip('.,;:!?')
            if base in EXCECOES or fim_frase:
                res.append(parte)
            else:
                res.append(letra.lower() + resto + pont)
            fim_frase = False
        else:
            res.append(parte)
            if re.search(r'[.!?]["”\']?\s*$', parte):
                fim_frase = True
            elif parte.strip():
                fim_frase = False
    return ''.join(res)

def capitalizar_sentencas(texto):
    return re.sub(r'([.!?]\s+)([a-záéíóúãõâêôç])',
                  lambda m: m.group(1) + m.group(2).upper(), texto)

def dividir_paragrafos(texto, alvo=110):
    texto = re.sub(r'\s+', ' ', texto).strip()
    sentencas = re.findall(r'[^.!?]+[.!?]?', texto)
    paragrafos, atual = [], ""
    for s in sentencas:
        s = s.strip()
        if not s: continue
        if len(atual.split()) + len(s.split()) > alvo and atual.strip():
            paragrafos.append(re.sub(r'\s{2,}', ' ', atual.strip()))
            atual = s
        else:
            atual = (atual + ' ' + s).strip()
    if atual.strip():
        paragrafos.append(re.sub(r'\s{2,}', ' ', atual.strip()))
    final = []
    for p in paragrafos:
        if p and p[0].islower():
            p = p[0].upper() + p[1:]
        final.append(p)
    return final

def main():
    t = SRC.read_text(encoding='utf-8').replace('\r\n', '\n')
    linhas = [l.strip() for l in t.split('\n') if l.strip()]
    fluxo = ' '.join(linhas)
    fluxo = re.sub(r'\b\d{2}:\d{2}:\d{2}\b', '', fluxo)
    fluxo = re.sub(r'\s+([,.;:!?])', r'\1', fluxo)

    correcoes = {
        "cai balão": "Caibalion", "Cai balão": "Caibalion",
        "cai bal eon": "Caibalion", "Cai bal eon": "Caibalion",
        "caibaleon": "Caibalion", "Caibaleon": "Caibalion",
        "o caibalion": "o Caibalion", "O caibalion": "O Caibalion",
        "de cai balão": "do Caibalion",
        "o sentido sense e o significado meani de natureza ou a universali":
        "o sentido e o significado de natureza ou a universalidade",
        "Segunda o princípio": "Segundo o princípio",
        "estilo verdades": "estilo as verdades",
        "Deixe seu lançamento": "Desde seu lançamento",
        "[Música]": "", "[música]": "",
        "áudio livro O Caibalion edição": "Fim do audiolivro O Caibalion",
        "inscrever em nosso Canal": "continuar explorando o hermetismo",
    }
    for a, b in correcoes.items():
        fluxo = fluxo.replace(a, b)
    # correções por regex (variações)
    fluxo = re.sub(r'(?i)diz o cai\s+bal[aã]o', 'diz o Caibalion', fluxo)
    fluxo = re.sub(r'(?i)\bcai\s+bal[aã]o\b', 'Caibalion', fluxo)
    fluxo = re.sub(r'\bmeani\b', 'significado', fluxo)
    fluxo = re.sub(r'\bsense\b', 'sentido', fluxo)
    fluxo = re.sub(r'\buniversali\b', 'universalidade', fluxo)
    fluxo = re.sub(r'\s{2,}', ' ', fluxo)

    # ---- Localizar marcos ----
    # Sumário vai de ~1100 até ~2600 (contém os 15 caps + parte 2 listada)
    # Corpo do Caibalion: primeiro "Capítulo 1 a filosofia hermética" após 9000
    m_p1 = re.search(r'Capítulo 1 a filosofia hermética', fluxo[9000:])
    p1_inicio = 9000 + m_p1.start() if m_p1 else None
    # Parte 2: "Capítulo primeiro introdução ao livro" (depois do corpo do Caibalion)
    m_p2 = re.search(r'Capítulo primeiro\s+Capítulo primeiro introdução ao livro', fluxo)
    if not m_p2:
        m_p2 = re.search(r'Capítulo primeiro introdução ao livro', fluxo)
    p2_inicio = m_p2.start() if m_p2 else None
    # Comentários: procura "preceitos budistas" (início dos comentários da edição)
    m_com = re.search(r'(?i)capítulo segundo\s+além disso os preceitos', fluxo)
    coment_inicio = m_com.start() if m_com else None

    print(f"Parte 1 (Caibalion) inicia: {p1_inicio}")
    print(f"Parte 2 (Sete Leis) inicia: {p2_inicio}")
    print(f"Comentários iniciam: {coment_inicio}")

    estrutura = []

    # ---- Apresentação (antes da parte 1, depois do sumário) ----
    if p1_inicio:
        apresentacao = fluxo[2600:p1_inicio]
        apresentacao = re.sub(r'(?i)(sum[aá]rio[^\n]*|contendo \d+ cap[ií]tulos[^\n]*|edi[cç][aã]o definitiva[^\n]*)', '', apresentacao)
        if apresentacao.strip():
            estrutura.append(("h2_parte", "APRESENTAÇÃO"))
            for p in dividir_paragrafos(corrigir_capitalizacao(apresentacao)):
                estrutura.append(("p", capitalizar_sentencas(p)))

    # ---- Parte 1: O Caibalion (caps 1-15) ----
    if p1_inicio:
        estrutura.append(("h1_parte", "PARTE I — O CAIBALION"))
        corpo1 = fluxo[p1_inicio:(p2_inicio or coment_inicio or len(fluxo))]
        # detecta por títulos conhecidos (robusto)
        caps1 = []
        for num, titulo in TITULOS_PARTE1.items():
            # busca o padrão "Capítulo N <título>" (mais robusto)
            num_texto = {1:"um",2:"dois",3:"três",4:"quatro",5:"cinco",6:"seis",7:"sete",
                         8:"oito",9:"nove",10:"dez",11:"onze",12:"doze",13:"treze",
                         14:"catorze",15:"quinze"}[num]
            padrao = re.compile(r'(?i)cap[ií]tulo\s+(?:' + str(num) + r'|' + num_texto +
                                r')\b[^.]{0,60}?' + re.escape(titulo))
            m = padrao.search(corpo1)
            if m:
                caps1.append((m.start(), num))
            else:
                # fallback: busca "Capítulo N" seguido de algo próximo ao título
                m2 = re.search(r'(?i)cap[ií]tulo\s+(?:' + str(num) + r'|' + num_texto + r')\b', corpo1)
                if m2:
                    caps1.append((m2.start(), num))
        caps1.sort()
        for i, (pos, num) in enumerate(caps1):
            fim_prox = caps1[i+1][0] if i+1 < len(caps1) else len(corpo1)
            texto = corpo1[pos:fim_prox].strip()
            # remove o cabeçalho "Capítulo X Título"
            texto = re.sub(r'^.*?' + re.escape(TITULOS_PARTE1[num]), TITULOS_PARTE1[num], texto, count=1, flags=re.I)
            texto = re.sub(r'^' + re.escape(TITULOS_PARTE1[num]) + r'[.!]?\s*', '', texto, count=1, flags=re.I)
            estrutura.append(("h1", f"CAPÍTULO {num}"))
            estrutura.append(("h2", TITULOS_PARTE1[num]))
            texto = corrigir_capitalizacao(texto)
            texto = re.sub(r'\s{2,}', ' ', texto)
            for p in dividir_paragrafos(texto):
                estrutura.append(("p", capitalizar_sentencas(p)))

    # ---- Parte 2: As Sete Leis Cósmicas ----
    if p2_inicio:
        estrutura.append(("h1_parte", "PARTE II — AS SETE LEIS CÓSMICAS"))
        corpo2 = fluxo[p2_inicio:(coment_inicio or len(fluxo))]
        caps2 = []
        for num, titulo in TITULOS_PARTE2.items():
            m = re.search(re.escape(titulo), corpo2, re.I)
            if m:
                caps2.append((m.start(), num))
        caps2.sort()
        for i, (pos, num) in enumerate(caps2):
            fim_prox = caps2[i+1][0] if i+1 < len(caps2) else len(corpo2)
            texto = corpo2[pos:fim_prox].strip()
            texto = re.sub(r'^.*?' + re.escape(TITULOS_PARTE2[num]), TITULOS_PARTE2[num], texto, count=1, flags=re.I)
            texto = re.sub(r'^' + re.escape(TITULOS_PARTE2[num]) + r'[.!]?\s*', '', texto, count=1, flags=re.I)
            estrutura.append(("h1", f"CAPÍTULO {num}"))
            estrutura.append(("h2", TITULOS_PARTE2[num]))
            texto = corrigir_capitalizacao(texto)
            texto = re.sub(r'\s{2,}', ' ', texto)
            for p in dividir_paragrafos(texto):
                estrutura.append(("p", capitalizar_sentencas(p)))

    # ---- Comentários da edição ----
    if coment_inicio:
        estrutura.append(("h1_parte", "COMENTÁRIOS DA EDIÇÃO"))
        coment = fluxo[coment_inicio:]
        # remove créditos finais
        coment = re.sub(r'(?i)(se este mergulho no mar do conhecimento[^\n]*|convidamos você a continuar explorando[^\n]*|futuros lançamentos[^\n]*|áudio livro O Caibalion[^\n]*|fim do audiolivro[^\n]*)', '', coment)
        for p in dividir_paragrafos(corrigir_capitalizacao(coment)):
            estrutura.append(("p", capitalizar_sentencas(p)))

    # ---- salvar ----
    texto_limpo = []
    for tipo, txt in estrutura:
        if tipo in ("h1", "h1_parte"):
            texto_limpo.append(f"\n\n{txt}")
        elif tipo == "h2":
            texto_limpo.append(txt if txt else "")
        else:
            texto_limpo.append(txt)
    OUT_TXT.write_text("\n\n".join(texto_limpo), encoding='utf-8')

    total_pal = sum(len(p.split()) for t, p in estrutura if t == "p")
    n_h1 = sum(1 for t, _ in estrutura if t == "h1")
    print(f"\nParágrafos: {sum(1 for t,_ in estrutura if t=='p')}")
    print(f"Palavras do corpo: {total_pal}")
    print(f"Capítulos (h1): {n_h1}")
    print(f"Arquivo salvo: {OUT_TXT}")

    # amostra
    print("\n=== AMOSTRA APRESENTAÇÃO ===")
    for tipo, txt in estrutura[:4]:
        print(f"  [{tipo}] {txt[:120]}")
    print("\n=== ESTRUTURA (títulos) ===")
    for tipo, txt in estrutura:
        if tipo in ("h1", "h1_parte"):
            print(f"  {txt}")

if __name__ == "__main__":
    main()
