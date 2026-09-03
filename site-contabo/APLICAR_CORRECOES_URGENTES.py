#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correcoes urgentes de confianca e coerencia no site vivo.

Rode DENTRO da pasta do site:
  cd /www/wwwroot/missaocomdeus.com.br
  python3 APLICAR_CORRECOES_URGENTES.py

O que faz:
  1. Home / FAQ: tira o texto antigo "As quatro aulas..." e coloca
     "Os modulos 1 a 3 ja estao gratis no site...", sem prometer surpresa
     sem nome (o presente ja foi nomeado na oferta).
  2. Home / banner fixo: tira "Peça seu código de acesso grátis à Laura" e
     "Pedir código grátis". Coloca o convite certo, sem prometer codigo gratis.
  3. Trilha e Anestesia / caixa de codigo: troca "Liberar Modulos 5, 6 e 7"
     por "Liberar os modulos restantes" e deixa claro que libera 4 a 7.

Nao substitui paginas inteiras. Nao mexe no player. Cria .bak antes de alterar.
Se o arquivo ja tiver o texto novo, nao cria backup nem mexe outra vez.
"""
from pathlib import Path
import datetime

SITE = Path('/www/wwwroot/missaocomdeus.com.br')

# (arquivo, texto antigo, texto novo)
TROCAS = [
    (
        'index.html',
        '<div class="faq-a"><p>Por R$ 37,00, pagamento único: os dois cursos em vídeo (14 módulos), os livros digitais Evolução da Alma e Anestesia Mental, o Devocional de 30 dias, o e-book Jesus Quer Falar com Seu Filho e a comunidade, vitalício, por e-mail na Kiwify. As quatro aulas no site são só o começo. E a casa reserva um presente depois do acesso. Não adiantamos o nome: chega como surpresa.</p></div>',
        '<div class="faq-a"><p>Por R$ 37,00, pagamento único: os dois cursos em vídeo (14 módulos), os livros digitais Evolução da Alma e Anestesia Mental, o Devocional de 30 dias, o e-book Jesus Quer Falar com Seu Filho e a comunidade, vitalício, por e-mail na Kiwify. Os módulos 1 a 3 já estão grátis no site, para você conhecer antes de decidir. Na área de membros você recebe o estudo completo e o presente extra da casa: o PDF do Novo Testamento como nunca lido, para guardar.</p></div>',
    ),
    (
        'index.html',
        '<span>A Trilogia completa da Evolução da Alma (7 módulos) está te esperando. Peça seu código de acesso grátis à Laura. 🕊️</span>\n    </div>\n    <div class="cta-btns">\n      <a class="btn btn-gold" href="/trilogia-da-alma">🎬 Quero assistir</a>\n      <a class="btn btn-ghost-light" href="https://wa.me/5528999111493?text=Ol%C3%A1%20Laura%2C%20vim%20pela%20Home%20e%20quero%20pedir%20meu%20c%C3%B3digo%20de%20acesso%20%F0%9F%99%8F" target="_blank" rel="noopener">💛 Pedir código grátis</a>\n    </div>',
        '<span>A Trilogia completa da Evolução da Alma (7 módulos) está te esperando. Os módulos 1 a 3 são grátis. Para conhecer o acesso completo, fale com a Laura. 🕊️</span>\n    </div>\n    <div class="cta-btns">\n      <a class="btn btn-gold" href="/trilogia-da-alma">🎬 Quero assistir</a>\n      <a class="btn btn-ghost-light" href="https://wa.me/5528999111493?text=Ol%C3%A1%20Laura%2C%20vim%20pela%20Home%20e%20quero%20entender%20o%20acesso%20completo%20%F0%9F%95%8A%EF%B8%8F" target="_blank" rel="noopener">💛 Falar com a Laura sobre o acesso</a>\n    </div>',
    ),
    (
        'trilogia-da-alma.html',
        '<h2>🔑 Liberar Módulos 5, 6 e 7</h2>\n    <p>Insira o código de acesso, se você já o recebeu:</p>',
        '<h2>🔑 Liberar os módulos restantes</h2>\n    <p>Se você já recebeu um código de acesso da Missão, insira aqui para liberar os módulos 4 a 7.</p>',
    ),
    (
        'anestesia-mental.html',
        '<h2>🔑 Liberar Módulos 5, 6 e 7</h2>\n    <p>Insira o código de acesso, se você já o recebeu:</p>',
        '<h2>🔑 Liberar os módulos restantes</h2>\n    <p>Se você já recebeu um código de acesso da Missão, insira aqui para liberar os módulos 4 a 7.</p>',
    ),
]


def main():
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    total = 0
    for nome, velho, novo in TROCAS:
        arq = SITE / nome
        if not arq.exists():
            print('AVISO: nao achei', nome)
            continue
        t = arq.read_text(encoding='utf-8', errors='replace')
        if novo in t:
            print('ja estava', nome)
            continue
        if velho not in t:
            print('nao achei o trecho em', nome)
            continue
        bak = arq.with_name('%s-antes-correcoes-urgentes-%s.bak' % (arq.stem, stamp))
        bak.write_text(t, encoding='utf-8')
        t = t.replace(velho, novo, 1)
        arq.write_text(t, encoding='utf-8')
        total += 1
        print('OK', nome, '->', bak.name)
    print('Trocas aplicadas:', total)
    print('Teste: Home FAQ "Os módulos 1 a 3" + banner sem "código grátis" + caixas de código "4 a 7".')


if __name__ == '__main__':
    main()
