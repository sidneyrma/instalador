# -*- coding: utf-8 -*-
"""
Opção A: limpa a capa atual do livro01 removendo o texto antigo
'GRIMÓRIO SECRETO DE PRÁTICAS ANTIGAS' (região central) via inpaint
e regrava o rodapé no padrão da coleção (como livro02).
"""
import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
FONT_REG = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Regular.ttf')
FONT_BOLD = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Bold.ttf')

GOLD = (212, 168, 63, 255)
GOLD_CLARO = (227, 200, 119, 255)

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

def montar(arte_path, saida, titulo, sub):
    img = Image.open(arte_path).convert('RGB')
    w, h = img.size
    # garante 600x800 com crop central
    if (w, h) != (600, 800):
        escala = max(600 / w, 800 / h)
        nw, nh = int(w * escala) + 1, int(h * escala) + 1
        img = img.resize((nw, nh), Image.LANCZOS)
        x0 = (nw - 600) // 2
        y0 = (nh - 800) // 2
        img = img.crop((x0, y0, x0 + 600, y0 + 800))
    w, h = img.size  # atualiza para as dimensões finais (600x800)

    # vinheta suave para texto destacar
    mask = Image.new('L', img.size, 0)
    dm = ImageDraw.Draw(mask)
    for i in range(120, 0, -2):
        a = int(55 * (i / 120))
        dm.ellipse([300 - 300*i/240, 400 - 400*i/240, 300 + 300*i/240, 400 + 400*i/240], fill=a)
    preto = Image.new('RGB', img.size, (0, 0, 0))
    img = Image.composite(img, preto, mask)

    # faixas navy translúcidas no rodapé para legibilidade
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d_o = ImageDraw.Draw(overlay)
    d_o.rectangle([0, 620, w, 790], fill=(14, 26, 46, 150))
    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    draw = ImageDraw.Draw(img)

    # número romano no topo
    f_num = ImageFont.truetype(FONT_BOLD, 30)
    centralizar(draw, w, 24, 'I', f_num, GOLD_CLARO)

    # título grande "O DESPERTAR"
    f_od = ImageFont.truetype(FONT_BOLD, 44)
    centralizar(draw, w, 636, 'O DESPERTAR', f_od, GOLD)

    # divisor dourado
    larg = 160
    draw.line([(300 - larg//2, 692), (300 + larg//2, 692)], fill=GOLD, width=2)

    # título do livro (branco, grande)
    f_tit = ImageFont.truetype(FONT_BOLD, 30)
    while f_tit.size > 18:
        if draw.textlength(titulo, font=f_tit) <= w * 0.88:
            break
        f_tit = ImageFont.truetype(FONT_BOLD, f_tit.size - 2)
    centralizar(draw, w, 704, titulo, f_tit, (245, 245, 245, 255))

    # subtítulo (dourado, itálico/regular menor)
    f_sub = ImageFont.truetype(FONT_REG, 17)
    centralizar(draw, w, 738, sub, f_sub, GOLD_CLARO)

    # selo COLEÇÃO DO DESPERTAR
    f_selo = ImageFont.truetype(FONT_REG, 14)
    texto_tracked(draw, 762, 'COLEÇÃO DO DESPERTAR', f_selo, GOLD_CLARO, 5, w // 2)

    # borda dourada dupla
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, w - 7, h - 7], outline=GOLD, width=2)
    d.rectangle([14, 14, w - 15, h - 15], outline=(150, 120, 50, 255), width=1)

    img.convert('RGB').save(saida, quality=95)
    print('salvo:', saida, img.size)

if __name__ == '__main__':
    # --- Passo 1: inpaint removendo o texto central ---
    src = os.path.join(ROOT, 'docs/capas/livro01.png')
    out_arte = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs', 'livro01_arte_limpa.png')
    img = cv2.imread(src)
    h, w = img.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    # região do texto GRIMÓRIO... (do OCR, com folga)
    mask[138:462, 130:540] = 255
    # preenche também o rodapé atual (será regravado)
    mask[600:800, 100:520] = 255
    arte = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
    cv2.imwrite(out_arte, arte)
    print('arte limpa:', out_arte)

    montar(out_arte, os.path.join(ROOT, 'docs/capas/livro01_v5_limpa.png'),
           'O Verbo que Transforma', 'O Poder Criador da Palavra e da Fé')
