# -*- coding: utf-8 -*-
"""
Painel v4, missaocomdeus.com.br

v3 (leituras + conversao) + ORIGEM:
  "De onde os nossos irmaos estao chegando": SEO (Google/Bing), site antigo
  compraoseu.com (redirecionado), redes, direto, etc.

Como funciona:
  - Le o log do Nginx do site NOVO e classifica o "Referer" (quem indicou).
  - Conta CHEGADAS (entradas): so o primeiro acesso da visita conta.
    Navegacao interna (de um livro para outro) nao conta como origem.
  - Le tambem o log do site ANTIGO (compraoseu.com): cada 301 que o servidor
    respondeu e uma pessoa que vinha do site antigo, e o log guarda de onde
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
    ('/livro01', 'Livro 01: O Verbo que Transforma'),
    ('/livro02', 'Livro 02: A Sabedoria dos Mestres'),
    ('/livro03', 'Livro 03: A Mente Renovada'),
    ('/livro04', 'Livro 04: Um Segundo com Deus'),
    ('/livro05', 'Livro 05: Evolução da Alma'),
    ('/livro06', 'Livro 06: Jesus Quer Falar com Seu Filho'),
    ('/livro07', 'Livro 07: O Caminho do Despertar'),
    ('/livro08', 'Livro 08: O Arquiteto da Realidade'),
    ('/livro09', 'Livro 09: Anestesia Mental'),
    ('/livro10', 'Livro 10: O Despertar do Observador'),
    ('/livro11', 'Livro 11: O Novo Testamento como nunca lido'),
    ('/livro12', 'Livro 12: Afirmações, Declarações e Orações'),
    ('/trilogia-da-alma', 'Trilogia da Alma, área de alunos'),
    ('/anestesia-mental', 'Anestesia Mental, área de alunos'),
    ('/obrigado', 'Página de obrigado (Kiwify)'),
    ('/palavra', 'Caderno Palavra de hoje (casa)'),
    ('/q-quiz-inicio', 'Quiz Home: iniciaram'),
    ('/q-quiz-fim', 'Quiz Home: concluíram'),
    ('/q-trilogia-m01', 'Trilogia, Módulo 01 (plays)'),
    ('/q-trilogia-m02', 'Trilogia, Módulo 02 (plays)'),
    ('/q-trilogia-m03', 'Trilogia, Módulo 03 (plays)'),
    ('/q-trilogia-m04', 'Trilogia, Módulo 04 (plays)'),
    ('/q-trilogia-m05', 'Trilogia, Módulo 05 (plays)'),
    ('/q-trilogia-m06', 'Trilogia, Módulo 06 (plays)'),
    ('/q-trilogia-m07', 'Trilogia, Módulo 07 (plays)'),
    ('/q-anestesia-m01', 'Anestesia, Módulo 01 (plays)'),
    ('/q-anestesia-m02', 'Anestesia, Módulo 02 (plays)'),
    ('/q-anestesia-m03', 'Anestesia, Módulo 03 (plays)'),
    ('/q-anestesia-m04', 'Anestesia, Módulo 04 (plays)'),
    ('/q-anestesia-m05', 'Anestesia, Módulo 05 (plays)'),
    ('/q-anestesia-m06', 'Anestesia, Módulo 06 (plays)'),
    ('/q-anestesia-m07', 'Anestesia, Módulo 07 (plays)'),
    ('/guia-pais-filhos', 'Guia Pais e Filhos (Quiz)'),
])

CONVERSAO = OrderedDict([
    ('/q-semeador', ('🎯', 'Quero Ser Semeador (R$ 37)')),
    ('/q-colaborador', ('🌱', 'Colaborador (R$ 19,90)')),
    ('/q-codigo', ('💬', 'Solicitar Código (WhatsApp)')),
    ('/q-whats', ('📱', 'Cliques no WhatsApp')),
    ('/q-palavra-play', ('🎧', 'Palavra de hoje (play)')),
    ('/q-palavra-share', ('📤', 'Palavra compartilhada')),
])

# Biblioteca depois da limpeza de 02/09/2026 (so o que e autoria da casa).
# Os livros sairam por risco de direito autoral (textos de outros autores).
LIVROS_NO_AR = (
    '/livro11', '/livro05', '/livro09', '/livro04', '/livro06', '/livro07', '/livro12',
)
LIVROS_REMOVIDOS = ('/livro01', '/livro02', '/livro03', '/livro08', '/livro10')

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
    ('desconhecida', ('❓', 'Sem origem (visita já começada antes do log)')),
])

SEO = ('google', 'buscadores')
REDES = ('instagram', 'tiktok', 'youtube', 'whatsapp', 'outros_social')

# Unidade honesta: VISITA (sessao). 30 min sem atividade = nova visita.
# E o mesmo criterio do Google Analytics.
SESSAO_MINUTOS = int(os.environ.get('STATS_SESSAO_MIN', '30'))

# Paginas da casa que NAO sao visita de irmao (painel, caderno, mural).
# Continuam aparecendo no ranking de paginas vistas, mas nao entram em visita/origem.
INTERNAS_EXCLUIR = {'/stats', '/palavra', '/mural'}

# IPs que nao devem entrar em nenhuma conta (ex.: o proprio computador do autor).
# Uso: STATS_IPS_IGNORAR="189.10.20.30,177.5.6.7" no cron.
IPS_IGNORAR = set(x.strip() for x in os.environ.get('STATS_IPS_IGNORAR', '').split(',') if x.strip())

# Enderecos que existiam de verdade no site antigo (usado para separar
# visita de gente x varredura de robo).
PAGINAS_ANTIGAS = set(['/', '/index'])
for _i in range(1, 13):
    PAGINAS_ANTIGAS.add('/livro%02d' % _i)
    PAGINAS_ANTIGAS.add('/livro%02d.html' % _i)
PAGINAS_ANTIGAS |= {
    '/trilogia-da-alma', '/anestesia-mental', '/trilogia', '/anestesia',
    '/obrigado', '/quiz', '/guia-pais-filhos', '/leitor', '/biblioteca',
}

# O que NAO e pagina: ataque, varredura, arquivo solto, endpoint.
# O site antigo responde 301 para tudo, entao o robo tambem "ganha" um 301.
RE_ATAQUE = re.compile(
    r'\.(php|asp|aspx|jsp|cgi|env|git|sql|bak|old|zip|rar|tar|gz|ini|log|'
    r'conf|swp|yml|yaml|xml|json|txt|csv|db|mdb|7z|iso|sh|pl|py|rb)$'
    r'|(wp-|wordpress|xmlrpc|phpmyadmin|pma|administrator|admin|login|logout|'
    r'signin|\.git|\.env|\.aws|\.ssh|shell|cmd\.|actuator|telescope|console|'
    r'vendor|node_modules|\.well-known|boaform|setup\.cgi|hudson|joomla|'
    r'drupal|magento|typo3|solr|jenkins|grafana|kibana|api/|cdn-cgi|'
    r'muieblackcat|aws|dbadmin|mysql|sqladmin|backup|test|dev)', re.I)

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
    ignorados = 0
    robos_por_dia = Counter()
    erros_por_dia = Counter()
    conv = Counter()
    conv_hoje = Counter()
    conv_por_dia = defaultdict(Counter)

    # --- origem (em VISITAS, nao em requisições)
    origens = Counter()
    origens_hoje = Counter()
    origens_ips = defaultdict(set)
    origens_por_dia = defaultdict(Counter)
    visitas_por_dia = Counter()
    refs_dom = Counter()
    entradas = Counter()
    entradas_hoje = Counter()
    entradas_por_origem = defaultdict(Counter)
    ultimo_acesso = {}          # visitante -> ultima vez visto (sessao)
    lista_visitas = []          # uma ficha por visita (sessao)
    vistas_internas = 0         # painel / caderno / mural / endpoints

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

            if IPS_IGNORAR and ip in IPS_IGNORAR:
                ignorados += 1
                continue
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

            # --- VISITAS (sessoes): 30 min sem atividade = nova visita.
            # A origem da visita e a origem do SEU PRIMEIRO acesso.
            if path in INTERNAS_EXCLUIR or path.endswith('.php'):
                vistas_internas += 1
            elif dt is not None:
                chave_vis = ip + '|' + ua[:60]
                nova = True
                if chave_vis in ultimo_acesso:
                    delta = (dt - ultimo_acesso[chave_vis]).total_seconds()
                    nova = (delta > SESSAO_MINUTOS * 60) or (delta < 0)
                if nova:
                    host_ref = host_de(ref)
                    interna = (host_ref in NOSSOS_HOSTS) or (
                        ref.startswith('/') and not host_ref)
                    utm = {}
                    if query:
                        try:
                            utm = {k.lower(): (v[0] if v else '')
                                   for k, v in parse_qs(query, keep_blank_values=False).items()}
                        except Exception:
                            utm = {}
                    if interna:
                        bucket = 'desconhecida'
                    else:
                        bucket = classificar_origem(
                            ref, utm.get('utm_source', ''), utm.get('utm_medium', ''))
                    lista_visitas.append({
                        'ip': ip, 'dia': chave_dia, 'dt': dt, 'origem': bucket,
                        'path': path, 'host': '' if interna else host_ref,
                    })
                ultimo_acesso[chave_vis] = dt

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

    # --- agrega as visitas (uma ficha por visita)
    visitas_hoje = 0
    for v in lista_visitas:
        b = v['origem']
        d = v['dia']
        origens[b] += 1
        origens_ips[b].add(v['ip'])
        if d:
            origens_por_dia[d][b] += 1
            visitas_por_dia[d] += 1
            if d == hoje_str:
                origens_hoje[b] += 1
                visitas_hoje += 1
                entradas_hoje[v['path']] += 1
        if v['host']:
            refs_dom[v['host']] += 1
        entradas[v['path']] += 1
        entradas_por_origem[b][v['path']] += 1

    total_visitas = len(lista_visitas)
    visitas_ontem = visitas_por_dia.get(ontem, 0)

    origem = {
        'origens': origens,
        'origens_hoje': origens_hoje,
        'origens_ips': origens_ips,
        'origens_por_dia': origens_por_dia,
        'total_visitas': total_visitas,
        'visitas_hoje': visitas_hoje,
        'visitas_ontem': visitas_ontem,
        'visitas_por_dia': visitas_por_dia,
        'vistas_internas': vistas_internas,
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
            conv, conv_hoje, conv_por_dia, origem, ignorados), None


def analisar_antigo(hoje_str):
    """Le o log do site antigo (compraoseu.com) com criterio.

    Cuidado que o painel v4 nao teve: o site antigo responde 301 para TUDO.
    Entao cada varredura de robo (/.env, /wp-login.php, /xmlrpc.php...) tambem
    recebe um 301 e, se a gente nao filtrar, entra na conta como se fosse irmao
    chegando. Por isso este bloco tem funil proprio, mostrado no painel:

        requisicoes no log
          - robos conhecidos (user-agent)
          - ataques, varreduras e arquivos que nunca existiram
          - IPs em modo varredura (muitos enderecos diferentes no mesmo dia)
        = requisicoes de gente
          -> agrupadas em VISITAS (sessoes de 30 min)

    O referer de cada visita diz onde a pessoa estava ANTES de cair no
    endereco antigo (Google, direto, Instagram...).
    """
    caminho = None
    for c in [LOG_ANTIGO] + CANDIDATOS_LOG_ANTIGO:
        if c and os.path.exists(c):
            caminho = c
            break
    if not caminho:
        return None

    # ---------------- passe 1: perfil de cada IP por dia
    bruto = 0
    robos = 0
    ataques = 0
    erros = 0
    internas = 0
    linhas_lidas = 0
    ips_ign = 0
    perfil = defaultdict(lambda: {'n': 0, 'paths': set(), 'conhecidos': 0})

    def varrer(f, fase):
        """fase 1 = perfil; fase 2 = sessoes."""
        nonlocal bruto, robos, ataques, erros, internas, linhas_lidas, ips_ign
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
            if fase == 1:
                linhas_lidas += 1
            if RE_EXT.search(url):
                continue

            chave_dia = None
            dt = None
            try:
                dt = datetime.strptime(data.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
                chave_dia = dt.strftime('%d/%m/%Y')
            except Exception:
                pass

            if IPS_IGNORAR and ip in IPS_IGNORAR:
                if fase == 1:
                    ips_ign += 1
                continue
            if ua == '-' or ua == '' or RE_BOT.search(ua):
                if fase == 1:
                    robos += 1
                continue
            if not (status.startswith('3') or status in ('200', '304')):
                if fase == 1:
                    erros += 1
                continue

            path = url.split('?')[0].rstrip('/')
            if path == '':
                path = '/'
            if path.endswith('.html'):
                path = path[:-5]
                if path == '/index':
                    path = '/'
            path_l = path.lower()

            if path.startswith('/.well-known'):
                continue
            # paginas internas da casa: nao e visita de irmao (o autor mesmo)
            if path_l in INTERNAS_EXCLUIR:
                if fase == 1:
                    internas += 1
                continue
            # o que nunca foi pagina da casa: ataque, varredura, endpoint
            if RE_ATAQUE.search(path_l):
                if fase == 1:
                    ataques += 1
                continue

            if fase == 1:
                bruto += 1
                p = perfil[(ip, chave_dia)]
                p['n'] += 1
                p['paths'].add(path_l)
                if path_l in PAGINAS_ANTIGAS:
                    p['conhecidos'] += 1
            else:
                yield ip, chave_dia, dt, path_l, url.split('?', 1)[1] if '?' in url else '', ref, ua

    with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
        for _ in varrer(f, 1):
            pass

    # quem esta claramente varrendo: muitos enderecos diferentes, quase nenhum conhecido
    scanners = set()
    descart_scanner = 0
    for (ip, dia), p in perfil.items():
        if len(p['paths']) >= 8 and p['conhecidos'] <= 2:
            scanners.add((ip, dia))
            descart_scanner += p['n']

    # ---------------- passe 2: sessoes de gente
    pessoas = set()
    ips = set()
    visitas = []
    ultimo = {}
    por_dia = defaultdict(Counter)      # dia -> origem -> visitas
    por_dia_vis = Counter()             # dia -> visitas
    urls = Counter()
    data_inicio = None
    data_fim = None

    with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
        for ip, chave_dia, dt, path_l, query, ref, ua in varrer(f, 2):
            if (ip, chave_dia) in scanners:
                continue
            if dt is None:
                continue
            urls[path_l] += 1
            ips.add(ip)
            if data_inicio is None or dt < data_inicio:
                data_inicio = dt
            if data_fim is None or dt > data_fim:
                data_fim = dt

            chave_vis = ip + '|' + ua[:60]
            nova = True
            if chave_vis in ultimo:
                delta = (dt - ultimo[chave_vis]).total_seconds()
                nova = (delta > SESSAO_MINUTOS * 60) or (delta < 0)
            ultimo[chave_vis] = dt
            if not nova:
                continue

            host_ref = host_de(ref)
            # referer do proprio site antigo = a pessoa ja estava la dentro
            if host_ref in ('compraoseu.com', 'www.compraoseu.com'):
                bucket = 'desconhecida'
            else:
                utm = {}
                if query:
                    try:
                        utm = {k.lower(): (v[0] if v else '')
                               for k, v in parse_qs(query, keep_blank_values=False).items()}
                    except Exception:
                        utm = {}
                bucket = classificar_origem(
                    ref, utm.get('utm_source', ''), utm.get('utm_medium', ''))
            visitas.append({'ip': ip, 'dia': chave_dia, 'origem': bucket, 'path': path_l})
            pessoas.add(ip)
            if chave_dia:
                por_dia[chave_dia][bucket] += 1
                por_dia_vis[chave_dia] += 1

    por_origem = Counter()
    for v in visitas:
        por_origem[v['origem']] += 1

    return {
        'arquivo': caminho,
        'bruto': bruto,
        'linhas_lidas': linhas_lidas,
        'ips_ign': ips_ign,
        'ext': max(0, linhas_lidas - (robos + erros + internas + ataques + bruto + ips_ign)),
        'robos': robos,
        'ataques': ataques,
        'erros': erros,
        'internas': internas,
        'scanners': len(scanners),
        'descart_scanner': descart_scanner,
        'requisicoes_gente': bruto - descart_scanner,
        'visitas': len(visitas),
        'pessoas': len(ips),
        'hoje': por_dia_vis.get(hoje_str, 0),
        'por_dia': por_dia_vis,
        'por_origem': por_origem,
        'por_dia_origem': por_dia,
        'urls': urls,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
    }


def gravar_leituras(contagens):
    livros = {}
    for p in LIVROS_NO_AR:
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


# ============================================================== PAINEL v6
# Termometro (02/09/2026)
#
# Regra de honradez, escrita aqui para nao se perder:
#   · cada bloco declara a sua BASE e o seu PERIODO;
#   · percentual so existe dentro de um mesmo bloco (soma 100%);
#   · medicoes diferentes NAO se somam nem se comparam;
#   · VISITA = sessao (30 min parado = nova visita), nao requisicao;
#   · robo, varredura, ataque, erro e pagina interna da casa nao sao visita;
#     e o descarte e mostrado no funil, nao escondido.


def _card_term(v, rotulo, rodape, extra=''):
    return (f'<div class="card {extra}"><div class="v">{v}</div>'
            f'<div class="l">{rotulo}</div>'
            f'<div class="h">{rodape}</div></div>')


def bloco_termometro_html(res, livros_total, livros_hoje, pdfs, pdfs_hoje,
                          sementes, sementes_hoje):
    """Os 6 numeros que o irmao deve olhar sempre."""
    (contagens, total_geral, data_inicio, data_fim, por_dia,
     contagens_hoje, total_hoje, total_ontem, variacao, hoje_str, ontem,
     ontem_mesmo_horario, projecao,
     unicos_hoje, unicos_ontem, unicos_total, visitantes_por_dia,
     descartados_robos, descartados_erros, robos_por_dia, erros_por_dia,
     conv, conv_hoje, conv_por_dia, origem, ignorados) = res

    visitas = origem['total_visitas']
    visitas_hoje = origem['visitas_hoje']
    visitas_ontem = origem['visitas_ontem']
    ppv = (total_geral / visitas) if visitas else 0.0

    cards = []
    cards.append(_card_term(
        f'{unicos_total}', '👥 Pessoas alcançadas',
        f'{unicos_hoje} hoje · IPs distintos', 'humano destaque'))
    cards.append(_card_term(
        f'{visitas}', '🚪 Visitas',
        f'{visitas_hoje} hoje · {visitas_ontem} ontem', 'destaque'))
    cards.append(_card_term(
        f'{ppv:.1f}', '📊 Páginas por visita',
        'acima de 3 = casa viva', 'humano destaque'))
    cards.append(_card_term(
        f'{livros_total}', '📖 Leituras (páginas de livro)',
        f'{livros_hoje} hoje', ''))
    cards.append(_card_term(
        f'{pdfs}', '⬇️ PDFs baixados',
        f'{pdfs_hoje} hoje', ''))
    cards.append(_card_term(
        f'{sementes}', '🎯 Sustento (Semeador + Colaborador)',
        f'{sementes_hoje} hoje', 'conv'))
    return ''.join(cards)


def bloco_origem_html(origem, antigo, periodo_txt, ignorados=0):
    """Versao enxuta: uma leitura de uma linha + UMA tabela, base unica."""
    origens = origem['origens']
    origens_hoje = origem['origens_hoje']
    origens_ips = origem['origens_ips']
    total = origem['total_visitas']
    base = total or 1

    def n(b):
        return int(origens.get(b, 0))

    def pessoas(b):
        return len(origens_ips.get(b, set()))

    def hoje_n(b):
        return int(origens_hoje.get(b, 0))

    n_seo = sum(n(b) for b in SEO)
    n_redes = sum(n(b) for b in REDES)

    linhas = []
    for b, (emoji, nome) in ORIGENS.items():
        v = n(b)
        if v == 0 and b in ('whatsapp', 'email', 'outros_social', 'desconhecida'):
            continue
        pct = v / base * 100
        hoje_txt = f' <span class="hj">+{hoje_n(b)} hoje</span>' if hoje_n(b) else ''
        marca = ' class="seo"' if b in SEO else ''
        linhas.append(
            f'<tr{marca}><td>{emoji} {html.escape(nome)}</td>'
            f'<td class="num">{v}{hoje_txt}</td>'
            f'<td class="num">{pessoas(b)}</td>'
            f'<td class="num">{pct:.1f}%</td>'
            f'<td><div class="barra"><div class="fill" style="width:{min(100, pct):.1f}%"></div></div></td></tr>')

    pct = lambda v: (v / base * 100) if total else 0.0

    return f"""
  <h2>De onde vêm <span class="selo-filtro">base: {total} visitas do site novo</span></h2>

  <p class="leitura">
    Das <b>{total}</b> visitas de <b>{periodo_txt}</b>:
    <b>{pct(n_seo):.0f}% pela busca (SEO)</b>,
    <b>{pct(n('antigo')):.0f}% com o endereço antigo declarado</b>,
    <b>{pct(n('direto')):.0f}% direto</b> e {pct(n_redes):.0f}% pelas redes{(' , e ' + format(pct(n('desconhecida')), '.0f') + '% começou antes de o log existir') if n('desconhecida') else ''}.
  </p>

  <table>
    <tr><th>Origem da visita</th><th>Visitas</th><th>Pessoas</th><th>%</th><th>Distribuição</th></tr>
    {''.join(linhas) or '<tr><td colspan="5">Sem dados</td></tr>'}
  </table>

  <p class="nota">
    «Site antigo» é quando o navegador avisa que a pessoa veio do compraoseu.com.
    «Direto» é quando ele <b>não avisa nada</b>: endereço digitado, favorito,
    link colado em aplicativo, <b>inclusive WhatsApp, Instagram e TikTok</b>,
    que abrem o link sem dizer de onde veio. Cada visita tem uma única origem,
    então as linhas somam 100%.
  </p>
"""


def bloco_antigo_html(antigo):
    """Medicao separada do endereco antigo. Base e periodo proprios."""
    if not antigo:
        return """
  <h3 style="color:#e3c877;font-size:1rem;margin:20px 0 8px;">🏠 Endereço antigo (compraoseu.com)</h3>
  <p class="nota">Não achei o log do endereço antigo neste servidor. Se o compraoseu.com
  estiver em <b>outra</b> máquina, copie o arquivo de log dele para
  <code>/www/wwwlogs/compraoseu.com.log</code> (ou ajuste
  <code>STATS_LOG_ANTIGO</code>) que esta tabela aparece sozinha.</p>
"""
    per = 'sem data'
    if antigo['data_inicio'] and antigo['data_fim']:
        per = (f"{antigo['data_inicio'].strftime('%d/%m/%Y')} a "
               f"{antigo['data_fim'].strftime('%d/%m/%Y')}")
    lo = antigo['por_origem']
    base_a = antigo['visitas'] or 1
    linhas_antigo = []
    for b, (emoji, nome) in ORIGENS.items():
        v = int(lo.get(b, 0))
        if v == 0:
            continue
        linhas_antigo.append(
            f'<tr><td>{emoji} {html.escape(nome)}</td>'
            f'<td class="num">{v}</td>'
            f'<td class="num">{v / base_a * 100:.1f}%</td></tr>')
    top_urls = ' · '.join(
        f'{html.escape(u)} ({c})' for u, c in antigo['urls'].most_common(6)) or 'nenhum'
    dias_a = sorted(antigo['por_dia'].keys(), key=chave_data, reverse=True)[:7]
    linhas_dias_a = '\n'.join(
        f'<tr><td>{d}</td><td class="num">{antigo["por_dia"].get(d, 0)}</td></tr>'
        for d in dias_a) or '<tr><td colspan="2">Sem dados</td></tr>'

    return f"""
  <p class="aviso" style="margin:0 0 14px;">
    <b>Período deste bloco: {per}.</b> Log próprio, base própria.
    <b>Não somar e não misturar</b> com os números de cima. São duas medições diferentes.
    O site antigo responde 301 para qualquer endereço, então robôs de varredura também
    recebiam 301. Por isso o funil abaixo existe e é mostrado inteiro.
  </p>
  <table>
    <tr><th>Funil do log do compraoseu.com (de cima para baixo)</th><th>Quantidade</th></tr>
    <tr><td><b>Linhas lidas no log</b></td><td class="num"><b>{antigo['linhas_lidas']}</b></td></tr>
    <tr><td>&nbsp;&nbsp;− imagens, CSS, JS e fontes (não são visita)</td><td class="num">{antigo['ext']}</td></tr>
    <tr><td>&nbsp;&nbsp;− robôs conhecidos (user-agent)</td><td class="num">{antigo['robos']}</td></tr>
    <tr><td>&nbsp;&nbsp;− erros fora de 200/301/304</td><td class="num">{antigo['erros']}</td></tr>
    <tr><td>&nbsp;&nbsp;− páginas internas da casa (/stats, /palavra, /mural)</td><td class="num">{antigo['internas']}</td></tr>
    <tr><td>&nbsp;&nbsp;− ataques e varreduras (arquivos que nunca existiram)</td><td class="num">{antigo['ataques']}</td></tr>
    {('<tr><td>&nbsp;&nbsp;− IPs ignorados (o senhor mesmo)</td><td class="num">' + str(antigo['ips_ign']) + '</td></tr>') if antigo.get('ips_ign') else ''}
    <tr style="background:rgba(201,162,75,.08)"><td><b>= requisições que sobraram</b></td><td class="num"><b>{antigo['bruto']}</b></td></tr>
    <tr><td>&nbsp;&nbsp;− IPs em modo varredura (muitos endereços diferentes, quase nenhum conhecido)</td><td class="num">{antigo['descart_scanner']}</td></tr>
    <tr style="background:rgba(201,162,75,.08)"><td><b>= requisições de gente</b></td><td class="num"><b>{antigo['requisicoes_gente']}</b></td></tr>
    <tr style="background:rgba(127,224,163,.10)"><td><b>= visitas</b> (sessões de {SESSAO_MINUTOS} min)</td><td class="num"><b>{antigo['visitas']}</b></td></tr>
    <tr><td><b>= pessoas</b> (IPs distintos no período)</td><td class="num"><b>{antigo['pessoas']}</b></td></tr>
  </table>

  <h3 style="color:#e3c877;font-size:.95rem;margin:20px 0 8px;">Dessas visitas, onde a pessoa estava antes:</h3>
  <table>
    <tr><th>Origem (medição própria do site antigo)</th><th>Visitas</th><th>% deste bloco</th></tr>
    {''.join(linhas_antigo) or '<tr><td colspan="3">Sem dados</td></tr>'}
  </table>

  <p class="nota">Endereços mais pedidos no site antigo: {top_urls}</p>

  <table>
    <tr><th>Dia (medição do site antigo)</th><th>Visitas</th></tr>
    {linhas_dias_a}
  </table>
"""


def montar_html(res, antigo):
    (contagens, total_geral, data_inicio, data_fim, por_dia,
     contagens_hoje, total_hoje, total_ontem, variacao, hoje_str, ontem,
     ontem_mesmo_horario, projecao,
     unicos_hoje, unicos_ontem, unicos_total, visitantes_por_dia,
     descartados_robos, descartados_erros, robos_por_dia, erros_por_dia,
     conv, conv_hoje, conv_por_dia, origem, ignorados) = res

    seta = '📈' if variacao > 0 else ('📉' if variacao < 0 else '➖')

    # ---------------------------------------------------------- periodo
    periodo = 'sem registro'
    if data_inicio and data_fim:
        periodo = (f'{data_inicio.strftime("%d/%m/%Y %H:%M")} até '
                   f'{data_fim.strftime("%d/%m/%Y %H:%M")}')

    # ---------------------------------------------------------- termometro
    livros_total = sum(contagens.get(p, 0) for p in LIVROS_NO_AR)
    livros_hoje = sum(contagens_hoje.get(p, 0) for p in LIVROS_NO_AR)
    pdfs = sum(contagens.get(k, 0) for k in DL_NOMES if k.startswith('/dl:'))
    pdfs_hoje = sum(contagens_hoje.get(k, 0) for k in DL_NOMES if k.startswith('/dl:'))
    sementes = conv.get('/q-semeador', 0) + conv.get('/q-colaborador', 0)
    sementes_hoje = conv_hoje.get('/q-semeador', 0) + conv_hoje.get('/q-colaborador', 0)
    palavra = conv.get('/q-palavra-play', 0)
    palavra_hoje = conv_hoje.get('/q-palavra-play', 0)
    cards_termo = bloco_termometro_html(res, livros_total, livros_hoje,
                                        pdfs, pdfs_hoje, sementes, sementes_hoje)

    # ---------------------------------------------------------- ranking
    itens = [(p, n, contagens.get(p, 0), contagens_hoje.get(p, 0))
             for p, n in PAGINAS.items() if p not in LIVROS_REMOVIDOS]
    itens_ordenados = sorted(itens, key=lambda x: -x[2])
    linhas = []
    for i, (path, nome, n, n_hoje) in enumerate(itens_ordenados, 1):
        pct = (n / total_geral * 100) if total_geral else 0
        medalha = {1: '🥇', 2: '🥈', 3: '🥉'}.get(i, '')
        hoje_txt = f' <span class="hj">+{n_hoje}</span>' if n_hoje else ''
        linhas.append(
            f'<tr><td class="num">{medalha} {i}</td>'
            f'<td><a href="https://missaocomdeus.com.br{path}">{html.escape(nome)}</a>'
            f'<br><span class="url">{path}</span></td>'
            f'<td class="num">{n}{hoje_txt}</td>'
            f'<td class="num">{pct:.1f}%</td></tr>')

    hist_removidos = ' · '.join(
        '%s %d' % (html.escape(PAGINAS.get(p, p)), int(contagens.get(p, 0)))
        for p in LIVROS_REMOVIDOS if int(contagens.get(p, 0)) > 0)

    # ---------------------------------------------------------- por dia
    dias = sorted(por_dia.keys(), key=chave_data, reverse=True)[:7]
    linhas_dias = '\n'.join(
        f'<tr><td>{d}</td><td class="num">{por_dia.get(d, 0)}</td>'
        f'<td class="num" style="color:#7fe0a3">{len(visitantes_por_dia.get(d, set()))}</td>'
        f'<td class="num" style="color:#9fb0c8">{robos_por_dia.get(d, 0) + erros_por_dia.get(d, 0)}</td></tr>'
        for d in dias) or '<tr><td colspan="4">Sem dados diários</td></tr>'

    dias_o = sorted(origem['visitas_por_dia'].keys(), key=chave_data, reverse=True)[:7]
    linhas_dias_o = '\n'.join(
        '<tr><td>%s</td><td class="num">%d</td><td class="num">%d</td>'
        '<td class="num">%d</td><td class="num">%d</td><td class="num">%d</td></tr>' % (
            d,
            sum(int(origem['origens_por_dia'].get(d, Counter()).get(b, 0)) for b in SEO),
            int(origem['origens_por_dia'].get(d, Counter()).get('antigo', 0)),
            int(origem['origens_por_dia'].get(d, Counter()).get('direto', 0)),
            sum(int(origem['origens_por_dia'].get(d, Counter()).get(b, 0)) for b in REDES),
            origem['visitas_por_dia'].get(d, 0))
        for d in dias_o) or '<tr><td colspan="6">Sem dados</td></tr>'

    # ---------------------------------------------------------- entradas
    def nome_pagina(p):
        return PAGINAS.get(p, p)

    linhas_entradas = ''.join(
        f'<tr><td>{html.escape(nome_pagina(p))} <span class="url">{html.escape(p)}</span></td>'
        f'<td class="num">{c}</td>'
        f'<td class="num" style="color:#7fe0a3">{origem["entradas_hoje"].get(p, 0)}</td></tr>'
        for p, c in origem['entradas'].most_common(12) if p not in LIVROS_REMOVIDOS
    ) or '<tr><td colspan="3">Sem dados</td></tr>'

    linhas_entradas_seo = ''.join(
        f'<tr><td>{html.escape(nome_pagina(p))} <span class="url">{html.escape(p)}</span></td>'
        f'<td class="num">{c}</td></tr>'
        for p, c in origem['entradas_por_origem'].get('google', Counter()).most_common(8)
        if p not in LIVROS_REMOVIDOS
    ) or '<tr><td colspan="2">Ainda sem visitas com origem no Google neste log</td></tr>'

    linhas_refs = ''.join(
        f'<tr><td>{html.escape(d)}</td><td class="num">{c}</td></tr>'
        for d, c in origem['refs_dom'].most_common(12)
    ) or '<tr><td colspan="2">Nenhum registrado</td></tr>'

    # ---------------------------------------------------------- conversao
    n_sem = conv.get('/q-semeador', 0)
    n_col = conv.get('/q-colaborador', 0)
    aula_gratis = sum(contagens.get(p, 0) for p in MODULOS_LIVRES)
    aula_hoje = sum(contagens_hoje.get(p, 0) for p in MODULOS_LIVRES)
    brinde_nt = contagens.get('/dl:brinde-nt', 0)
    taxa = (sementes / unicos_total * 100) if unicos_total else 0

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
        f'<div class="card conv"><div class="v">{aula_gratis}</div>'
        f'<div class="l">🎬 Aulas grátis (módulos livres)</div>'
        f'<div class="h">{aula_hoje} hoje</div></div>')
    cards_conv.append(
        f'<div class="card conv"><div class="v">{brinde_nt}</div>'
        f'<div class="l">🎁 Brinde do NT baixado</div>'
        f'<div class="h">obrigado {contagens.get("/obrigado", 0)}</div></div>')
    cards_conv.append(
        f'<div class="card conv"><div class="v">{palavra}</div>'
        f'<div class="l">🎧 Palavra de hoje (plays)</div>'
        f'<div class="h">{palavra_hoje} hoje · {conv.get("/q-palavra-share", 0)} compart.</div></div>')
    cards_conv.append(
        f'<div class="card conv destaque"><div class="v">{taxa:.1f}%</div>'
        f'<div class="l">📈 Sustento / pessoas</div>'
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
        for k, nome in DL_NOMES.items())

    outros = sorted([(k, v) for k, v in contagens.items() if k.startswith('/outros:')],
                    key=lambda x: -x[1])
    linhas_outros = '\n'.join(
        f'<tr><td>{html.escape(k.replace("/outros:", "/"))}</td><td class="num">{v}</td></tr>'
        for k, v in outros[:15]) or '<tr><td colspan="2">Nenhum</td></tr>'

    bloco_origem = bloco_origem_html(origem, antigo, periodo, ignorados)

    # ============================================================== HTML
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Termômetro da Missão · missaocomdeus.com.br</title>
<style>
  :root {{ --navy:#0e1a2e; --gold:#c9a24b; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:'Segoe UI',system-ui,sans-serif; background:var(--navy); color:#e8ecf3; line-height:1.5; }}
  .wrap {{ max-width:960px; margin:0 auto; padding:24px 16px 60px; }}
  h1 {{ color:var(--gold); font-size:1.6rem; margin-bottom:4px; }}
  .sub {{ color:#9fb0c8; font-size:.88rem; margin-bottom:20px; }}
  .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(155px,1fr)); gap:12px; margin-bottom:14px; }}
  .card {{ background:#16283f; border:1px solid rgba(201,162,75,.25); border-radius:10px; padding:16px; text-align:center; }}
  .card .v {{ font-size:1.7rem; font-weight:700; color:var(--gold); }}
  .card .l {{ font-size:.73rem; color:#9fb0c8; text-transform:uppercase; letter-spacing:.05em; margin-top:6px; }}
  .card .h {{ font-size:.72rem; color:#7fe0a3; margin-top:4px; }}
  .card.destaque {{ border-color:var(--gold); background:linear-gradient(180deg,#1a2c47,#16283f); }}
  .card.humano .v {{ color:#7fe0a3; }}
  .card.conv {{ border-color:rgba(127,224,163,.35); }}
  .card.conv .v {{ color:#7fe0a3; }}
  h2 {{ color:var(--gold); font-size:1.15rem; margin:28px 0 10px; }}
  .selo-filtro {{ display:inline-block; background:rgba(127,224,163,.12); border:1px solid rgba(127,224,163,.4); color:#7fe0a3; font-size:.72rem; padding:3px 10px; border-radius:20px; margin-left:8px; vertical-align:middle; }}
  .leitura {{ background:#16283f; border-left:3px solid var(--gold); border-radius:8px; padding:12px 16px; font-size:.95rem; margin:0 0 14px; }}
  .nota {{ font-size:.8rem; color:#9fb0c8; }}
  .aviso {{ background:rgba(201,162,75,.08); border:1px solid rgba(201,162,75,.35); border-radius:8px; padding:12px 14px; font-size:.85rem; color:#c9d4e3; }}
  table {{ width:100%; border-collapse:collapse; background:#16283f; border-radius:10px; overflow:hidden; }}
  th {{ background:rgba(201,162,75,.15); color:var(--gold); text-align:left; padding:10px 12px; font-size:.78rem; text-transform:uppercase; letter-spacing:.05em; }}
  td {{ padding:9px 12px; border-top:1px solid rgba(201,162,75,.15); font-size:.9rem; vertical-align:middle; }}
  .num {{ text-align:center; white-space:nowrap; }}
  .hj {{ color:#7fe0a3; font-size:.75rem; }}
  .url {{ color:#7f92ad; font-size:.75rem; }}
  .barra {{ background:#0e1a2e; border-radius:6px; height:12px; overflow:hidden; min-width:100px; }}
  .fill {{ background:linear-gradient(90deg,#c9a24b,#e3c877); height:100%; border-radius:6px; }}
  tr.seo td {{ background:rgba(201,162,75,.08); }}
  .hoje {{ display:flex; gap:14px; flex-wrap:wrap; background:#16283f; border:1px solid rgba(201,162,75,.25); border-radius:10px; padding:14px 18px; margin-bottom:8px; }}
  .hoje .bloco {{ flex:1; min-width:110px; }}
  .hoje .rot {{ font-size:.72rem; color:#9fb0c8; text-transform:uppercase; letter-spacing:.05em; }}
  .hoje .val {{ font-size:1.4rem; font-weight:700; color:#fff; }}
  .hoje .val.gold {{ color:var(--gold); }}
  details {{ background:#16283f; border:1px solid rgba(201,162,75,.25); border-radius:10px; margin-bottom:10px; }}
  summary {{ cursor:pointer; padding:13px 16px; color:var(--gold); font-weight:600; font-size:.95rem; list-style:none; }}
  summary::-webkit-details-marker {{ display:none; }}
  summary::before {{ content:'\\25B8  '; }}
  details[open] summary::before {{ content:'\\25BE  '; }}
  .dbody {{ padding:0 16px 16px; }}
  .dbody table {{ margin-bottom:12px; }}
  code {{ background:#0e1a2e; padding:2px 6px; border-radius:4px; color:#e3c877; font-size:.85rem; }}
  a {{ color:#e3c877; }}
  footer {{ text-align:center; color:#7f92ad; font-size:.78rem; margin-top:32px; }}
</style>
</head>
<body>
<div class="wrap">

  <h1>🌡️ Termômetro da Missão <span class="selo-filtro">v6 · medição honesta</span></h1>
  <p class="sub">missaocomdeus.com.br · período <b>{periodo}</b> · gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>

  <h2>O que olhar sempre</h2>
  <div class="cards">{cards_termo}</div>

  <table>
    <tr><th>Indicador</th><th>O que é</th><th>O que observar</th></tr>
    <tr><td>👥 Pessoas alcançadas</td><td>IPs distintos que abriram a casa no período</td>
        <td>É o tamanho da nossa roda. Deve crescer semana a semana. Aproximação: IP de celular é compartilhado e muda ao longo do dia.</td></tr>
    <tr><td>🚪 Visitas</td><td>Cada vez que alguém chega. {SESSAO_MINUTOS} minutos parado = nova visita</td>
        <td>Compare <b>hoje</b> com <b>ontem no mesmo horário</b>. Comparar dia cheio com dia pela metade engana.</td></tr>
    <tr><td>📊 Páginas por visita</td><td>Quantas páginas a pessoa abre antes de ir embora</td>
        <td>Entre 2 e 3 é comum na internet. <b>Acima de 3 é sinal de casa viva</b>: a pessoa está lendo, não só passando.</td></tr>
    <tr><td>📖 Leituras</td><td>Páginas de livro abertas (só os 7 que ficaram)</td>
        <td>É o coração da casa. Se cai enquanto as visitas sobem, a pessoa entra e não lê.</td></tr>
    <tr><td>⬇️ PDFs baixados</td><td>Arquivos que saíram da casa</td>
        <td>Semente que a pessoa leva consigo e pode repassar.</td></tr>
    <tr><td>🎯 Sustento</td><td>Cliques em Semeador e Colaborador</td>
        <td>O que mantém a missão de pé. Clique não é compra: a venda acontece na Kiwify.</td></tr>
  </table>

  <h2>Hoje e ontem</h2>
  <div class="hoje">
    <div class="bloco"><div class="rot">Ontem completo</div><div class="val">{total_ontem}</div></div>
    <div class="bloco"><div class="rot">Hoje até agora</div><div class="val gold">{total_hoje}</div></div>
    <div class="bloco"><div class="rot">Ontem até esta hora</div><div class="val">{ontem_mesmo_horario}</div></div>
    <div class="bloco"><div class="rot">Variação (justa)</div><div class="val gold">{seta} {variacao:+.1f}%</div></div>
    <div class="bloco"><div class="rot">Projeção do dia</div><div class="val gold">~{projecao}</div></div>
  </div>
  <p class="nota" style="margin:0 0 6px;">Páginas vistas por gente. Pessoas únicas: <b>{unicos_hoje}</b> hoje · <b>{unicos_ontem}</b> ontem.</p>

  {bloco_origem}

  <h2>Detalhes <span class="selo-filtro">abre o que quiser</span></h2>

  <details>
    <summary>🏠 Endereço antigo compraoseu.com (medição separada, não somar)</summary>
    <div class="dbody">{bloco_antigo_html(antigo)}</div>
  </details>

  <details>
    <summary>📍 Por qual página eles entram · 🔎 o que o Google entrega · 🔗 quem nos indica</summary>
    <div class="dbody">
      <h3 style="color:#e3c877;font-size:.95rem;margin:4px 0 8px;">Página de entrada</h3>
      <table>
        <tr><th>Página de entrada</th><th>Visitas</th><th>Hoje</th></tr>
        {linhas_entradas}
      </table>
      <h3 style="color:#e3c877;font-size:.95rem;margin:18px 0 8px;">Páginas que o Google mais entrega</h3>
      <table>
        <tr><th>Página (visita com origem no Google)</th><th>Visitas</th></tr>
        {linhas_entradas_seo}
      </table>
      <h3 style="color:#e3c877;font-size:.95rem;margin:18px 0 8px;">Domínios que nos indicam</h3>
      <table>
        <tr><th>Domínio de onde a pessoa veio</th><th>Visitas</th></tr>
        {linhas_refs}
      </table>
    </div>
  </details>

  <details>
    <summary>📖 Ranking das páginas</summary>
    <div class="dbody">
      <table>
        <tr><th>#</th><th>Página</th><th>Acessos</th><th>%</th></tr>
        {''.join(linhas)}
      </table>
      {'<p class="nota">🚫 Fora do ar desde 02/09/2026 (histórico, não contam nos totais): ' + hist_removidos + '. Saíram por não serem de autoria da casa.</p>' if hist_removidos else ''}
      <h3 style="color:#e3c877;font-size:.95rem;margin:18px 0 8px;">Outras páginas</h3>
      <table>
        <tr><th>Página</th><th>Acessos</th></tr>
        {linhas_outros}
      </table>
    </div>
  </details>

  <details>
    <summary>🎯 Conversão (o que move a missão)</summary>
    <div class="dbody">
      <div class="cards">{''.join(cards_conv)}</div>
      <table>
        <tr><th>Ação</th><th>Total</th><th>Hoje</th></tr>
        {linhas_conv}
      </table>
      <p class="nota">Semeador e Colaborador = clique no link da Kiwify (a compra acontece lá fora).
      WhatsApp = rascunho aberto, ainda precisa a pessoa Enviar. Aulas grátis = toques nos
      módulos livres 1 a 3. Página de obrigado ≠ download: o brinde é o arquivo
      livro11-onovotestamenento.pdf.</p>
    </div>
  </details>

  <details>
    <summary>⬇️ Downloads detalhados</summary>
    <div class="dbody">
      <table>
        <tr><th>Arquivo</th><th>Total</th><th>Hoje</th></tr>
        {linhas_dl}
      </table>
      <p class="nota">«evalma» junta o nome antigo com o novo. Jesus Quer Falar aparece duas vezes
      porque são dois arquivos diferentes. «PDF com nome chutado» é quando alguém digita o
      endereço do arquivo direto, sem passar pela página.</p>
    </div>
  </details>

  <details>
    <summary>📅 Por dia (últimos 7)</summary>
    <div class="dbody">
      <table>
        <tr><th>Dia</th><th>Páginas (gente)</th><th>Pessoas</th><th>Descartados</th></tr>
        {linhas_dias}
      </table>
      <h3 style="color:#e3c877;font-size:.95rem;margin:18px 0 8px;">Visitas por dia e origem</h3>
      <table>
        <tr><th>Dia</th><th>SEO</th><th>Site antigo</th><th>Direto</th><th>Redes</th><th>Visitas</th></tr>
        {linhas_dias_o}
      </table>
    </div>
  </details>

  <details>
    <summary>🧹 O funil: o que NÃO entra na conta (e por quê)</summary>
    <div class="dbody">
      <table>
        <tr><th>Etapa</th><th>Quantidade</th></tr>
        <tr><td>Robôs conhecidos descartados</td><td class="num">{descartados_robos}</td></tr>
        <tr><td>Ataques, varreduras e erros descartados</td><td class="num">{descartados_erros}</td></tr>
        <tr><td>Páginas internas da casa (/stats, /palavra, /mural) fora da conta</td><td class="num">{origem['vistas_internas']}</td></tr>
        <tr style="background:rgba(201,162,75,.08)"><td><b>= páginas vistas por gente</b></td><td class="num"><b>{total_geral}</b></td></tr>
        <tr style="background:rgba(127,224,163,.10)"><td><b>= visitas</b> (sessões de {SESSAO_MINUTOS} min)</td><td class="num"><b>{origem['total_visitas']}</b></td></tr>
        <tr><td><b>= pessoas</b> (IPs distintos no período)</td><td class="num"><b>{unicos_total}</b></td></tr>
        {('<tr><td>Acessos descontados por IP ignorado (o senhor mesmo)</td><td class="num">' + str(ignorados) + '</td></tr>') if ignorados else ''}
      </table>
      <p class="nota" style="margin-top:12px;">
        <b>Regras desta medição:</b><br>
        · <b>Visita</b> = sessão: {SESSAO_MINUTOS} minutos sem atividade conta como nova visita
          (mesmo critério do Google Analytics). Navegar de um livro para outro é a <i>mesma</i> visita.<br>
        · <b>Origem da visita</b> = origem do primeiro acesso dela. Uma visita tem uma única origem.<br>
        · <b>Não entram:</b> robôs, varreduras, ataques, erros, e as páginas internas da casa,
          que não são visita de irmão.<br>
        · <b>Limite honesto:</b> WhatsApp, Instagram e TikTok abrem o link sem avisar de onde veio,
          então essa pessoa cai em «Direto». Por isso existe a marcação <code>utm_source</code>.<br>
        · <b>Cada bloco tem período e base próprios. Percentual só dentro do mesmo bloco.</b>
      </p>
    </div>
  </details>

  <footer>Período: {periodo} · Missão com Deus<br>
  Painel v6 (termômetro). noindex. Só para o administrador.</footer>
</div>
</body>
</html>"""



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
        print('log do site antigo lido:', antigo['arquivo'])
        print('  funil: %d requisicoes -> %d de gente -> %d visitas (%d IPs). Descartados: %d robos, %d ataques, %d varredura, %d paginas internas.'
              % (antigo['bruto'], antigo['requisicoes_gente'], antigo['visitas'],
                 antigo['pessoas'], antigo['robos'], antigo['ataques'], antigo['descart_scanner'], antigo['internas']))
    else:
        print('AVISO: log do site antigo (compraoseu.com) nao encontrado.')
    print('Acesse: https://missaocomdeus.com.br/stats.html')


if __name__ == '__main__':
    main()
