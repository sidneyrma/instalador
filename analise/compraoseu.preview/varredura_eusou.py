# -*- coding: utf-8 -*-
"""
Varredura profunda nos livros 10, 08, 07, 03, 02, 01 para extrair TODAS as
afirmações e declarações que envolvem "EU SOU" (e variações relacionadas).
Gera um JSON estruturado para a página de estudos.
"""
import re, html, json
from pathlib import Path

ROOT = Path('/home/user/instalador')

# Livros e suas fontes (obras reescritas + textos originais)
LIVROS = {
    'livro01': {
        'titulo': 'O Verbo que Transforma',
        'fontes': [ROOT/'analise/livro01_reescrito/obra_livro01_v2.md'],
    },
    'livro02': {
        'titulo': 'A Sabedoria dos Mestres',
        'fontes': [ROOT/'analise/livro02_reescrito/obra_livro02_v2.md',
                   ROOT/'livro/livro02.txt',
                   ROOT/'livro/Livro02_atualizar.txt'],
    },
    'livro03': {
        'titulo': 'A Mente Renovada',
        'fontes': [ROOT/'analise/livro03_reescrito/obra_livro03_v2.md'],
    },
    'livro07': {
        'titulo': 'O Caminho do Despertar',
        'fontes': [ROOT/'analise/compraoseu.preview/obra/O_Caminho_do_Despertar_FINAL.md'],
    },
    'livro08': {
        'titulo': 'O Arquiteto da Realidade',
        'fontes': [ROOT/'analise/livro08_reescrito/obra_livro08_v2.md',
                   ROOT/'livro/Livro08.txt'],
    },
    'livro10': {
        'titulo': 'O Despertar do Observador',
        'fontes': [ROOT/'analise/livro10/obra_livro10_completa_v2.md',
                   ROOT/'livro/livro10-A.txt',
                   ROOT/'livro/livro10-B.txt',
                   ROOT/'livro/livro10-C.txt'],
    },
}

def limpar(texto):
    texto = re.sub(r'<[^>]+>', ' ', texto)
    texto = html.unescape(texto)
    return re.sub(r'\s+', ' ', texto)

def extrair_frases(texto, slug):
    """Extrai frases com 'eu sou' e padrões de afirmação."""
    frases = []
    # remove timestamps tipo [00:00]
    texto = re.sub(r'\[\d+:\d+\]', '', texto)
    # 1. Frases com "eu sou" (case insensitive)
    for m in re.finditer(r'[^.!?;\n]*\beu\s+sou\b[^.!?;]*[.!?]', texto, re.IGNORECASE):
        frase = ' '.join(m.group(0).split())
        if 8 < len(frase) < 300:
            frases.append(frase)
    # 2. Padrões de afirmação (aspas com conteúdo declarativo)
    for m in re.finditer(r'"([^"]{10,150})"', texto):
        frase = m.group(1).strip()
        if re.search(r'\beu\b', frase, re.IGNORECASE) and any(w in frase.lower() for w in ['sou','posso','tenho','estou','creio','sei','amo','sinto','mereço','recebo']):
            frases.append(f'"{frase}"')
    # remove duplicatas preservando ordem
    vistos = set()
    unicas = []
    for f in frases:
        chave = f.lower()[:80]
        if chave not in vistos:
            vistos.add(chave)
            unicas.append(f)
    return unicas

resultado = {}
for slug, info in LIVROS.items():
    todas = []
    for fonte in info['fontes']:
        if fonte.exists():
            t = limpar(fonte.read_text(encoding='utf-8', errors='ignore'))
            todas.extend(extrair_frases(t, slug))
    # deduplica
    vistos = set()
    unicas = []
    for f in todas:
        chave = f.lower()[:80]
        if chave not in vistos:
            vistos.add(chave)
            unicas.append(f)
    resultado[slug] = {
        'titulo': info['titulo'],
        'afirmacoes': unicas,
    }
    print(f"{slug} ({info['titulo']}): {len(unicas)} afirmações")

# Salva JSON
OUT_JSON = ROOT/'analise/livro_afirmacoes/afirmacoes_eusou_por_livro.json'
OUT_JSON.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"\n✅ JSON salvo: {OUT_JSON}")
print(f"Total geral: {sum(len(v['afirmacoes']) for v in resultado.values())} afirmações")
