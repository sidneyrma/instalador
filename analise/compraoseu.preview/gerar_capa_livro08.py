# -*- coding: utf-8 -*-
"""
Gera a capa do Livro 08 — "Você e o Universo · O Inconsciente e as suas Criações"
a partir da screenshot do YouTube (livro/Screenshot_20260808-115400_YouTube.jpg).

Edições aplicadas:
  1. Remove os escritos vermelhos/brancos cortados na borda direita ("QUA/DES/NAC").
  2. Ajusta para as dimensões padrão da coleção (600x800, proporção 3:4).
  3. Composição no estilo das capas místicas: fundo escuro, moldura dourada,
     arte central, título em serifa dourada e selo COLEÇÃO DO DESPERTAR.

Saídas:
  - analise/compraoseu.preview/imgs/capas_editadas/08_capa.png   (600x800)
  - docs/capas/livro08.png                                       (600x800, p/ GitHub Pages)
  - analise/compraoseu.preview/imgs/capas_editadas/08_arte_limpa.png (arte extraída)
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, ImageEnhance

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
SRC = os.path.join(ROOT, 'livro', 'Screenshot_20260808-115400_YouTube.jpg')
OUT_CAPA = os.path.join(ROOT, 'analise', 'compraoseu.preview', 'imgs', 'capas_editadas', '08_capa.png')
OUT_DOCS = os.path.join(ROOT, 'docs', 'capas', 'livro08.png')
OUT_ARTE = os.path.join(ROOT, 'analise', 'compraoseu.preview', 'imgs', 'capas_editadas', '08_arte_limpa.png')

FONTE_TITULO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Bold.ttf')
FONTE_TEXTO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Regular.ttf')
FONTE_ITALICO = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Italic.ttf')

OURO = (201, 162, 75)
OURO_CLARO = (227, 200, 119)
CREME = (238, 232, 218)
PRETO = (7, 9, 15)


def fonte(path, size):
    return ImageFont.truetype(path, size)


def texto_tracked(draw, xy, text, font, fill, tracking=0, anchor_center_x=None):
    """Desenha texto com espaçamento manual (letter-spacing)."""
    x0, y0 = xy
    if tracking == 0:
        if anchor_center_x is not None:
            bbox = draw.textbbox((0, 0), text, font=font)
            w = bbox[2] - bbox[0]
            x0 = anchor_center_x - w / 2
        draw.text((x0, y0), text, font=font, fill=fill)
        return
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    if anchor_center_x is not None:
        x0 = anchor_center_x - total / 2
    for ch, w in zip(text, widths):
        draw.text((x0, y0), ch, font=font, fill=fill)
        x0 += w + tracking


def desenha_texto_centralizado(draw, cy, text, font, fill, tracking=0):
    """Centraliza em (300, cy)."""
    texto_tracked(draw, (0, cy), text, font, fill, tracking=tracking, anchor_center_x=300)


def main():
    im = Image.open(SRC).convert('RGB')
    arr = np.array(im).astype(int)

    # ---------------------------------------------------------------
    # 1) Limpeza: apaga o bloco de escritos cortados da borda direita
    # ---------------------------------------------------------------
    # A pilha de texto ("QUA..." branco, "DES..."/"NAC..." vermelhos) vive em
    # x ~450-590, y ~130-420. Substituímos por uma cor escura amostrada das
    # bordas da região para se misturar com o fundo.
    x0, y0, x1, y1 = 445, 125, 590, 425
    borda = np.concatenate([
        arr[y0:y1, x0:x0 + 4].reshape(-1, 3),
        arr[y0:y1, x1 - 4:x1].reshape(-1, 3),
        arr[y0:y0 + 4, x0:x1].reshape(-1, 3),
    ])
    cor_fundo = np.median(borda, axis=0).astype(int)
    arr[y0:y1, x0:x1] = cor_fundo

    # Suaviza as bordas da área limpa para não deixar corte visível
    limpo = Image.fromarray(arr.astype(np.uint8))
    mask = Image.new('L', limpo.size, 0)
    ImageDraw.Draw(mask).rectangle([x0, y0, x1, y1], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(14))
    arr2 = np.array(limpo).astype(int)
    m = np.array(mask).astype(float)[:, :, None] / 255.0
    arr_final = (arr2 * (1 - m) + cor_fundo[None, None, :] * m).astype(np.uint8)
    limpo = Image.fromarray(arr_final)

    # ---------------------------------------------------------------
    # 2) Recorte da arte central (arco + figura + base)
    # ---------------------------------------------------------------
    # Conteúdo útil: x 55-440, y 10-560 (a figura termina ~y 540-560 e o
    # pedestal iluminado ~y 528-552).
    arte = limpo.crop((55, 10, 440, 560))
    arte.save(OUT_ARTE)
    print('Arte limpa salva:', OUT_ARTE, arte.size)

    # ---------------------------------------------------------------
    # 3) Tela da capa 600x800
    # ---------------------------------------------------------------
    W, H = 600, 800
    capa = Image.new('RGB', (W, H), PRETO)
    d = ImageDraw.Draw(capa)

    # Fundo: gradiente vertical sutil (#0b0f1c -> #000) + brilho dourado central
    base = np.zeros((H, W, 3), dtype=np.uint8)
    for yy in range(H):
        t = yy / H
        v = int(8 + 6 * (1 - t))  # levemente mais claro no topo
        base[yy, :, :] = (v, v + 2, v + 10)
    brilho = Image.new('L', (W, H), 0)
    ImageDraw.Draw(brilho).ellipse([90, 40, 510, 560], fill=60)
    brilho = brilho.filter(ImageFilter.GaussianBlur(160))
    glow = np.zeros((H, W, 3), dtype=np.float32)
    for ch, val in zip(range(3), OURO_CLARO):
        glow[:, :, ch] = val * (np.array(brilho).astype(np.float32) / 255.0)
    base = np.clip(base.astype(np.float32) + glow * 0.16, 0, 255).astype(np.uint8)
    capa = Image.fromarray(base)

    # ---------------------------------------------------------------
    # 4) Arte central
    # ---------------------------------------------------------------
    alvo_h = 500
    escala = alvo_h / arte.size[1]
    arte2 = arte.resize((int(arte.size[0] * escala), alvo_h), Image.LANCZOS)
    # Realce para a capa: o vídeo original é muito escuro
    arte2 = ImageEnhance.Brightness(arte2).enhance(1.5)
    arte2 = ImageEnhance.Contrast(arte2).enhance(1.15)
    arte2 = ImageEnhance.Color(arte2).enhance(1.1)
    pos_x = (W - arte2.size[0]) // 2
    pos_y = 38
    # leve sombra/vignette para integrar com o fundo
    capa.paste(arte2, (pos_x, pos_y))
    d = ImageDraw.Draw(capa)

    # Vinheta suave nas bordas da arte (fade p/ preto)
    fade = Image.new('L', (W, H), 0)
    ImageDraw.Draw(fade).rectangle([pos_x - 26, pos_y - 26, pos_x + arte2.size[0] + 26, pos_y + alvo_h + 26], fill=255)
    fade = fade.filter(ImageFilter.GaussianBlur(34))
    esc = Image.new('RGB', (W, H), (0, 0, 0))
    capa = Image.composite(capa, esc, fade)
    d = ImageDraw.Draw(capa)

    # Fade inferior (para dar contraste ao texto):
    # o PIL usa image1 onde a máscara é ALTA — portanto 255 no topo -> 0 embaixo.
    grad = Image.new('L', (W, H), 255)
    gd = ImageDraw.Draw(grad)
    for yy in range(560, H):
        a = int(255 * ((yy - 560) / 150) ** 1.6)
        gd.line([0, yy, W, yy], fill=255 - min(a, 235))
    esc2 = Image.new('RGB', (W, H), (2, 3, 6))
    capa = Image.composite(capa, esc2, grad)
    d = ImageDraw.Draw(capa)

    # ---------------------------------------------------------------
    # 5) Moldura dourada dupla
    # ---------------------------------------------------------------
    for inset in (14, 18):
        d.rectangle([inset, inset, W - 1 - inset, H - 1 - inset], outline=OURO, width=1)

    # ---------------------------------------------------------------
    # 6) Textos (base)
    # ---------------------------------------------------------------
    # Filete dourado decorativo
    d.line([300 - 130, 596, 300 + 130, 596], fill=OURO, width=1)
    d.ellipse([296, 592, 304, 600], outline=OURO, width=1)

    # Título principal
    f_titulo = fonte(FONTE_TITULO, 44)
    desenha_texto_centralizado(d, 612, 'VOCÊ E O UNIVERSO', f_titulo, OURO_CLARO, tracking=2)

    # Subtítulo
    f_sub = fonte(FONTE_ITALICO, 23)
    desenha_texto_centralizado(d, 672, 'O Inconsciente e as suas Criações', f_sub, CREME)

    # Selo
    f_selo = fonte(FONTE_TEXTO, 15)
    desenha_texto_centralizado(d, 724, 'C O L L E C T I O   O C C U L T A', f_selo, OURO, tracking=1)

    # ---------------------------------------------------------------
    # 7) Salvar
    # ---------------------------------------------------------------
    os.makedirs(os.path.dirname(OUT_CAPA), exist_ok=True)
    os.makedirs(os.path.dirname(OUT_DOCS), exist_ok=True)
    capa.save(OUT_CAPA)
    capa.save(OUT_DOCS)
    print('Capa salva:', OUT_CAPA, capa.size)
    print('Capa p/ GitHub Pages:', OUT_DOCS, capa.size)


if __name__ == '__main__':
    main()
