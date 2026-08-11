# -*- coding: utf-8 -*-
"""
Gera os ícones do PWA a partir da opção A escolhida (livro aberto com luz).

Ícones gerados em docs/icones/ (servidos pelo GitHub Pages):
  - icon-192.png            (192x192, purpose: any)
  - icon-512.png            (512x512, purpose: any)
  - icon-512-maskable.png   (512x512, purpose: maskable, com área segura 80%)
  - apple-touch-icon.png    (180x180, iOS)
  - favicon.png             (64x64, opcional)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
SRC = os.path.join(ROOT, 'analise', 'compraoseu.preview', 'pwa', 'opcao_A_livro.png')
OUT_DIR = os.path.join(ROOT, 'docs', 'icones')

NAVY = (14, 26, 46)


def recortar_centro(im, alvo):
    """Recorta o quadrado central (cover) e redimensiona para alvo x alvo."""
    w, h = im.size
    lado = min(w, h)
    x0 = (w - lado) // 2
    y0 = (h - lado) // 2
    im = im.crop((x0, y0, x0 + lado, y0 + lado))
    return im.resize((alvo, alvo), Image.LANCZOS)


def preencher_maskable(im, alvo):
    """
    Gera ícone maskable: o desenho fica dentro da área segura central (80%),
    e o fundo navy se estende até as bordas (para o recorte circular do Android).
    """
    # pega o quadrado central da arte original (90% para dar folga) e reduz p/ 80%
    w, h = im.size
    lado = int(min(w, h) * 0.90)
    x0 = (w - lado) // 2
    y0 = (h - lado) // 2
    arte = im.crop((x0, y0, x0 + lado, y0 + lado)).resize((int(alvo*0.78), int(alvo*0.78)), Image.LANCZOS)

    # tela com fundo navy
    icon = Image.new('RGBA', (alvo, alvo), NAVY + (255,))
    # aplica leve vinheta/difusão para integrar
    arte = arte.filter(ImageFilter.GaussianBlur(0.6))
    x = (alvo - arte.width) // 2
    y = (alvo - arte.height) // 2
    icon.paste(arte, (x, y), arte)
    return icon.convert('RGB')


def main():
    im = Image.open(SRC).convert('RGBA')
    os.makedirs(OUT_DIR, exist_ok=True)

    # any
    for alvo, nome in [(192, 'icon-192.png'), (512, 'icon-512.png')]:
        icone = recortar_centro(im, alvo).convert('RGB')
        icone.save(os.path.join(OUT_DIR, nome), optimize=True)
        print(f'✔ {nome} ({alvo}x{alvo})')

    # maskable
    icone = preencher_maskable(im, 512)
    icone.save(os.path.join(OUT_DIR, 'icon-512-maskable.png'), optimize=True)
    print('✔ icon-512-maskable.png (512x512)')

    # apple touch (180) — sem cantos transparentes (iOS exige quadrado preenchido)
    icone = recortar_centro(im, 180).convert('RGB')
    icone.save(os.path.join(OUT_DIR, 'apple-touch-icon.png'), optimize=True)
    print('✔ apple-touch-icon.png (180x180)')

    # favicon 64
    icone = recortar_centro(im, 64).convert('RGB')
    icone.save(os.path.join(OUT_DIR, 'favicon.png'), optimize=True)
    print('✔ favicon.png (64x64)')

    print('\nPronto! Ícones em:', OUT_DIR)


if __name__ == '__main__':
    main()
