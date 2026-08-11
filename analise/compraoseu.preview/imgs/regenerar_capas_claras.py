# -*- coding: utf-8 -*-
"""
Regenera as capas dos cards (livro01, 02, 03) em estilo CLARO e legível:
- Imagem clareada (+45% brilho, leve contraste)
- Faixa inferior CREME opaca com "LIBER OCCULTUS" em NAVY escuro (contraste máximo)
- Título do livro em navy escuro
- Número romano no topo com fundo claro
- Sem vinheta escura cobrindo a imagem
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter, ImageOps
from pathlib import Path

BASE = Path('/tmp/capas_base')
OUT = Path('/home/user/instalador/analise/compraoseu.preview/imgs/capas_editadas')
OUT.mkdir(parents=True, exist_ok=True)

FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'

NAVY = (14, 26, 46, 255)          # texto escuro
NAVY_SUAVE = (30, 45, 70, 235)
CREME = (246, 241, 231, 255)      # faixa clara
GOLD = (201, 162, 75, 255)        # dourado

# arquivo -> (título grande latim, título do livro, número romano)
CONFIG = {
    '01_capa.png': ("LIBER OCCULTUS", "O Ouro das Palavras", "I"),
    '02_capa.png': ("LIBER OCCULTUS", "O Livro Proibido dos Mestres", "II"),
    '03_capa.png': ("LIBER OCCULTUS", "O Caibalion", "III"),
}

def fonte(tam, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, tam)

def centralizar(draw, w, y, texto, font, cor):
    bbox = draw.textbbox((0, 0), texto, font=font)
    x = (w - (bbox[2] - bbox[0])) // 2
    draw.text((x, y), texto, font=font, fill=cor)
    return bbox[2] - bbox[0]

def processar(arquivo):
    cfg = CONFIG[arquivo]
    img = Image.open(BASE / arquivo).convert('RGB')
    W, H = img.size  # esperado 600x800

    # ---- 1) Clarear a imagem (autocontrast + gamma: clareia tons escuros sem estourar) ----
    img = ImageOps.autocontrast(img, cutoff=1)
    # gamma < 1 clareia os tons escuros
    img = Image.eval(img, lambda v: int(((v / 255.0) ** 0.38) * 255))
    img = ImageEnhance.Color(img).enhance(1.2)
    img = ImageEnhance.Contrast(img).enhance(1.05)

    draw = ImageDraw.Draw(img)

    # ---- 2) Faixa inferior CREME (opaca) ----
    faixa_alt = int(H * 0.30)  # 30% inferior
    y_faixa = H - faixa_alt
    draw.rectangle([0, y_faixa, W, H], fill=CREME)
    # borda dourada entre imagem e faixa
    draw.line([(0, y_faixa), (W, y_faixa)], fill=GOLD, width=3)

    # ---- 3) Textos na faixa creme (navy escuro = contraste máximo) ----
    # "LIBER OCCULTUS" grande
    f_tit = fonte(58, True)
    centralizar(draw, W, y_faixa + 34, cfg[0], f_tit, NAVY)

    # divisor dourado
    div_w = 140
    dy = y_faixa + 118
    draw.line([(W//2 - div_w//2, dy), (W//2 + div_w//2, dy)], fill=GOLD, width=3)

    # título do livro
    f_sub = fonte(30, False)
    centralizar(draw, W, dy + 16, cfg[1], f_sub, NAVY_SUAVE)

    # selo
    f_selo = fonte(17, True)
    centralizar(draw, W, dy + 60, "C O L L E C T I O   O C C U L T A", f_selo, GOLD)

    # ---- 4) Número romano no topo (com fundo claro para legibilidade) ----
    f_num = fonte(34, True)
    bbox = draw.textbbox((0, 0), cfg[2], font=f_num)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    nx = (W - tw) // 2 - 8
    ny = 22
    draw.rounded_rectangle([nx-6, ny-4, nx+tw+10, ny+th+10], radius=10,
                           fill=(246, 241, 231, 200))
    draw.text((nx, ny), cfg[2], font=f_num, fill=NAVY)

    # ---- 5) Borda dourada ----
    draw.rectangle([6, 6, W-7, H-7], outline=GOLD, width=3)
    draw.rectangle([14, 14, W-15, H-15], outline=(150, 120, 50, 255), width=1)

    # ---- 6) Salvar ----
    nome_out = arquivo.replace('.png', '_clara.png')
    img.convert('RGB').save(OUT / nome_out, quality=95)
    print(f"  {arquivo} -> {nome_out} (clara)")

print("=== REGENERANDO CAPAS CLARAS ===")
for arq in CONFIG:
    processar(arq)
print("Pronto!")
