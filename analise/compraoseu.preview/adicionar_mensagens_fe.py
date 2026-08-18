#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona a seção "Mensagens de Fé para o Dia a Dia" ao livro de Afirmações:

  - Item no sumário (toc-parte "💬 Mensagens de Fé")
  - Nova seção <section class="capitulo" id="mensagens-dia"> em formato FAQ
    (toque para abrir e fechar), posicionada ANTES das Orações de Fé
    (mantendo a decisão de as orações ficarem por último).

Todas as mensagens são originais, humanizadas (sem travessões, sem
reticências, sem asteriscos) e usam versículos que NÃO repetem os que já
estão na página (verificado).

Uso: python3 adicionar_mensagens_fé.py
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]
ORIG = RAIZ / "paginas" / "livro12_preview.html"

# (emoji, situação, mensagem, versículo texto, referência)
MENSAGENS = [
    ("🌅", "Para começar o dia com fé",
     "Antes de olhar para o celular, olhe para o céu. Este dia é uma dádiva, e você não precisa carregá-lo sozinho. Comece com gratidão e deixe que a alegria do Senhor seja a sua força.",
     "Este é o dia que fez o Senhor; regozijemo-nos e alegremo-nos nele.", "Salmo 118:24"),
    ("💼", "Para o trabalho e as tarefas",
     "Trabalhe com o coração, não apenas com as mãos. O que você faz hoje, mesmo o mais simples, pode ser feito como uma oferta de amor. Não é sobre o resultado, é sobre a fidelidade.",
     "E tudo quanto fizerdes, fazei-o de todo o coração, como ao Senhor, e não aos homens.", "Colossenses 3:23"),
    ("😰", "Para a ansiedade",
     "Respire fundo e lembre: você não precisa saber o dia de amanhã, precisa confiar em quem o conhece. Entregue a preocupação em oração e deixe a paz agir dentro de você.",
     "Não estejais ansiosos por coisa alguma; antes, em tudo, sejam conhecidas as vossas petições diante de Deus; e a paz de Deus guardará os vossos corações.", "Filipenses 4:6-7"),
    ("💧", "Para a tristeza",
     "Chorar não é fraqueza, é humanidade. Deus não se afasta de quem chora; Ele se aproxima. Entregue a dor a Ele e permita que o conforto chegue no tempo certo.",
     "Perto está o Senhor dos que têm o coração quebrantado e salva os contritos de espírito.", "Salmo 34:18"),
    ("🛡️", "Para o medo",
     "O medo sussurra, mas a fé fala mais alto. Você não precisa ser forte o tempo todo, precisa estar seguro nos braços de quem nunca falha.",
     "Não temas, porque eu sou contigo; não te assombres, porque eu sou o teu Deus.", "Isaías 41:10"),
    ("🏡", "Para a família",
     "O lar se constrói com presença, paciência e perdão. Escolha hoje abençoar os seus com palavras boas e com o exemplo do seu amor.",
     "Eu e a minha casa serviremos ao Senhor.", "Josué 24:15"),
    ("🌙", "Para a noite",
     "Antes de dormir, faça as pazes com o dia. O que não foi feito espera por amanhã, e o que foi dito demais, entregue ao perdão. Descanse em paz.",
     "Em paz também me deitarei e dormirei, porque só tu, Senhor, me fazes habitar em segurança.", "Salmo 4:8"),
    ("🌱", "Para recomeçar",
     "Nenhum erro de ontem define o amanhã. A misericórdia de Deus se renova a cada manhã, e com ela, a sua chance de começar de novo.",
     "As misericórdias do Senhor são a causa de não sermos consumidos; renovam-se cada manhã.", "Lamentações 3:22-23"),
    ("🕊️", "Para o cansaço",
     "Se você está cansado, não precisa fingir que está bem. Descanse em Deus, entregue o peso e receba o alívio que só Ele dá.",
     "Vinde a mim, todos os que estais cansados e oprimidos, e eu vos aliviarei.", "Mateus 11:28"),
    ("🙌", "Para quando nada parece mudar",
     "Há um tempo para semear e um tempo para colher. Não desista no meio do caminho: o que você planta com fé, Deus rega com cuidado.",
     "E não nos cansemos de fazer o bem, porque a seu tempo ceifaremos, se não houvermos desfalecido.", "Gálatas 6:9"),
    ("💌", "Para confiar em Deus",
     "O seu coração pode não entender o caminho, mas pode confiar em quem o guia. Reconheça o Senhor em cada passo e Ele endireitará as suas veredas.",
     "Confia no Senhor de todo o teu coração e não te estribes no teu próprio entendimento.", "Provérbios 3:5-6"),
    ("🕊️", "Para entregar as preocupações",
     "Jogue sobre Deus tudo o que pesa: o medo, a dúvida, a mágoa. Ele cuida de você com um cuidado que não falha.",
     "Lançando sobre ele toda a vossa ansiedade, porque ele tem cuidado de vós.", "1 Pedro 5:7"),
]

SECAO = []
SECAO.append('<section class="capitulo" id="mensagens-dia">')
SECAO.append('<p class="cap-num">💬 Mensagens de Fé</p>')
SECAO.append('<h2 class="cap-titulo">Mensagens para o Dia a Dia</h2>')
SECAO.append('<p>Pequenas mensagens de ânimo para as situações do dia a dia, com versículos que tocam a alma. Toque em cada uma para abrir e fechar.</p>')
for emoji, titulo, mensagem, versiculo, ref in MENSAGENS:
    SECAO.append('<div class="faq-item"><div class="faq-q" onclick="this.parentElement.classList.toggle(\'aberto\')"><span>' +
                 emoji + ' ' + titulo + '</span><span class="seta">▼</span></div><div class="faq-a">' +
                 '<p>' + mensagem + '</p>' +
                 '<p class="ref">"' + versiculo + '" (' + ref + ')</p>' +
                 '</div></div>')
SECAO.append('<nav class="cap-nav"><a href="#como-usar">← Anterior</a><a href="#sumario">Sumário</a><a href="#oracoes-fe">Próximo →</a></nav>')
SECAO.append('</section>')
BLOCO = "\n".join(SECAO)


def main():
    html = ORIG.read_text(encoding="utf-8")

    # 1. Sumário: adicionar antes do bloco das Orações de Fé
    alvo_sumario = '<li class="toc-parte">🙌 Orações de Fé</li>'
    item_sumario = ('<li class="toc-parte">💬 Mensagens de Fé</li>\n'
                    '<li><a href="#mensagens-dia">Mensagens para o dia a dia (toque para abrir)</a></li>\n')
    assert alvo_sumario in html, "alvo do sumário não encontrado"
    if 'id="mensagens-dia"' not in html:
        html = html.replace(alvo_sumario, item_sumario + alvo_sumario, 1)

        # 2. Seção: antes de <section class="capitulo" id="oracoes-fe">
        alvo_secao = '<section class="capitulo" id="oracoes-fe">'
        assert alvo_secao in html, "seção oracoes-fe não encontrada"
        html = html.replace(alvo_secao, BLOCO + "\n" + alvo_secao, 1)

        ORIG.write_text(html, encoding="utf-8")
        print("Seção adicionada em:", ORIG.name, f"({len(MENSAGENS)} mensagens)")
    else:
        print("Já existe; nada a fazer.")


if __name__ == "__main__":
    main()
    print("Concluído.")
