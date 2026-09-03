#!/usr/bin/env python3
# Pasta do SITE, junto do enquete.php.
# Tira o e-mail da resposta publica da enquete. O voto e o texto continuam.
# Nao apaga enquete_dados.json. Nao substitui o PHP inteiro.

from pathlib import Path
import datetime

ARQ = Path('/www/wwwroot/missaocomdeus.com.br/enquete.php')

OLD = "$res['comentarios'] = isset($dados['comentarios']) ? array_slice(array_reverse($dados['comentarios']), 0, 20) : array();"

NEW = """$comentarios_publicos = isset($dados['comentarios']) ? array_slice(array_reverse($dados['comentarios']), 0, 20) : array();
    $res['comentarios'] = array_map(function ($c) {
        return array(
            'texto' => isset($c['texto']) ? $c['texto'] : '',
            'data' => isset($c['data']) ? $c['data'] : '',
        );
    }, $comentarios_publicos);"""


def main():
    if not ARQ.exists():
        raise SystemExit('enquete.php nao encontrado. Rode na pasta do site.')
    t = ARQ.read_text(encoding='utf-8', errors='replace')
    bak = ARQ.with_name('enquete-antes-sem-email-%s.bak' % datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
    bak.write_text(t, encoding='utf-8')

    if "$comentarios_publicos" in t and "email fica de fora" in t.replace(" ", ""):
        print('Ja estava sem e-mail na resposta. Nao mexi.')
        print('Backup:', bak.name)
        return

    if 'array_map(function ($c)' in t and "'texto'" in t and OLD not in t:
        print('Ja estava filtrando o e-mail. Nao mexi.')
        print('Backup:', bak.name)
        return

    if OLD not in t:
        raise SystemExit('Nao achei a linha antiga. Nao mexi no PHP.')

    t = t.replace(OLD, NEW, 1)
    ARQ.write_text(t, encoding='utf-8')
    print('OK enquete: e-mail nao volta na resposta publica.')
    print('Backup:', bak.name)
    print('O JSON interno continua com e-mail se ja tinha. So a pagina/API nao mostra.')


if __name__ == '__main__':
    main()
