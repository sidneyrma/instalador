# -*- coding: utf-8 -*-
"""
Reordena os cards da biblioteca na Home e adiciona o Livro 11 no topo.

Nova ordem (posição -> livro original):
 1: Livro 11 (novo)  -> "Em breve"
 2: Livro 05 -> Evolução da Alma
 3: Livro 09 -> Anestesia Mental
 4: Livro 04 -> Um Segundo com Deus
 5: Livro 06 -> Jesus Quer Falar com Seu Filho
 6: Livro 01 -> O Verbo que Transforma
 7: Livro 03 -> A Mente Renovada
 8: Livro 07 -> O Caminho do Despertar
 9: Livro 08 -> O Arquiteto da Realidade
10: Livro 10 -> O Despertar do Observador
11: Livro 02 -> A Sabedoria dos Mestres
"""
import re
from pathlib import Path

HOME = Path('/home/user/instalador/paginas/home_preview.html')
texto = HOME.read_text(encoding='utf-8')

inicio = texto.find('<section class="biblioteca" id="biblioteca">')
fim = texto.find('</section>', inicio)
secao = texto[inicio:fim]

cab = secao[:secao.find('      <!-- LIVRO 01 -->')]
idx_foot = secao.find('<p class="bib-foot">')
rodape = secao[idx_foot:] if idx_foot != -1 else ''

# Captura cada card: começa com comentário (LIVRO ou DEVOCIONAL) e vai até </div>\n      </div>
cards = re.findall(r'<!-- (?:LIVRO \d+[^>]*|DEVOCIONAL) -->.*?</div>\n      </div>', secao, re.DOTALL)
print('Cards encontrados:', len(cards))

# Mapeia cada card pelo bib-num real
card_por_num = {}
for c in cards:
    m = re.search(r'<span class="bib-num">Livro (\d+) ·', c)
    if m:
        card_por_num[int(m.group(1))] = c
    else:
        print('⚠ card sem numeração:', c[:60])
print('Números reais:', sorted(card_por_num.keys()))

card11 = '''      <!-- LIVRO 11: O NOVO TESTAMENTO -->
      <div class="bib-card">
        <div class="bib-capa"><img class="capa-img" src="https://i.ibb.co/qF4mk3GC/livro11.jpg" alt="O Novo Testamento como nunca lido - capa"></div>
        <div class="bib-corpo">
          <span class="bib-num">Livro 01 · Em breve</span>
          <h3>O Novo Testamento como nunca lido</h3>
          <p class="bib-desc">Uma jornada simples pelas Boas Novas de Cristo, com as passagens mais faladas, as parábolas e os sermões explicados para despertar a fé.</p>
          <div class="bib-badges">
            <span class="bib-badge">20 capítulos</span>
            <span class="bib-badge">✨ Em breve</span>
          </div>
          <div class="bib-ctas">
            <a class="btn" href="#" style="pointer-events:none;opacity:.75;">Em breve</a>
            <a class="btn btn-sec" href="https://pay.kiwify.com.br/iVfp2bi">Portal</a>
          </div>
        </div>
      </div>'''

nova_ordem = [11, 5, 9, 4, 6, 1, 3, 7, 8, 10, 2]

cards_ordenados = []
for pos, num in enumerate(nova_ordem, start=1):
    card = card11 if num == 11 else card_por_num[num]
    card = re.sub(r'<!-- [^>]*-->', f'<!-- LIVRO {pos:02d} -->', card, count=1)
    card = re.sub(r'<span class="bib-num">Livro \d+ · ', f'<span class="bib-num">Livro {pos:02d} · ', card)
    cards_ordenados.append(card)

nova_secao = cab + '\n\n' + '\n\n'.join(cards_ordenados) + '\n    ' + rodape
texto_novo = texto[:inicio] + nova_secao + texto[fim:]
HOME.write_text(texto_novo, encoding='utf-8')
print('✅ Home reordenada com', len(cards_ordenados), 'cards')
