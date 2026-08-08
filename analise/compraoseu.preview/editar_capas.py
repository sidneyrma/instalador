# -*- coding: utf-8 -*-
"""
Edita as capas místicas (subidas no GitHub) e gera versões com:
- "LIBER OCCULTUS" (em latim, dourado, serifado) + título do livro
- Vinheta (bordas escuras) para o texto se destacar
- Borda dourada + número romano (misterioso)
- Proporção 3:4 (estilo livro) pronta para os cards da Home

Gera VÁRIAS opções para o usuário escolher visualmente.
"""
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from pathlib import Path

ORIG = Path('/tmp/imgs_originais')
OUT = Path('/home/user/instalador/analise/compraoseu.preview/imgs/capas_editadas')
OUT.mkdir(parents=True, exist_ok=True)

FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'

GOLD = (212, 168, 63, 255)      # dourado
GOLD_CLARO = (227, 200, 119, 255)
NAVY = (14, 26, 46, 255)

# Mapa: arquivo -> (título grande, subtítulo, número romano)
CONFIG = {
    '01.jfif':   ("LIBER OCCULTUS", "O Ouro das Palavras", "I"),
    '02.jfif':   ("LIBER OCCULTUS", "O Livro Proibido dos Mestres", "II"),
    '03.jfif':   ("LIBER OCCULTUS", "O Ouro das Palavras", "I"),
    '04.jfif':   ("KYBALION", "Os Sete Princípios Herméticos", "III"),
    '05.jfif':   ("LIBER OCCULTUS", "O Livro Proibido dos Mestres", "II"),
    'images.jfif': ("LIBER OCCULTUS", "O Ouro das Palavras", "I"),
    'images (1).jfif': ("LIBER OCCULTUS", "O Livro Proibido dos Mestres", "II"),
    'images (2).jfif': ("LIBER OCCULTUS", "O Ouro das Palavras", "I"),
    'images (4).jfif': ("KYBALION", "Os Sete Princípios Herméticos", "III"),
}

def fonte(tamanho, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, tamanho)

def centralizar(draw, img_w, y, texto, font, cor, sombra=True):
    """Desenha texto centralizado com sombra sutil."""
    bbox = draw.textbbox((0, 0), texto, font=font)
    w = bbox[2] - bbox[0]
    x = (img_w - w) // 2
    if sombra:
        draw.text((x+2, y+2), texto, font=font, fill=(0, 0, 0, 180))
    draw.text((x, y), texto, font=font, fill=cor)
    return w

def vinheta(img, forca=70):
    """Escurece as bordas (efeito misterioso) — mantém centro visível."""
    mask = Image.new('L', img.size, 0)
    d = ImageDraw.Draw(mask)
    w, h = img.size
    # gradiente radial aproximado com elipses
    for i in range(120, 0, -2):
        alpha = int(forca * (i / 120))
        d.ellipse([w/2 - w*i/240, h/2 - h*i/240, w/2 + w*i/240, h/2 + h*i/240], fill=alpha)
    preto = Image.new('RGB', img.size, (0, 0, 0))
    img = Image.composite(img, preto, mask)
    return img

def processar(arquivo):
    cfg = CONFIG[arquivo]
    img = Image.open(ORIG / arquivo).convert('RGB')

    # --- 1) proporção 3:4 (600x800) com crop central ---
    alvo_w, alvo_h = 600, 800
    # redimensiona cobrindo
    escala = max(alvo_w / img.width, alvo_h / img.height)
    novo_w, novo_h = int(img.width * escala) + 1, int(img.height * escala) + 1
    img = img.resize((novo_w, novo_h), Image.LANCZOS)
    # crop central
    x0 = (novo_w - alvo_w) // 2
    y0 = (novo_h - alvo_h) // 2
    img = img.crop((x0, y0, x0 + alvo_w, y0 + alvo_h))

    # --- 2) leve suavização e vinheta ---
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = vinheta(img, 60)

    # --- 3) sobreposição navy translúcida nas faixas de texto ---
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d_over = ImageDraw.Draw(overlay)
    d_over.rectangle([0, 40, alvo_w, 150], fill=(14, 26, 46, 120))       # faixa superior
    d_over.rectangle([0, alvo_h - 190, alvo_w, alvo_h - 30], fill=(14, 26, 46, 130))  # faixa inferior
    img = Image.alpha_composite(img.convert('RGBA'), overlay)

    draw = ImageDraw.Draw(img)

    # --- 4) textos ---
    # número romano (superior, discreto)
    f_num = fonte(30, True)
    centralizar(draw, alvo_w, 52, cfg[2], f_num, GOLD_CLARO)

    # "LIBER OCCULTUS" grande
    f_tit = fonte(52, True)
    centralizar(draw, alvo_w, alvo_h - 165, cfg[0], f_tit, GOLD)

    # divisor dourado
    d = ImageDraw.Draw(img)
    largura_div = 160
    d.line([(alvo_w//2 - largura_div//2, alvo_h - 108), (alvo_w//2 + largura_div//2, alvo_h - 108)],
           fill=GOLD, width=2)

    # subtítulo
    f_sub = fonte(26, False)
    centralizar(draw, alvo_w, alvo_h - 92, cfg[1], f_sub, (240, 240, 240, 230))

    # selo "COLEÇÃO DO DESPERTAR" pequeno
    f_selo = fonte(18, True)
    centralizar(draw, alvo_w, alvo_h - 52, "C O L L E C T I O   O C C U L T A", f_selo, GOLD_CLARO)

    # --- 5) borda dourada dupla ---
    d.rectangle([6, 6, alvo_w - 7, alvo_h - 7], outline=GOLD, width=2)
    d.rectangle([14, 14, alvo_w - 15, alvo_h - 15], outline=(150, 120, 50, 255), width=1)

    # --- 6) salvar ---
    nome_base = arquivo.replace('.jfif', '')
    saida = OUT / f"{nome_base}_capa.png"
    img.convert('RGB').save(saida, quality=92)
    return saida, img.size

print("=== GERANDO CAPAS EDITADAS ===")
for arquivo in sorted(CONFIG.keys()):
    saida, dim = processar(arquivo)
    print(f"  {arquivo} -> {saida.name} ({dim[0]}x{dim[1]})")

print(f"\nTotal: {len(list(OUT.glob('*.png')))} capas em {OUT}")
