# -*- coding: utf-8 -*-
"""
Edita a capa da Trilogia (capa.jpg): substitui o fundo branco por um fundo
navy escuro com gradiente, no tema do Portal O Despertar (#0e1a2e → #16283f),
preservando o conteúdo central com transição suave.
"""
import numpy as np
from PIL import Image, ImageFilter

SRC = '/tmp/capa_nova.jpg'
OUT = '/home/user/instalador/analise/compraoseu.preview/imgs/capa_trilogia_navy.jpg'

NAVY1 = np.array([0x1a, 0x2e, 0x4e])   # azul-marinho (0e1a2e em BGR? não: RGB)
NAVY2 = np.array([0x28, 0x3f, 0x5e])   # navy mais claro (16283f)

# Usamos RGB (PIL) — cores do tema:
NAVY_TOP = np.array([14, 26, 46])      # #0e1a2e
NAVY_BOT = np.array([22, 40, 63])      # #16283f

img = Image.open(SRC).convert('RGB')
w, h = img.size
arr = np.array(img).astype(np.float32)

# --- 1) Mapa de "brancura": alto brilho + baixa saturação ---
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
maxc = np.maximum(np.maximum(r, g), b)
minc = np.minimum(np.minimum(r, g), b)
sat = np.where(maxc > 0, (maxc - minc) / np.maximum(maxc, 1), 0)
white = np.clip((maxc - 200) / 55.0, 0, 1) * np.clip(1 - sat * 2.5, 0, 1)

# --- 2) Gradiente navy vertical (suave) ---
grad = np.linspace(0, 1, h)[:, None, None]
navy = NAVY_TOP[None, None, :] * (1 - grad) + NAVY_BOT[None, None, :] * grad

# --- 3) Suavizar a máscara de brancura (para não deixar bordas duras) ---
wm = Image.fromarray((white * 255).astype(np.uint8))
wm = wm.filter(ImageFilter.GaussianBlur(6))
white = np.array(wm).astype(np.float32)[..., None] / 255.0

# --- 4) Compor: onde é branco, usa o navy; onde é conteúdo, mantém ---
out = arr * (1 - white) + navy * white
out = np.clip(out, 0, 255).astype(np.uint8)

Image.fromarray(out).save(OUT, quality=95)
print('Salvo:', OUT)

# --- validar ---
arr2 = np.array(Image.open(OUT).convert('RGB'))
borda = arr2[:15, :, :].mean(axis=(0, 1))
branco2 = (arr2 > 230).all(axis=2).mean() * 100
print('Borda superior nova (RGB):', borda.round(1))
print(f'Pixels brancos restantes: {branco2:.1f}%')
print('Brilho médio:', round(float(arr2.mean()), 1))
