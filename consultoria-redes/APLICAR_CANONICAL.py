# -*- coding: utf-8 -*-
"""
APLICAR_CANONICAL.py — Missao com Deus

Acrescenta a linha <link rel="canonical"> no <head> das paginas PUBLICAS.
Serve para o Google saber qual e o endereco oficial de cada pagina.
Assim os links marcados (utm_source) que o senhor compartilha nao viram
"pagina repetida" no painel do Search Console.

Regras da casa que este script respeita:
  - faz backup (.bak) de cada arquivo ANTES de mexer;
  - nao mexe no corpo da pagina, so no <head>;
  - nao toca no player da Palavra, no banner, no quiz, na enquete;
  - nao mexe em pagina noindex (palavra, mural, obrigado, guia-pais-filhos, stats);
  - se a pagina ja tem canonical, nao faz nada nela (pode rodar duas vezes).

Como usar (aaPanel Terminal):
  python3 /home/deploy/APLICAR_CANONICAL.py
"""
import os
import shutil
from datetime import datetime

SITE = os.environ.get('SITE_DIR', '/www/wwwroot/missaocomdeus.com.br')
BASE = 'https://missaocomdeus.com.br'

# arquivo na pasta -> endereco oficial na internet
PAGINAS = {
    'index.html': '/',
    'livro01.html': '/livro01',
    'livro02.html': '/livro02',
    'livro03.html': '/livro03',
    'livro04.html': '/livro04',
    'livro05.html': '/livro05',
    'livro06.html': '/livro06',
    'livro07.html': '/livro07',
    'livro08.html': '/livro08',
    'livro09.html': '/livro09',
    'livro10.html': '/livro10',
    'livro11.html': '/livro11',
    'livro12.html': '/livro12',
    'trilogia-da-alma.html': '/trilogia-da-alma',
    'anestesia-mental.html': '/anestesia-mental',
    'leitor.html': '/leitor',
}


def main():
    if not os.path.isdir(SITE):
        print('Pasta do site nao encontrada:', SITE)
        print('Se o site estiver em outro lugar: SITE_DIR=/caminho python3 APLICAR_CANONICAL.py')
        return

    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    feitos, pulados, erros = [], [], []

    for arquivo, caminho in PAGINAS.items():
        alvo = os.path.join(SITE, arquivo)
        if not os.path.isfile(alvo):
            pulados.append((arquivo, 'arquivo nao existe'))
            continue
        try:
            with open(alvo, 'r', encoding='utf-8', errors='ignore') as f:
                conteudo = f.read()
        except Exception as e:
            erros.append((arquivo, str(e)))
            continue

        if 'rel="canonical"' in conteudo:
            pulados.append((arquivo, 'ja tem canonical'))
            continue

        if '</head>' not in conteudo:
            erros.append((arquivo, 'nao achei </head>'))
            continue

        linha = '  <link rel="canonical" href="%s%s">\n' % (BASE, caminho)
        novo = conteudo.replace('</head>', linha + '</head>', 1)

        backup = alvo + '.bak-' + stamp
        try:
            shutil.copy2(alvo, backup)
            with open(alvo, 'w', encoding='utf-8') as f:
                f.write(novo)
            feitos.append((arquivo, caminho, backup))
        except Exception as e:
            erros.append((arquivo, str(e)))

    print('--- CANONICAL ---')
    for a, c, b in feitos:
        print('OK   %-24s -> %s%s   (backup: %s)' % (a, BASE, c, os.path.basename(b)))
    for a, motivo in pulados:
        print('--   %-24s (%s)' % (a, motivo))
    for a, e in erros:
        print('ERRO %-24s %s' % (a, e))
    print('Total: %d alterados, %d pulados, %d com erro.' % (len(feitos), len(pulados), len(erros)))
    if feitos:
        print('Conferir no navegador: abrir a pagina e pressionar Ctrl+U (ver fonte).')


if __name__ == '__main__':
    main()
