# -*- coding: utf-8 -*-
"""OCR nas capas atuais para mapear textos e posições."""
import os, sys
import numpy as np
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

OCR = RapidOCR()

def ocr_boxes(path):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    scale = 2
    arr = np.array(img.resize((w*scale, h*scale), Image.LANCZOS))
    res, _ = OCR(arr)
    print(f"--- {path} ({w}x{h}) ---")
    for b, t, s in (res or []):
        x0, y0 = int(b[0][0]/scale), int(b[0][1]/scale)
        x1, y1 = int(b[2][0]/scale), int(b[2][1]/scale)
        print(f"  [{x0:4d},{y0:4d} -> {x1:4d},{y1:4d}] conf={float(s):.2f}  '{t}'")

for p in sys.argv[1:]:
    ocr_boxes(p)
