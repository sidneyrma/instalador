# -*- coding: utf-8 -*-
"""
Painel v4 — missaocomdeus.com.br

v3 (leituras + conversao) + ORIGEM:
  "De onde os nossos irmaos estao chegando" — SEO (Google/Bing), site antigo
  compraoseu.com (redirecionado), redes, direto, etc.

Como funciona:
  - Le o log do Nginx do site NOVO e classifica o "Referer" (quem indicou).
  - Conta CHEGADAS (entradas): so o primeiro acesso da visita conta.
    Navegacao interna (de um livro para outro) nao conta como origem.
  - Le tambem o log do site ANTIGO (compraoseu.com): cada 301 que o servidor
    respondeu e uma pessoa que vinha do site antigo — e o log guarda de onde
    ela veio antes (Google? direto? Instagram?).
  - Se a URL tiver utm_source=... (links marcados), ele manda na classificacao.

Nada de cookie, nada de script de terceiro, nada de JS. So o log do servidor.

Cron (aaPanel, ja existente):
  python3 /home/deploy/gerar_estatisticas.py

Logs lidos (da para mudar por variavel de ambiente, mas o padrao ja serve):
  /www/wwwlogs/missaocomdeus.com.br.log   -> env STATS_LOG
  /www/wwwlogs/compraoseu.com.log         -> env STATS_LOG_ANTIGO
"""
import os
import re
import json
import glob
import html
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, timedelta
from urllib.parse import parse_qs

LOG = os.environ.get('STATS_LOG', '/www/wwwlogs/missaocomdeus.com.br.log')
# Opcional: logs ja rotacionados (o aaPanel guarda os antigos com outro nome).
# Ex.: STATS_LOG_EXTRA="/www/wwwlogs/missaocomdeus.com.br.log-*"
EXTRA_LOGS = os.environ.get('STATS_LOG_EXTRA', '').strip()
OUT = os.environ.get('STATS_OUT', '/www/wwwroot/missaocomdeus.com.br/stats.html')
LEITURAS = os.environ.get('STATS_LEITURAS', '/www/wwwroot/missaocomdeus.com.br/leituras.json')
SITE = '/www/wwwroot/missaocomdeus.com.br'

# Log do site antigo (so 301). Se nao existir, o painel avisa e segue sem ele.
LOG_ANTIGO = os.environ.get(
    'STATS_LOG_ANTIGO',
    '/www/wwwlogs/compraoseu.com.log')
CANDIDATOS_LOG_ANTIGO = [
    '/www/wwwlogs/compraoseu.com.log',
    '/www/wwwlogs/compraoseu.com.br.log',
    '/www/wwwlogs/www.compraoseu.com.log',
]

# Dominios da casa: referer daqui = navegacao interna (nao e chegada)
NOSSOS_HOSTS = {
    'missaocomdeus.com.br', 'www.missaocomdeus.com.br',
    '212.28.182.86', 'localhost',
}

PAGINAS = OrderedDict([
    ('/', 'Home (início)'),
    ('/livro01', 'Livro 01 — O Verbo que Transforma'),
    ('/livro02', 'Livro 02 — A Sabedoria dos Mestres'),
    ('/livro03', 'Livro 03 — A Mente Renovada'),
    ('/livro04', 'Livro 04 — Um Segundo com Deus'),
    ('/livro05', 'Livro 05 — Evolução da Alma'),
    ('/livro06', 'Livro 06 — Jesus Quer Falar com Seu Filho'),
    ('/livro07', 'Livro 07 — O Caminho do Despertar'),
    ('/livro08', 'Livro 08 — O Arquiteto da Realidade'),
    ('/livro09', 'Livro 09 — Anestesia Mental'),
    ('/livro10', 'Livro 10 — O Despertar do Observador'),
    ('/livro11', 'Livro 11 — O Novo Testamento como nunca lido'),
    ('/livro12', 'Livro 12 — Afirmações, Declarações e Orações'),
    ('/trilogia-da-alma', 'Trilogia da Alma — Área de alunos'),
    ('/anestesia-mental', 'Anestesia Mental — Área de alunos'),
    ('/obrigado', 'Página de obrigado (Kiwify)'),
    ('/palavra', 'Caderno Palavra de hoje (casa)'),
    ('/q-quiz-inicio', 'Quiz Home — iniciaram'),
    ('/q-quiz-fim', 'Quiz Home — concluíram'),
    ('/q-trilogia-m01', 'Trilogia — Módulo 01 (plays)'),
    ('/q-trilogia-m02', 'Trilogia — Módulo 02 (plays)'),
    ('/q-trilogia-m03', 'Trilogia — Módulo 03 (plays)'),
    ('/q-trilogia-m04', 'Trilogia — Módulo 04 (plays)'),
    ('/q-trilogia-m05', 'Trilogia — Módulo 05 (plays)'),
    ('/q-trilogia-m06', 'Trilogia — Módulo 06 (plays)'),
    ('/q-trilogia-m07', 'Trilogia — Módulo 07 (plays)'),
    ('/q-anestesia-m01', 'Anestesia — Módulo 01 (plays)'),
    ('/q-anestesia-m02', 'Anestesia — Módulo 02 (plays)'),
    ('/q-anestesia-m03', 'Anestesia — Módulo 03 (plays)'),
    ('/q-anestesia-m04', 'Anestesia — Módulo 04 (plays)'),
    ('/q-anestesia-m05', 'Anestesia — Módulo 05 (plays)'),
    ('/q-anestesia-m06', 'Anestesia — Módulo 06 (plays)'),
    ('/q-anestesia-m07', 'Anestesia — Módulo 07 (plays)'),
    ('/guia-pais-filhos', 'Guia Pais e Filhos — Quiz'),
])

CONVERSAO = OrderedDict([
    ('/q-semeador', ('🎯', 'Quero Ser Semeador (R$ 37)')),
    ('/q-colaborador', ('🌱', 'Colaborador (R$ 19,90)')),
    ('/q-codigo', ('💬', 'Solicitar Código (WhatsApp)')),
    ('/q-whats', ('📱', 'Cliques no WhatsApp')),
    ('/q-palavra-play', ('🎧', 'Palavra de hoje (play)')),
    ('/q-palavra-share', ('📤', 'Palavra compartilhada')),
])

MODULOS_LIVRES = (
    '/q-trilogia-m01', '/q-trilogia-m02', '/q-trilogia-m03',
    '/q-anestesia-m01', '/q-anestesia-m02', '/q-anestesia-m03',
)

ALIAS_CONV = {
    '/q-colaborador19': '/q-colaborador',
    '/q-colaborador19-anestesia': '/q-colaborador',
    '/q-semeador-anestesia': '/q-semeador',
    '/trilogia': '/trilogia-da-alma',
    '/anestesia': '/anestesia-mental',
}

PDF_MAP = {
    '/ebooks/evolucao-da-alma.pdf': '/dl:evolucao',
    '/ebooks/evolucao-da-alma-evalma.pdf': '/dl:evolucao',
    '/ebooks/anestesia-mental.pdf': '/dl:anestesia',
    '/ebooks/anestesia-mental-evalma.pdf': '/dl:anestesia',
    '/ebooks/um-segundo-com-deus-vol-01.pdf': '/dl:devocional-quiz',
    '/ebooks/jesus-quer-falar.pdf': '/dl:jesus-quiz',
    '/ebooks/jesus-quer-falar-com-seu-filho.pdf': '/dl:jesus-livro',
    '/ebooks/livro11-onovotestamenento.pdf': '/dl:brinde-nt',
    '/ebooks/livro11.pdf': '/dl:chute-pdf',
    '/ebooks/livro10.pdf': '/dl:chute-pdf',
}

DL_NOMES = OrderedDict([
    ('/dl:brinde-nt', 'Brinde extra · PDF do NT (página de obrigado)'),
    ('/dl:evolucao', 'PDF Evolução da Alma (evalma + nome antigo)'),
    ('/dl:anestesia', 'PDF Anestesia Mental (evalma + nome antigo)'),
    ('/dl:devocional-quiz', 'PDF Devocional Vol. 01 (quiz, livre)'),
    ('/dl:jesus-quiz', 'PDF Jesus Quer Falar (quiz, livre)'),
    ('/dl:jesus-livro', 'PDF Jesus Quer Falar com Seu Filho (outro arquivo)'),
    ('/dl:chute-pdf', 'PDF com nome chutado (livro10 / livro11 sem evalma)'),
    ('/q-palavra-play', 'Palavra de hoje (plays no botão)'),
    ('/q-palavra-share', 'Palavra compartilhada'),
])

# ------------------------------------------------------------------ ORIGEM

# Baldes de origem. A ordem aqui e a ordem que aparece no painel.
ORIGENS = OrderedDict([
    ('google', ('🔎', 'Google (busca / SEO)')),
    ('buscadores', ('🔍', 'Outros buscadores (Bing, Yahoo, DuckDuckGo)')),
    ('antigo', ('🏠', 'Site antigo compraoseu.com')),
    ('instagram', ('📸', 'Instagram / Facebook')),
    ('tiktok', ('🎵', 'TikTok')),
    ('youtube', ('▶️', 'YouTube')),
    ('whatsapp', ('💬', 'WhatsApp')),
    ('email', ('📧', 'E-mail / lista')),
    ('outros_social', ('👥', 'Outras redes (Pinterest, X, LinkedIn)')),
    ('sites', ('🔗', 'Outros sites (parceiros, fóruns, blogs)')),
    ('direto', ('🧭', 'Direto (digitou, favoritos, app)')),
])

SEO = ('google', 'buscadores')
REDES = ('instagram', 'tiktok', 'youtube', 'whatsapp', 'outros_social')

BUSCADORES = (
    'bing.com', 'yahoo.', 'duckduckgo.com', 'yandex.', 'baidu.',
    'ecosia.org', 'search.brave.com', 'startpage.com', 'mojeek.com',
    'qwant.com', 'sapo.pt', 'uol.com.br/busca', 'globo.com/busca',
)

RE_COMPLETA = re.compile(
    r'^(\S+) \S+ \S+ \[([^\]]+)\] "GET (\S+) HTTP[^"]*" (\d{3}) \S+ "([^"]*)" "([^"]*)"')
RE_SIMPLES = re.compile(r'^(\S+) .*?\[([^\]]+)\] "GET (\S+) HTTP')
RE_EXT = re.compile(
    r'\.(png|jpg|jpeg|gif|svg|ico|css|js|woff2?|webp|xml|json|txt|webmanifest)$', re.I)
RE_BOT = re.compile(
    r'bot|crawl|spider|slurp|scan|monitor|probe|python|curl|wget|httpclient|'
    r'go-http|libwww|java/|okhttp|headless|lighthouse|pingdom|uptime|'
    r'facebookexternalhit|whatsapp|telegrambot|twitterbot|linkedinbot|'
    r'semrush|ahrefs|mj12|dotbot|petalbot|bytespider|zgrab|masscan|nuclei', re.I)
RE_HOST = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.-]*://([^/]+)')


def chave_data(s):
    """Ordena dias no formato dd/mm/YYYY (ordem certa mesmo virando o mes)."""
    try:
        return datetime.strptime(s, '%d/%m/%Y')
    except Exception:
        return datetime.min


def host_de(url):
    """Pega so o dominio de uma URL de referencia."""
    if not url or url == '-':
        return ''
    m = RE_HOST.match(url)
    if m:
        return m.group(1).lower().split(':')[0]
    return ''


def classificar_origem(referer, utm_source='', utm_medium=''):
    """Devolve o balde de origem. UTM manda; se nao tiver, usa o Referer."""
    s = (utm_source or '').strip().lower()
    m = (utm_medium or '').strip().lower()

    if s:
        if 'google' in s or s in ('gsearch', 'seo', 'busca'):
            return 'google'
        if 'bing' in s or 'yahoo' in s or 'duckduckgo' in s or 'buscador' in s:
            return 'buscadores'
        if 'compraoseu' in s or 'antigo' in s:
            return 'antigo'
        if 'instagram' in s or 'facebook' in s or s.startswith('fb') or 'meta' in s:
            return 'instagram'
        if 'tiktok' in s:
            return 'tiktok'
        if 'youtube' in s:
            return 'youtube'
        if 'whatsapp' in s or 'whats' in s or 'zap' in s:
            return 'whatsapp'
        if 'email' in s or 'newsletter' in s or 'lista' in s or 'formsubmit' in s:
            return 'email'
        if 'pinterest' in s or 'linkedin' in s or 'twitter' in s or s == 'x':
            return 'outros_social'
        if m in ('cpc', 'paid', 'ads', 'social', 'referral'):
            return 'sites'
        return 'sites'

    r = (referer or '').strip()
    if not r or r == '-':
        return 'direto'
    rl = r.lower()
    host = host_de(r)

    if 'compraoseu.com' in host or 'compraoseu.com' in rl:
        return 'antigo'
    if host.startswith('google.') or '.google.' in host or host == 'google.com':
        return 'google'
    if any(b in host for b in BUSCADORES) or host.startswith('search.') or '/search' in rl:
        return 'buscadores'
    if 'instagram' in host or 'facebook' in host or host.endswith('fb.me') \
            or 'messenger' in host or host.endswith('fbcdn.net'):
        return 'instagram'
    if 'tiktok' in host or host.endswith('tiktokcdn.com'):
        return 'tiktok'
    if 'youtube' in host or host.endswith('youtu.be'):
        return 'youtube'
    if 'whatsapp' in host or host.endswith('wa.me') or 'whatsapp' in rl:
        return 'whatsapp'
    if 'pinterest' in host or 'linkedin' in host or 'twitter' in host \
            or host == 'x.com' or host.endswith('t.co'):
        return 'outros_social'
    if 'mail.google' in rl or 'android.gm' in rl or 'outlook.live' in host:
        return 'email'
    if host:
        return 'sites'
    return 'direto'


def lista_logs():
    """O log atual + os rotacionados que o autor autorizou via STATS_LOG_EXTRA."""
    arquivos = [LOG]
    if EXTRA_LOGS:
        for padrao in EXTRA_LOGS.split(','):
            padrao = padrao.strip()
            if padrao:
                arquivos.extend(sorted(glob.glob(padrao)))
    vistos = []
    for a in arquivos:
        if a not in vistos and os.path.isfile(a):
            vistos.append(a)
    return vistos


def garantir_pixels():
    for nome in ('q-semeador', 'q-colaborador', 'q-colaborador19',
                 'q-colaborador19-anestesia', 'q-codigo', 'q-whats', 'q-aula-gratis',
                 'q-palavra-play', 'q-palavra-share'):
        p = os.path.join(SITE, nome)
        if not os.path.isfile(p):
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    f.write('ok\n')
            except Exception:
                pass


def analisar():
    contagens = Counter()
    contagens_hoje = Counter()
    total_geral = 0
    data_inicio = None
    data_fim = None
    por_dia = Counter()
    visitantes_por_dia = defaultdict(set)
    visitantes_total = set()
    descartados_robos = 0
    descartados_erros = 0
    robos_por_dia = Counter()
    erros_por_dia = Counter()
    conv = Counter()
    conv_hoje = Counter()
    conv_por_dia = defaultdict(Counter)

    # --- origem
    origens = Counter()
    origens_hoje = Counter()
    origens_ips = defaultdict(set)
    origens_por_dia = defaultdict(Counter)
    total_chegadas = 0
    chegadas_hoje = 0
    chegadas_por_dia = Counter()
    refs_dom = Counter()
    entradas = Counter()
    entradas_hoje = Counter()
    entradas_por_origem = defaultdict(Counter)

    agora = datetime.now()
    hoje_str = agora.strftime('%d/%m/%Y')
    ontem = (agora - timedelta(days=1)).strftime('%d/%m/%Y')
    data_ontem = agora.date() - timedelta(days=1)
    acessos_ontem_mesmo_horario = 0

    if not os.path.exists(LOG):
        return None, 'Log não encontrado: ' + LOG

    def linhas():
        """Le o log atual (e os rotacionados, se o autor liberou)."""
        for caminho in lista_logs():
            with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
                for linha in f:
                    yield linha

    for linha in linhas():
            m = RE_COMPLETA.match(linha)
            if m:
                ip, data, url, status, ref, ua = (m.group(1), m.group(2), m.group(3),
                                                  m.group(4), m.group(5), m.group(6))
            else:
                m = RE_SIMPLES.match(linha)
                if not m:
                    continue
                ip, data, url = m.group(1), m.group(2), m.group(3)
                status, ref, ua = '200', '-', 'desconhecido'
            if RE_EXT.search(url):
                continue

            chave_dia = None
            dt = None
            try:
                dt = datetime.strptime(data.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
                chave_dia = dt.strftime('%d/%m/%Y')
            except Exception:
                pass

            if ua == '-' or ua == '' or RE_BOT.search(ua):
                descartados_robos += 1
                if chave_dia:
                    robos_por_dia[chave_dia] += 1
                continue
            if status not in ('200', '304'):
                descartados_erros += 1
                if chave_dia:
                    erros_por_dia[chave_dia] += 1
                continue

            path = url.split('?')[0].rstrip('/')
            query = url.split('?', 1)[1] if '?' in url else ''
            if path == '':
                path = '/'
            if path.endswith('.html'):
                path = path[:-5]
                if path == '/index':
                    path = '/'
            path = ALIAS_CONV.get(path, path)
            path_l = path.lower()

            if path.startswith('/.well-known'):
                continue

            dl_key = PDF_MAP.get(path_l)
            if dl_key:
                contagens[dl_key] += 1
                if chave_dia == hoje_str:
                    contagens_hoje[dl_key] += 1
                total_geral += 1
                if dt is not None:
                    por_dia[chave_dia] += 1
                    visitantes_por_dia[chave_dia].add(ip)
                    visitantes_total.add(ip)
                    if data_inicio is None or dt < data_inicio:
                        data_inicio = dt
                    if data_fim is None or dt > data_fim:
                        data_fim = dt
                continue

            if path_l.startswith('/audio/palavra-dia-') and path_l.endswith('.mp3'):
                continue

            if path in CONVERSAO:
                conv[path] += 1
                if chave_dia:
                    conv_por_dia[chave_dia][path] += 1
                    if chave_dia == hoje_str:
                        conv_hoje[path] += 1
                continue

            # --- ORIGEM: so conta CHEGADA (referer de fora da casa)
            host_ref = host_de(ref)
            interna = (host_ref in NOSSOS_HOSTS) or (
                ref.startswith('/') and not host_ref)
            if not interna:
                utm = {}
                if query:
                    try:
                        utm = {k.lower(): (v[0] if v else '')
                               for k, v in parse_qs(query, keep_blank_values=False).items()}
                    except Exception:
                        utm = {}
                bucket = classificar_origem(
                    ref, utm.get('utm_source', ''), utm.get('utm_medium', ''))
                origens[bucket] += 1
                origens_ips[bucket].add(ip)
                if chave_dia:
                    origens_por_dia[chave_dia][bucket] += 1
                    chegadas_por_dia[chave_dia] += 1
                    if chave_dia == hoje_str:
                        origens_hoje[bucket] += 1
                        chegadas_hoje += 1
                total_chegadas += 1
                if host_ref:
                    refs_dom[host_ref] += 1
                entradas[path] += 1
                entradas_por_origem[bucket][path] += 1
                if chave_dia == hoje_str:
                    entradas_hoje[path] += 1

            if path in PAGINAS or path.startswith('/livro'):
                contagens[path] += 1
            else:
                contagens['/outros:' + path] += 1
            total_geral += 1

            if dt is not None:
                por_dia[chave_dia] += 1
                visitantes_por_dia[chave_dia].add(ip)
                visitantes_total.add(ip)
                if chave_dia == hoje_str and (path in PAGINAS or path.startswith('/livro')):
                    contagens_hoje[path] += 1
                if dt.date() == data_ontem and (dt.hour, dt.minute) <= (agora.hour, agora.minute):
                    acessos_ontem_mesmo_horario += 1
                if data_inicio is None or dt < data_inicio:
                    data_inicio = dt
                if data_fim is None or dt > data_fim:
                    data_fim = dt

    total_hoje = por_dia.get(hoje_str, 0)
    total_ontem = por_dia.get(ontem, 0)
    if acessos_ontem_mesmo_horario > 0:
        variacao = ((total_hoje - acessos_ontem_mesmo_horario) / acessos_ontem_mesmo_horario) * 100
    else:
        variacao = 100.0 if total_hoje > 0 else 0.0
    horas_decorridas = agora.hour + agora.minute / 60.0
    projecao = int(round(total_hoje / horas_decorridas * 24)) if horas_decorridas > 0 else total_hoje

    unicos_hoje = len(visitantes_por_dia.get(hoje_str, set()))
    unicos_ontem = len(visitantes_por_dia.get(ontem, set()))
    unicos_total = len(visitantes_total)

    origem = {
        'origens': origens,
        'origens_hoje': origens_hoje,
        'origens_ips': origens_ips,
        'origens_por_dia': origens_por_dia,
        'total_chegadas': total_chegadas,
        'chegadas_hoje': chegadas_hoje,
        'chegadas_por_dia': chegadas_por_dia,
        'refs_dom': refs_dom,
        'entradas': entradas,
        'entradas_hoje': entradas_hoje,
        'entradas_por_origem': entradas_por_origem,
    }

    return (contagens, total_geral, data_inicio, data_fim, por_dia,
            contagens_hoje, total_hoje, total_ontem, variacao, hoje_str, ontem,
            acessos_ontem_mesmo_horario, projecao,
            unicos_hoje, unicos_ontem, unicos_total, visitantes_por_dia,
            descartados_robos, descartados_erros, robos_por_dia, erros_por_dia,
            conv, conv_hoje, conv_por_dia, origem), None


def analisar_antigo(hoje_str):
    """Le o log do site antigo (compraoseu.com).

    Cada visita que o servidor respondeu com 301 e uma pessoa que veio do
    endereco antigo. O referer dessa linha diz de onde ela estava antes
    (Google, direto, Instagram...). Isso responde: "veio pelo SEO ou pelo
    site antigo?" - as duas coisas ao mesmo tempo.
    """
    caminho = None
    for c in [LOG_ANTIGO] + CANDIDATOS_LOG_ANTIGO:
        if c and os.path.exists(c):
            caminho = c
            break
    if not caminho:
        return None

    total = 0
    hoje = 0
    por_dia = Counter()
    por_origem = Counter()
    por_origem_hoje = Counter()
    ips = set()
    urls = Counter()
    data_inicio = None
    data_fim = None
    descartados = 0

    with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            m = RE_COMPLETA.match(linha)
            if m:
                ip, data, url, status, ref, ua = (m.group(1), m.group(2), m.group(3),
                                                  m.group(4), m.group(5), m.group(6))
            else:
                m = RE_SIMPLES.match(linha)
                if not m:
                    continue
                ip, data, url = m.group(1), m.group(2), m.group(3)
                status, ref, ua = '301', '-', 'desconhecido'
            if RE_EXT.search(url):
                continue

            chave_dia = None
            try:
                dt = datetime.strptime(data.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
                chave_dia = dt.strftime('%d/%m/%Y')
                if data_inicio is None or dt < data_inicio:
                    data_inicio = dt
                if data_fim is None or dt > data_fim:
                    data_fim = dt
            except Exception:
                dt = None

            if ua == '-' or ua == '' or RE_BOT.search(ua):
                descartados += 1
                continue
            if not status.startswith('3') and status not in ('200', '304'):
                descartados += 1
                continue

            host_ref = host_de(ref)
            if host_ref in NOSSOS_HOSTS:
                continue

            query = url.split('?', 1)[1] if '?' in url else ''
            utm = {}
            if query:
                try:
                    utm = {k.lower(): (v[0] if v else '')
                           for k, v in parse_qs(query, keep_blank_values=False).items()}
                except Exception:
                    utm = {}
            bucket = classificar_origem(
                ref, utm.get('utm_source', ''), utm.get('utm_medium', ''))

            total += 1
            ips.add(ip)
            por_origem[bucket] += 1
            urls[url.split('?')[0]] += 1
            if chave_dia:
                por_dia[chave_dia] += 1
                if chave_dia == hoje_str:
                    hoje += 1
                    por_origem_hoje[bucket] += 1

    return {
        'arquivo': caminho,
        'total': total,
        'hoje': hoje,
        'por_dia': por_dia,
        'por_origem': por_origem,
        'por_origem_hoje': por_origem_hoje,
        'pessoas': len(ips),
        'urls': urls,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'descartados': descartados,
    }


def gravar_leituras(contagens):
    livros = {}
    for i in range(1, 13):
        p = '/livro%02d' % i
        livros[p] = int(contagens.get(p, 0))
    top = sorted(livros.items(), key=lambda x: -x[1])
    top3 = [p for p, n in top if n > 0][:3]
    doc = {
        'atualizado': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'livros': livros,
        'top3': top3,
    }
    try:
        with open(LEITURAS, 'w', encoding='utf-8') as f:
            json.dump(doc, f, ensure_ascii=False)
        print('leituras.json em', LEITURAS)
    except Exception as e:
        print('AVISO leituras.json:', e)


def bloco_origem_html(origem, antigo):
    """Monta a secao 'De onde vem os nossos irmaos'."""
    origens = origem['origens']
    origens_hoje = origem['origens_hoje']
    origens_ips = origem['origens_ips']
    origens_por_dia = origem['origens_por_dia']
    total = origem['total_chegadas']
    refs_dom = origem['refs_dom']
    entradas = origem['entradas']
    entradas_por_origem = origem['entradas_por_origem']

    def n(b):
        return int(origens.get(b, 0))

    def pessoas(b):
        return len(origens_ips.get(b, set()))

    def hoje_n(b):
        return int(origens_hoje.get(b, 0))

    n_seo = sum(n(b) for b in SEO)
    n_redes = sum(n(b) for b in REDES)
    n_antigo = antigo['total'] if antigo else n('antigo')

    # ---- cards
    def card(emoji, valor, rotulo, rodape):
        return (f'<div class="card origem"><div class="v">{valor}</div>'
                f'<div class="l">{emoji} {rotulo}</div>'
                f'<div class="h">{rodape}</div></div>')

    cards = []
    cards.append(card('🔎', n_seo, 'SEO (busca)',
                      f'{sum(hoje_n(b) for b in SEO)} hoje · {sum(pessoas(b) for b in SEO)} pessoas'))
    cards.append(card('🏠', n_antigo, 'Site antigo',
                      (f'{antigo["hoje"]} hoje · {antigo["pessoas"]} pessoas' if antigo else 'log antigo não lido')))
    cards.append(card('🧭', n('direto'), 'Direto',
                      f'{hoje_n("direto")} hoje · {pessoas("direto")} pessoas'))
    cards.append(card('📣', n_redes, 'Redes (IG/FB/TikTok/YT/Zap)',
                      f'{sum(hoje_n(b) for b in REDES)} hoje · {sum(pessoas(b) for b in REDES)} pessoas'))
    cards.append(card('🔗', n('sites'), 'Outros sites',
                      f'{hoje_n("sites")} hoje · {pessoas("sites")} pessoas'))
    cards.append(card('📊', total, 'Chegadas (total)',
                      f'{origem["chegadas_hoje"]} hoje'))

    # ---- tabela de origens
    linhas = []
    for b, (emoji, nome) in ORIGENS.items():
        v = n(b)
        pct = (v / total * 100) if total else 0
        destaque = ' style="background:rgba(201,162,75,.08)"' if b in SEO else ''
        linhas.append(f"""
        <tr{destaque}>
          <td>{emoji} {html.escape(nome)}</td>
          <td class="num">{v}</td>
          <td class="num">{pessoas(b)}</td>
          <td class="num" style="color:#7fe0a3">{hoje_n(b)}</td>
          <td class="num">{pct:.1f}%</td>
          <td><div class="barra"><div class="fill" style="width:{min(100,pct):.1f}%"></div></div></td>
        </tr>""")

    # ---- site antigo
    if antigo:
        periodo_antigo = '—'
        if antigo['data_inicio'] and antigo['data_fim']:
            periodo_antigo = (f"{antigo['data_inicio'].strftime('%d/%m/%Y')} até "
                              f"{antigo['data_fim'].strftime('%d/%m/%Y')}")
        lo = antigo['por_origem']
        tot_antigo = antigo['total'] or 1
        linhas_antigo = []
        for b, (emoji, nome) in ORIGENS.items():
            v = int(lo.get(b, 0))
            if v == 0:
                continue
            pct = v / tot_antigo * 100
            linhas_antigo.append(f"""
        <tr>
          <td>{emoji} {html.escape(nome)}</td>
          <td class="num">{v}</td>
          <td class="num">{pct:.1f}%</td>
        </tr>""")
        top_urls = ' · '.join(
            f'{html.escape(u)} ({c})' for u, c in antigo['urls'].most_common(6)
        ) or '—'
        antigo_html = f"""
  <h3 style="color:#e3c877;font-size:1rem;margin:22px 0 8px;">🏠 Quem chegou pelo site antigo (compraoseu.com)</h3>
  <div class="comparacao" style="border-color:rgba(201,162,75,.5);margin-bottom:16px;">
    <div class="bloco"><div class="rot">Total de visitas no site antigo</div><div class="val gold">{antigo['total']}</div></div>
    <div class="bloco"><div class="rot">Pessoas (IPs)</div><div class="val">{antigo['pessoas']}</div></div>
    <div class="bloco"><div class="rot">Hoje</div><div class="val verde">{antigo['hoje']}</div></div>
    <div class="bloco"><div class="rot">Período no log</div><div class="val" style="font-size:1rem">{periodo_antigo}</div></div>
  </div>
  <table>
    <tr><th>Antes de cair no site antigo, a pessoa estava em:</th><th>Visitas</th><th>%</th></tr>
    {''.join(linhas_antigo) or '<tr><td colspan="3">Sem dados</td></tr>'}
  </table>
  <p style="font-size:.8rem;color:#9fb0c8;">Endereços mais pedidos no site antigo: {top_urls}</p>
"""
    else:
        antigo_html = """
  <h3 style="color:#e3c877;font-size:1rem;margin:22px 0 8px;">🏠 Site antigo (compraoseu.com)</h3>
  <p class="aviso">Não achei o log do site antigo neste servidor. Se o compraoseu.com estiver em
  <b>outra</b> máquina, copie o arquivo de log dele para <code>/www/wwwlogs/compraoseu.com.log</code>
  (ou ajuste a variável <code>STATS_LOG_ANTIGO</code>) que esta tabela aparece sozinha.</p>
"""

    # ---- dominios que indicam
    linhas_refs = ''.join(
        f'<tr><td>{html.escape(d)}</td><td class="num">{c}</td></tr>'
        for d, c in refs_dom.most_common(12)
    ) or '<tr><td colspan="2">Nenhum registrado</td></tr>'

    # ---- paginas de entrada
    def nome_pagina(p):
        return PAGINAS.get(p, p)

    linhas_entradas = ''.join(
        f'<tr><td>{html.escape(nome_pagina(p))} <span class="url">{html.escape(p)}</span></td>'
        f'<td class="num">{c}</td><td class="num" style="color:#7fe0a3">'
        f'{origem["entradas_hoje"].get(p, 0)}</td></tr>'
        for p, c in entradas.most_common(8)
    ) or '<tr><td colspan="3">Sem dados</td></tr>'

    # ---- paginas de entrada vindas do Google (SEO)
    linhas_entradas_seo = ''.join(
        f'<tr><td>{html.escape(nome_pagina(p))} <span class="url">{html.escape(p)}</span></td>'
        f'<td class="num">{c}</td></tr>'
        for p, c in entradas_por_origem.get('google', Counter()).most_common(8)
    ) or '<tr><td colspan="2">Ainda sem chegadas pelo Google neste log</td></tr>'

    # ---- ultimos 7 dias
    dias = sorted(origem['chegadas_por_dia'].keys(),
                  key=chave_data, reverse=True)[:7]
    linhas_dias = []
    for d in dias:
        od = origens_por_dia.get(d, Counter())
        a = antigo['por_dia'].get(d, 0) if antigo else 0
        linhas_dias.append(
            f'<tr><td>{d}</td>'
            f'<td class="num">{sum(int(od.get(b, 0)) for b in SEO)}</td>'
            f'<td class="num">{int(od.get("direto", 0))}</td>'
            f'<td class="num">{sum(int(od.get(b, 0)) for b in REDES)}</td>'
            f'<td class="num" style="color:#e3c877">{a}</td>'
            f'<td class="num">{origem["chegadas_por_dia"].get(d, 0)}</td></tr>')
    if antigo:
        for d in sorted(set(antigo['por_dia'].keys()), key=chave_data, reverse=True)[:7]:
            if d in dias:
                continue
            linhas_dias.append(
                f'<tr><td>{d}</td><td class="num">0</td><td class="num">0</td>'
                f'<td class="num">0</td><td class="num" style="color:#e3c877">'
                f'{antigo["por_dia"].get(d, 0)}</td><td class="num">0</td></tr>')
    tabela_dias = '\n'.join(linhas_dias) or '<tr><td colspan="6">Sem dados</td></tr>'

    pct_seo = (n_seo / total * 100) if total else 0
    pct_antigo = (n_antigo / total * 100) if total else 0
    pct_direto = (n('direto') / total * 100) if total else 0
    pct_redes = (n_redes / total * 100) if total else 0

    return f"""
  <h2>De onde vêm os nossos irmãos <span class="selo-filtro">novo · v4</span></h2>
  <div class="cards">{''.join(cards)}</div>
  <p style="font-size:.92rem;color:#e8ecf3;margin:-16px 0 12px;">
    <b>Resposta curta:</b> de <b>{total}</b> chegadas, <b>{pct_seo:.0f}% vêm da busca (SEO)</b>,
    <b>{pct_antigo:.0f}% entraram pelo endereço antigo compraoseu.com</b> (o redirecionamento 301),
    {pct_direto:.0f}% vieram direto e {pct_redes:.0f}% das redes.
  </p>
  <p class="aviso" style="margin:0 0 20px;">
    <b>Como ler sem se enganar:</b> quem vem do compraoseu.com atravessa o redirecionamento e
    chega aqui — e o navegador guarda a origem de <i>antes</i> (Google, por exemplo). Por isso
    essas visitas <b>já estão contadas</b> dentro do número de SEO/Direto aqui de cima:
    <b>não some os dois blocos.</b> A tabela do site antigo logo abaixo responde a outra
    pergunta: «do que chega pelo endereço antigo, quanto é busca e quanto é gente que
    digitou o endereço?»
  </p>
  <table>
    <tr><th>Origem</th><th>Chegadas</th><th>Pessoas</th><th>Hoje</th><th>%</th><th>Distribuição</th></tr>
    {''.join(linhas)}
  </table>
  <p style="font-size:.8rem;color:#9fb0c8;">
    <b>Chegada</b> = o primeiro acesso da visita, quando quem indicou é de fora da casa.
    Navegar de um livro para outro não conta (é a mesma visita). Robôs e buscadores de
    empresa (SEMrush, Ahrefs) não entram. <b>Direto</b> costuma crescer quando o link é
    colado em grupos de WhatsApp e no Instagram, porque esses apps não avisam de onde
    a pessoa veio. Por isso vale marcar os links com <code>utm_source</code>.
  </p>
  {antigo_html}

  <h3 style="color:#e3c877;font-size:1rem;margin:26px 0 8px;">📍 Por qual página eles entram</h3>
  <table>
    <tr><th>Página de entrada</th><th>Chegadas</th><th>Hoje</th></tr>
    {linhas_entradas}
  </table>

  <h3 style="color:#e3c877;font-size:1rem;margin:26px 0 8px;">🔎 Páginas que o Google mais entrega</h3>
  <table>
    <tr><th>Página (chegada pelo Google)</th><th>Chegadas</th></tr>
    {linhas_entradas_seo}
  </table>

  <h3 style="color:#e3c877;font-size:1rem;margin:26px 0 8px;">🔗 Quem nos indica (domínios)</h3>
  <table>
    <tr><th>Domínio de onde a pessoa veio</th><th>Chegadas</th></tr>
    {linhas_refs}
  </table>

  <h3 style="color:#e3c877;font-size:1rem;margin:26px 0 8px;">📅 Últimos 7 dias por origem</h3>
  <table>
    <tr><th>Dia</th><th>SEO (busca)</th><th>Direto</th><th>Redes</th><th>Pelo site antigo</th><th>Chegadas (novo)</th></tr>
    {tabela_dias}
  </table>
"""


def montar_html(res, antigo):
    (contagens, total_geral, data_inicio, data_fim, por_dia,
     contagens_hoje, total_hoje, total_ontem, variacao, hoje_str, ontem,
     ontem_mesmo_horario, projecao,
     unicos_hoje, unicos_ontem, unicos_total, visitantes_por_dia,
     descartados_robos, descartados_erros, robos_por_dia, erros_por_dia,
     conv, conv_hoje, conv_por_dia, origem) = res

    if variacao > 0:
        seta = '📈'
    elif variacao < 0:
        seta = '📉'
    else:
        seta = '➖'

    itens = []
    for path, nome in PAGINAS.items():
        itens.append((path, nome, contagens.get(path, 0), contagens_hoje.get(path, 0)))
    itens_ordenados = sorted(itens, key=lambda x: -x[2])

    linhas = []
    for i, (path, nome, n, n_hoje) in enumerate(itens_ordenados, 1):
        pct = (n / total_geral * 100) if total_geral else 0
        medalha = {1: '🥇', 2: '🥈', 3: '🥉'}.get(i, '')
        hoje_txt = f'<span style="color:#7fe0a3">({n_hoje} hoje)</span>' if n_hoje else ''
        linhas.append(f"""
        <tr>
          <td class="num">{medalha} {i}</td>
          <td><a href="https://missaocomdeus.com.br{path}">{html.escape(nome)}</a>
<span class="url">{path}</span></td>
          <td class="num">{n} {hoje_txt}</td>
          <td class="num">{pct:.1f}%</td>
          <td><div class="barra"><div class="fill" style="width:{min(100,pct)}%"></div></div></td>
        </tr>""")

    dias = sorted(por_dia.keys(), key=chave_data, reverse=True)[:7]
    linhas_dias = '\n'.join(
        f'<tr><td>{d}</td><td class="num">{por_dia.get(d, 0)}</td>'
        f'<td class="num" style="color:#7fe0a3">{len(visitantes_por_dia.get(d, set()))}</td>'
        f'<td class="num" style="color:#9fb0c8">{robos_por_dia.get(d, 0) + erros_por_dia.get(d, 0)}</td></tr>'
        for d in dias
    ) or '<tr><td colspan="4">Sem dados diários</td></tr>'

    outros = [(k, v) for k, v in contagens.items() if k.startswith('/outros:')]
    outros.sort(key=lambda x: -x[1])
    linhas_outros = '\n'.join(
        f'<tr><td>{html.escape(k.replace("/outros:", "/"))}</td><td class="num">{v}</td></tr>'
        for k, v in outros[:15]
    ) or '<tr><td colspan="2">Nenhum</td></tr>'

    total_livros = sum(contagens.get(p, 0) for p, _ in PAGINAS.items() if p.startswith('/livro'))
    total_home = contagens.get('/', 0)
    livros_lidos = sum(1 for p, _ in PAGINAS.items() if p.startswith('/livro') and contagens.get(p, 0) > 0)

    n_sem = conv.get('/q-semeador', 0)
    n_col = conv.get('/q-colaborador', 0)
    pediram_code = conv.get('/q-codigo', 0) + conv.get('/q-whats', 0)
    aula_gratis = sum(contagens.get(p, 0) for p in MODULOS_LIVRES)
    aula_hoje = sum(contagens_hoje.get(p, 0) for p in MODULOS_LIVRES)
    brinde_nt = contagens.get('/dl:brinde-nt', 0)
    brinde_hoje = contagens_hoje.get('/dl:brinde-nt', 0)
    taxa = (n_sem / unicos_total * 100) if unicos_total else 0

    cards_conv = []
    cards_conv.append(
        f'<div class="card conv"><div class="v">{n_sem}</div>'
        f'<div class="l">🎯 Semeador R$ 37</div>'
        f'<div class="h">{conv_hoje.get("/q-semeador", 0)} hoje</div></div>')
    cards_conv.append(
        f'<div class="card conv"><div class="v">{n_col}</div>'
        f'<div class="l">🌱 Colaborador R$ 19,90</div>'
        f'<div class="h">{conv_hoje.get("/q-colaborador", 0)} hoje</div></div>')
    cards_conv.append(
        f'<div class="card conv"><div class="v">{pediram_code}</div>'
        f'<div class="l">💬 Código / WhatsApp</div>'
        f'<div class="h">{conv_hoje.get("/q-codigo", 0) + conv_hoje.get("/q-whats", 0)} hoje</div></div>')
    cards_conv.append(
        f'<div class="card conv"><div class="v">{aula_gratis}</div>'
        f'<div class="l">🎬 Aula grátis (plays 1 a 3)</div>'
        f'<div class="h">{aula_hoje} hoje</div></div>')
    cards_conv.append(
        f'<div class="card conv"><div class="v">{brinde_nt}</div>'
        f'<div class="l">🎁 PDF NT baixado</div>'
        f'<div class="h">{brinde_hoje} hoje · obrigado {contagens.get("/obrigado", 0)}</div></div>')
    cards_conv.append(
        f'<div class="card conv destaque"><div class="v">{taxa:.1f}%</div>'
        f'<div class="l">📈 Semeador / pessoas</div>'
        f'<div class="h">{unicos_total} pessoas</div></div>')

    linhas_conv = '\n'.join(
        f'<tr><td>{emoji} {html.escape(nome)}</td><td class="num">{conv.get(path, 0)}</td>'
        f'<td class="num" style="color:#7fe0a3">{conv_hoje.get(path, 0)}</td></tr>'
        for path, (emoji, nome) in CONVERSAO.items()
    ) or '<tr><td colspan="3">Sem cliques de conversão ainda</td></tr>'

    def _dl_n(k):
        if k.startswith('/q-'):
            return conv.get(k, 0), conv_hoje.get(k, 0)
        return contagens.get(k, 0), contagens_hoje.get(k, 0)

    linhas_dl = '\n'.join(
        f'<tr><td>{html.escape(nome)}</td><td class="num">{_dl_n(k)[0]}</td>'
        f'<td class="num" style="color:#7fe0a3">{_dl_n(k)[1]}</td></tr>'
        for k, nome in DL_NOMES.items()
    )

    periodo = '—'
    if data_inicio and data_fim:
        periodo = f'{data_inicio.strftime("%d/%m/%Y %H:%M")} até {data_fim.strftime("%d/%m/%Y %H:%M")}'

    bloco_origem = bloco_origem_html(origem, antigo)

    html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Estatisticas de Acesso — Portal O Despertar</title>
<style>
  :root {{ --navy:#0e1a2e; --gold:#c9a24b; --cream:#faf6ee; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:'Segoe UI',system-ui,sans-serif; background:var(--navy); color:#e8ecf3; line-height:1.5; }}
  .wrap {{ max-width:960px; margin:0 auto; padding:24px 16px 60px; }}
  h1 {{ color:var(--gold); font-size:1.6rem; margin-bottom:4px; }}
  .sub {{ color:#9fb0c8; font-size:.9rem; margin-bottom:24px; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-bottom:28px; }}
  .card {{ background:#16283f; border:1px solid rgba(201,162,75,.25); border-radius:10px; padding:16px; text-align:center; }}
  .card .v {{ font-size:1.6rem; font-weight:700; color:var(--gold); }}
  .card .l {{ font-size:.75rem; color:#9fb0c8; text-transform:uppercase; letter-spacing:.06em; }}
  .card .h {{ font-size:.72rem; color:#7fe0a3; margin-top:4px; }}
  .card.destaque {{ border-color:var(--gold); background:linear-gradient(180deg,#1a2c47,#16283f); }}
  .card.humano .v {{ color:#7fe0a3; }}
  .card.conv {{ border-color:rgba(127,224,163,.35); }}
  .card.conv .v {{ color:#7fe0a3; }}
  .card.origem {{ border-color:rgba(201,162,75,.45); }}
  table {{ width:100%; border-collapse:collapse; background:#16283f; border-radius:10px; overflow:hidden; }}
  th {{ background:rgba(201,162,75,.15); color:var(--gold); text-align:left; padding:10px 12px; font-size:.8rem; text-transform:uppercase; letter-spacing:.05em; }}
  td {{ padding:10px 12px; border-top:1px solid rgba(201,162,75,.15); font-size:.92rem; vertical-align:middle; }}
  .num {{ text-align:center; white-space:nowrap; }}
  .url {{ color:#7f92ad; font-size:.75rem; }}
  .barra {{ background:#0e1a2e; border-radius:6px; height:12px; overflow:hidden; min-width:120px; }}
  .fill {{ background:linear-gradient(90deg,#c9a24b,#e3c877); height:100%; border-radius:6px; }}
  h2 {{ color:var(--gold); font-size:1.15rem; margin:32px 0 12px; }}
  .comparacao {{ background:#16283f; border:1px solid rgba(201,162,75,.25); border-radius:10px; padding:16px 20px; margin-bottom:28px; display:flex; gap:24px; flex-wrap:wrap; align-items:center; }}
  .comparacao .bloco {{ flex:1; min-width:130px; }}
  .comparacao .rot {{ font-size:.75rem; color:#9fb0c8; text-transform:uppercase; letter-spacing:.05em; }}
  .comparacao .val {{ font-size:1.5rem; font-weight:700; color:#fff; }}
  .comparacao .val.gold {{ color:var(--gold); }}
  .comparacao .val.verde {{ color:#7fe0a3; }}
  footer {{ text-align:center; color:#7f92ad; font-size:.78rem; margin-top:40px; }}
  .selo-filtro {{ display:inline-block; background:rgba(127,224,163,.12); border:1px solid rgba(127,224,163,.4); color:#7fe0a3; font-size:.72rem; padding:3px 10px; border-radius:20px; margin-left:8px; vertical-align:middle; }}
  .aviso {{ background:rgba(201,162,75,.08); border:1px solid rgba(201,162,75,.35); border-radius:8px; padding:12px 14px; font-size:.85rem; color:#c9d4e3; }}
  code {{ background:#0e1a2e; padding:2px 6px; border-radius:4px; color:#e3c877; font-size:.85rem; }}
  a {{ color:#e3c877; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Estatisticas de Acesso <span class="selo-filtro">v4 leitores reais + conversao + origem</span></h1>
  <p class="sub">Portal O Despertar · missaocomdeus.com.br · gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>

  <div class="comparacao">
    <div class="bloco"><div class="rot">Ontem completo ({ontem})</div><div class="val">{total_ontem}</div></div>
    <div class="bloco"><div class="rot">Hoje até agora ({hoje_str})</div><div class="val gold">{total_hoje}</div></div>
    <div class="bloco"><div class="rot">Ontem até este horário</div><div class="val">{ontem_mesmo_horario}</div></div>
    <div class="bloco"><div class="rot">Variação (justa)</div><div class="val gold">{seta} {variacao:+.1f}%</div></div>
    <div class="bloco"><div class="rot">Projeção do dia</div><div class="val gold">~{projecao}</div></div>
    <div class="bloco"><div class="rot">Total geral</div><div class="val">{total_geral}</div></div>
  </div>

  <div class="comparacao" style="border-color:rgba(127,224,163,.4);">
    <div class="bloco"><div class="rot">Visitantes únicos HOJE</div><div class="val verde">{unicos_hoje}</div></div>
    <div class="bloco"><div class="rot">Visitantes únicos ONTEM</div><div class="val verde">{unicos_ontem}</div></div>
    <div class="bloco"><div class="rot">Visitantes únicos TOTAL</div><div class="val verde">{unicos_total}</div></div>
    <div class="bloco"><div class="rot">Robôs descartados</div><div class="val" style="font-size:1.1rem;">{descartados_robos}</div></div>
    <div class="bloco"><div class="rot">Ataques/erros descartados</div><div class="val" style="font-size:1.1rem;">{descartados_erros}</div></div>
  </div>
  <p style="font-size:.8rem;color:#9fb0c8;margin:-18px 0 24px;">Só entram páginas 200/304 de gente. Visitantes únicos = IPs diferentes no dia.</p>

  {bloco_origem}

  <div class="cards">
    <div class="card destaque"><div class="v">{total_home}</div><div class="l">Visitas à Home</div></div>
    <div class="card destaque"><div class="v">{total_livros}</div><div class="l">Acessos aos livros</div></div>
    <div class="card"><div class="v">{livros_lidos}</div><div class="l">Livros lidos</div></div>
    <div class="card"><div class="v">{contagens.get('/guia-pais-filhos',0)}</div><div class="l">Quiz Pais e Filhos</div></div>
    <div class="card humano"><div class="v">{unicos_total}</div><div class="l">Pessoas (IPs únicos)</div></div>
  </div>

  <h2>CONVERSÃO (o que move a missão)</h2>
  <div class="cards">{''.join(cards_conv)}</div>
  <table>
    <tr><th>Ação</th><th>Total</th><th>Hoje</th></tr>
    {linhas_conv}
  </table>
  <p style="font-size:.8rem;color:#9fb0c8;">Semeador = clique no Kiwify R$ 37. Colaborador = clique no Kiwify R$ 19,90. WhatsApp = rascunho aberto (ainda precisa Enviar). Aula grátis = toques nos vídeos livres (módulos 1 a 3), não um pixel antigo. Taxa = semeadores / pessoas únicas. Página de obrigado ≠ PDF baixado: o brinde é o download de livro11-onovotestamenento.pdf.</p>

  <h2>Downloads (PDFs e Palavra)</h2>
  <table>
    <tr><th>Arquivo</th><th>Total</th><th>Hoje</th></tr>
    {linhas_dl}
  </table>
  <p style="font-size:.8rem;color:#9fb0c8;">Jesus Quer Falar aparece duas vezes porque são dois arquivos: o do quiz (jesus-quer-falar.pdf) e o nome longo do livro. evalma junta o nome antigo com o novo. Quiz permanece sem evalma.</p>

  <h2>Ranking (Home + Livros + Quiz)</h2>
  <table>
    <tr><th>#</th><th>Página</th><th>Acessos (total · hoje)</th><th>%</th><th>Distribuição</th></tr>
    {''.join(linhas)}
  </table>

  <h2>Acessos por dia (últimos 7)</h2>
  <table>
    <tr><th>Dia</th><th>Páginas (humanos)</th><th>Visitantes únicos</th><th>Descartados</th></tr>
    {linhas_dias}
  </table>

  <h2>Outras páginas</h2>
  <table>
    <tr><th>Página</th><th>Acessos</th></tr>
    {linhas_outros}
  </table>

  <footer>Período: {periodo} · Missão com Deus<br>
  Painel v4 (origem dos acessos). noindex. Só para o administrador.</footer>
</div>
</body>
</html>"""
    return html_doc


def main():
    garantir_pixels()
    res, err = analisar()
    if err:
        print('ERRO:', err)
        return
    hoje_str = res[9]
    antigo = analisar_antigo(hoje_str)
    arquivos = lista_logs()
    if len(arquivos) > 1:
        print('lendo %d arquivos de log (atual + rotacionados)' % len(arquivos))
    gravar_leituras(res[0])
    doc = montar_html(res, antigo)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(doc)
    print('stats.html gerado em', OUT)
    if antigo:
        print('log do site antigo lido:', antigo['arquivo'], '->', antigo['total'], 'visitas')
    else:
        print('AVISO: log do site antigo (compraoseu.com) nao encontrado.')
    print('Acesse: https://missaocomdeus.com.br/stats.html')


if __name__ == '__main__':
    main()
