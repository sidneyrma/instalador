# -*- coding: utf-8 -*-
"""
APLICAR_LIMPEZA_LIVROS.py — Missao com Deus
==========================================
Tira da casa os livros que NAO sao de autoria da casa (risco de direito autoral).

O que este script faz, nesta ordem:

  1. FAZ BACKUP de tudo antes de mexer (index.html, sitemap.xml, sw.js, e os
     proprios livros), tudo dentro de /home/deploy/_limpeza-<data>/, com um
     LEIA-ME.txt ensinando a desfazer.
  2. Remove os CARDS da biblioteca na Home (index.html).
  3. Renumera os cards que ficam (01, 02, 03...) sem deixar buraco.
  4. Remove os enderecos do sitemap.xml (senao o Google continua achando).
  5. Remove os enderecos do sw.js e sobe a versao do cache (v3 -> v4).
     ISSO E IMPORTANTE: sem isso, quem ja instalou o site como app no celular
     continua abrindo os livros pelo cache, mesmo depois de apagados.
  6. Move os arquivos HTML para fora da pasta publica (passam a dar 404).
  7. Verifica se a Home continua inteira (enquete, quiz, banner, player,
     FormSubmit). Se qualquer um sumir, ele RESTAURA o backup e avisa.

O que ele NAO faz: nao mexe em mais nada da Home, nao toca no player da
Palavra, na apaga a enquete, o quiz, o banner nem o formulario.

Como usar (aaPanel Terminal):
  python3 /home/deploy/APLICAR_LIMPEZA_LIVROS.py

Para simular antes sem mexer em nada (so mostra o que faria):
  python3 /home/deploy/APLICAR_LIMPEZA_LIVROS.py --simular
"""
import os
import re
import sys
import shutil
from datetime import datetime

SITE = os.environ.get('SITE_DIR', '/www/wwwroot/missaocomdeus.com.br')
DESTINO_BACKUP = os.environ.get('BACKUP_DIR', '/home/deploy')
SIMULAR = '--simular' in sys.argv

# ------------------------------------------------------------------ CONFIG
# Livros que SAEM da casa (arquivo -> nome)
REMOVER = [
    ('/livro01', 'O Verbo que Transforma'),
    ('/livro02', 'A Sabedoria dos Mestres'),
    ('/livro03', 'A Mente Renovada'),
    ('/livro08', 'O Arquiteto da Realidade'),
    ('/livro10', 'O Despertar do Observador'),
]

# Livros que FICAM (so para o relatorio; a ordem e a que aparece na Home)
FICAM = [
    ('/livro11', 'O Novo Testamento como nunca lido'),
    ('/livro05', 'Evolução da Alma'),
    ('/livro09', 'Anestesia Mental'),
    ('/livro04', 'Um Segundo com Deus'),
    ('/livro06', 'Jesus Quer Falar com Seu Filho'),
    ('/livro07', 'O Caminho do Despertar'),
    ('/livro12', 'Comece o dia com Afirmações, Declarações e Orações'),
]

# Se preferir manter os numeros antigos dos cards, troque para False.
RENUMERAR = True

# Se algum destes sumir da Home depois da limpeza, o script desfaz tudo.
TRAVAS = ['enquete', 'quiz', 'cta-cursos', 'biblioteca', 'FormSubmit']

RE_CARD = re.compile(r'<!-- LIVRO (\d{2}) -->')
RE_BIB_NUM = re.compile(r'(<span class="bib-num">\s*Livro )(\d{2})( ·)')


def ok(msg):
    print('  OK   ' + msg)


def aviso(msg):
    print('  --   ' + msg)


def erro(msg):
    print('  ERRO ' + msg)


def main():
    print('=' * 66)
    print('LIMPEZA DA BIBLIOTECA — Missao com Deus')
    print('=' * 66)
    if SIMULAR:
        print('MODO SIMULACAO: nada sera alterado.\n')

    if not os.path.isdir(SITE):
        erro('Pasta do site nao encontrada: ' + SITE)
        print('Se o site estiver em outro lugar:')
        print('  SITE_DIR=/caminho python3 APLICAR_LIMPEZA_LIVROS.py')
        return

    caminhos_remover = [p for p, _ in REMOVER]
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    backup = os.path.join(DESTINO_BACKUP, '_limpeza-' + stamp)

    # ---------------------------------------------------------- 1) BACKUP
    print('\n[1/6] Preparando backup em %s' % backup)
    if not SIMULAR:
        os.makedirs(backup, exist_ok=True)
    for nome in ['index.html', 'sitemap.xml', 'sw.js']:
        origem = os.path.join(SITE, nome)
        if os.path.isfile(origem):
            if not SIMULAR:
                shutil.copy2(origem, os.path.join(backup, nome + '.bak'))
            ok('backup de %s' % nome)
        else:
            aviso('%s nao existe (segue sem ele)' % nome)

    # ------------------------------------------------------ 2) INDEX.HTML
    print('\n[2/6] Removendo os cards da Home')
    idx = os.path.join(SITE, 'index.html')
    if not os.path.isfile(idx):
        erro('index.html nao encontrado. Nada foi feito.')
        return
    with open(idx, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()

    partes = RE_CARD.split(original)
    if len(partes) < 4:
        erro('Nao achei os marcadores "<!-- LIVRO NN -->" na Home.')
        erro('Nada foi alterado. Me chame para ajustar o script na mao.')
        return

    # partes = [texto_antes, num1, corpo1, num2, corpo2, ...]
    cabeca = partes[0]
    blocos = []
    for i in range(1, len(partes) - 1, 2):
        blocos.append([partes[i], partes[i + 1]])       # [numero, conteudo]

    total_antes = len(blocos)
    mantidos = []
    for num, corpo in blocos:
        alvo = None
        for p in caminhos_remover:
            if 'href="%s"' % p in corpo:
                alvo = p
                break
        if alvo:
            nome = dict(REMOVER).get(alvo, alvo)
            aviso('removendo card %s (%s) -> %s' % (num, alvo, nome))
        else:
            mantidos.append([num, corpo])

    if len(mantidos) == total_antes:
        aviso('Nenhum card removido (ja foram removidos antes?).')

    novo = cabeca
    for i, (num, corpo) in enumerate(mantidos, 1):
        marcador = '<!-- LIVRO %02d -->' % (i if RENUMERAR else int(num))
        corpo_novo = corpo
        if RENUMERAR:
            corpo_novo = RE_BIB_NUM.sub(
                lambda m: m.group(1) + '%02d' % i + m.group(3), corpo_novo, count=1)
        novo += marcador + corpo_novo
        titulo = re.search(r'<h3>(.*?)</h3>', corpo, re.S)
        titulo = titulo.group(1).strip()[:38] if titulo else '?'
        ok('card %02d -> %s' % (i if RENUMERAR else int(num), titulo))

    # ------------------------------------------------------------- TRAVAS
    print('\n[3/6] Conferindo se a Home continua inteira')
    seguro = True
    for t in TRAVAS:
        if t not in novo:
            erro('sumiu da Home: %s' % t)
            seguro = False
        else:
            ok('%s continua no lugar' % t)
    if not seguro:
        erro('A limpeza foi CANCELADA. Nada foi gravado.')
        erro('O backup anterior esta em: %s' % backup)
        return

    if len(novo) > len(original) * 0.75:
        ok('tamanho da Home: %d -> %d bytes (queda normal)' % (len(original), len(novo)))
    else:
        erro('a Home encolheu demais (%d -> %d). Cancelado por seguranca.'
             % (len(original), len(novo)))
        return

    if not SIMULAR:
        with open(idx, 'w', encoding='utf-8') as f:
            f.write(novo)

    # -------------------------------------------------------- 4) SITEMAP
    print('\n[4/6] Limpando o sitemap.xml')
    sm = os.path.join(SITE, 'sitemap.xml')
    if os.path.isfile(sm):
        with open(sm, 'r', encoding='utf-8') as f:
            sms = f.read()
        antes = sms
        for p in caminhos_remover:
            sms = re.sub(r'\s*<url>\s*<loc>[^<]*%s</loc>.*?</url>' % re.escape(p),
                         '', sms, flags=re.S)
        if sms != antes:
            if not SIMULAR:
                with open(sm, 'w', encoding='utf-8') as f:
                    f.write(sms)
            ok('sitemap atualizado (%d -> %d urls)'
               % (antes.count('<url>'), sms.count('<url>')))
        else:
            aviso('nenhuma url removida do sitemap (verificar a mao)')
    else:
        aviso('sitemap.xml nao encontrado')

    # ------------------------------------------------------------ 5) SW.JS
    print('\n[5/6] Limpando o cache do app (sw.js)')
    sw = os.path.join(SITE, 'sw.js')
    if os.path.isfile(sw):
        with open(sw, 'r', encoding='utf-8') as f:
            sws = f.read()
        antes = sws
        m = re.search(r"const URLS = \[([^\]]*)\]", sws)
        if m:
            dentro = m.group(1)
            itens = re.findall(r"'([^']*)'", dentro)
            itens_novos = [i for i in itens if i not in caminhos_remover]
            sws = sws[:m.start()] + "const URLS = [" + ", ".join(
                "'%s'" % i for i in itens_novos) + "]" + sws[m.end():]
            ok('sw.js: %d -> %d enderecos no cache' % (len(itens), len(itens_novos)))
        else:
            aviso('nao achei a lista URLS no sw.js (verificar a mao)')

        def subir_versao(mo):
            nome = mo.group(1)
            mm = re.search(r'-v(\d+)$', nome)
            if mm:
                return "const CACHE = '%s-v%d'" % (nome[:mm.start()], int(mm.group(1)) + 1)
            return "const CACHE = '%s-v2'" % nome

        sws_nova = re.sub(r"const CACHE = '([^']*)'", subir_versao, sws)
        if sws_nova != sws:
            ok('versao do cache subiu (obriga o celular a baixar a lista nova)')
        sws = sws_nova
        if sws != antes and not SIMULAR:
            with open(sw, 'w', encoding='utf-8') as f:
                f.write(sws)
    else:
        aviso('sw.js nao encontrado')

    # --------------------------------------------------- 6) MOVER OS HTML
    print('\n[6/6] Movendo os arquivos para fora da pasta publica')
    for p, nome in REMOVER:
        arquivo = os.path.join(SITE, p.lstrip('/') + '.html')
        if os.path.isfile(arquivo):
            if not SIMULAR:
                shutil.copy2(arquivo, os.path.join(backup, os.path.basename(arquivo)))
                os.remove(arquivo)
            ok('%s.html -> guardado em %s' % (p.lstrip('/'), backup))
        else:
            aviso('%s.html nao existe (ja foi removido?)' % p.lstrip('/'))

    # PDFs? (so avisa, nao apaga nada)
    pasta_ebooks = os.path.join(SITE, 'ebooks')
    if os.path.isdir(pasta_ebooks):
        suspeitos = []
        for raiz, _, arquivos in os.walk(pasta_ebooks):
            for a in arquivos:
                baixo = a.lower()
                for p in caminhos_remover:
                    if baixo.startswith(p.lstrip('/')):
                        suspeitos.append(a)
        if suspeitos:
            print('\n  ATENCAO: achei estes PDFs que podem ser dos livros removidos:')
            for a in suspeitos:
                print('     - /ebooks/%s   (NAO apaguei nada; confira)' % a)

    # ------------------------------------------------------------ LEIA-ME
    if not SIMULAR:
        guia = [
            'BACKUP DA LIMPEZA DOS LIVROS — %s' % datetime.now().strftime('%d/%m/%Y %H:%M'),
            '',
            'Aqui estao guardados os arquivos como estavam ANTES da limpeza.',
            'Nada foi perdido.',
            '',
            'SE QUISER DESFAZER TUDO, rode estas linhas no Terminal do aaPanel:',
            '',
            'cp %s/index.html.bak %s/index.html' % (backup, SITE),
            'cp %s/sitemap.xml.bak %s/sitemap.xml' % (backup, SITE),
            'cp %s/sw.js.bak %s/sw.js' % (backup, SITE),
        ]
        for p, _ in REMOVER:
            guia.append('cp %s/%s.html %s/%s.html'
                        % (backup, p.lstrip('/'), SITE, p.lstrip('/')))
        guia += [
            '',
            'Depois abra o site e confira. Se algo sair do lugar, me chame.',
            '',
            'Os livros que sairam do ar (por nao serem de autoria da casa):',
        ]
        for p, nome in REMOVER:
            guia.append('  - %s  %s' % (p, nome))
        guia += ['', 'Os livros que ficaram:']
        for p, nome in FICAM:
            guia.append('  - %s  %s' % (p, nome))
        with open(os.path.join(backup, 'LEIA-ME.txt'), 'w', encoding='utf-8') as f:
            f.write('\n'.join(guia) + '\n')

    # ------------------------------------------------------------ RESUMO
    print('\n' + '=' * 66)
    print('RESUMO')
    print('=' * 66)
    print('Cards na biblioteca: %d -> %d' % (total_antes, len(mantidos)))
    print('Livros que sairam do ar:')
    for p, nome in REMOVER:
        print('   - %-34s %s' % (nome, p))
    print('Livros que ficaram:')
    for i, (p, nome) in enumerate(FICAM, 1):
        print('   %02d. %-34s %s' % (i, nome, p))
    print('\nBackup e arquivos guardados em:')
    print('   %s' % backup)
    print('   (tem um LEIA-ME.txt la dentro ensinando a desfazer)')
    if SIMULAR:
        print('\n>>> SIMULACAO: nada foi gravado.')
    else:
        print('\nFalta um passo so, feito a mao:')
        print('  Google Search Console > Remocoes > pedir a remocao destes enderecos:')
        for p in caminhos_remover:
            print('     https://missaocomdeus.com.br%s' % p)
    print('=' * 66)


if __name__ == '__main__':
    main()
