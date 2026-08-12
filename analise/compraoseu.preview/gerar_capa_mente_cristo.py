# -*- coding: utf-8 -*-
"""
Edição melhorada da capa de "A Mente de Cristo" (livro/A Mente de Cristo.png, 368x470).

Melhorias aplicadas:
  1. Crop central para 3:4 (600x800) — sem cortar o título "A MENTE DE CRISTO".
  2. Upscale LANCZOS + nitidez (Unsharp Mask) para compensar a resolução pequena.
  3. Realce de brilho, contraste e saturação (a original é escura, média ~40).
  4. Vinheta suave nas bordas (padrão da coleção).
  5. Faixa navy translúcida na base para destacar o título original.
  6. Selo "COLEÇÃO DO DESPERTAR" dourado no topo (identidade da coleção).
  7. Moldura dourada dupla (padrão das demais capas).
  8. Otimização web: PNG-8 (256 cores) em docs/capas/mente_cristo.png.

Saídas:
  - analise/compraoseu.preview/imgs/capas_editadas/mente_cristo_capa.png (600x800, PNG)
  - docs/capas/mente_cristo.png (600x800, PNG-8 otimizado p/ GitHub Pages)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SRC = os.path.join(ROOT, 'livro', 'A Mente de Cristo.png')
OUT_CAPA = os.path.join(ROOT, 'analise', 'compraoseu.preview', 'imgs', 'capas_editadas', 'mente_cristo_capa.png')
OUT_DOCS = os.path.join(ROOT, 'docs', 'capas', 'mente_cristo.png')

FONTE_TEXTO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Regular.ttf')
FONTE_TITULO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Bold.ttf')

OURO = (201, 162, 75)
OURO_CLARO = (227, 200, 119)
W, H = 600, 800


def desenha_selo(img):
    """Selo 'COLEÇÃO DO DESPERTAR' centralizado no topo, com sombra."""
    d = ImageDraw.Draw(img, 'RGBA')
    try:
        f = ImageFont.truetype(FONTE_TEXTO, 15)
    except Exception:
        f = ImageFont.load_default()
    texto = "C O L E Ç Ã O   D O   D E S P E R T A R"
    # sombra
    bbox = d.textbbox((0, 0), texto, font=f)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    d.text((x + 1, 33), texto, font=f, fill=(0, 0, 0, 170))
    d.text((x, 32), texto, font=f, fill=OURO_CLARO + (255,))
    return img


def main():
    im = Image.open(SRC).convert('RGB')
    sw, sh = im.size

    # --- 1) crop central 3:4 ---
    escala = max(W / sw, H / sh)
    nw, nh = round(sw * escala), round(sh * escala)
    im2 = im.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - W) // 2
    y0 = (nh - H) // 2
    capa = im2.crop((x0, y0, x0 + W, y0 + H))

    # --- 2) nitidez e realce ---
    capa = capa.filter(ImageFilter.UnsharpMask(radius=2.2, percent=105, threshold=3))
    capa = ImageEnhance.Brightness(capa).enhance(1.12)
    capa = ImageEnhance.Contrast(capa).enhance(1.10)
    capa = ImageEnhance.Color(capa).enhance(1.12)

    # --- 3) vinheta suave ---
    arr = np.array(capa).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    dx = (xx - W / 2) / (W / 2)
    dy = (yy - H / 2) / (H / 2)
    d = np.sqrt(dx * dx + dy * dy)
    vign = np.clip(1.0 - 0.32 * np.clip(d - 0.5, 0, None) ** 1.4, 0.55, 1.0)
    for ch in range(3):
        arr[:, :, ch] *= vign
    capa = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

    # --- 4) faixa navy translúcida na base (destaca o título original) ---
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d_ov = ImageDraw.Draw(overlay)
    d_ov.rectangle([0, H - 150, W, H - 22], fill=(14, 26, 46, 135))
    capa = Image.alpha_composite(capa.convert('RGBA'), overlay).convert('RGB')

    # --- 5) selo no topo ---
    capa = desenha_selo(capa)

    # --- 6) moldura dourada dupla ---
    d = ImageDraw.Draw(capa)
    for inset in (12, 16):
        d.rectangle([inset, inset, W - 1 - inset, H - 1 - inset], outline=OURO, width=1)

    # --- 7) salvar ---
    os.makedirs(os.path.dirname(OUT_CAPA), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_DOCS), exist_ok=True)
    capa.save(OUT_CAPA)
    capa_web = capa.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                             dither=Image.Dither.FLOYDSTEINBERG)
    capa_web.save(OUT_DOCS, optimize=True)
    print('Capa melhorada:', OUT_CAPA, capa.size)
    print('Capa web:', OUT_DOCS, capa.size, f'({os.path.getsize(OUT_DOCS)//1024} KB)')


if __name__ == '__main__':
    main()
