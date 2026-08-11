# -*- coding: utf-8 -*-
"""
Normaliza "O Livro Proibido dos Mestres" (livro02) — transcrição de áudio.
Estratégia robusta:
1. Junta TODAS as linhas num fluxo contínuo (as quebras são artificiais)
2. Detecta capítulos em qualquer posição
3. Divide em parágrafos coerentes (~100-130 palavras, cortando em .!?)
4. Corrige capitalização indevida e nomes próprios
5. Gera texto limpo + estrutura
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE.parent.parent / "livro" / "livro02.txt"
OUT_TXT = HERE / "livro02_limpo.txt"

EXCECOES = {
    "Deus", "Jesus", "Cristo", "Mestre", "Mestres", "Alma", "Universo",
    "Hermes", "Trismegisto", "Apolônio", "Tiana", "Hipátia", "Alexandria",
    "Lao", "Lao-Tsé", "Padmasambhava", "Buda", "Moisés", "Sócrates", "Platão",
    "Pitágoras", "Salomão", "Davi", "Israel", "Egito", "Terra", "Shabat",
    "Capítulo", "Capítulos", "Mente", "Corpo", "Espírito", "Espanhol",
}

TITULOS_CAP = {
    1: "O Juramento do Silêncio",
    2: "O Código das Vibrações",
    3: "A Linguagem do Universo",
    4: "A Geometria Sagrada das Emoções",
    5: "O Ritual dos Três Portais",
    6: "O Poder Oculto da Palavra não Dita",
    7: "As Leis Esquecidas da Manifestação",
    8: "O Mapa Oculto da Alma",
    9: "O Espelho dos Mestres",
    10: "A Chave Final, o Retorno do Mestre Interior",
}
NUM_MAP = {"um":1,"dois":2,"três":3,"tres":3,"quatro":4,"cinco":5,
           "seis":6,"sete":7,"oito":8,"nove":9,"dez":10}

def corrigir_capitalizacao(texto):
    partes = re.split(r'(\s+)', texto)
    res = []
    fim_frase = True
    for parte in partes:
        if not parte.strip():
            res.append(parte); continue
        # palavra que começa com maiúscula (qualquer tamanho, ex.: "E", "Um", "Deus")
        m = re.match(r'^([A-ZÁÉÍÓÚÃÕÂÊÔÇ])([a-záéíóúãõâêôç]*)(.*)$', parte)
        if m:
            letra, resto, pont = m.group(1), m.group(2), m.group(3)
            base = (letra + resto).rstrip('.,;:!?')
            if base in EXCECOES:
                res.append(parte)              # nome próprio → mantém
            elif fim_frase:
                res.append(parte)              # início de frase → mantém
            else:
                res.append(letra.lower() + resto + pont)  # meio de frase → minúscula
            fim_frase = False
        else:
            res.append(parte)
            if re.search(r'[.!?]["”\']?\s*$', parte):
                fim_frase = True
            elif parte.strip():
                fim_frase = False
    return ''.join(res)

def capitalizar_sentencas(texto):
    """Capitaliza a primeira letra após . ! ? (início de sentença)."""
    # exceções de abreviações
    def repl(m):
        return m.group(1) + m.group(2).upper()
    texto = re.sub(r'([.!?]\s+)([a-záéíóúãõâêôç])', repl, texto)
    return texto

def main():
    t = SRC.read_text(encoding='utf-8').replace('\r\n', '\n')
    linhas = [l.strip() for l in t.split('\n') if l.strip()]

    # 1) fluxo contínuo
    fluxo = ' '.join(linhas)

    # 2) remover espaço antes de pontuação
    fluxo = re.sub(r'\s+([,.;:!?])', r'\1', fluxo)

    # 3) correções de transcrição
    correcoes = {
        "Lautsé": "Lao-Tsé",
        "Padma Sambava": "Padmasambhava",
        "Ipatia": "Hipátia",
        "Hipátia De Alexandria": "Hipátia de Alexandria",
        "sobre seu peso das Palavras": "sobre o peso das palavras",
        "sobre seu peso das palavras": "sobre o peso das palavras",
        "O 111 para": "O 111 para",
    }
    for a, b in correcoes.items():
        fluxo = fluxo.replace(a, b)

    # 4) detectar capítulos (em qualquer posição)
    caps = []
    for m in re.finditer(r'Cap[ií]tulo\s+(um|dois|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|\d+)[,.]?\s*', fluxo):
        caps.append((m.start(), m.end(), m.group(1).lower()))
    print("Capítulos detectados:", [(c[2], c[0]) for c in caps])

    # 5) dividir em segmentos por capítulo
    segmentos = []  # (num_cap, texto_bruto)
    for i, (inicio, fim, num_word) in enumerate(caps):
        num = NUM_MAP.get(num_word) or int(num_word)
        fim_prox = caps[i+1][0] if i+1 < len(caps) else len(fluxo)
        segmentos.append((num, fluxo[fim:fim_prox].strip()))
    # texto antes do cap 1 = introdução/capa
    pre_cap1 = fluxo[:caps[0][0]].strip() if caps else fluxo.strip()

    # 6) corrigir capitalização em cada segmento e dividir em parágrafos
    def dividir_paragrafos(texto, alvo=110):
        """Divide em parágrafos de ~alvo palavras, cortando em pontuação final."""
        # normaliza espaços
        texto = re.sub(r'\s+', ' ', texto).strip()
        # divide em sentenças preservando pontuação
        sentencas = re.findall(r'[^.!?]+[.!?]?', texto)
        paragrafos = []
        atual = ""
        for s in sentencas:
            s = s.strip()
            if not s:
                continue
            if len(atual.split()) + len(s.split()) > alvo and atual.strip():
                paragrafos.append(re.sub(r'\s{2,}', ' ', atual.strip()))
                atual = s
            else:
                atual = (atual + ' ' + s).strip()
        if atual.strip():
            paragrafos.append(re.sub(r'\s{2,}', ' ', atual.strip()))
        # garante que cada parágrafo começa com maiúscula
        final = []
        for p in paragrafos:
            if p and p[0].islower():
                p = p[0].upper() + p[1:]
            final.append(p)
        return final

    estrutura = []  # (tipo, texto)
    if pre_cap1:
        for p in dividir_paragrafos(corrigir_capitalizacao(pre_cap1)):
            estrutura.append(("p", p))

    for num, texto in segmentos:
        estrutura.append(("h1", f"CAPÍTULO {num}"))
        estrutura.append(("h2", TITULOS_CAP[num]))
        texto_corrigido = corrigir_capitalizacao(texto)
        # remove o título antigo repetido no início (ex.: "O ritual dos três portais.")
        titulo_limpo = TITULOS_CAP[num]
        texto_corrigido = re.sub(r'^\s*' + re.escape(titulo_limpo) + r'[.!]?\s*', '', texto_corrigido, flags=re.I)
        # também remove variações ("O ritual dos Três Portais." com capitalização original)
        primeira_sentenca = re.match(r'^([^.!?]+[.!?]?)', texto_corrigido)
        if primeira_sentenca:
            s = primeira_sentenca.group(1).strip()
            s_limpo = re.sub(r'[.!]', '', s).lower().strip()
            t_limpo = re.sub(r'[.!]', '', titulo_limpo).lower().strip()
            if s_limpo == t_limpo or s_limpo == t_limpo + ' o ' or t_limpo in s_limpo:
                texto_corrigido = texto_corrigido[len(s):].strip()
        # normaliza espaços duplos
        texto_corrigido = re.sub(r'\s{2,}', ' ', texto_corrigido)
        for p in dividir_paragrafos(texto_corrigido):
            estrutura.append(("p", capitalizar_sentencas(p)))

    # 7) texto limpo (para referência)
    texto_limpo = []
    for tipo, txt in estrutura:
        if tipo == "h1":
            texto_limpo.append(f"\n\n{txt}")
        elif tipo == "h2":
            texto_limpo.append(txt)
        else:
            texto_limpo.append(txt)
    OUT_TXT.write_text("\n\n".join(texto_limpo), encoding='utf-8')

    total_pal = sum(len(p.split()) for _, p in estrutura if _ == "p")
    print(f"\nTotal palavras do corpo: {total_pal}")
    print(f"Blocos: {len(estrutura)}")
    print(f"Capítulos: {len(segmentos)}")

    # validação final: mostra estrutura
    caps_vistos = [t for t, _ in estrutura if t == "h1"]
    print(f"Títulos h1: {caps_vistos}")

    # amostras
    print("\n=== AMOSTRA INTRO (limpa) ===")
    for tipo, txt in estrutura[:3]:
        print(f"  [{tipo}] {txt[:120]}")
    print("\n=== AMOSTRA CAP 5 (limpa) ===")
    for tipo, txt in estrutura:
        if tipo == "h1" and "5" in txt:
            break
    cont = 0
    mostrar = False
    for tipo, txt in estrutura:
        if tipo == "h1" and "CAPÍTULO 5" in txt:
            mostrar = True
        elif tipo == "h1" and mostrar:
            break
        if mostrar and tipo == "p":
            cont += 1
            if cont <= 2:
                print(f"  [p] {txt[:130]}")

if __name__ == "__main__":
    main()
