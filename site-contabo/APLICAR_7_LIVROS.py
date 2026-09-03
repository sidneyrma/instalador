#!/usr/bin/env python3
# Pasta do SITE.
# Troca "12 livros" pelo que a prateleira mostra agora: 7 da Missao.
# Nao substitui paginas inteiras. Nao mexe no player.

from pathlib import Path
import datetime

SITE = Path('/www/wwwroot/missaocomdeus.com.br')

PARES = [
    ('<li>12 livros online</li>', '<li>7 livros online</li>'),
    (
        'Gratidão a quem ajuda a manter 12 livros gratuitos vivos para milhares de irmãos:',
        'Gratidão a quem ajuda a manter os livros gratuitos da Missão vivos para milhares de irmãos:',
    ),
]


def limpa(arq):
    if not arq.exists():
        print('AVISO: nao achei', arq.name)
        return 0
    t = arq.read_text(encoding='utf-8', errors='replace')
    n = 0
    for a, b in PARES:
        if a in t:
            t = t.replace(a, b)
            n += 1
            print('OK', arq.name + ':', a[:50])
    if n:
        bak = arq.with_name('%s-antes-7livros-%s.bak' % (
            arq.stem, datetime.datetime.now().strftime('%Y%m%d-%H%M%S')))
        # backup already? write bak from original - we mutated t. Need bak first.
        pass
    return n, t


def main():
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    total = 0
    for nome in ('index.html', 'trilogia-da-alma.html', 'anestesia-mental.html'):
        arq = SITE / nome
        if not arq.exists():
            print('AVISO: nao achei', nome)
            continue
        orig = arq.read_text(encoding='utf-8', errors='replace')
        t = orig
        n = 0
        for a, b in PARES:
            c = t.count(a)
            if c:
                t = t.replace(a, b)
                n += c
                print('OK', nome, '(%d):' % c, a[:48])
        if n:
            bak = arq.with_name('%s-antes-7livros-%s.bak' % (arq.stem, stamp))
            bak.write_text(orig, encoding='utf-8')
            arq.write_text(t, encoding='utf-8')
            total += n
        else:
            print(nome, ': nada de 12 livros')
    print('Trocas:', total)
    print('Teste: Home bloco Leitura no portal. Sem 12 livros.')


if __name__ == '__main__':
    main()
