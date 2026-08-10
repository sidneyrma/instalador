# -*- coding: utf-8 -*-
"""Gera favicons da marca (azul-marinho + cruz dourada) em 16px, 32px e SVG."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path('/home/user/instalador/analise/seo/favicon')
OUT.mkdir(parents=True, exist_ok=True)

NAVY = (14, 26, 46, 255)        # #0e1a2e
GOLD = (201, 162, 75, 255)      # #c9a24b
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def desenhar(tamanho):
    img = Image.new('RGBA', (tamanho, tamanho), NAVY)
    d = ImageDraw.Draw(img)
    # borda dourada fina
    b = max(1, tamanho // 16)
    d.rectangle([b, b, tamanho - b - 1, tamanho - b - 1], outline=GOLD, width=b)
    # cruz dourada central
    cx = tamanho // 2
    cy = tamanho // 2
    v = max(2, tamanho // 8)      # espessura
    h = int(tamanho * 0.44)       # altura/braço
    d.rectangle([cx - v // 2, cy - h, cx + v // 2, cy + h], fill=GOLD)
    d.rectangle([cx - h, cy - v // 2, cx + h, cy + v // 2], fill=GOLD)
    return img

for t in (16, 32):
    img = desenhar(t)
    img.save(OUT / f'favicon-{t}.png')
    print(f'favicon-{t}.png OK')

# 32px também como favicon.ico (Pillow grava ico)
desenhar(32).save(OUT / 'favicon.ico', format='ICO', sizes=[(32, 32)])
print('favicon.ico OK')

# SVG
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="10" fill="#0e1a2e"/>
  <rect x="2" y="2" width="60" height="60" rx="8" fill="none" stroke="#c9a24b" stroke-width="2"/>
  <rect x="28" y="12" width="8" height="40" fill="#c9a24b"/>
  <rect x="12" y="28" width="40" height="8" fill="#c9a24b"/>
</svg>'''
(OUT / 'favicon.svg').write_text(svg, encoding='utf-8')
print('favicon.svg OK')

# Prévia 64px para o usuário ver
desenhar(64).save('/home/user/instalador/analise/seo/favicon-preview.png')
print('preview 64px OK')
print('Arquivos:', sorted(p.name for p in OUT.iterdir()))
