#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ajustes do Livro 12 (Afirmações) pedidos pelo autor em 18/08:
1. "Como usar este guia" sobe por inteiro para a página "Sobre este guia"
   (abaixo do box Atenção).
2. "Mensagens para o Dia a Dia" e "Orações no Nome de Jesus" sobem para
   logo depois de "Sobre este guia".
3. A videoaula (aula grátis) permanece no fim.
4. Paz e Emoções: última mensagem longa encurtada (só o início, padrão de
   lembrar a passagem).
5. Proteção e Segurança: removidas as duas partes longas do Salmo 23.
6. Relacionamentos e Perdão: mensagens do Salmo 51 e de Mateus 5:44
   encurtadas (só até onde o autor pediu).
"""
import re, sys

ARQUIVOS = [
    "site-contabo/livro12.html",
    "paginas/livro12_leitor_preview.html",
]

def extrai_secao(html, sec_id):
    """Extrai a section .capitulo com o id dado (do <section até </section>\n)."""
    marca = '<section class="capitulo" id="%s">' % sec_id
    ini = html.index(marca)
    fim = html.index("</section>", ini) + len("</section>")
    # inclui a quebra de linha seguinte, se houver
    if fim < len(html) and html[fim] == "\n":
        fim += 1
    return html[ini:fim], ini, fim

def processa(caminho):
    with open(caminho, encoding="utf-8") as f:
        html = f.read()

    # ---------- 4. Paz e Emoções: encurtar a mensagem longa ----------
    longa_paz = ('<p class="afirmacao">✨ Não andeis ansiosos pelo dia de amanhã, '
                 'nem pela vossa vida, pelo que haveis de comer ou beber, nem pelo corpo, '
                 'pelo que haveis de vestir. Olhai para as aves do céu, que não semeiam nem colhem, '
                 'e o Pai celestial as alimenta. Buscai primeiro o Reino de Deus, e todas estas '
                 'coisas vos serão acrescentadas. (Mateus 6:25-34)</p>')
    curta_paz = ('<p class="afirmacao">✨ Não andeis ansiosos pelo dia de amanhã, '
                 'nem pela vossa vida. (Mateus 6:25-34)</p>')
    assert longa_paz in html, "mensagem longa de Paz e Emoções não encontrada"
    html = html.replace(longa_paz, curta_paz)

    # ---------- 5. Proteção: remover as duas partes longas do Salmo 23 ----------
    salmo23_a = ('<p class="afirmacao">✨ O Senhor é o meu pastor, nada me faltará. '
                 'Deitar-me faz em verdes pastos, guia-me mansamente a águas tranquilas. '
                 'Refrigera a minha alma, guia-me pelas veredas da justiça por amor do seu nome. '
                 'Ainda que eu andasse pelo vale da sombra da morte, não temeria mal algum, '
                 'porque tu estás comigo; a tua vara e o teu cajado me consolam. (Salmo 23)</p>\n')
    salmo23_b = ('<p class="afirmacao">✨ Preparas uma mesa perante mim na presença dos meus '
                 'inimigos, unges a minha cabeça com óleo, o meu cálice transborda. Certamente '
                 'que a bondade e a misericórdia me seguirão todos os dias da minha vida, e '
                 'habitarei na casa do Senhor por longos dias. (Salmo 23:5-6)</p>\n')
    assert salmo23_a in html, "Salmo 23 parte 1 não encontrado"
    assert salmo23_b in html, "Salmo 23 parte 2 não encontrado"
    html = html.replace(salmo23_a, "").replace(salmo23_b, "")

    # ---------- 6. Relacionamentos e Perdão: encurtar duas mensagens ----------
    longa_cria = ('<p class="afirmacao">✨ Cria em mim, ó Deus, um coração puro e renova em mim '
                  'um espírito estável. Não me lances fora da tua presença e não retires de mim o '
                  'teu Santo Espírito. Restitui-me a alegria da tua salvação e sustenta-me com um '
                  'espírito voluntário. (Salmo 51:10-12)</p>')
    curta_cria = ('<p class="afirmacao">✨ Cria em mim, ó Deus, um coração puro e renova em mim '
                  'um espírito estável. Não me lances fora da tua presença. (Salmo 51:10-11)</p>')
    assert longa_cria in html, "Salmo 51 não encontrado"
    html = html.replace(longa_cria, curta_cria)

    longa_amai = ('<p class="afirmacao">✨ Jesus disse: Amai os vossos inimigos, bendizei os que '
                  'vos maldizem, fazei bem aos que vos odeiam e orai pelos que vos maltratam e vos '
                  'perseguem, para que sejais filhos do vosso Pai que está nos céus. '
                  '(Mateus 5:44-45)</p>')
    curta_amai = ('<p class="afirmacao">✨ Jesus disse: Amai os vossos inimigos, bendizei os que '
                  'vos maldizem, fazei bem aos que vos odeiam. (Mateus 5:44)</p>')
    assert longa_amai in html, "Mateus 5:44 não encontrado"
    html = html.replace(longa_amai, curta_amai)

    # ---------- 1. "Como usar este guia" sobe para "Sobre este guia" ----------
    sec_como, ini, fim = extrai_secao(html, "como-usar")
    html = html[:ini] + html[fim:]  # remove a seção do lugar antigo

    # conteúdo interno (os 4 parágrafos)
    paragrafos = re.findall(r'<p><strong>.*?</p>', sec_como, flags=re.S)
    assert len(paragrafos) == 4, "esperava 4 parágrafos em Como usar"
    bloco_como = ('\n      <span id="como-usar"></span>\n'
                  '      <h3 style="color:var(--ouro);font-family:inherit;margin:1.8rem 0 .8rem;">'
                  '📌 Como usar este guia</h3>\n'
                  + "\n".join("      " + p for p in paragrafos) + "\n")

    alvo_aviso = ('<div class="box aviso"><h3>Atenção</h3><p>As afirmações devem ser usadas '
                  'alinhadas à Palavra de Deus. O nome "EU SOU" é o nome sagrado de Deus '
                  '(Êxodo 3:14). Quando declaramos, declaramos quem somos em Cristo, não uma '
                  'autossuficiência vazia.</p></div>')
    assert alvo_aviso in html, "box Atenção não encontrado"
    html = html.replace(alvo_aviso, alvo_aviso + bloco_como)

    # ---------- 2. Mensagens do Dia a Dia e Orações no Nome de Jesus sobem ----------
    sec_msg, ini, fim = extrai_secao(html, "mensagens-dia")
    html = html[:ini] + html[fim:]
    sec_ora, ini, fim = extrai_secao(html, "oracoes-fe")
    html = html[:ini] + html[fim:]

    # inserir logo após a seção "abertura" (Sobre este guia)
    _, _, fim_abertura = extrai_secao(html, "abertura")
    html = html[:fim_abertura] + sec_msg + sec_ora + html[fim_abertura:]

    # ---------- 3. Corrigir as navegações (Anterior/Próximo) ----------
    trocas_nav = [
        # abertura -> próximo agora é mensagens-dia
        ('<nav class="cap-nav"><a href="#sumario">Sumário</a><a href="#gratidao">Próximo →</a></nav>',
         '<nav class="cap-nav"><a href="#sumario">Sumário</a><a href="#mensagens-dia">Próximo →</a></nav>'),
        # mensagens-dia: anterior = abertura
        ('<nav class="cap-nav"><a href="#como-usar">← Anterior</a><a href="#sumario">Sumário</a><a href="#oracoes-fe">Próximo →</a></nav>',
         '<nav class="cap-nav"><a href="#abertura">← Anterior</a><a href="#sumario">Sumário</a><a href="#oracoes-fe">Próximo →</a></nav>'),
        # oracoes-fe: anterior = mensagens-dia, próximo = gratidao
        ('<nav class="cap-nav"><a href="#como-usar">← Anterior</a><a href="#sumario">Sumário</a><a href="#fim">Fim</a></nav>',
         '<nav class="cap-nav"><a href="#mensagens-dia">← Anterior</a><a href="#sumario">Sumário</a><a href="#gratidao">Próximo →</a></nav>'),
        # gratidao: anterior = oracoes-fe
        ('<nav class="cap-nav"><a href="#abertura">← Anterior</a><a href="#sumario">Sumário</a><a href="#cat-1">Próximo →</a></nav>',
         '<nav class="cap-nav"><a href="#oracoes-fe">← Anterior</a><a href="#sumario">Sumário</a><a href="#cat-1">Próximo →</a></nav>'),
        # oracoes (dia a dia): próximo = versiculos
        ('<nav class="cap-nav"><a href="#cat-8">← Anterior</a><a href="#sumario">Sumário</a><a href="#oracoes-fe">Próximo →</a></nav>',
         '<nav class="cap-nav"><a href="#cat-8">← Anterior</a><a href="#sumario">Sumário</a><a href="#versiculos">Próximo →</a></nav>'),
        # versiculos: agora é a última página de leitura -> Fim
        ('<nav class="cap-nav"><a href="#oracoes">← Anterior</a><a href="#sumario">Sumário</a><a href="#como-usar">Próximo →</a></nav>',
         '<nav class="cap-nav"><a href="#oracoes">← Anterior</a><a href="#sumario">Sumário</a><a href="#fim">Fim</a></nav>'),
    ]
    for velho, novo in trocas_nav:
        assert velho in html, "nav não encontrada: " + velho[:60]
        html = html.replace(velho, novo)

    # ---------- Sumário: nova ordem + remoção de "Como usar" ----------
    itens = {}
    for li_id, chave in [
        ("li-gratidao", "gratidao"), ("li-mensagens-dia", "mensagens-dia"),
        ("li-oracoes-fe", "oracoes-fe"), ("li-oracoes", "oracoes"),
        ("li-versiculos", "versiculos"), ("li-como-usar", "como-usar"),
    ]:
        m = re.search(r'<li id="%s">.*?</li>\n?' % li_id, html)
        assert m, "item do sumário não encontrado: " + li_id
        itens[li_id] = m.group(0)

    # remove "Como usar" do sumário (agora faz parte de Sobre este guia)
    html = html.replace(itens["li-como-usar"], "")

    # remove as partes/itens que serão reordenados
    parte_msg = '<li class="toc-parte">💬 Mensagens de Fé</li>\n'
    parte_ora = '<li class="toc-parte">🙌 Orações de Fé</li>\n'
    assert parte_msg in html and parte_ora in html
    html = html.replace(parte_msg + itens["li-mensagens-dia"], "")
    html = html.replace(parte_ora + itens["li-oracoes-fe"], "")

    # insere Mensagens + Orações de Fé no TOPO do sumário (antes de Gratidão)
    parte_grat = '<li class="toc-parte">🙌 Gratidão</li>'
    assert parte_grat in html
    html = html.replace(
        parte_grat,
        parte_msg + itens["li-mensagens-dia"] + parte_ora + itens["li-oracoes-fe"] + parte_grat,
        1,
    )

    # ---------- NOMES do leitor: remover "como-usar" ----------
    html = html.replace('    "como-usar": "Como usar",\n', '')
    html = html.replace('"como-usar": "Como usar",', '')

    with open(caminho, "w", encoding="utf-8") as f:
        f.write(html)
    print("OK:", caminho)

if __name__ == "__main__":
    for arq in ARQUIVOS:
        processa(arq)
    print("Concluído.")
