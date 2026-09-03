#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Identidade unica da casa: MISSÃO COM DEUS.

Rode DENTRO da pasta do site:
  cd /www/wwwroot/missaocomdeus.com.br
  python3 APLICAR_IDENTIDADE_MISSAO.py

O que faz:
  - Tira a marca antiga "Portal O Despertar" das paginas publicas, titulo,
    meta, cabecalho, rodape, enquete.php, manifest.json e sw.js.
  - Troca "Coleção do Despertar" por "Coleção Missão com Deus" nos arquivos
    visiveis (livros, capa e creditos), para o Google nao misturar duas marcas.
  - Corrige os dois trechos que ainda podem estar antigos no ar:
    "código de acesso grátis à Laura" e "Liberar Módulos 5, 6 e 7".
  - Cria backup .bak antes de alterar. Nao toca em dados dos usuarios.

Nao substitui paginas inteiras. Nao mexe no player. Confere antes de aplicar.
"""
from pathlib import Path
import datetime

SITE = Path('/www/wwwroot/missaocomdeus.com.br')

# Arquivos que nao podem ser alterados: sao dados dos usuarios ou gerados.
SKIP_NAMES = {'enquete_dados.json', 'enquete_ips.json', 'leituras.json'}

# Aplicadas em todos os arquivos de codigo da pasta do site.
SUBS = [
    # Marca antiga.
    ('Portal O Despertar', 'Missão com Deus'),
    ('Portal O <b>Despertar</b>', 'Missão com <b>Deus</b>'),
    # Coleção/id da marca.
    ('Coleção do Despertar', 'Coleção Missão com Deus'),
    ('Portal O Despertar', 'Missão com Deus'),
    # PWA.
    ('"id": "portal-o-despertar"', '"id": "missao-com-deus"'),
    ('const CACHE = \'portal-despertar-v5\'', 'const CACHE = \'missao-com-deus-v6\''),
    ('/* Service Worker — Portal O Despertar (PWA) */', '/* Service Worker — Missão com Deus (PWA) */'),
    # Leitor demo (se estiver no servidor).
    ('Leitor do Despertar v2', 'Leitor Missão com Deus v2'),
    ('Demonstração do Leitor do Despertar', 'Demonstração do Leitor Missão com Deus'),
    ('O <span>Despertar</span> · Leitor v2', 'Missão com <span>Deus</span> · Leitor v2'),
    ('O Despertar · Coleção do Despertar · missaocomdeus.com.br', 'Missão com Deus · Coleção Missão com Deus · missaocomdeus.com.br'),
    # Limpeza de duplicatas que o replace pode produzir.
    ('© Coleção Missão com Deus · Missão com Deus · Missão com Deus<br>', '© Missão com Deus · Todos os direitos reservados.<br>'),
    ('Missão com Deus · Missão com Deus · missaocomdeus.com.br', 'Missão com Deus · missaocomdeus.com.br'),
    ('Missão com Deus · Missão com Deus, Desperte sua mente', 'Missão com Deus, Desperte sua mente'),
    ('Missão com Deus · Missão com Deus', 'Missão com Deus'),
    ('"name": "Missão com Deus — Missão com Deus"', '"name": "Missão com Deus — Portal de leitura"'),
    ('← Voltar ao Missão com Deus', '← Voltar à Missão com Deus'),
    ('enquete do Missão com Deus', 'enquete da Missão com Deus'),
    # Textos que ainda podem estar antigos no ar (correcao da confianca).
    ('Peça seu código de acesso grátis à Laura. 🕊️', 'Os módulos 1 a 3 são grátis. Para conhecer o acesso completo, fale com a Laura. 🕊️'),
    ('Pedir código grátis', 'Falar com a Laura sobre o acesso'),
    ('<h2>🔑 Liberar Módulos 5, 6 e 7</h2>\n    <p>Insira o código de acesso, se você já o recebeu:</p>', '<h2>🔑 Liberar os módulos restantes</h2>\n    <p>Se você já recebeu um código de acesso da Missão, insira aqui para liberar os módulos 4 a 7.</p>'),
    # Aula grátis dos livros precisa ser dos modulos 1 a 3, nunca do 4.
    ('Módulo 04: Perdão como libertação da alma\n    <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;background:#000;">\n      <iframe src="https://www.youtube-nocookie.com/embed/fO5RIdrFzMw" title="Aula grátis: Módulo 04: Perdão como libertação da alma"',
     'Módulo 03: A Superação das dificuldades emocionais\n    <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;background:#000;">\n      <iframe src="https://www.youtube-nocookie.com/embed/4UmQlRiirXs" title="Aula grátis: Módulo 03: A Superação das dificuldades emocionais"'),
    ('Módulo 04: O Impulso sem Consciência\n    <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;background:#000;">\n      <iframe src="https://www.youtube-nocookie.com/embed/f_GxlRva2CQ" title="Aula grátis: Módulo 04: O Impulso sem Consciência"',
     'Módulo 03: O Governo da Mente\n    <div style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;background:#000;">\n      <iframe src="https://www.youtube-nocookie.com/embed/4IwyK4pmaJI" title="Aula grátis: Módulo 03: O Governo da Mente"'),
]


def listar_arquivos():
    out = []
    for path in sorted(SITE.rglob('*')):
        if not path.is_file():
            continue
        if path.name in SKIP_NAMES:
            continue
        if path.suffix.lower() not in ('.html', '.php', '.json', '.js'):
            continue
        if '.bak' in path.name:
            continue
        out.append(path)
    return out


def main():
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    total = 0
    arquivos = listar_arquivos()
    if not arquivos:
        print('Nenhum arquivo encontrado em', SITE)
        return
    for arq in arquivos:
        try:
            orig = arq.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        if orig is None or not orig.strip():
            continue
        t = orig
        for a, b in SUBS:
            t = t.replace(a, b)
        if t == orig:
            continue
        bak = arq.with_name('%s-antes-identidade-missao-%s.bak' % (arq.stem, stamp))
        try:
            bak.write_text(orig, encoding='utf-8')
        except Exception:
            pass
        arq.write_text(t, encoding='utf-8')
        total += 1
        print('OK', arq.name, '->', bak.name)
    print('Arquivos alterados:', total)
    print('Teste: titulo da Home = Missão com Deus · logo = Missão com Deus · PWA = Missão com Deus')


if __name__ == '__main__':
    main()
