# -*- coding: utf-8 -*-
"""Regrava a capa do livro03 com o novo título 'A Mente Renovada'.
Usa a arte da capa atual (mente_cristo.png) e regrava o rodapé no padrão da coleção."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from criar_capa_livro01 import montar

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
ARTE = os.path.join(ROOT, 'docs', 'capas', 'mente_cristo.png')

montar(ARTE,
       os.path.join(ROOT, 'docs', 'capas', 'livro03.png'),
       'A Mente Renovada', 'O Pensar com Cristo que Transforma a Vida')
print('OK capa livro03')
