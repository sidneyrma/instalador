# -*- coding: utf-8 -*-
"""
Gera a página HTML do livro 'Comece o dia com Afirmações, Declarações e Orações'.
Inclui: gratidão, 8 categorias de afirmações, orações do dia, orações de fé e versículos.
"""
import re, html
from pathlib import Path

ROOT = Path('/home/user/instalador')
OUT = ROOT / 'paginas' / 'livro12_preview.html'

TITULO = 'Comece o dia com Afirmações, Declarações e Orações'
SUBTITULO = 'Versículos, gratidão, afirmações e orações para fortalecer a sua fé'

def esc(t):
    return html.escape(t, quote=False)

GRATIDAO = [
    'Em tudo dai graças, porque esta é a vontade de Deus em Cristo Jesus para convosco. (1 Tessalonicenses 5:18)',
    'Bendize, ó minha alma, ao Senhor, e não te esqueças de nenhum dos seus benefícios. Ele perdoa todas as tuas iniquidades e sara todas as tuas enfermidades. (Salmo 103:2-3)',
    'Entrai pelas portas dele com gratidão e nos seus átrios com louvor; louvai-o e bendizei o seu nome. (Salmo 100:4)',
    'Toda a boa dádiva e todo o dom perfeito vem do alto, descendo do Pai das luzes. (Tiago 1:17)',
    'Obrigado, Senhor, pelo dom da vida, pelo ar que respiro, pelo pão de cada dia e pelo teu amor que nunca falha.',
    'Obrigado, Senhor, porque até nas dificuldades tu estás comigo, e todas as coisas cooperam para o meu bem. (Romanos 8:28)',
    'Obrigado, Pai, pela família, pelos amigos e pelas pessoas que colocas no meu caminho como bênção.',
    'Comece o dia agradecendo. A gratidão abre as portas do céu e transforma o coração.',
]

CATEGORIAS = [
    {'titulo': 'Saúde e Cura', 'icone': '🩺', 'afirmacoes': [
        'Eu sou curado pelas feridas de Jesus. (Isaías 53:5)',
        'Eu sou templo do Espírito Santo, e a vida de Deus flui em mim. (1 Coríntios 6:19)',
        'Eu sou renovado em saúde, porque o Senhor é o meu médico.',
        'Eu sou forte, resiliente e capaz de superar qualquer desafio.',
        'Senhor, tu és o médico de minha alma e de meu corpo. Renova minha mente e sara minhas emoções.',
    ]},
    {'titulo': 'Rejuvenescimento e Vitalidade', 'icone': '🌿', 'afirmacoes': [
        'Eu sou renovado como a águia, e as minhas forças se renovam. (Isaías 40:31)',
        'Eu sou nova criatura em Cristo, e cada dia a minha vitalidade é renovada. (2 Coríntios 5:17)',
        'Eu sou cheio de vida, porque o Espírito que habita em mim é vida.',
        'Eu sou jovem no coração, porque a alegria do Senhor é a minha força. (Neemias 8:10)',
        'Eu sou restaurado em corpo, alma e espírito, porque Deus é o restaurador da minha vida.',
    ]},
    {'titulo': 'Paz e Emoções (ansiedade, medo)', 'icone': '🕊️', 'afirmacoes': [
        'Eu sou guardado pela paz de Deus, que excede todo entendimento. (Filipenses 4:7)',
        'Eu sou livre do medo, porque Deus não me deu espírito de temor. (2 Timóteo 1:7)',
        'Eu sou tranquilo, porque o Senhor está comigo e nada me faltará. (Salmo 23:1)',
        'Eu sou a consciência que observa os pensamentos, e essa consciência é de Deus.',
        'Eu sou pacificador, porque sou filho de Deus. (Mateus 5:9)',
        'Senhor, quando o medo bater à porta, envia a fé para atender.',
        'Não andeis ansiosos pelo dia de amanhã, nem pela vossa vida, pelo que haveis de comer ou beber, nem pelo corpo, pelo que haveis de vestir. Olhai para as aves do céu, que não semeiam nem colhem, e o Pai celestial as alimenta. Buscai primeiro o Reino de Deus, e todas estas coisas vos serão acrescentadas. (Mateus 6:25-34)',
        'Jesus disse: Não andeis ansiosos pela vossa vida. O vosso Pai celestial sabe que necessitais de todas estas coisas. (Mateus 6:25, 32)',
    ]},
    {'titulo': 'Prosperidade e Provisão', 'icone': '💛', 'afirmacoes': [
        'Eu sou próspero na vontade de Deus, porque Ele supre todas as minhas necessidades. (Filipenses 4:19)',
        'Eu sou um canal limpo de riqueza infinita.',
        'Eu sou abençoado para ser bênção. (Gênesis 12:2)',
        'Eu sou o templo do verbo dourado, e a provisão de Deus flui em minha vida.',
        'Eu sou grato, porque todas as coisas cooperam para o bem. (Romanos 8:28)',
    ]},
    {'titulo': 'Identidade em Cristo (quem eu sou)', 'icone': '👑', 'afirmacoes': [
        'Eu sou filho amado de Deus.',
        'Eu sou mais que vencedor em Cristo Jesus. (Romanos 8:37)',
        'Eu sou luz do mundo. (Mateus 5:14)',
        'Eu sou sal da terra. (Mateus 5:13)',
        'Eu sou amado com amor eterno. (Jeremias 31:3)',
        'Eu sou digno(a) de amor, paz e felicidade.',
        'Eu sou cidadão do Reino de Deus.',
        'Eu sou esperança viva pela ressurreição de Jesus. (1 Pedro 1:3)',
    ]},
    {'titulo': 'Proteção e Segurança', 'icone': '🛡️', 'afirmacoes': [
        'Eu sou guardado pelo Senhor, que é o meu refúgio e fortaleza. (Salmo 46:1)',
        'Eu sou protegido debaixo das asas do Altíssimo. (Salmo 91)',
        'Eu sou seguro, porque o Senhor é o meu pastor. (Salmo 23:1)',
        'Eu sou livre, porque Cristo me libertou. (Gálatas 5:1)',
        'Eu sou ovelha do Bom Pastor, e nada me faltará. (Salmo 23:1)',
        'O Senhor é o meu pastor, nada me faltará. Deitar-me faz em verdes pastos, guia-me mansamente a águas tranquilas. Refrigera a minha alma, guia-me pelas veredas da justiça por amor do seu nome. Ainda que eu andasse pelo vale da sombra da morte, não temeria mal algum, porque tu estás comigo; a tua vara e o teu cajado me consolam. (Salmo 23)',
        'Preparas uma mesa perante mim na presença dos meus inimigos, unges a minha cabeça com óleo, o meu cálice transborda. Certamente que a bondade e a misericórdia me seguirão todos os dias da minha vida, e habitarei na casa do Senhor por longos dias. (Salmo 23:5-6)',
    ]},
    {'titulo': 'Força e Superação', 'icone': '💪', 'afirmacoes': [
        'Eu sou forte na força do Senhor. (Efésios 6:10)',
        'Eu posso todas as coisas naquele que me fortalece. (Filipenses 4:13)',
        'Eu sou capaz, porque Deus está comigo.',
        'Eu sou alguém que cria oportunidades e encontra soluções.',
        'Eu sou uma pessoa capaz de crescer e evoluir.',
    ]},
    {'titulo': 'Relacionamentos e Perdão', 'icone': '❤️', 'afirmacoes': [
        'Eu sou perdoado, porque Cristo me perdoou. (Efésios 4:32)',
        'Eu sou próximo de qualquer pessoa que precisa de mim, onde quer que ela esteja.',
        'Eu sou amoroso, porque o amor de Deus foi derramado no meu coração. (Romanos 5:5)',
        'Eu sou compassivo, porque fui compadecido por Deus.',
        'Eu sou um instrumento de paz, porque sou filho do Príncipe da Paz.',
        'Cria em mim, ó Deus, um coração puro e renova em mim um espírito estável. Não me lances fora da tua presença e não retires de mim o teu Santo Espírito. Restitui-me a alegria da tua salvação e sustenta-me com um espírito voluntário. (Salmo 51:10-12)',
        'Jesus disse: Amai os vossos inimigos, bendizei os que vos maldizem, fazei bem aos que vos odeiam e orai pelos que vos maltratam e vos perseguem, para que sejais filhos do vosso Pai que está nos céus. (Mateus 5:44-45)',
        'Perdoa-nos as nossas dívidas, assim como nós perdoamos aos nossos devedores. (Mateus 6:12)',
    ]},
]

ORACOES = [
    'Senhor, ajuda-me a reconhecer que não sou meus pensamentos. Ensina-me a observar a mente com serenidade e a escolher, dia após dia, o pensamento que vem de ti.',
    'Senhor, coloca guarda em meus lábios. Que minhas palavras sejam sementes de bênção e que minha fé cresça a cada dia no exercício da confiança.',
    'Senhor, purifica meu olhar e meu coração. Tira de mim o julgamento, o ressentimento e a duplicidade. Dá-me o olho único, que vê a verdade.',
    'Senhor, ensina-me a orar sem cessar. Que meu coração esteja em diálogo contigo em cada momento, em cada tarefa, em cada encontro.',
    'Senhor, dá-me um coração grato em todos os dias, nos fáceis e nos difíceis. Ensina-me a lembrar tuas bondades e a reconhecer o bem que permanece.',
    'Senhor Jesus, tu és o mesmo ontem, hoje e eternamente. Aumenta a minha fé, para que eu confie na tua palavra mesmo quando as circunstâncias parecem impossíveis.',
    'Pai de amor, obrigado porque não me rejeitas quando volto para ti. Obrigado porque correste ao meu encontro, me abraçaste, me restauraste.',
    'Senhor, prepara o solo do meu coração. Arranca as pedras, remove os espinhos, ara a terra com a tua Palavra. Que eu ouça, compreenda e retenha os teus ensinamentos.',
    'Senhor Jesus, eu quero te seguir, mas muitas vezes tenho medo da cruz. Ajuda-me a confiar que o teu caminho é o caminho da vida.',
    'Senhor, obrigado pelos talentos que me confiaste. Ajuda-me a não os enterrar por medo, mas a multiplicá-los com fé e coragem, para a tua glória.',
]

ORACOES_DE_FE = [
    {'titulo': 'Oração de Proteção (baseada no Salmo 91)', 'icone': '🛡️', 'orao': 'Senhor Deus Altíssimo, tu és o meu refúgio e a minha fortaleza, em ti confio. Tu me livras do laço do inimigo e da palavra destruidora. Sob as tuas asas encontro abrigo, e a tua verdade é o meu escudo. Não temerei os terrores da noite, nem a seta que voa de dia, porque ordenaste aos teus anjos que me guardem em todos os meus caminhos. Em nome de Jesus, amém.'},
    {'titulo': 'Oração de Autoridade no Nome de Jesus', 'icone': '✝️', 'orao': 'Senhor Jesus, tu és o nome que está acima de todo nome, e diante de ti todo joelho se dobra, no céu, na terra e debaixo da terra. Pela autoridade do teu nome, eu declaro que todo medo, toda ansiedade, toda opressão e todo mal se curvam diante de ti. Nada me atingirá, porque estou escondido em ti. Que a tua paz, que excede todo entendimento, guarde o meu coração e a minha mente. Amém.'},
    {'titulo': 'Oração de Cura do Corpo e da Alma', 'icone': '🩺', 'orao': 'Senhor Jesus, pelas tuas feridas fui curado. Tu levaste as minhas dores e carregaste as minhas enfermidades. Toca o meu corpo, sara as minhas emoções, renova as minhas forças. Derrama a tua vida em cada célula do meu ser. Que a tua paz invada a minha alma e a tua saúde flua em mim. Confio em ti, meu médico e meu Senhor. Amém.'},
    {'titulo': 'Oração pela Família', 'icone': '🏡', 'orao': 'Senhor, eu e a minha casa serviremos ao Senhor. Abençoa a minha família, une os nossos corações, afasta de nós toda divisão, brigas e incompreensão. Que o amor, o respeito e o diálogo reinem no nosso lar. Protege cada membro da minha família, guia os nossos passos e faz de nós um instrumento do teu amor. Em nome de Jesus, amém.'},
    {'titulo': 'Oração de Trabalho e Provisão', 'icone': '💼', 'orao': 'Senhor, tu és a minha provisão e o meu provedor. Abençoa o trabalho das minhas mãos, abre portas que nenhum homem pode fechar, e guia-me nos caminhos profissionais. Dai-me sabedoria, diligência e honestidade. Eu busco primeiro o teu Reino, e confio que todas as coisas me serão acrescentadas segundo a tua vontade. Em nome de Jesus, amém.'},
    {'titulo': 'Oração de Paz e Serenidade', 'icone': '🌊', 'orao': 'Senhor, tu és a minha paz. A tua paz, que excede todo entendimento, guarda o meu coração e a minha mente em Cristo Jesus. Não ando ansioso por coisa alguma, mas em tudo, pela oração e súplica, apresento os meus pedidos a ti. Entrego as minhas preocupações, confio no teu cuidado, e descanso em ti, porque tu cuidas de mim. Amém.'},
    {'titulo': 'Oração por Causas Difíceis', 'icone': '⚡', 'orao': 'Senhor Jesus, para ti nada é impossível. Tu és o Deus que faz caminho onde não há caminho, que abre portas que ninguém pode fechar. Apresento diante de ti esta causa que parece sem solução. Aumenta a minha fé, dá-me esperança e paciência. Eu creio que estás agindo, mesmo quando não vejo. Que a tua vontade seja feita, e que a tua glória se manifeste. Amém.'},
    {'titulo': 'Oração de Gratidão e Louvor', 'icone': '🙌', 'orao': 'Senhor, em tudo eu dou graças, porque esta é a tua vontade para mim. Bendigo o teu nome por cada bênção, por cada desafio, por cada aprendizado. Toda boa dádiva vem de ti. Que o meu coração seja cheio de gratidão, e que o meu louvor suba como incenso diante de ti. Obrigado pelo teu amor que nunca falha. Em nome de Jesus, amém.'},
    {'titulo': 'Oração de Perdão e Recomeço', 'icone': '❤️', 'orao': 'Senhor, cria em mim um coração puro e renova em mim um espírito estável. Perdoa as minhas falhas, como eu perdoo aqueles que me feriram. Ajuda-me a amar os meus inimigos, a bendizer os que me maldizem e a orar por aqueles que me perseguem, como Jesus ensinou. Restitui-me a alegria da tua salvação e sustenta-me com um espírito voluntário. Amém.'},
    {'titulo': 'Oração de Entrega e Confiança', 'icone': '🤲', 'orao': 'Senhor, entrego a minha vida nas tuas mãos. Não a minha vontade, mas a tua seja feita. Confio no teu plano, mesmo quando não entendo. Tu conheces o meu futuro, tu seguras o meu amanhã. Ensina-me a viver um dia de cada vez, confiando na tua bondade. Que eu descanse em ti, porque tu és o meu pastor e nada me faltará. Em nome de Jesus, amém.'},
]


VERSICULOS = [
    ('Posso todas as coisas naquele que me fortalece.', 'Filipenses 4:13'),
    ('Todas as coisas cooperam para o bem daqueles que amam a Deus.', 'Romanos 8:28'),
    ('Maior é o que está em mim do que o que está no mundo.', '1 João 4:4'),
    ('Eu e o Pai somos um.', 'João 10:30'),
    ('O Senhor é o meu pastor; nada me faltará.', 'Salmo 23:1'),
    ('Deus é o nosso refúgio e fortaleza, socorro bem presente na angústia.', 'Salmo 46:1'),
    ('A alegria do Senhor é a minha força.', 'Neemias 8:10'),
    ('Vivo pela fé no Filho de Deus, que me amou e se entregou por mim.', 'Gálatas 2:20'),
    ('A morte e a vida estão no poder da língua.', 'Provérbios 18:21'),
    ('Pela fé entendemos que os mundos foram criados pela palavra de Deus.', 'Hebreus 11:3'),
]

def build():
    # Sumário
    toc = ['<li class="toc-parte">🙌 Gratidão</li>']
    toc.append('<li><a href="#gratidao">Versículos e mensagens de gratidão</a></li>')
    toc.append('<li class="toc-parte">📂 Categorias de Afirmações</li>')
    for i, cat in enumerate(CATEGORIAS, 1):
        toc.append(f'<li><a href="#cat-{i}">{cat["icone"]} {esc(cat["titulo"])}</a></li>')
    toc.append('<li class="toc-parte">🙏 Orações</li>')
    toc.append('<li><a href="#oracoes">Orações para o dia a dia</a></li>')
    toc.append('<li class="toc-parte">📖 Versículos</li>')
    toc.append('<li><a href="#versiculos">Versículos de declaração</a></li>')
    toc.append('<li><a href="#como-usar">Como usar este guia</a></li>')
    toc.append('<li class="toc-parte">🙌 Orações de Fé</li>')
    toc.append('<li><a href="#oracoes-fe">Orações no Nome de Jesus (toque para abrir)</a></li>')
    toc_html = '\n'.join(toc)

    corpo = []

    # Abertura
    corpo.append('''<section class="capitulo" id="abertura">
      <p class="cap-num">Coleção do Despertar</p>
      <h2 class="cap-titulo">Sobre este guia</h2>
      <p>Este guia reúne versículos, mensagens de gratidão, afirmações e orações para você começar cada dia na presença de Deus. O poder da palavra é um tema central dos nossos livros: a Bíblia ensina que a morte e a vida estão no poder da língua (Provérbios 18:21).</p>
      <div class="box aviso"><h3>Atenção</h3><p>As afirmações devem ser usadas alinhadas à Palavra de Deus. O nome "EU SOU" é o nome sagrado de Deus (Êxodo 3:14). Quando declaramos, declaramos quem somos em Cristo, não uma autossuficiência vazia.</p></div>
      <nav class="cap-nav"><a href="#sumario">Sumário</a><a href="#gratidao">Próximo →</a></nav>
    </section>''')

    # Gratidão
    sec = ['<section class="capitulo" id="gratidao">']
    sec.append('<p class="cap-num">🙌 Gratidão</p>')
    sec.append('<h2 class="cap-titulo">Versículos e mensagens de gratidão</h2>')
    sec.append('<p>A gratidão é a porta que abre o coração para as bênçãos de Deus. Comece o dia agradecendo, e tudo ao seu redor se transforma.</p>')
    for msg in GRATIDAO:
        sec.append(f'<p class="afirmacao">🙏 {esc(msg)}</p>')
    sec.append('<nav class="cap-nav"><a href="#abertura">← Anterior</a><a href="#sumario">Sumário</a><a href="#cat-1">Próximo →</a></nav>')
    sec.append('</section>')
    corpo.append('\n'.join(sec))

    # Categorias
    for i, cat in enumerate(CATEGORIAS, 1):
        sec = [f'<section class="capitulo" id="cat-{i}">']
        sec.append(f'<p class="cap-num">{cat["icone"]} Categoria {i}</p>')
        sec.append(f'<h2 class="cap-titulo">{esc(cat["titulo"])}</h2>')
        sec.append('<div class="lista-afirmacoes">')
        for af in cat['afirmacoes']:
            sec.append(f'<p class="afirmacao">✨ {esc(af)}</p>')
        sec.append('</div>')
        nav = ['<nav class="cap-nav">']
        if i > 1:
            nav.append(f'<a href="#cat-{i-1}">← Anterior</a>')
        else:
            nav.append('<a href="#gratidao">← Anterior</a>')
        nav.append('<a href="#sumario">Sumário</a>')
        if i < len(CATEGORIAS):
            nav.append(f'<a href="#cat-{i+1}">Próximo →</a>')
        else:
            nav.append('<a href="#oracoes">Próximo →</a>')
        nav.append('</nav>')
        sec.append('\n'.join(nav))
        sec.append('</section>')
        corpo.append('\n'.join(sec))

    # Orações do dia
    sec = ['<section class="capitulo" id="oracoes">']
    sec.append('<p class="cap-num">🙏 Orações</p>')
    sec.append('<h2 class="cap-titulo">Orações para o dia a dia</h2>')
    for oracao in ORACOES:
        sec.append(f'<div class="box oracao"><p>{esc(oracao)}</p></div>')
    sec.append('<nav class="cap-nav"><a href="#cat-8">← Anterior</a><a href="#sumario">Sumário</a><a href="#oracoes-fe">Próximo →</a></nav>')
    sec.append('</section>')
    corpo.append('\n'.join(sec))



    # Versículos
    sec = ['<section class="capitulo" id="versiculos">']
    sec.append('<p class="cap-num">📖 Versículos</p>')
    sec.append('<h2 class="cap-titulo">Versículos de declaração</h2>')
    for texto, ref in VERSICULOS:
        sec.append(f'<div class="box versiculo"><p>"{esc(texto)}" <span class="ref">({esc(ref)})</span></p></div>')
    sec.append('<nav class="cap-nav"><a href="#oracoes">← Anterior</a><a href="#sumario">Sumário</a><a href="#como-usar">Próximo →</a></nav>')
    sec.append('</section>')
    corpo.append('\n'.join(sec))

    # Como usar
    sec = ['<section class="capitulo" id="como-usar">']
    sec.append('<p class="cap-num">📌 Guia de uso</p>')
    sec.append('<h2 class="cap-titulo">Como usar este guia</h2>')
    sec.append('<p><strong>Pela manhã:</strong> comece agradecendo (seção Gratidão) e escolha 1-2 afirmações para repetir com fé, em voz alta.</p>')
    sec.append('<p><strong>Ao longo do dia:</strong> quando um pensamento negativo vier, substitua por uma declaração da Palavra.</p>')
    sec.append('<p><strong>À noite:</strong> ore com uma das orações do guia, do dia ou das orações de fé.</p>')
    sec.append('<p><strong>Sempre alinhado à Palavra:</strong> as afirmações não são mantras vazios, são verdades de Deus aplicadas à vida.</p>')
    sec.append('<nav class="cap-nav"><a href="#versiculos">← Anterior</a><a href="#sumario">Sumário</a><a href="#oracoes-fe">Próximo →</a></nav>')
    sec.append('</section>')
    corpo.append('\n'.join(sec))

    # Orações de Fé (formato FAQ - por último)
    sec = ['<section class="capitulo" id="oracoes-fe">']
    sec.append('<p class="cap-num">🙏 Orações de Fé</p>')
    sec.append('<h2 class="cap-titulo">Orações no Nome de Jesus</h2>')
    sec.append('<p>Orações baseadas no Evangelho, professando o poder e a autoridade no nome que está acima de todo nome. Toque em cada oração para abrir e fechar.</p>')
    for oracao in ORACOES_DE_FE:
        sec.append(f'<div class="faq-item"><div class="faq-q" onclick="this.parentElement.classList.toggle(\'aberto\')"><span>{oracao["icone"]} {esc(oracao["titulo"])}</span><span class="seta">▼</span></div><div class="faq-a"><p>{esc(oracao["orao"])}</p></div></div>')
    sec.append('<nav class="cap-nav"><a href="#como-usar">← Anterior</a><a href="#sumario">Sumário</a><a href="#fim">Fim</a></nav>')
    sec.append('</section>')
    corpo.append('\n'.join(sec))

    corpo_html = '\n'.join(corpo)

    css = """
:root{
  --navy:#0e1a2e; --navy2:#16283f;
  --ouro:#c9a24b; --ouro-claro:#e3c877;
  --papel:#faf6ee; --tinta:#2b2620; --tinta2:#6b6255;
  --linha:#e4dccb; --cta:#b8860b;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--navy); color:var(--tinta);
  font-family:Georgia,'Times New Roman',Times,serif; line-height:1.75;
}
.wrap{max-width:46rem; margin:0 auto}
.topbar{background:var(--navy); border-bottom:3px solid var(--ouro); position:sticky; top:0; z-index:50}
.topbar .wrap{display:flex; align-items:center; justify-content:space-between; padding:.8rem 1.2rem; gap:10px}
.topbar .logo{color:#fff; font-size:1.05rem; text-decoration:none}
.topbar .logo span{color:var(--ouro)}
.topbar .ler{color:var(--ouro-claro); font-size:.78rem; letter-spacing:.2em; text-transform:uppercase}
.capa{min-height:60vh; display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:3rem 1.2rem; color:#fff;
  background:radial-gradient(900px 500px at 70% -10%, rgba(201,162,75,.2), transparent 60%), linear-gradient(170deg,var(--navy) 0%,#120b18 100%);}
.capa .selo{font-size:.78rem; letter-spacing:.4em; text-transform:uppercase; color:var(--ouro-claro); margin-bottom:1.6rem}
.capa h1{font-size:clamp(1.8rem,5vw,2.8rem); margin:0 0 .6rem; line-height:1.12}
.capa .sub{font-style:italic; color:#cfd6e2; font-size:1.1rem; margin-bottom:1.8rem; max-width:34rem}
.capa .autor{font-size:.9rem; letter-spacing:.3em; text-transform:uppercase; color:var(--ouro); margin-bottom:2.4rem}
.capa .inicio{display:inline-block; background:linear-gradient(180deg,#d4a83f,var(--cta)); color:#fff;
  font-weight:700; padding:14px 30px; border-radius:8px; text-decoration:none; font-size:1rem}
.capa .aviso2{font-size:.78rem; color:#8fa0b8; margin-top:1.4rem; max-width:26rem; line-height:1.5}
#sumario{background:var(--navy2); color:#fff; padding:3rem 1.2rem}
#sumario h2{text-align:center; color:var(--ouro); font-size:1.4rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1.4rem}
#sumario ul{list-style:none; padding:0; margin:0 auto; max-width:34rem}
#sumario li{border-bottom:1px solid rgba(201,162,75,.25)}
#sumario li.toc-parte{color:var(--ouro); font-weight:700; padding:.9rem .4rem .4rem; letter-spacing:.08em; text-transform:uppercase; font-size:.85rem}
#sumario a{display:block; color:#e8ecf3; text-decoration:none; padding:.8rem .4rem; font-size:1rem}
#sumario a:hover{color:var(--ouro-claro); padding-left:.8rem}
.leitura{background:var(--papel); padding:2.6rem 1.2rem 4rem}
.leitura .wrap{background:#fff; border:1px solid var(--linha); border-radius:12px;
  padding:2.2rem 1.6rem; box-shadow:0 10px 30px rgba(0,0,0,.08)}
.capitulo{margin-top:3rem; padding-top:2rem; border-top:1px solid var(--linha)}
.cap-num{letter-spacing:.3em; text-transform:uppercase; font-size:.78rem; color:var(--ouro); margin:0 0 .5rem}
.cap-titulo{font-size:1.5rem; color:var(--navy); margin:0 0 1.2rem}
.capitulo p{margin:0 0 1rem; text-align:justify}
.afirmacao{background:#fdf6e3; border-left:4px solid var(--ouro); border-radius:8px;
  padding:.8rem 1rem; margin:.6rem 0; text-align:left; font-size:1.02rem;}
.box{border-radius:10px; padding:1rem 1.2rem; margin:1.2rem 0}
.box h3{margin:0 0 .4rem; font-size:1rem; letter-spacing:.05em}
.box p{margin:0; text-align:justify}
.box.aviso{background:#fdecea; border-left:4px solid #c0392b}
.box.aviso h3{color:#a93226}
.box.oracao{background:#e8eef7; border-left:4px solid #4a6fa5}
.box.oracao h3{color:#33507a}
.box.versiculo{background:#fdf6e3; border-left:4px solid var(--ouro)}
.box.versiculo h3{color:var(--cta)}
.ref{color:var(--cta); font-style:italic; font-size:.9rem}
.cap-nav{display:flex; justify-content:space-between; gap:.6rem; flex-wrap:wrap; margin-top:2.4rem;
  padding-top:1rem; border-top:1px dashed var(--linha); font-size:.9rem; font-family:system-ui,sans-serif}
.cap-nav a{color:var(--navy2); text-decoration:none; border-bottom:1px dotted var(--ouro); padding:2px 4px}
.cap-nav a:hover{color:var(--cta)}
#fim{background:var(--navy); color:#fff; text-align:center; padding:4rem 1.2rem}
#fim h2{font-size:1.5rem; margin-bottom:.8rem}
#fim p{color:#c4cdda; max-width:32rem; margin:0 auto 1.6rem}
#fim .cred{font-size:.82rem; color:#8fa0b8; margin-top:1.6rem; line-height:1.6}
footer{background:#0a1322; color:#7f8ca1; text-align:center; padding:1.6rem 1.2rem; font-size:.8rem}
@media (max-width:560px){
  body{font-size:17px}
  .leitura .wrap{padding:1.4rem 1rem}
  .cap-titulo{font-size:1.3rem}
}
  /* FAQ (accordion) das Orações de Fé */
  .faq-item{background:#faf6ee;border:1px solid #e4dccb;border-radius:10px;margin-bottom:10px;overflow:hidden;}
  .faq-q{display:flex;justify-content:space-between;align-items:center;padding:14px 18px;cursor:pointer;font-weight:700;color:#0e1a2e;font-size:1rem;background:#fdf6e3;}
  .faq-q .seta{transition:transform .2s;color:#b8860b;font-size:1.1rem;}
  .faq-item.aberto .faq-q .seta{transform:rotate(180deg);}
  .faq-a{display:none;padding:14px 18px;color:#2b2620;font-size:.95rem;line-height:1.7;background:#fff;}
  .faq-item.aberto .faq-a{display:block;}
"""

    html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(TITULO)} — {esc(SUBTITULO)}</title>
<meta name="description" content="{esc(TITULO)}. Versículos, gratidão, afirmações e orações para começar o dia na presença de Deus.">
<style>{css}</style>
</head>
<body>

<header class="topbar">
  <div class="wrap">
    <a class="logo" href="#">Missão <span>com Deus</span></a>
    <span class="ler">Comece o dia</span>
  </div>
</header>

<section class="capa">
  <p class="selo">Coleção do Despertar</p>
  <h1>{esc(TITULO)}</h1>
  <p class="sub">{esc(SUBTITULO)}</p>
  <p class="autor">Compilado das obras do Portal · Versão de leitura</p>
  <a class="inicio" href="#sumario">Começar a leitura →</a>
  <p class="aviso2">✨ Versículos, gratidão, afirmações e orações para fortalecer a fé.</p>
</section>

<section id="sumario">
  <h2>Sumário</h2>
  <ul>
{toc_html}
  </ul>
</section>

<main class="leitura">
  <div class="wrap">
{corpo_html}
  </div>
</main>

<section id="fim">
  <h2>O Poder da Palavra</h2>
  <p>"A morte e a vida estão no poder da língua." (Provérbios 18:21)</p>
  <p>Que as suas palavras sejam sempre sementes de fé, amor e esperança, na natureza de Deus.</p>
  <p class="cred">© Coleção do Despertar · Missão com Deus · CompraOSeu<br>
  Versão de leitura — para uso pessoal e avaliação.</p>
</section>

<footer>
  <p>Missão com Deus · CompraOSeu — Desperte sua mente, fortaleça sua fé, transforme sua vida.</p>
</footer>

</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html_doc, encoding='utf-8')
    print("Gerado:", OUT, f"({OUT.stat().st_size:,} bytes)")
    print(f"Categorias: {len(CATEGORIAS)} | Orações do dia: {len(ORACOES)} | Orações de fé: {len(ORACOES_DE_FE)} | Versículos: {len(VERSICULOS)}")

if __name__ == '__main__':
    build()
