#!/usr/bin/env python3
# Pasta do SITE.
# Os outros leitores tinham href="#" (por isso livro04#).
# Agora todos: Missao com Deus -> https://missaocomdeus.com.br/#biblioteca

from pathlib import Path
import datetime

SITE = Path('/www/wwwroot/missaocomdeus.com.br')
DEST = 'https://missaocomdeus.com.br/#biblioteca'

ALVOS = [
    '<a class="logo" href="#">',
    '<a class="logo" href="#capa">',
    '<a class="logo" href="/">',
]


def main():
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    novo = '<a class="logo" href="%s">' % DEST
    ok = 0
    for i in range(1, 13):
        arq = SITE / ('livro%02d.html' % i)
        if not arq.exists():
            print('AVISO:', arq.name)
            continue
        t = arq.read_text(encoding='utf-8', errors='replace')
        trecho = t[max(0, t.find('class="logo"') - 40): t.find('class="logo"') + 90] if 'class="logo"' in t else ''
        if 'href="%s"' % DEST in trecho or "href='%s'" % DEST in trecho:
            print(arq.name, 'ja ok')
            continue
        bak = arq.with_name('%s-antes-logo2-%s.bak' % (arq.stem, stamp))
        bak.write_text(t, encoding='utf-8')
        n = 0
        for a in ALVOS:
            if a in t:
                t = t.replace(a, novo, 1)
                n += 1
                break
        if n:
            arq.write_text(t, encoding='utf-8')
            ok += 1
            print('OK', arq.name)
        else:
            print('nao achei', arq.name, repr(trecho[:80]))
    print('Atualizados:', ok)
    print('Teste: /livro04 clicar Missao com Deus. Barra: missaocomdeus.com.br/#biblioteca')


if __name__ == '__main__':
    main()
