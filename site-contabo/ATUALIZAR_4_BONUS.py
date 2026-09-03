#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualizacao do acesso completo: agora sao 4 bonus, nao mais "um brinde extra".

Rode DENTRO da pasta do site:
  cd /www/wwwroot/missaocomdeus.com.br
  python3 ATUALIZAR_4_BONUS.py

O que faz:
  - Home: vitrine "Nossas Obras" com descricoes reais + oferta com 4 bonus.
  - Home: FAQ e card "Acesso completo" alinhados ao checkout.
  - Pontes (Trilogia e Anestesia): card e modal com 4 bonus.
  - Livro 07 e Livro 11: portao de acesso com 4 bonus + convite correto.
  - Livro 09: corrige "Módulos 1 a 4" para "Módulos 1 a 3".
  - Mantem os ajustes urgentes de coerencia (3 aulas, sem codigo gratis,
    "Liberar os modulos restantes").

Nao substitui paginas inteiras. Cria .bak antes de alterar.
"""
from pathlib import Path
import datetime

SITE = Path('/www/wwwroot/missaocomdeus.com.br')

TROCAS = [
    ('index.html', '''<p>Livro digital completo + Curso em vídeo com 7 módulos para o despertar da alma e o governo das emoções.</p>
          <ul class="obra-itens">
            <li>✅ Livro Digital (versão completa)</li>
            <li>✅ Curso em Vídeo (7 módulos)</li>
            <li>✅ Acesso à Comunidade</li>
          </ul>''', '''<p>Aprenda a reconhecer e governar as emoções que tomam conta da sua vida: ansiedade, medo, mágoas e dúvidas. Um caminho de leitura, oração e prática para acalmar a mente e despertar a alma em Deus.</p>
          <ul class="obra-itens">
            <li>✅ Livro completo para ler em casa</li>
            <li>✅ 7 videoaulas guiadas pela Palavra</li>
            <li>✅ Oração e prática em cada capítulo</li>
            <li>✅ Acesso à comunidade vitalícia</li>
          </ul>'''),
    ('index.html', '''<p>Livro digital completo + Curso em vídeo com 7 módulos para quebrar correntes invisíveis e retomar a soberania da mente.</p>
          <ul class="obra-itens">
            <li>✅ Livro Digital (versão completa)</li>
            <li>✅ Curso em Vídeo (7 módulos)</li>
            <li>✅ Acesso à Comunidade</li>
          </ul>''', '''<p>Entenda como os pensamentos acelerados, os algoritmos e os padrões invisíveis roubam a sua paz, e aprenda em Cristo a retomar o governo da sua mente.</p>
          <ul class="obra-itens">
            <li>✅ Livro completo para ler em casa</li>
            <li>✅ 7 videoaulas guiadas pela Palavra</li>
            <li>✅ Estratégias práticas de sobriedade mental</li>
            <li>✅ Acesso à comunidade vitalícia</li>
          </ul>'''),
    ('index.html', '''<p>Devocional de 30 dias + E-book infantil Jesus Quer Falar com Seu Filho para toda a família.</p>
          <ul class="obra-itens">
            <li>✅ Devocional 30 dias</li>
            <li>✅ E-book Infantil</li>
            <li>✅ Acesso à Comunidade</li>
          </ul>''', '''<p>30 dias de oração, reflexão e prática para começar cada manhã na presença de Deus, mesmo em meio à correria. Trinta dias para criar um novo ritmo de fé.</p>
          <ul class="obra-itens">
            <li>✅ Devocional de 30 dias</li>
            <li>✅ Oração e prática para o seu dia</li>
            <li>✅ E-book infantil Jesus quer falar com seu filho</li>
            <li>✅ Acesso à comunidade vitalícia</li>
          </ul>'''),
    ('index.html', '''<p>Uma jornada simples pelas Boas Novas de Cristo. Livro aberto. Leia de graça.</p>
          <ul class="obra-itens">
            <li>✅ Obra da Missão</li>
            <li>✅ Disponível na biblioteca</li>
            <li>✅ Leitura gratuita no portal</li>
          </ul>''', '''<p>As Boas Novas de Cristo em linguagem simples: evangelhos, parábolas, sermões, cartas e esperança. Uma jornada clara para quem quer entender a fé e despertar.</p>
          <ul class="obra-itens">
            <li>✅ Obra da Missão</li>
            <li>✅ 20 capítulos em leitura limpa</li>
            <li>✅ Leitura gratuita no portal</li>
            <li>✅ PDF de bônus no acesso completo</li>
          </ul>'''),
    ('index.html', '''<p>Obra infantil cristã: Mandamentos, valores bíblicos e o amor de Jesus para as crianças.</p>
          <ul class="obra-itens">
            <li>✅ E-book infantil da Missão</li>
            <li>✅ Atividades para pintar e desenhar</li>
            <li>✅ Leitura gratuita no portal</li>
          </ul>''', '''<p>Uma obra para a família: os Mandamentos, os valores bíblicos e o amor de Jesus explicados para as crianças, com atividades para ler, pintar e fazer juntos.</p>
          <ul class="obra-itens">
            <li>✅ Obra infantil da Missão</li>
            <li>✅ Histórias e versículos para conversar</li>
            <li>✅ Atividades para pintar e desenhar</li>
            <li>✅ Leitura gratuita no portal</li>
          </ul>'''),
    ('index.html', '''<h2>🕊️ Seja um Semeador da Missão e ganhe um Brinde Extra</h2>''',
     '''<h2>🕊️ Seja um Semeador da Missão e ganhe 4 bônus</h2>'''),
    ('index.html', '''<ul>
          <li>✅ Somente os livros digitais da Missão (versão completa)</li>
          <li>✅ Todos os Cursos em Vídeo (14 módulos)</li>
          <li>✅ Devocional Um Segundo com Deus (30 dias)</li>
          <li>✅ E-book Jesus Quer Falar com Seu Filho</li>
          <li>✅ Acesso Vitalício à Comunidade Portal Missão com Deus</li>
          <li>🎁 Brinde extra: PDF O Novo Testamento como nunca lido (para guardar)</li>

        </ul>''', '''<ul>
          <li>✅ Livro digital completo: Evolução da Alma</li>
          <li>✅ Livro digital completo: Anestesia Mental</li>
          <li>✅ 7 módulos em vídeo: Evolução da Alma</li>
          <li>✅ 7 módulos em vídeo: Anestesia Mental</li>
          <li>✅ Acesso vitalício à Área de Membros e à Comunidade</li>
          <li>🎁 Bônus 1: O Novo Testamento como nunca lido</li>
          <li>🎁 Bônus 2: Devocional Um Segundo com Deus, 30 dias</li>
          <li>🎁 Bônus 3: Jesus Quer Falar com Seu Filho</li>
          <li>🎁 Bônus 4: Afirmações, Declarações e Orações, guia diário em PDF</li>

        </ul>'''),
    ('index.html', '''<li>Livros digitais da Missão + 14 módulos</li>
          <li>Exercícios, comunidade e Devocional</li>
          <li>R$ 37,00 pagamento único</li>''',
     '''<li>2 livros digitais completos</li>
          <li>14 módulos em vídeo</li>
          <li>Exercícios, comunidade e 4 bônus</li>
          <li>R$ 37,00 pagamento único</li>'''),
    ('index.html', '''As quatro aulas no site são só o começo. E a casa reserva um presente depois do acesso. Não adiantamos o nome: chega como surpresa.''',
     '''Os módulos 1 a 3 já estão grátis no site, para você conhecer antes de decidir. Além disso, a casa envia 4 bônus: o Novo Testamento como nunca lido, o Devocional Um Segundo com Deus, o e-book Jesus Quer Falar com Seu Filho e o guia diário Afirmações, Declarações e Orações em PDF.'''),
    ('index.html', '''Os módulos 1 a 3 já estão grátis no site, para você conhecer antes de decidir. Na área de membros você recebe o estudo completo e o presente extra da casa: o PDF do Novo Testamento como nunca lido, para guardar.''',
     '''Os módulos 1 a 3 já estão grátis no site, para você conhecer antes de decidir. Além disso, a casa envia 4 bônus: o Novo Testamento como nunca lido, o Devocional Um Segundo com Deus, o e-book Jesus Quer Falar com Seu Filho e o guia diário Afirmações, Declarações e Orações em PDF.'''),

    ('trilogia-da-alma.html', '''<p style="text-align:center;color:#e3c877;font-size:.92rem;margin:10px 0 0;">🎁 Brinde extra: PDF O Novo Testamento como nunca lido, para guardar.</p>''',
     '''<p style="text-align:center;color:#e3c877;font-size:.92rem;margin:10px 0 0;">🎁 E, além do acesso completo, a casa envia 4 bônus:</p>
    <p style="text-align:center;color:#b0bec5;font-size:.84rem;margin:4px 0 0;">O Novo Testamento, o Devocional 30 dias, o e-book Jesus Quer Falar com Seu Filho e o guia Afirmações, Declarações e Orações em PDF.</p>'''),
    ('trilogia-da-alma.html', '''<li>✅ Os dois cursos em vídeo (14 módulos)</li>
        <li>✅ Livros digitais + comunidade vitalícia</li>
        <li>✅ Devocional e e-book infantil de brinde</li>
        <li>🎁 Brinde extra: PDF do Novo Testamento como nunca lido</li>''',
     '''<li>✅ 2 livros digitais completos</li>
        <li>✅ 14 módulos em vídeo</li>
        <li>✅ Acesso vitalício à Área de Membros</li>
        <li>🎁 Bônus 1: O Novo Testamento como nunca lido</li>
        <li>🎁 Bônus 2: Devocional Um Segundo com Deus, 30 dias</li>
        <li>🎁 Bônus 3: Jesus Quer Falar com Seu Filho</li>
        <li>🎁 Bônus 4: Afirmações, Declarações e Orações, em PDF</li>'''),

    ('anestesia-mental.html', '''<p style="text-align:center;color:#e3c877;font-size:.92rem;margin:10px 0 0;">🎁 Brinde extra: PDF O Novo Testamento como nunca lido, para guardar.</p>''',
     '''<p style="text-align:center;color:#e3c877;font-size:.92rem;margin:10px 0 0;">🎁 E, além do acesso completo, a casa envia 4 bônus:</p>
    <p style="text-align:center;color:#b0bec5;font-size:.84rem;margin:4px 0 0;">O Novo Testamento, o Devocional 30 dias, o e-book Jesus Quer Falar com Seu Filho e o guia Afirmações, Declarações e Orações em PDF.</p>'''),
    ('anestesia-mental.html', '''<li>✅ Os dois cursos em vídeo (14 módulos)</li>
        <li>✅ Livros digitais + comunidade vitalícia</li>
        <li>✅ Devocional e e-book infantil de brinde</li>
        <li>🎁 Brinde extra: PDF do Novo Testamento como nunca lido</li>''',
     '''<li>✅ 2 livros digitais completos</li>
        <li>✅ 14 módulos em vídeo</li>
        <li>✅ Acesso vitalício à Área de Membros</li>
        <li>🎁 Bônus 1: O Novo Testamento como nunca lido</li>
        <li>🎁 Bônus 2: Devocional Um Segundo com Deus, 30 dias</li>
        <li>🎁 Bônus 3: Jesus Quer Falar com Seu Filho</li>
        <li>🎁 Bônus 4: Afirmações, Declarações e Orações, em PDF</li>'''),

    ('livro07.html', '''<p class="portao-preco">Pagamento único · Acesso vitalício · Pix imediato · Cartão até 4x · menos de R$ 1,25/dia</p>''',
     '''<p class="portao-preco">Pagamento único · Acesso vitalício · Pix imediato · Cartão até 4x · menos de R$ 1,25/dia</p>
    <p style="color:#e3c877;font-size:.9rem;margin-top:16px;">🎁 Além do acesso completo, a casa envia 4 bônus:</p>
    <p style="color:#b0bec5;font-size:.82rem;margin:4px 0 0;">O Novo Testamento, o Devocional Um Segundo com Deus, o e-book Jesus Quer Falar com Seu Filho e o guia Afirmações, Declarações e Orações em PDF.</p>'''),
    ('livro07.html', '''<strong>Quer assistir as videoaulas do Livro Evolução da Alma? 👀</strong>
      <span>Módulos 1 a 4 já estão na área do Aluno. Uma prévia resumida te aguarda.</span>''',
     '''<strong>Quer conhecer o acesso completo da Missão? 👀</strong>
      <span>Módulos 1 a 3 de cada curso já estão disponíveis. O restante está na área de membros.</span>'''),

    ('livro11.html', '''<p class="portao-preco">Pagamento único · Acesso vitalício · Pix imediato · Cartão até 4x · menos de R$ 1,25/dia</p>''',
     '''<p class="portao-preco">Pagamento único · Acesso vitalício · Pix imediato · Cartão até 4x · menos de R$ 1,25/dia</p>
    <p style="color:#e3c877;font-size:.9rem;margin-top:16px;">🎁 Além do acesso completo, a casa envia 4 bônus:</p>
    <p style="color:#b0bec5;font-size:.82rem;margin:4px 0 0;">O Novo Testamento, o Devocional Um Segundo com Deus, o e-book Jesus Quer Falar com Seu Filho e o guia Afirmações, Declarações e Orações em PDF.</p>'''),
    ('livro11.html', '''<strong>Quer assistir as videoaulas do Livro Evolução da Alma? 👀</strong>
      <span>Módulos 1 a 3 já estão na área do Aluno. Uma prévia resumida te aguarda.</span>''',
     '''<strong>Quer conhecer o acesso completo da Missão? 👀</strong>
      <span>Módulos 1 a 3 de cada curso já estão disponíveis. O restante está na área de membros.</span>'''),

    ('livro09.html', '''Módulos 1 a 4 já estão na área do Aluno. Uma prévia resumida te aguarda.''',
     '''Módulos 1 a 3 já estão na área do Aluno. Uma prévia resumida te aguarda.'''),
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
        bak = arq.with_name('%s-antes-4bonus-%s.bak' % (arq.stem, stamp))
        bak.write_text(t, encoding='utf-8')
        t = t.replace(velho, novo, 1)
        arq.write_text(t, encoding='utf-8')
        total += 1
        print('OK', nome, '->', bak.name)
    print('Trocas aplicadas:', total)
    print('Teste: Home oferta com 4 bônus, pontes com 4 bônus, livros 07/11 com 4 bônus.')


if __name__ == '__main__':
    main()
