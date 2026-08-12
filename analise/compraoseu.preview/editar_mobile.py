# -*- coding: utf-8 -*-
"""
Edita o mockup mobile.jpg (3 celulares):
- Celular 1 (esquerda): capa atual -> Livro 05 (evolucaoolivro.png)
- Celular 2 (centro):   capa atual -> Livro 09 (anest9x16.png)
- Celular 3 (direita):  capa "Arquivo Secreto" -> Livro 07 (capa_despertar.png)
- Remove o texto "ARQUIVO SECRETO" (coberto pela capa nova)
- Adiciona "VideoAulas" em fonte menor abaixo dos dois primeiros celulares

Salva em analise/compraoseu.preview/imgs/mobile_editado.png (SEM tocar na Home).
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASE = '/tmp/mobile.jpg'
OUT = '/home/user/instalador/analise/compraoseu.preview/imgs/mobile_editado.png'
CAPA1 = '/tmp/evolucaoolivro.png'   # Livro 05
CAPA2 = '/tmp/anest9x16.png'        # Livro 09
CAPA3 = '/home/user/instalador/docs/capas/capa_despertar.png'  # Livro 07
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

img = Image.open(BASE).convert('RGB')
w, h = img.size
print("base:", img.size)

def colar_capa(capa_path, box, img):
    """Cola a capa preenchendo o box em modo COVER (crop central, sem distorcer)."""
    x0, y0, x1, y1 = box
    bw, bh = x1-x0, y1-y0
    capa = Image.open(capa_path).convert('RGB')
    cw, ch = capa.size
    # escala para cobrir
    escala = max(bw/cw, bh/ch)
    nw, nh = int(cw*escala)+1, int(ch*escala)+1
    capa = capa.resize((nw, nh), Image.LANCZOS)
    # crop central
    cx0, cy0 = (nw-bw)//2, (nh-bh)//2
    capa = capa.crop((cx0, cy0, cx0+bw, cy0+bh))
    img.paste(capa, (x0, y0))
    print(f"  colada capa em box={box}")

# Regiões das telas (estimadas pela análise de cores/OCR)
colar_capa(CAPA1, (38, 72, 216, 448), img)   # celular 1 (Livro 05)
colar_capa(CAPA2, (274, 72, 452, 430), img)  # celular 2 (Livro 09)
colar_capa(CAPA3, (450, 55, 596, 330), img)  # celular 3 (Livro 07) - cobre "Arquivo Secreto"

# Texto "VideoAulas" em fonte menor abaixo dos dois primeiros celulares
draw = ImageDraw.Draw(img)
f = ImageFont.truetype(FONT, 17)
cor = (30, 45, 80)  # navy escuro
for cx in (127, 363):
    texto = 'VideoAulas'
    bb = draw.textbbox((0,0), texto, font=f)
    tw = bb[2]-bb[0]
    draw.text((cx - tw/2, 490), texto, font=f, fill=cor)
    print(f"  'VideoAulas' em x={cx}")

img.save(OUT, quality=95)
print("Salvo:", OUT)
