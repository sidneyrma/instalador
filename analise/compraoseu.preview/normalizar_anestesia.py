# -*- coding: utf-8 -*-
"""
Normaliza "Anestesia Mental e seus Algoritmos da Escravidão" (DOCX) para a página
de leitura online (Livro 09 da Coleção do Despertar).

Processos:
  1. Extrai os parágrafos do DOCX.
  2. Monta a estrutura editorial: partes introdutórias + 16 capítulos + partes finais.
  3. Cria títulos editoriais para os capítulos 2, 5 e 15 (faltavam no original).
  4. Corrige erros óbvios de digitação/formação (títulos quebrados, espaços, duplicações).
  5. Gera anestesia_dados.json no mesmo formato dos outros livros:
     {titulo, subtitulo, estrutura: [{tipo: h1_parte|h1|h2|p, texto}]}
"""
import json, re
from pathlib import Path
import docx

HERE = Path(__file__).parent
SRC = Path(__file__).resolve().parents[2] / "livro" / "Anestesia Mental e seus Algoritmos da Escravidão 16 Correção.docx"
OUT = HERE / "anestesia_dados.json"

TITULO = "Anestesia Mental"
SUBTITULO = "e seus Algoritmos da Escravidão — o manual de retorno à sua versão original"

# Títulos dos capítulos (2, 5 e 15 são criações editoriais — faltavam no original)
TITULOS_CAP = {
    1: "O Algoritmo da Anestesia Mental",
    2: "O Governo do Pensamento",
    3: "O Poder do Isolamento e o Casulo",
    4: "Governo do Tempo e Disciplina",
    5: "O Autodomínio e o Governo da Vontade",
    6: "O Legado da Maturidade e a Inteireza",
    7: "Detox da Alma e o Reset do Shabat",
    8: "A Estética do Silêncio e o Comando Final",
    9: "A Engenharia do Algoritmo da Alma",
    10: "Anestesia Mental e o Despertar Coletivo",
    11: "A Disciplina da Alma: O Algoritmo da Vitória",
    12: "A Coragem de Ser Inteiro no Mundo Fragmentado",
    13: "Ansiedade Espiritual e Exaustão Digital",
    14: "A Estética do Silêncio: Ouvindo a Voz no Vácuo Digital",
    15: "O Comando Final: Viva a Vida em Alta Definição",
    16: "Checklist Final de Reprogramação Mental",
}

# Correções de texto (erros óbvios encontrados no DOCX)
CORRECOES = [
    ("3.2 2 Desmame Social", "3.2 Desmame Social"),
    ("A Voz que que sussurra", "A Voz que Sussurra"),
    ("14.2 O Jejum de Dados:", "14.2 O Jejum de Dados"),
    ("11.1 A Rotina como Ritual de Libertação :", "11.1 A Rotina como Ritual de Libertação:"),
    ("4.3 Disciplina: A Liberdade dos Escolhidos ", "4.3 Disciplina: A Liberdade dos Escolhidos"),
    ("2.2 Pensar não é Acumular, é Filtrar ", "2.2 Pensar não é Acumular, é Filtrar"),
    ("“A sabedoria sem ação é apenas entretenimento intelectual. ”", "“A sabedoria sem ação é apenas entretenimento intelectual.”"),
]

# Partes introdutórias: (tipo, rótulo sumário, subtítulo opcional, início, fim)
PARTES_INTRO = [
    ("PREFÁCIO", "O Fim da Simulação", 5, 12),
    ("NOTA DO EDITOR", None, 14, 23),
    ("APRESENTAÇÃO", "Você é o Mestre ou o Escravo do seu Código Interno?", 24, 35),
    ("AGRADECIMENTOS", None, 44, 47),
    ("SOBRE A COMPRAOSEU", "Uma Missão com Deus", 48, 61),
    ("A ESSÊNCIA DA TRILOGIA", None, 62, 82),
    ("PRINCÍPIOS DO DESPERTAR", None, 83, 95),
    ("REVISÃO", "O Protocolo da Reprogramação", 96, 106),
]

# Subseções da parte "A ESSÊNCIA DA TRILOGIA": (título, início, fim)
SUB_TRILOGIA = [
    ("O Algoritmo da Alma", 62, 69),
    ("Anestesia Mental — A Hipnose da Sobrevivência", 70, 74),
    ("Solidão Funcional — O Retiro Estratégico do Guerreiro", 75, 82),
]

# Capítulos: (número, título, início, fim)
CAPS = [
    (1, 107, 151), (2, 152, 212), (3, 213, 230), (4, 231, 260), (5, 261, 285),
    (6, 286, 313), (7, 314, 330), (8, 331, 348), (9, 349, 381), (10, 382, 418),
    (11, 419, 443), (12, 444, 475), (13, 476, 525), (14, 526, 579), (15, 580, 597),
    (16, 598, 607),
]

# Partes finais: (rótulo, subtítulo, início, fim)
PARTES_FINAL = [
    ("CASO DE USO", None, 608, 622),
    ("O PROTOCOLO DA ETERNIDADE", "Do Despertar ao Governo: A Manifestação dos Filhos", 623, 631),
    ("CADERNO DE ATIVAÇÃO", "Lucidez não é Conforto", 632, 690),
    ("CONCLUSÃO DA OBRA", None, 691, 694),
    ("MISSÃO", "Exercícios de Ativação — Log de Execução", 695, 710),
    ("ORAÇÃO FINAL", "Regeneração e Nova Identidade", 711, 719),
]

# Subseções do CADERNO DE ATIVAÇÃO: (título, início, fim)
SUB_CADERNO = [
    ("🛡️ Protocolo de 7 Dias: O Reset dos Algoritmos", 634, 636),
    ("DIA 1: O Jejum da Dopamina Digital", 637, 640),
    ("DIA 2: O Silêncio do Deserto", 641, 644),
    ("DIA 3: A Auditoria das Opiniões", 645, 648),
    ("DIA 4: O Governo do “Não”", 649, 652),
    ("DIA 5: A Limpeza dos Ídolos Mentais", 653, 656),
    ("DIA 6: A Coerência do Agir", 657, 660),
    ("DIA 7: O Transbordamento da Maturidade", 661, 664),
    ("Exercício 1: O Inventário das Vozes", 665, 669),
    ("Exercício 2: O Jejum de Ruídos", 670, 674),
    ("Exercício 3: Mapa da Dependência de Aprovação", 675, 679),
    ("Exercício 4: A Auditoria das Conexões", 680, 684),
    ("Exercício 5: O Plano de Guerra Financeira", 685, 690),
]


def limpar(texto):
    """Limpa espaços múltiplos e quebras dentro do parágrafo."""
    texto = re.sub(r'\s+', ' ', texto).strip()
    for a, b in CORRECOES:
        texto = texto.replace(a, b)
    return texto


def eh_secao_num(texto):
    """True se o parágrafo é uma seção numerada (ex.: 1.1, 2.3, 10.2)."""
    return bool(re.match(r'^\d{1,2}\.\d{1,2}\s+', texto)) or texto.startswith('🗝️')


def eh_titulo_dia(texto):
    """True se o parágrafo é um título de DIA/EXERCÍCIO no caderno."""
    return bool(re.match(r'^(DIA\s+\d|EXERCÍCIO\s+\d)', texto, re.IGNORECASE))


def processar_faixa(paras, inicio, fim, com_secoes=False, subsecoes=None):
    """Processa uma faixa de parágrafos, retornando lista de (tipo, texto).

    com_secoes=True: detecta seções numeradas (N.N) como h2 dentro da faixa.
    subsecoes: lista de (título, ini, fim) que viram h2 na ordem.
    """
    estrutura = []
    if subsecoes:
        # adiciona as subseções na ordem; o conteúdo fora delas vira parágrafo
        cobertos = set()
        for titulo, ini, fim_sub in subsecoes:
            estrutura.append({"tipo": "h2", "texto": titulo})
            for i in range(ini, fim_sub + 1):
                t = limpar(paras[i])
                if t:
                    estrutura.append({"tipo": "p", "texto": t})
                cobertos.add(i)
        # parágrafos da faixa fora das subseções
        for i in range(inicio, fim + 1):
            if i in cobertos:
                continue
            t = limpar(paras[i])
            if t:
                estrutura.append({"tipo": "p", "texto": t})
        return estrutura

    for i in range(inicio, fim + 1):
        raw = paras[i]
        primeira_linha = raw.split('\n')[0].strip()
        t = limpar(raw)
        if not t:
            continue
        # pula o título do capítulo repetido dentro do corpo (ex.: "CAPÍTULO 16 - CHECKLIST...")
        if re.match(r'^CAP[IÍ]TULO\s+\d+\s*[-–]', t, re.IGNORECASE):
            continue
        if com_secoes and (eh_secao_num(primeira_linha) or eh_titulo_dia(t)):
            # título da seção = primeira linha, sem o número (ex.: "1.1 O Abismo..." -> "O Abismo...")
            t_limpo = re.sub(r'^\d{1,2}\.\d{1,2}\s+', '', limpar(primeira_linha))
            estrutura.append({"tipo": "h2", "texto": t_limpo})
        else:
            estrutura.append({"tipo": "p", "texto": t})
    return estrutura


def main():
    doc = docx.Document(str(SRC))
    paras = [p.text for p in doc.paragraphs]

    estrutura = []

    # ---- Partes introdutórias ----
    for rotulo, subtitulo, ini, fim in PARTES_INTRO:
        estrutura.append({"tipo": "h1_parte", "texto": rotulo})
        if subtitulo:
            estrutura.append({"tipo": "h2", "texto": subtitulo})
        subsecoes = None
        if rotulo == "A ESSÊNCIA DA TRILOGIA":
            subsecoes = SUB_TRILOGIA
        estrutura.extend(processar_faixa(paras, ini, fim, subsecoes=subsecoes))

    # ---- Capítulos ----
    for num, ini, fim in CAPS:
        estrutura.append({"tipo": "h1", "texto": f"CAPÍTULO {num}"})
        estrutura.append({"tipo": "h2", "texto": TITULOS_CAP[num]})
        estrutura.extend(processar_faixa(paras, ini, fim, com_secoes=True))

    # ---- Partes finais ----
    for rotulo, subtitulo, ini, fim in PARTES_FINAL:
        estrutura.append({"tipo": "h1_parte", "texto": rotulo})
        if subtitulo:
            estrutura.append({"tipo": "h2", "texto": subtitulo})
        subsecoes = None
        if rotulo == "CADERNO DE ATIVAÇÃO":
            subsecoes = SUB_CADERNO
        estrutura.extend(processar_faixa(paras, ini, fim, subsecoes=subsecoes))

    dados = {"titulo": TITULO, "subtitulo": SUBTITULO, "estrutura": estrutura}
    OUT.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding='utf-8')

    n_p = sum(1 for e in estrutura if e['tipo'] == 'p')
    n_h1 = sum(1 for e in estrutura if e['tipo'] == 'h1')
    n_parte = sum(1 for e in estrutura if e['tipo'] == 'h1_parte')
    n_h2 = sum(1 for e in estrutura if e['tipo'] == 'h2')
    palavras = sum(len(e['texto'].split()) for e in estrutura)
    print(f'✅ {OUT.name}: {len(estrutura)} blocos | {n_parte} partes, {n_h1} capítulos, {n_h2} subtítulos, {n_p} parágrafos')
    print(f'   Palavras totais: {palavras}')


if __name__ == '__main__':
    main()
