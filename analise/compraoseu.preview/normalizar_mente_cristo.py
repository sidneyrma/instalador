# -*- coding: utf-8 -*-
"""
Normaliza "A Mente de Cristo" (livro/A Mente de Cristo.txt) para a página de leitura.

Processos:
  1. Remove timestamps do YouTube ([mm:ss]).
  2. Remove a chamada de inscrição/curtida do canal ("Notamos que mais de 80% ... conteúdo para você.").
  3. Corrige "Ement Fox" -> "Emmet Fox" (nome do autor dos ensinamentos).
  4. Estrutura: Introdução + 17 capítulos (títulos extraídos e capitalizados).
  5. Divide em parágrafos (~120 palavras), corrige capitalização de sentenças.
  6. Salva mente_cristo_dados.json (mesmo formato do livro08: {titulo, subtitulo, estrutura[{tipo, texto}]}).
"""
import json, re
from pathlib import Path

HERE = Path(__file__).parent
SRC = Path(__file__).resolve().parents[2] / "livro" / "A Mente de Cristo.txt"
OUT = HERE / "mente_cristo_dados.json"

TITULO = "A Mente de Cristo"
SUBTITULO = "Como Pensar com o Espírito e não com o Mundo"

# Títulos dos capítulos (editorial, capitalizados)
TITULOS_CAP = {
    1: "O Pensamento de Cristo",
    2: "Não Vos Conformeis com Este Mundo",
    3: "A Mente que Estava em Cristo",
    4: "O Reino de Deus Está Dentro de Vós",
    5: "Como um Homem Pensa em seu Coração, Assim Ele É",
    6: "Arrependei-vos",
    7: "Vós Sois a Luz do Mundo",
    8: "A Vontade de Deus",
    9: "Sede, Pois, Perfeitos",
    10: "O Olho Único",
    11: "Orai Sem Cessar",
    12: "Jesus e a Lei Mental",
    13: "A Mente Renovada e o Corpo Saudável",
    14: "Não Temas, Apenas Crê",
    15: "Cristo em Vós, a Esperança da Glória",
    16: "A Unidade com o Todo",
    17: "O Poder da Gratidão",
}

# Trecho da chamada do canal a REMOVER (pedido do usuário)
CHAMADA_CANAL = re.compile(
    r"Notamos que\s+mais de 80% dos que visitam o\s+nosso canal não estão inscritos\..*?mais e melhor conteúdo para você\.",
    re.DOTALL | re.IGNORECASE,
)


def capitalizar_sentencas(texto):
    """Capitaliza a primeira letra de cada sentença."""
    def fix(m):
        return m.group(0).upper()
    # capitaliza após . ! ? seguidos de espaço, e no início
    texto = re.sub(r'(^|[.!?]\s+)([a-zà-ú])', lambda m: m.group(1) + m.group(2).upper(), texto)
    return texto


def dividir_paragrafos(texto, alvo=120):
    """Divide o texto em parágrafos de ~alvo palavras, respeitando sentenças."""
    texto = re.sub(r'\s+', ' ', texto).strip()
    sentencas = re.findall(r'[^.!?]+[.!?]?', texto)
    paragrafos, atual = [], ""
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
    final = []
    for p in paragrafos:
        if p and p[0].islower():
            p = p[0].upper() + p[1:]
        final.append(p)
    return final


def main():
    raw = SRC.read_text(encoding='utf-8').replace('\r\n', '\n')
    # 1) Remove timestamps
    fluxo = re.sub(r'\s*\[\d{1,3}:\d{2}(?::\d{2})?\]\s*', ' ', raw)
    fluxo = re.sub(r'\s+', ' ', fluxo).strip()
    # 2) Remove chamada do canal
    fluxo = CHAMADA_CANAL.sub(' ', fluxo)
    fluxo = re.sub(r'\s+', ' ', fluxo).strip()
    # 3) Corrige nome do autor
    fluxo = fluxo.replace('Ement Fox', 'Emmet Fox')
    # corrige erros óbvios de transcrição
    fluxo = fluxo.replace('Filipenses 2 horas 5', 'Filipenses 2:5')
    # remove "M." solto no final (resquício de transcrição, ex.: "...que é eterna. M.")
    fluxo = re.sub(r'\s+M\.\s*$', '', fluxo)
    # ajusta espaço antes de pontuação
    fluxo = re.sub(r'\s+([,.;:!?])', r'\1', fluxo)
    fluxo = fluxo.replace(' .', '.')

    # ---- Divide em capítulos ----
    # aceita: "Capítulo 4ro"/"4º"/"4°" (erro de transcrição de 4º) e números por extenso
    caps = list(re.finditer(
        r'Cap[ií]tulo\s+(?:um|dois|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|treze|quatorze|quinze|dezesseis|dezessete|\d{1,2}\w*º?°?)\s*\.\s*',
        fluxo, flags=re.IGNORECASE))

    segmentos = []
    for i, m in enumerate(caps):
        num_txt = m.group(0)
        mnum = re.search(r'(\d{1,2}\w*º?°?|um|dois|tr[eê]s|quatro|cinco|seis|sete|oito|nove|dez|onze|doze|treze|quatorze|quinze|dezesseis|dezessete)', num_txt, re.IGNORECASE)
        num_map = {"um": 1, "dois": 2, "três": 3, "tres": 3, "quatro": 4, "cinco": 5, "seis": 6,
                   "sete": 7, "oito": 8, "nove": 9, "dez": 10, "onze": 11, "doze": 12,
                   "treze": 13, "quatorze": 14, "quinze": 15, "dezesseis": 16, "dezessete": 17}
        token = mnum.group(1).lower()
        if token in num_map:
            num = num_map[token]
        else:
            num = int(re.match(r'(\d+)', token).group(1))  # "4ro" -> 4
        fim = caps[i+1].start() if i+1 < len(caps) else len(fluxo)
        corpo = fluxo[m.end():fim].strip()
        segmentos.append((num, corpo))

    pre_cap1 = fluxo[:caps[0].start()].strip() if caps else fluxo.strip()

    # ---- Estrutura ----
    estrutura = []

    # Introdução
    intro = pre_cap1
    # remove o título repetido no fim da intro, se houver
    intro = intro.strip()
    if intro:
        for p in dividir_paragrafos(capitalizar_sentencas(intro), alvo=110):
            estrutura.append({"tipo": "p", "texto": p})

    # Capítulos
    for num, corpo in segmentos:
        if num not in TITULOS_CAP:
            print(f'⚠️ Capítulo {num} sem título definido — usando texto bruto')
            continue
        titulo = TITULOS_CAP[num]
        estrutura.append({"tipo": "h1", "texto": f"CAPÍTULO {num}"})
        estrutura.append({"tipo": "h2", "texto": titulo})

        corpo_corrigido = capitalizar_sentencas(corpo)
        # remove a repetição do título no início do corpo (ex.: "O pensamento de Cristo. Não se trata de...")
        corpo_corrigido = re.sub(
            r'^' + re.escape(titulo) + r'[.!]?\s+', '', corpo_corrigido, flags=re.IGNORECASE)
        # remove primeira sentença se for exatamente o título (variações de caixa)
        prim = re.match(r'^([^.!?]+[.!?]?)', corpo_corrigido)
        if prim:
            s = prim.group(1).strip()
            s_limpo = re.sub(r'[.!]', '', s).lower().strip()
            t_limpo = re.sub(r'[.!]', '', titulo).lower().strip()
            if s_limpo == t_limpo or t_limpo in s_limpo:
                corpo_corrigido = corpo_corrigido[len(s):].strip()
        corpo_corrigido = re.sub(r'\s{2,}', ' ', corpo_corrigido)
        for p in dividir_paragrafos(corpo_corrigido):
            estrutura.append({"tipo": "p", "texto": p})

    dados = {"titulo": TITULO, "subtitulo": SUBTITULO, "estrutura": estrutura}
    OUT.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding='utf-8')

    # relatório
    n_p = sum(1 for e in estrutura if e['tipo'] == 'p')
    n_h1 = sum(1 for e in estrutura if e['tipo'] == 'h1')
    palavras = sum(len(e['texto'].split()) for e in estrutura)
    print(f'✅ {OUT.name} gerado: {len(estrutura)} blocos ({n_h1} capítulos, {n_p} parágrafos)')
    print(f'   Palavras totais: {palavras}')


if __name__ == '__main__':
    main()
