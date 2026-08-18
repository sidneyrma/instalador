# -*- coding: utf-8 -*-
"""Verifica contexto de cada checkout: o preço exibido ao lado bate com o checkout?"""
import re

BASE = '/tmp/compraoseu_preview'
PAGINAS = ['home', 'evolucao', 'anestesia', 'devocional']

PRECO_POR_CHECKOUT = {
    'iVfp2bi': '49,00',
    'ptH32K9': '19,90',
    'NCf1jh4': '19,90',
    'CF9nhFx': '9,90',
}

for pag in PAGINAS:
    body = open(f'{BASE}/{pag}_BODY.html', encoding='utf-8').read()
    # remove comentários para não poluir
    body_limpo = re.sub(r'<!--.*?-->', '', body, flags=re.S)
    print(f"\n===== {pag.upper()} =====")
    for ck, preco_esperado in PRECO_POR_CHECKOUT.items():
        # encontra todas as ocorrências do link
        for m in re.finditer(re.escape(ck), body_limpo):
            start = max(0, m.start()-700)
            ctx = body_limpo[start:m.end()+200]
            # extrai preços no contexto
            precos = re.findall(r'R\$\s*(\d+[.,]\d{2})', ctx)
            # preço grande (sem riscado) = o que aparece destacado
            # verifica se o esperado aparece no contexto
            if preco_esperado in body_limpo[max(0,m.start()-700):m.end()+200]:
                status = 'OK ✓ (preço correto no contexto)'
            else:
                status = f'ATENÇÃO: preços no contexto: {precos}'
            print(f"  {ck} (esperado R$ {preco_esperado}): {status}")
