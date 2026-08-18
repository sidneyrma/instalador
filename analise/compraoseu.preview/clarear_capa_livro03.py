# -*- coding: utf-8 -*-
"""
Clareia a capa do livro03 'A Mente Renovada' (docs/capas/livro03.png).
- Clareia fortemente a área da arte (y < 620) com gamma + brilho + contraste
- Reconstrói o rodapé (y >= 620) no padrão da coleção com textos dourados
Valida o resultado com métricas de brilho.
"""
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
FONT_REG = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Regular.ttf')
FONT_BOLD = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Bold.ttf')
GOLD = (212, 168, 63, 255)
GOLD_CLARO = (230, 205, 130, 255)

def texto_tracked(d, y, texto, font, fill, tracking, centro_x):
    widths = [d.textlength(ch, font=font) for ch in texto]
    total = sum(widths) + tracking * (len(texto) - 1)
    x = centro_x - total / 2
    for ch, w in zip(texto, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += w + tracking

def centralizar(d, img_w, y, texto, font, fill, sombra=True):
    bbox = d.textbbox((0, 0), texto, font=font)
    w = bbox[2] - bbox[0]
    x = (img_w - w) // 2
    if sombra:
        d.text((x + 2, y + 2), texto, font=font, fill=(0, 0, 0, 170))
    d.text((x, y), texto, font=font, fill=fill)
    return w

# 1) Abrir
img = Image.open(os.path.join(ROOT, 'docs/capas/livro03.png')).convert('RGB')
arr = np.array(img).astype(np.float32)

# 2) Clarear a área da arte (toda a imagem primeiro, depois reconstruir rodapé)
# gamma forte para abrir as sombras
arr = np.power(arr / 255.0, 0.24)
arr = arr * 1.8           # brilho
arr = (arr - 0.5) * 1.42 + 0.5  # contraste
arr = np.clip(arr, 0, 1) * 255
img_clara = arr.astype(np.uint8)

# 3) Reconstruir o rodapé (y 620-800) com fundo navy e textos
pil = Image.fromarray(img_clara).convert('RGBA')
draw = ImageDraw.Draw(pil)

# fundo navy do rodapé com leve gradiente
for y in range(620, 800):
    t = (y - 620) / 180.0
    navy = (14 + int(6*t), 26 + int(10*t), 46 + int(16*t))
    draw.line([(0, y), (600, y)], fill=navy + (255,))

# número romano no topo (acima do rodapé, discreto) — na verdade 'I' já foi perdido; recolocar
f_num = ImageFont.truetype(FONT_BOLD, 26)
centralizar(draw, 600, 22, 'I', f_num, GOLD_CLARO)

# título grande 'O DESPERTAR'
f_od = ImageFont.truetype(FONT_BOLD, 42)
centralizar(draw, 600, 636, 'O DESPERTAR', f_od, GOLD)

# divisor dourado
draw.line([(600//2 - 150, 692), (600//2 + 150, 692)], fill=GOLD, width=2)

# título do livro
f_tit = ImageFont.truetype(FONT_BOLD, 30)
while f_tit.size > 17:
    if draw.textlength('A Mente Renovada', font=f_tit) <= 600 * 0.88:
        break
    f_tit = ImageFont.truetype(FONT_BOLD, f_tit.size - 2)
centralizar(draw, 600, 704, 'A Mente Renovada', f_tit, (250, 250, 250, 255))

# subtítulo
f_sub = ImageFont.truetype(FONT_REG, 17)
centralizar(draw, 600, 740, 'O Pensar com Cristo que Transforma a Vida', f_sub, GOLD_CLARO)

# selo COLEÇÃO DO DESPERTAR
f_selo = ImageFont.truetype(FONT_REG, 14)
texto_tracked(draw, 764, 'COLEÇÃO DO DESPERTAR', f_selo, GOLD_CLARO, 5, 600 // 2)

# borda dourada dupla
d = ImageDraw.Draw(pil)
d.rectangle([6, 6, 593, 793], outline=GOLD, width=2)
d.rectangle([14, 14, 585, 785], outline=(150, 120, 50, 255), width=1)

out = os.path.join(ROOT, 'docs/capas/livro03.png')
pil.convert('RGB').save(out, quality=95)
print('Salvo:', out)

# 4) Validar
arr2 = np.array(Image.open(out).convert('RGB'))
print("Brilho médio total:", round(float(arr2.mean()),1))
print("Brilho área do livro (y85-620):", round(float(arr2[85:620,0:600].mean()),1))
print("Brilho rodapé (y620-800):", round(float(arr2[620:800,0:600].mean()),1))
