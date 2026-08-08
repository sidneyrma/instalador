# -*- coding: utf-8 -*-
"""
Prepara a capa de "A Mente de Cristo" (livro/A Mente de Cristo.png, 368x470)
para o padrão da coleção: 600x800 (3:4), com moldura dourada e otimização web.

Saídas:
  - analise/compraoseu.preview/imgs/capas_editadas/mente_cristo_capa.png (600x800)
  - docs/capas/mente_cristo.png (600x800, PNG-8 otimizado p/ GitHub Pages)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SRC = os.path.join(ROOT, 'livro', 'A Mente de Cristo.png')
OUT_CAPA = os.path.join(ROOT, 'analise', 'compraoseu.preview', 'imgs', 'capas_editadas', 'mente_cristo_capa.png')
OUT_DOCS = os.path.join(ROOT, 'docs', 'capas', 'mente_cristo.png')

OURO = (201, 162, 75)
W, H = 600, 800


def main():
    im = Image.open(SRC).convert('RGB')
    sw, sh = im.size
    # cover-crop para 3:4
    escala = max(W / sw, H / sh)
    nw, nh = round(sw * escala), round(sh * escala)
    im2 = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - W) // 2
    y0 = (nh - H) // 2
    capa = im2.crop((x0, y0, x0 + W, y0 + H))

    # leve escurecimento nas bordas (vinheta) para integrar com o fundo da coleção
    arr = np.array(capa).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    dx = (xx - W / 2) / (W / 2)
    dy = (yy - H / 2) / (H / 2)
    d = np.sqrt(dx * dx + dy * dy)
    vign = np.clip(1.0 - 0.30 * np.clip(d - 0.55, 0, None) ** 1.4, 0.55, 1.0)
    for ch in range(3):
        arr[:, :, ch] *= vign
    capa = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    # moldura dourada dupla (padrão da coleção)
    d = ImageDraw.Draw(capa)
    for inset in (12, 16):
        d.rectangle([inset, inset, W - 1 - inset, H - 1 - inset], outline=OURO, width=1)

    os.makedirs(os.path.dirname(OUT_CAPA), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_DOCS), exist_ok=True)
    capa.save(OUT_CAPA)
    capa_web = capa.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    capa_web.save(OUT_DOCS, optimize=True)
    print('Capa salva:', OUT_CAPA, capa.size)
    print('Capa web:', OUT_DOCS, capa.size, f"({os.path.getsize(OUT_DOCS)//1024} KB)")


if __name__ == '__main__':
    main()
