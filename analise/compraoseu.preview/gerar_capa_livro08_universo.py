# -*- coding: utf-8 -*-
"""
Gera a capa v2 do Livro 08 — "Você e o Universo · O Inconsciente e as suas Criações"
com a imagem da imensidão do universo (galáxia espiral) gerada por IA.

Motivação: a capa anterior usava a arte do vídeo com o texto "Reality Does Not Exist",
que é contrário à mensagem do livro ("todos criamos realidades em nossas mentes,
existentes ou não — e elas nos moldam"). Esta capa transmite o vasto campo de
possibilidades que a mente observa e cria.

Saídas:
  - analise/compraoseu.preview/imgs/capas_editadas/08_capa.png   (600x800)
  - docs/capas/livro08.png                                       (600x800, p/ GitHub Pages)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
ARTE = os.path.join(ROOT, 'analise', 'compraoseu.preview', 'imgs', 'capas_editadas', '08_universo_raw.png')
OUT_CAPA = os.path.join(ROOT, 'analise', 'compraoseu.preview', 'imgs', 'capas_editadas', '08_capa.png')
OUT_DOCS = os.path.join(ROOT, 'docs', 'capas', 'livro08.png')

FONTE_TITULO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Bold.ttf')
FONTE_TEXTO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Regular.ttf')
FONTE_ITALICO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Italic.ttf')

OURO = (201, 162, 75)
OURO_CLARO = (227, 200, 119)
CREME = (238, 232, 218)
PRETO = (4, 6, 12)

W, H = 600, 800


def fonte(path, size):
    return ImageFont.truetype(path, size)


def desenha_texto_centralizado(draw, cy, text, font, fill, tracking=0, center_x=W // 2):
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = center_x - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, cy), ch, font=font, fill=fill)
        x += w + tracking


def main():
    # ---------------------------------------------------------------
    # 1) Fundo: universo 600x800 (cover a partir da imagem 3:4)
    # ---------------------------------------------------------------
    arte = Image.open(ARTE).convert('RGB')
    arte = ImageEnhance.Color(arte).enhance(1.15)
    # já é 3:4 (896x1200) -> redimensiona direto
    capa = arte.resize((W, H), Image.LANCZOS)
    base = np.array(capa).astype(np.float32)

    # 2) Vinheta suave: escurece bordas (foco no centro da galáxia)
    vigneta = np.ones((H, W), dtype=np.float32)
    yy, xx = np.mgrid[0:H, 0:W]
    # distância normalizada a partir do centro
    dx = (xx - W / 2) / (W / 2)
    dy = (yy - H / 2) / (H / 2)
    d = np.sqrt(dx * dx + dy * dy)
    vigneta = np.clip(1.0 - 0.42 * np.clip(d - 0.35, 0, None) ** 1.5, 0.45, 1.0)
    for ch in range(3):
        base[:, :, ch] *= vigneta

    # 3) Fade escuro no topo e na base (contraste p/ selo e título)
    for yy2 in range(0, 200):
        t = yy2 / 200
        fade = 0.55 * t
        base[yy2, :, :] *= (1 - fade)
    for yy2 in range(H - 260, H):
        t = (yy2 - (H - 260)) / 260
        fade = 0.72 * t
        base[yy2, :, :] *= (1 - fade)

    capa = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(capa)

    # ---------------------------------------------------------------
    # 4) Moldura dourada dupla
    # ---------------------------------------------------------------
    for inset in (14, 18):
        d.rectangle([inset, inset, W - 1 - inset, H - 1 - inset], outline=OURO, width=1)

    # ---------------------------------------------------------------
    # 5) Textos
    # ---------------------------------------------------------------
    # Filete decorativo (acima do título)
    d.line([W // 2 - 130, 588, W // 2 + 130, 588], fill=OURO, width=1)
    d.ellipse([W // 2 - 4, 584, W // 2 + 4, 592], outline=OURO, width=1)

    f_titulo = fonte(FONTE_TITULO, 46)
    desenha_texto_centralizado(d, 606, 'VOCÊ E O UNIVERSO', f_titulo, OURO_CLARO, tracking=2)

    f_sub = fonte(FONTE_ITALICO, 23)
    desenha_texto_centralizado(d, 668, 'O Inconsciente e as suas Criações', f_sub, CREME)

    f_selo = fonte(FONTE_TEXTO, 15)
    desenha_texto_centralizado(d, 728, 'C O L L E C T I O   O C C U L T A', f_selo, OURO, tracking=1)

    # ---------------------------------------------------------------
    # 6) Salvar
    # ---------------------------------------------------------------
    os.makedirs(os.path.dirname(OUT_CAPA), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_DOCS), exist_ok=True)
    capa.save(OUT_CAPA)
    # Versão otimizada (PNG-8, 256 cores) para o GitHub Pages — ~60% menor,
    # diferença visual imperceptível, no mesmo patamar das outras capas da coleção.
    capa_web = capa.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                             dither=Image.Dither.FLOYDSTEINBERG)
    capa_web.save(OUT_DOCS, optimize=True)
    print('Capa universo salva:', OUT_CAPA, capa.size)
    print('Capa p/ GitHub Pages (otimizada):', OUT_DOCS, capa.size)


if __name__ == '__main__':
    main()
