# -*- coding: utf-8 -*-
"""Monta capas v5 do livro01 a partir das artes geradas (rodapé padrão da coleção)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from criar_capa_livro01 import montar

IMGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

montar(os.path.join(IMGS, 'arte1_verbo.png'),
       os.path.join(ROOT, 'docs/capas/livro01_v5_arte1.png'),
       'O Verbo que Transforma', 'O Poder Criador da Palavra e da Fé')

montar(os.path.join(IMGS, 'arte2_verbo.png'),
       os.path.join(ROOT, 'docs/capas/livro01_v5_arte2.png'),
       'O Verbo que Transforma', 'O Poder Criador da Palavra e da Fé')

print('OK')
