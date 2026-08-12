# -*- coding: utf-8 -*-
"""
Gera a capa do Livro 10 — "O Despertar do Observador"
no estilo da Coleção do Despertar (navy + dourado, moldura, selo).
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
OUT_CAPA = os.path.join(ROOT, 'analise', 'compraoseu.preview', 'imgs', 'capas_editadas', 'livro10_capa.png')
OUT_DOCS = os.path.join(ROOT, 'docs', 'capas', 'livro10.png')

FONTE_TITULO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Bold.ttf')
FONTE_TEXTO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Regular.ttf')
FONTE_ITALICO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Italic.ttf')

OURO = (201, 162, 75)
OURO_CLARO = (227, 200, 119)
CREME = (238, 232, 218)
W, H = 600, 800


def fonte(path, size):
    return ImageFont.truetype(path, size)


def texto_tracked(draw, y, texto, font, fill, tracking, centro_x):
    widths = [draw.textlength(ch, font=font) for ch in texto]
    total = sum(widths) + tracking * (len(texto) - 1)
    x = centro_x - total / 2
    for ch, w in zip(texto, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def main():
    # Fundo: gradiente navy + brilho dourado central
    base = np.zeros((H, W, 3), dtype=np.float32)
    for yy in range(H):
        t = yy / H
        v = 8 + 6 * (1 - t)
        base[yy, :, :] = (v, v + 2, v + 10)
    brilho = Image.new('L', (W, H), 0)
    ImageDraw.Draw(brilho).ellipse([70, 60, 530, 460], fill=70)
    brilho = brilho.filter(ImageFilter.GaussianBlur(170))
    glow = np.zeros((H, W, 3), dtype=np.float32)
    for ch, val in zip(range(3), OURO_CLARO):
        glow[:, :, ch] = val * (np.array(brilho).astype(np.float32) / 255.0)
    base = np.clip(base + glow * 0.16, 0, 255).astype(np.uint8)
    capa = Image.fromarray(base)
    d = ImageDraw.Draw(capa)

    # Moldura dupla
    for inset in (14, 18):
        d.rectangle([inset, inset, W - 1 - inset, H - 1 - inset], outline=OURO, width=1)

    # Símbolo: olho/observador estilizado (círculo com pupila) em dourado
    cx, cy, r = W // 2, 230, 90
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=OURO, width=3)
    d.ellipse([cx - r + 22, cy - r + 22, cx + r - 22, cy + r - 22], outline=OURO, width=2)
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=OURO)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(14, 26, 46))

    # Filete decorativo
    d.line([W // 2 - 130, 470, W // 2 + 130, 470], fill=OURO, width=1)
    d.ellipse([W // 2 - 4, 466, W // 2 + 4, 474], outline=OURO, width=1)

    # Título
    f_titulo = fonte(FONTE_TITULO, 40)
    texto_tracked(d, 492, 'O DESPERTAR DO', f_titulo, OURO_CLARO, 2, W // 2)
    texto_tracked(d, 540, 'OBSERVADOR', f_titulo, OURO_CLARO, 2, W // 2)

    # Subtítulo
    f_sub = fonte(FONTE_ITALICO, 21)
    texto_tracked(d, 604, 'As Leis Invisíveis que Moldam a Realidade', f_sub, CREME, 0, W // 2)

    # Selo
    f_selo = fonte(FONTE_TEXTO, 15)
    texto_tracked(d, 726, 'C O L E Ç Ã O   D O   D E S P E R T A R', f_selo, OURO, 1, W // 2)

    os.makedirs(os.path.dirname(OUT_CAPA), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_DOCS), exist_ok=True)
    capa.save(OUT_CAPA)
    capa_web = capa.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    capa_web.save(OUT_DOCS, optimize=True)
    print('Capa salva:', OUT_CAPA, capa.size)
    print('Capa web:', OUT_DOCS, capa.size, f'({os.path.getsize(OUT_DOCS)//1024} KB)')


if __name__ == '__main__':
    main()
