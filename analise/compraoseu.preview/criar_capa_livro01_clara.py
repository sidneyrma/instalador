# -*- coding: utf-8 -*-
"""
Capa CLARA do livro01 usando a imagem 'images (4)' (livro com símbolos).
- clareia a arte (gamma + brilho) para o livro aparecer
- amplia para 600x600 (interpolação cúbica + nitidez)
- canvas 600x800 com fundo desfocado
- rodapé com faixa suave e textos da coleção (SEM vinheta escura)
"""
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
IMGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')
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
        d.text((x + 2, y + 2), texto, font=font, fill=(0, 0, 0, 160))
    d.text((x, y), texto, font=font, fill=fill)
    return w

# --- 1) arte clara ---
src = os.path.join(IMGS, 'images (4).jfif')
img = cv2.imread(src)
# clareia: gamma < 1 clareia sombras
imgf = img.astype(np.float32) / 255.0
imgf = np.power(imgf, 0.62)          # gamma
imgf = imgf * 1.18                   # brilho
imgf = (imgf - 0.5) * 1.12 + 0.5     # contraste
imgf = np.clip(imgf, 0, 1) * 255
img = imgf.astype(np.uint8)
# upscale para 600x600
arte = cv2.resize(img, (600, 600), interpolation=cv2.INTER_CUBIC)
arte = cv2.GaussianBlur(arte, (0, 0), 0.6)
arte = cv2.addWeighted(arte, 1.35, cv2.GaussianBlur(arte, (0, 0), 2.2), -0.35, 0)  # nitidez
cv2.imwrite(os.path.join(IMGS, 'livro01_arte_usuario_clara.png'), arte)

# --- 2) canvas 600x800 com fundo desfocado ---
fundo = cv2.resize(img, (600, 800), interpolation=cv2.INTER_CUBIC)
fundo = cv2.GaussianBlur(fundo, (21, 21), 0)
fundo = np.clip(fundo.astype(np.float32) * 0.65, 0, 255).astype(np.uint8)
canvas = fundo.copy()
y0 = 90
canvas[y0:y0+600, 0:600] = arte

pil = Image.fromarray(canvas).convert('RGB')

# --- 3) faixa suave no rodapé (gradiente) ---
overlay = Image.new('RGBA', pil.size, (0, 0, 0, 0))
d_o = ImageDraw.Draw(overlay)
for i, alpha in enumerate(range(0, 130, 10)):
    d_o.rectangle([0, 620 + i * 4, 600, 624 + i * 4], fill=(12, 22, 40, alpha))
for i, alpha in enumerate(range(130, 0, -10)):
    d_o.rectangle([0, 700 + i * 4, 600, 704 + i * 4], fill=(12, 22, 40, alpha))
pil = Image.alpha_composite(pil.convert('RGBA'), overlay)
draw = ImageDraw.Draw(pil)

# --- 4) textos ---
f_num = ImageFont.truetype(FONT_BOLD, 26)
centralizar(draw, 600, 26, 'I', f_num, GOLD_CLARO)

f_od = ImageFont.truetype(FONT_BOLD, 42)
centralizar(draw, 600, 642, 'O DESPERTAR', f_od, GOLD)

draw.line([(600//2 - 150, 696), (600//2 + 150, 696)], fill=GOLD, width=2)

f_tit = ImageFont.truetype(FONT_BOLD, 30)
while f_tit.size > 17:
    if draw.textlength('O Verbo que Transforma', font=f_tit) <= 600 * 0.88:
        break
    f_tit = ImageFont.truetype(FONT_BOLD, f_tit.size - 2)
centralizar(draw, 600, 708, 'O Verbo que Transforma', f_tit, (248, 248, 248, 255))

f_sub = ImageFont.truetype(FONT_REG, 17)
centralizar(draw, 600, 742, 'O Poder Criador da Palavra e da Fé', f_sub, GOLD_CLARO)

f_selo = ImageFont.truetype(FONT_REG, 14)
texto_tracked(draw, 766, 'COLEÇÃO DO DESPERTAR', f_selo, GOLD_CLARO, 5, 600 // 2)

# borda dourada
d = ImageDraw.Draw(pil)
d.rectangle([6, 6, 593, 793], outline=GOLD, width=2)
d.rectangle([14, 14, 585, 785], outline=(150, 120, 50, 255), width=1)

out = os.path.join(ROOT, 'docs/capas/livro01_v5_clara.png')
pil.convert('RGB').save(out, quality=95)
print('salvo:', out)
