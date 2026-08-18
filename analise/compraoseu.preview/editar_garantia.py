# -*- coding: utf-8 -*-
"""
Edita a imagem da garantia (garantia.jpg): substitui "14 dias" por "7 dias".
- Título dourado: "GARANTIA INCONDICIONAL DE 14 DIAS" -> "7 DIAS"
- Corpo branco: "Teste por 14 dias sem risco." -> "7 dias"
Mantém estilo/fonte aproximada (serif para título, sans para corpo).
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = '/tmp/garantia.jpg'
OUT = '/home/user/instalador/analise/compraoseu.preview/imgs/garantia_editada.jpg'

img = Image.open(BASE).convert('RGB')
w, h = img.size
print("base:", img.size)

F_SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
F_SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def pintar_e_desenhar(box, texto, fonte_path, cor_texto, tam_texto, cor_fundo=None):
    """Pinta o box com cor_fundo (ou média local) e desenha texto centralizado."""
    x0, y0, x1, y1 = box
    # cor de fundo: média das bordas (ou parâmetro)
    arr = np.array(img.convert('RGB'))
    if cor_fundo is None:
        margens = np.concatenate([arr[y0:y1, max(0,x0-6):x0].reshape(-1,3),
                                  arr[y0:y1, x1:min(w,x1+6)].reshape(-1,3)])
        cf = tuple(int(v) for v in margens.mean(axis=0))
    else:
        cf = cor_fundo
    # pinta
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], fill=cf)
    # desenha texto
    font = ImageFont.truetype(fonte_path, tam_texto)
    bb = d.textbbox((0, 0), texto, font=font)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    tx = x0 + (x1-x0-tw)/2 - bb[0]
    ty = y0 + (y1-y0-th)/2 - bb[1]
    d.text((tx, ty), texto, font=font, fill=cor_texto)
    print(f"  box={box} cor_fundo={cf} texto='{texto}'")

# 1) Título: "14" em x≈705-741, y≈63-91
pintar_e_desenhar((696, 62, 752, 92), '7', F_SERIF, (150, 128, 130), 30,
                  cor_fundo=(50, 20, 23))

# 2) "Teste por 14": "14" em x≈598-696, y≈149-225
pintar_e_desenhar((590, 150, 705, 226), '7', F_SANS, (245, 243, 243), 78,
                  cor_fundo=(48, 18, 21))

img.save(OUT, quality=95)
print("Salvo:", OUT)
