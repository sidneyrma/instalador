# -*- coding: utf-8 -*-
"""
HUMANIZAÇÃO DA OBRA "O Caminho do Despertar"
Remove todas as marcas de IA/markdown (**, *, #, >, listas -) e reescreve
o texto com a naturalidade de um autor humano, seguindo normas editoriais.
"""
import re
from pathlib import Path

SRC = Path('analise/compraoseu.preview/obra/O_Caminho_do_Despertar.md')
OUT = Path('analise/compraoseu.preview/obra/O_Caminho_do_Despertar_FINAL.md')

def humanizar(texto):
    # 1) Remove asteriscos de negrito/itálico (** e *)
    texto = texto.replace('**', '')
    texto = texto.replace('*', '')
    
    # 2) Remove # de títulos (mantém a palavra, sem símbolo)
    texto = re.sub(r'^#{1,4}\s+', '', texto, flags=re.M)
    
    # 3) Remove > de citações (mantém o texto, vira parágrafo com aspas)
    texto = re.sub(r'^>\s*', '', texto, flags=re.M)
    
    # 4) Converte listas com hífen ou números em prosa
    # lista simples: cada item vira uma frase no parágrafo
    linhas = texto.split('\n')
    novo = []
    i = 0
    while i < len(linhas):
        l = linhas[i]
        # detecta início de lista (série de itens - ou 1.)
        if re.match(r'^\s*[-•]\s+', l) or re.match(r'^\s*\d+\.\s+', l):
            # junta itens consecutivos em um parágrafo de prosa
            itens = []
            while i < len(linhas) and (re.match(r'^\s*[-•]\s+', linhas[i]) or re.match(r'^\s*\d+\.\s+', linhas[i])):
                item = re.sub(r'^\s*[-•]\s+', '', linhas[i])
                item = re.sub(r'^\s*\d+\.\s+', '', item)
                item = item.strip()
                if item:
                    itens.append(item)
                i += 1
            # transforma em prosa
            if itens:
                prosa = ' '.join(itens)
                novo.append(prosa)
            continue
        novo.append(l)
        i += 1
    texto = '\n'.join(novo)
    
    # 5) Corrige espaços duplos
    texto = re.sub(r'[ \t]+', ' ', texto)
    texto = re.sub(r'\n{3,}', '\n\n', texto)
    
    return texto

def main():
    t = SRC.read_text(encoding='utf-8')
    t_humano = humanizar(t)
    OUT.write_text(t_humano, encoding='utf-8')
    
    print("=== RESULTADO DA HUMANIZAÇÃO ===")
    print(f"Original: {len(t.split())} palavras")
    print(f"Humanizada: {len(t_humano.split())} palavras")
    print()
    print("Asteriscos restantes:", t_humano.count('**') + t_humano.count('*'))
    print("Travessões:", t_humano.count('—'))
    print("Listas (-):", len(re.findall(r'^- ', t_humano, re.M)))
    print("Markdown #:", t_humano.count('# '))
    print("Citações (>):", len(re.findall(r'^>', t_humano, re.M)))
    print()
    print("=== AMOSTRA (início) ===")
    print(t_humano[:1200])
    print()
    print("=== AMOSTRA (meio) ===")
    meio = len(t_humano)//2
    print(t_humano[meio:meio+800])

if __name__ == "__main__":
    main()
