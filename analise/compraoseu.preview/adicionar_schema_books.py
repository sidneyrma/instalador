# -*- coding: utf-8 -*-
"""
Adiciona Schema.org Book (JSON-LD) em cada página de livro (livro01-10)
para o Google exibir rich snippets (capa, título, descrição) nos resultados.

Insere o JSON-LD logo após a tag </title> de cada página.
"""
import json
import re
from pathlib import Path

PAGINAS = Path('/home/user/instalador/paginas')

LIVROS = {
    'livro01': {
        'titulo': 'O Verbo que Transforma',
        'subtitulo': 'O Poder Criador da Palavra e da Fé',
        'desc': 'Uma obra original sobre o poder criador da palavra e da fé, para a saúde, a abundância e a superação.',
        'capa': 'https://i.ibb.co/b52wmSGm/livro01jpg.jpg',
        'num': 1,
    },
    'livro02': {
        'titulo': 'A Sabedoria dos Mestres',
        'subtitulo': 'O Despertar do Conhecimento que Liberta a Alma',
        'desc': 'Uma obra original sobre as leis da vibração, a linguagem do universo e o mestre interior.',
        'capa': 'https://i.ibb.co/W42S6bX0/livro02jpg.jpg',
        'num': 2,
    },
    'livro03': {
        'titulo': 'A Mente Renovada',
        'subtitulo': 'O Pensar com Cristo que Transforma a Vida',
        'desc': 'Uma obra original sobre a renovação da mente, o governo do pensamento, a oração e a gratidão.',
        'capa': 'https://i.ibb.co/20jLgxZN/livro03jpg.jpg',
        'num': 3,
    },
    'livro04': {
        'titulo': 'Um Segundo com Deus',
        'subtitulo': 'Devocional Vol. 01',
        'desc': 'Devocional de 30 dias com reflexões, orações e versículos para renovar a fé e encontrar paz.',
        'capa': 'https://i.ibb.co/LdbL0QdH/livro04jpg.jpg',
        'num': 4,
    },
    'livro05': {
        'titulo': 'Evolução da Alma',
        'subtitulo': 'Caminhos para o Autoconhecimento, Fé e Transformação Pessoal',
        'desc': 'Caminhos para o autoconhecimento, a fé e a transformação pessoal, com preces e ensinamentos bíblicos.',
        'capa': 'https://i.ibb.co/kgBz01dc/livro05jpg.jpg',
        'num': 5,
    },
    'livro06': {
        'titulo': 'Jesus Quer Falar com Seu Filho',
        'subtitulo': 'Livro Infantil Cristão',
        'desc': 'Uma obra infantil cristã que ensina os Mandamentos, valores bíblicos e o amor de Jesus às crianças.',
        'capa': 'https://i.ibb.co/G3n3wTXD/livro06jpg.jpg',
        'num': 6,
    },
    'livro07': {
        'titulo': 'O Caminho do Despertar',
        'subtitulo': 'A Jornada Solitária da Alma',
        'desc': 'A Jornada Solitária da Alma, uma obra que reúne a sabedoria dos ensinamentos ocultos, a profundidade da fé e o conhecimento da alma humana.',
        'capa': 'https://i.ibb.co/SDML88Rq/livro07jpg.jpg',
        'num': 7,
    },
    'livro08': {
        'titulo': 'O Arquiteto da Realidade',
        'subtitulo': 'O Poder da Mente que Cria o Mundo que Você Vive',
        'desc': 'Uma obra original sobre crenças, mente profunda e o estado do criador.',
        'capa': 'https://i.ibb.co/mV3S1m78/livro08jpg.jpg',
        'num': 8,
    },
    'livro09': {
        'titulo': 'Anestesia Mental',
        'subtitulo': 'e seus Algoritmos da Escravidão',
        'desc': 'As correntes invisíveis que controlam sua mente e como se libertar em Cristo.',
        'capa': 'https://i.ibb.co/6JrkxbJC/livro09jpg.jpg',
        'num': 9,
    },
    'livro10': {
        'titulo': 'O Despertar do Observador',
        'subtitulo': 'As Leis Invisíveis que Moldam a Realidade',
        'desc': 'Uma obra original que une sabedoria ancestral, o poder do pensamento e práticas para o despertar da consciência.',
        'capa': 'https://i.ibb.co/mV3RKS17/livro10jpg.jpg',
        'num': 10,
    },
}


def jsonld(livro):
    url = f'https://www.compraoseu.com/{livro}'
    titulo_completo = f"{livro['titulo']} — {livro['subtitulo']}"
    data = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": titulo_completo,
        "alternateName": livro['titulo'],
        "url": url,
        "image": livro['capa'],
        "description": livro['desc'],
        "inLanguage": "pt-BR",
        "author": {
            "@type": "Organization",
            "name": "Missão com Deus — Coleção do Despertar",
            "url": "https://compraoseu.com"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Missão com Deus — CompraOSeu"
        },
        "isAccessibleForFree": True,
        "bookFormat": "https://schema.org/EBook",
        "numberOfPages": None,
        "offers": {
            "@type": "Offer",
            "url": url,
            "availability": "https://schema.org/InStock",
            "price": "0",
            "priceCurrency": "BRL"
        },
        "genre": "Espiritualidade Cristã",
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    for slug, livro in LIVROS.items():
        arquivo = PAGINAS / f'{slug}_preview.html'
        if not arquivo.exists():
            print(f'⚠ não encontrado: {arquivo}')
            continue
        html = arquivo.read_text(encoding='utf-8')
        if 'application/ld+json' in html:
            print(f'⏭ {slug} já tem JSON-LD')
            continue
        bloco = f'<script type="application/ld+json">\n{jsonld(livro)}\n</script>'
        # insere após a tag </title>
        html = re.sub(r'(</title>)', r'\1\n' + bloco, html, count=1)
        arquivo.write_text(html, encoding='utf-8')
        print(f'✔ {slug}: JSON-LD adicionado')


if __name__ == '__main__':
    main()
