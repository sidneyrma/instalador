# -*- coding: utf-8 -*-
"""
Migra as capas da "Coleção Oculta" para a "Coleção do Despertar".

Regrava sobre as imagens existentes:
  - "COLLECTIO OCCULTA" / "COLEÇÃO OCULTA"  ->  "COLEÇÃO DO DESPERTAR" (selo)
  - "LIBER OCCULTUS"                         ->  "O DESPERTAR" (título grande)

Usa a fonte Tinos (livro/fontes) e as cores originais (dourado sobre fundo escuro).
"""
import os, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from rapidocr_onnxruntime import RapidOCR

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
FONT_REG = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Regular.ttf')
FONT_BOLD = os.path.join(ROOT, 'livro', 'fontes', 'Tinos-Bold.ttf')

# alvos: arquivo -> lista de (texto_antigo, texto_novo, tipo)
# tipo: 'selo' (pequeno, tracking) ou 'titulo' (grande, bold)
ALVOS = [
    ('docs/capas/livro01.png', [('COLLECTIO OCCULTA', 'COLEÇÃO DO DESPERTAR', 'selo'),
                                ('LIBER OCCULTUS', 'O DESPERTAR', 'titulo')]),
    ('docs/capas/livro02.png', [('COLLECTIO OCCULTA', 'COLEÇÃO DO DESPERTAR', 'selo'),
                                ('LIBER OCCULTUS', 'O DESPERTAR', 'titulo')]),
    ('docs/capas/livro03.png', [('COLLECTIO OCCULTA', 'COLEÇÃO DO DESPERTAR', 'selo'),
                                ('LIBER OCCULTUS', 'O DESPERTAR', 'titulo')]),
    ('docs/capas/livro08.png', [('COLLECTIO OCCULTA', 'COLEÇÃO DO DESPERTAR', 'selo')]),
    ('docs/capas/mente_cristo.png', [('COLLECTIO OCCULTA', 'COLEÇÃO DO DESPERTAR', 'selo')]),
    ('analise/compraoseu.preview/obra/capas/capa_despertar.png',
     [('COLEÇÃO OCULTA', 'COLEÇÃO DO DESPERTAR', 'selo')]),
]

OCR = None


def ocr_boxes(img):
    """Retorna lista de (texto, x0, y0, x1, y1) na escala original."""
    global OCR
    if OCR is None:
        OCR = RapidOCR()
    w, h = img.size
    scale = 2
    arr = np.array(img.resize((w*scale, h*scale), Image.LANCZOS))
    res, _ = OCR(arr)
    boxes = []
    for b, t, s in (res or []):
        x0, y0 = int(b[0][0]/scale), int(b[0][1]/scale)
        x1, y1 = int(b[2][0]/scale), int(b[2][1]/scale)
        boxes.append((t, x0, y0, x1, y1))
    return boxes


def achar_box(boxes, texto):
    """Procura um box cujo texto contenha o alvo (case-insensitive)."""
    t = re.sub(r'\s+', '', texto).lower()
    for txt, x0, y0, x1, y1 in boxes:
        tt = re.sub(r'\s+', '', txt).lower()
        if t in tt or tt in t:
            return (x0, y0, x1, y1)
    return None


def texto_tracked(draw, y, texto, font, fill, tracking, centro_x):
    widths = [draw.textlength(ch, font=font) for ch in texto]
    total = sum(widths) + tracking * (len(texto) - 1)
    x = centro_x - total / 2
    for ch, w in zip(texto, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking


def regravar(img, box, texto_novo, tipo, cor_texto, cor_fundo):
    """Preenche o box com cor_fundo e desenha texto_novo centralizado."""
    x0, y0, x1, y1 = box
    pad = 6
    x0, y0, x1, y1 = max(0, x0-pad), max(0, y0-pad), min(img.width, x1+pad), min(img.height, y1+pad)
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], fill=tuple(cor_fundo))
    centro_x = img.width // 2
    if tipo == 'titulo':
        # tenta tamanho que caiba na largura disponível
        larg = x1 - x0
        size = 40
        while size > 16:
            f = ImageFont.truetype(FONT_BOLD, size)
            w_txt = d.textlength(texto_novo, font=f)
            if w_txt <= larg * 0.92:
                break
            size -= 2
        f = ImageFont.truetype(FONT_BOLD, size)
        bbox = d.textbbox((0, 0), texto_novo, font=f)
        th = bbox[3] - bbox[1]
        ty = (y0 + y1) // 2 - th // 2 - bbox[1]
        d.text((centro_x - w_txt/2, ty), texto_novo, font=f, fill=tuple(cor_texto))
    else:  # selo
        larg = x1 - x0
        size = 14
        while size > 7:
            f = ImageFont.truetype(FONT_REG, size)
            tracking = max(0, int(size * 0.55))
            widths = [f.getlength(ch) for ch in texto_novo]
            total = sum(widths) + tracking * (len(texto_novo) - 1)
            if total <= larg * 0.94:
                break
            size -= 1
        f = ImageFont.truetype(FONT_REG, size)
        tracking = max(0, int(size * 0.55))
        bbox = d.textbbox((0, 0), texto_novo, font=f)
        th = bbox[3] - bbox[1]
        ty = (y0 + y1) // 2 - th // 2 - bbox[1]
        texto_tracked(d, ty, texto_novo, f, tuple(cor_texto), tracking, centro_x)
    return img


def main():
    for arquivo, trocas in ALVOS:
        caminho = os.path.join(ROOT, arquivo)
        if not os.path.exists(caminho):
            print(f'⚠ {arquivo} não encontrado')
            continue
        img = Image.open(caminho).convert('RGB')
        boxes = ocr_boxes(img)
        cor_selo = (222, 197, 120)
        cor_titulo = (212, 168, 63)
        cor_fundo_selo = None
        cor_fundo_titulo = None
        arr = np.array(img).astype(int)
        for antigo, novo, tipo in trocas:
            box = achar_box(boxes, antigo)
            if not box:
                print(f'  ⚠ "{antigo}" não localizado em {arquivo}')
                continue
            # cor de fundo = média das bordas laterais do box
            x0, y0, x1, y1 = box
            margens = np.concatenate([arr[y0:y1, max(0,x0-8):x0].reshape(-1,3),
                                      arr[y0:y1, x1:min(img.width,x1+8)].reshape(-1,3)])
            cor_fundo = tuple(int(v) for v in margens.mean(axis=0))
            if tipo == 'selo':
                cor_fundo_selo = cor_fundo
            else:
                cor_fundo_titulo = cor_fundo
            img = regravar(img, box, novo, tipo,
                           cor_selo if tipo == 'selo' else cor_titulo,
                           cor_fundo)
            print(f'  ✔ {arquivo}: "{antigo}" -> "{novo}" (box {box}, fundo {cor_fundo})')
        img.save(caminho)
        print(f'  ✔ salvo: {arquivo}')


if __name__ == '__main__':
    main()
