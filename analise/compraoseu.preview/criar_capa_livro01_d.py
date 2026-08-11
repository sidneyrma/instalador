# -*- coding: utf-8 -*-
"""
Opção D: capa do livro01 usando a imagem 'images (4)' enviada pelo usuário
(restaurada do git). Remove os textos antigos (KYBALION, Os Sete Princípios
Herméticos, COLLECTIO OCCULTA) via inpaint e regrava o rodapé padrão.
"""
import os, sys
import numpy as np
import cv2
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from criar_capa_livro01 import montar

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
IMGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')

# Base: versão ampliada antiga (600x800) da mesma imagem
src = os.path.join(IMGS, 'capas_editadas', 'images (4)_capa.png')
img = cv2.imread(src)
h, w = img.shape[:2]
mask = np.zeros((h, w), dtype=np.uint8)

# regiões de texto antigo (do OCR, com folga)
# KYBALION (título grande) + subtítulo + selo
mask[628:702, 110:500] = 255
mask[700:748, 80:520] = 255
mask[742:776, 115:490] = 255
# número romano no topo (área ampla para garantir)
mask[40:110, 220:380] = 255

arte = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
out_arte = os.path.join(IMGS, 'images4_arte_limpa.png')
cv2.imwrite(out_arte, arte)
print('arte limpa:', out_arte)

montar(out_arte, os.path.join(ROOT, 'docs/capas/livro01_v5_arte3.png'),
       'O Verbo que Transforma', 'O Poder Criador da Palavra e da Fé')
