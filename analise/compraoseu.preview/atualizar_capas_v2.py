# -*- coding: utf-8 -*-
"""
Atualiza as capas dos cards da Home com os novos links imgbb (refeitos com
mais qualidade) e adiciona 2 novos cards ao final: Apoio e Garantia.
Também atualiza as páginas individuais dos livros cuja capa mudou.
"""
import re
from pathlib import Path

ROOT = Path('/home/user/instalador')
HOME = ROOT / 'paginas' / 'home_preview.html'

# Mapeamento: link antigo -> link novo (por título do card na Home)
TROCAS = [
    # O Novo Testamento (card 1)
    ('https://i.ibb.co/qF4mk3GC/livro11.jpg', 'https://i.ibb.co/9myJ3XXb/livro01.jpg'),
    # O Verbo que Transforma (card 6)
    ('https://i.ibb.co/b52wmSGm/livro01jpg.jpg', 'https://i.ibb.co/23CJFpyq/livro06.jpg'),
    # A Mente Renovada (card 7)
    ('https://i.ibb.co/20jLgxZN/livro03jpg.jpg', 'https://i.ibb.co/TB1L9fv9/livro07.jpg'),
    # O Caminho do Despertar (card 8)
    ('https://i.ibb.co/SDML88Rq/livro07jpg.jpg', 'https://i.ibb.co/Gf7WWL6H/livro08.jpg'),
    # O Arquiteto da Realidade (card 9)
    ('https://i.ibb.co/mV3S1m78/livro08jpg.jpg', 'https://i.ibb.co/vCz5jKND/livro09.jpg'),
    # O Despertar do Observador (card 10)
    ('https://i.ibb.co/mV3RKS17/livro10jpg.jpg', 'https://i.ibb.co/ZRXwG60f/livro10.jpg'),
    # A Sabedoria dos Mestres (card 11)
    ('https://i.ibb.co/W42S6bX0/livro02jpg.jpg', 'https://i.ibb.co/0jS3KGHc/livro11.jpg'),
]

texto = HOME.read_text(encoding='utf-8')
for antigo, novo in TROCAS:
    if antigo in texto:
        texto = texto.replace(antigo, novo)
        print(f'✔ {antigo.split("/")[-1]} -> {novo.split("/")[-1]}')
    else:
        print(f'⚠ não encontrado: {antigo}')

# Adiciona CSS para card com imagem inteira (não cortada)
css_inteiro = '''
  .bib-capa.inteiro{height:300px;}
  .bib-capa.inteiro .capa-img{object-fit:contain;padding:8px;}
'''
# insere antes do fechamento do </style>
if '.bib-capa.inteiro' not in texto:
    texto = texto.replace('</style>', css_inteiro + '</style>', 1)
    print('✔ CSS .bib-capa.inteiro adicionado')

# Adiciona os 2 cards antes do rodapé da biblioteca
card_apoio = '''      <!-- CARD APOIO -->
      <div class="bib-card">
        <div class="bib-capa inteiro"><img class="capa-img" src="https://i.ibb.co/WWfW18pY/ajuda.jpg" alt="Ajude o Portal O Despertar"></div>
        <div class="bib-corpo">
          <span class="bib-num">🙏 Apoie o Portal</span>
          <h3>Ajude a manter esta obra viva</h3>
          <p class="bib-desc">Cada contribuição mantém o Portal aberto e a leitura gratuita disponível para todos que precisam despertar.</p>
          <div class="bib-badges">
            <span class="bib-badge">💛 Missão com Deus</span>
          </div>
          <div class="bib-ctas">
            <a class="btn" href="https://pay.kiwify.com.br/CF9nhFx">Apoiar com R$ 9,90</a>
            <a class="btn btn-sec" href="https://pay.kiwify.com.br/iVfp2bi">Portal</a>
          </div>
        </div>
      </div>'''

card_garantia = '''      <!-- CARD GARANTIA -->
      <div class="bib-card">
        <div class="bib-capa inteiro"><img class="capa-img" src="https://i.ibb.co/xqftx9DS/7dias.jpg" alt="Garantia incondicional de 7 dias"></div>
        <div class="bib-corpo">
          <span class="bib-num">🛡️ Garantia</span>
          <h3>7 dias de garantia incondicional</h3>
          <p class="bib-desc">Se não fizer sentido para você, devolvemos 100% do investimento, sem perguntas e sem burocracia.</p>
          <div class="bib-badges">
            <span class="bib-badge">🛡️ Risco zero</span>
          </div>
          <div class="bib-ctas">
            <a class="btn" href="https://pay.kiwify.com.br/iVfp2bi">Garantir meu acesso</a>
          </div>
        </div>
      </div>'''

marcador = '    <p class="bib-foot">'
if marcador in texto and 'CARD APOIO' not in texto:
    texto = texto.replace(marcador, card_apoio + '\n\n' + card_garantia + '\n\n' + marcador, 1)
    print('✔ Cards de Apoio e Garantia adicionados')

HOME.write_text(texto, encoding='utf-8')
print('✅ Home atualizada')

# Atualiza páginas individuais dos livros cuja capa mudou (para consistência)
paginas_trocas = {
    'livro01': ('https://i.ibb.co/b52wmSGm/livro01jpg.jpg', 'https://i.ibb.co/23CJFpyq/livro06.jpg'),
    'livro02': ('https://i.ibb.co/W42S6bX0/livro02jpg.jpg', 'https://i.ibb.co/0jS3KGHc/livro11.jpg'),
    'livro03': ('https://i.ibb.co/20jLgxZN/livro03jpg.jpg', 'https://i.ibb.co/TB1L9fv9/livro07.jpg'),
    'livro07': ('https://i.ibb.co/SDML88Rq/livro07jpg.jpg', 'https://i.ibb.co/Gf7WWL6H/livro08.jpg'),
    'livro08': ('https://i.ibb.co/mV3S1m78/livro08jpg.jpg', 'https://i.ibb.co/vCz5jKND/livro09.jpg'),
    'livro10': ('https://i.ibb.co/mV3RKS17/livro10jpg.jpg', 'https://i.ibb.co/ZRXwG60f/livro10.jpg'),
}
for slug, (antigo, novo) in paginas_trocas.items():
    p = ROOT / 'paginas' / f'{slug}_preview.html'
    if p.exists():
        t = p.read_text(encoding='utf-8')
        if antigo in t:
            t = t.replace(antigo, novo)
            p.write_text(t, encoding='utf-8')
            print(f'✔ {slug}_preview.html atualizado')
        else:
            print(f'⚠ {slug}_preview.html: link antigo não encontrado')
