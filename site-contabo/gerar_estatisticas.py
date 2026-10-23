# -*- coding: utf-8 -*-
"""
Painel V8, missaocomdeus.com.br

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

Analise de logs e leitura da base geografica local do navegador. Sem chamadas externas nesta geracao.

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
import time
import unicodedata
import urllib.request
import urllib.error
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

# --- GEO: Estados e Cidades (futuras campanhas patrocinadas) ------------------
# Fonte publica gratis da ip-api.com (batch ate ~100 IPs por chamada).
# O cache evita consultar o mesmo IP de novo a cada geracao.
GEO_CACHE = os.environ.get('GEO_CACHE', '/home/deploy/geo_cache.json')
GEO_VISITAS = os.environ.get('GEO_VISITAS', '/www/wwwroot/missaocomdeus.com.br/geo_visitas.json')
GEO_VISITAS_ALT1 = os.environ.get('GEO_VISITAS_ALT1', '/home/deploy/geo_visitas.json')
GEO_VISITAS_ALT2 = os.environ.get('GEO_VISITAS_ALT2', '')
GEO_API = os.environ.get(
    'GEO_API',
    'http://ip-api.com/batch?fields=status,countryCode,regionName,city&lang=pt-BR')
GEO_MAX_IP = int(os.environ.get('GEO_MAX_IP', '600'))
GEO_MAX_POR_LOTE = 100


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
    ('/livro08', 'Livro 08: Pais e Filhos: Construindo um Futuro'),
    ('/livro08-arquiteto', 'Livro 08: O Arquiteto da Realidade'),
    ('/livro09', 'Livro 09: Anestesia Mental'),
    ('/livro10', 'Livro 10: O Despertar do Observador'),
    ('/livro11', 'Livro 11: O Novo Testamento como nunca lido'),
    ('/livro12', 'Livro 12: Afirmações, Declarações e Orações'),
    ('/trilogia-da-alma', 'Trilogia da Alma, área de alunos'),
    ('/anestesia-mental', 'Anestesia Mental, área de alunos'),
    ('/obrigado', 'Página de obrigado (Kiwify)'),
    ('/palavra', 'Palavra de hoje'),
    ('/q-quiz-inicio', 'Termômetro anterior: inícios (histórico)'),
    ('/q-quiz-fim', 'Termômetro anterior: finais (histórico)'),
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
    ('/biblica', 'Motivação Bíblica'),
    ('/salmos', 'Salmos'),
    ('/guia-pais-filhos', 'Guia Pais e Filhos \u2014 Quiz'),
    ('/guardar', 'Acesso completo'),
    ('/guia-pais-filhos-espelho', 'Filhos e Pais: O Espelho'),
    ('/nossa-missao', 'Nossa Missão'),
    ('/q-guardar', 'Acesso: abriram a página'),
    ('/q-guardar-kiwify', 'Acesso: foram à Kiwify'),
])

CONVERSAO = OrderedDict([
    ('/q-termo-v2-inicio', ('🌱', 'Termômetro V2: inícios (eventos)')),
    ('/q-termo-v2-fim', ('🌿', 'Termômetro V2: resultados exibidos (eventos)')),
    ('/q-semeador', ('🎯', 'Acesso completo R$ 57')),
    ('/q-codigo', ('💬', 'Fale com a Laura (área de alunos)')),
    ('/q-laura', ('🕊️', 'Falar com a Laura (banner da Home)')),
    ('/q-whats', ('📱', 'Cliques no WhatsApp')),
    ('/q-palavra-play', ('🎧', 'Palavra de hoje (play)')),
    ('/q-palavra-share', ('📤', 'Palavra compartilhada')),
    ('/q-livro-share', ('📖', 'Livros compartilhados')),
])

# Acoes que sairam do ar. Nao contam mais no painel.
CONVERSAO_REMOVIDA = ('/q-colaborador', '/q-aula-gratis')

# Biblioteca depois da limpeza de 02/09/2026 (so o que e autoria da casa).
# Os livros sairam por risco de direito autoral (textos de outros autores).
LIVROS_NO_AR = (
    '/livro11', '/livro05', '/livro09', '/livro04', '/livro06', '/livro07', '/livro12', '/livro08',
)
LIVROS_REMOVIDOS = ('/livro01', '/livro02', '/livro03', '/livro08-arquiteto', '/livro10')

MODULOS_LIVRES = (
    '/q-trilogia-m01', '/q-trilogia-m02', '/q-trilogia-m03',
    '/q-anestesia-m01', '/q-anestesia-m02', '/q-anestesia-m03',
)

ALIAS_CONV = {
    '/q-semeador-anestesia': '/q-semeador',
    '/trilogia': '/trilogia-da-alma',
    '/anestesia': '/anestesia-mental',
}

PDF_MAP = {
    '/ebooks/livro05-evalma.pdf': '/dl:evolucao',
    '/ebooks/livro07-o-c-d.pdf': '/dl:caminho',
    '/ebooks/livro09-amental.pdf': '/dl:anestesia',
    '/ebooks/Um-Segundo-com-Deus-Vol-01.pdf': '/dl:devocional-quiz',

    '/ebooks/evolucao-da-alma.pdf': '/dl:evolucao',
    '/ebooks/evolucao-da-alma-evalma.pdf': '/dl:evolucao',
    '/ebooks/anestesia-mental.pdf': '/dl:anestesia',
    '/ebooks/anestesia-mental-evalma.pdf': '/dl:anestesia',
    '/ebooks/um-segundo-com-deus-vol-01.pdf': '/dl:devocional-quiz',
    '/ebooks/jesus-quer-falar.pdf': '/dl:jesus-quiz',
    '/ebooks/jesus-quer-falar-com-seu-filho.pdf': '/dl:jesus-livro',
    '/ebooks/livro11-o-n-t.pdf': '/dl:brinde-nt',
    '/ebooks/livro11-onovotestamenento.pdf': '/dl:brinde-nt',
    '/ebooks/livro12-a-d-o.pdf': '/dl:afirmacoes',
    '/ebooks/livro11.pdf': '/dl:chute-pdf',
    '/ebooks/livro10.pdf': '/dl:chute-pdf',
}

DL_NOMES = OrderedDict([
    ('/dl:brinde-nt', 'Bônus 1: PDF do NT (página de obrigado)'),
    ('/dl:evolucao', 'PDF Evolução da Alma (evalma + nome antigo)'),
    ('/dl:anestesia', 'PDF Anestesia Mental (evalma + nome antigo)'),
    ('/dl:devocional-quiz', 'Bônus 2: PDF Devocional Um Segundo com Deus (30 dias)'),
    ('/dl:jesus-quiz', 'PDF Jesus Quer Falar (quiz, livre)'),
    ('/dl:jesus-livro', 'Bônus 3: PDF Jesus Quer Falar com Seu Filho'),
    ('/dl:afirmacoes', 'Bônus 4: PDF Afirmações, Declarações e Orações'),
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
    r'\.(png|jpg|jpeg|gif|svg|ico|css|js|woff2?|webp|xml|json|txt|webmanifest|mp3|mp4)$', re.I)
RE_BOT = re.compile(
    r'bot|crawl|spider|slurp|scan|monitor|probe|python|curl|wget|httpclient|'
    r'go-http|libwww|java/|okhttp|headless|lighthouse|pingdom|uptime|'
    r'facebookexternalhit|telegrambot|twitterbot|linkedinbot|'
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
    for nome in ('q-semeador', 'q-codigo', 'q-laura', 'q-whats',
                 'q-palavra-play', 'q-palavra-share', 'q-livro-share', 'q-guardar', 'q-guardar-kiwify'):
        p = os.path.join(SITE, nome)
        if not os.path.isfile(p):
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    f.write('ok\n')
            except Exception:
                pass


# MISSAO_SW_PREFETCH_V2: criterio proprio, nao e identificacao de pessoas.
def _sw_precarga(metodo, referer):
    from urllib.parse import urlsplit
    if metodo != 'GET' or not isinstance(referer, str):
        return False
    try:
        u = urlsplit(referer)
        return (u.scheme in ('http', 'https')
                and u.hostname in ('missaocomdeus.com.br', 'www.missaocomdeus.com.br')
                and u.username is None and u.password is None
                and u.port in (None, 80 if u.scheme == 'http' else 443)
                and u.path == '/sw.js')
    except (ValueError, TypeError):
        return False


def _sw_precarga_alvo(metodo, referer, url):
    # Referer SW sozinho NAO distingue pre-carga de eventos reais via fetch.
    # Escopo conservador: somente destinos da lista URLS do SW recebido.
    from urllib.parse import urlsplit
    if not _sw_precarga(metodo, referer):
        return False
    try:
        return urlsplit(url).path in (
            '/', '/manifest.json', '/livro04', '/livro05', '/livro06',
            '/livro07', '/livro09', '/livro11', '/quiz', '/guia-pais-filhos')
    except (ValueError, TypeError):
        return False


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
    descartados_pre_carga_sw = 0
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
            if _sw_precarga_alvo('GET', ref, url):
                descartados_pre_carga_sw += 1
                continue
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
            if path == '/livro08' and dt is not None and dt < datetime(2026, 9, 2):
                path = '/livro08-arquiteto'
            path_l = path.lower()

            # Acoes que sairam do ar: ignorar por completo (cache, pagina velha).
            if path in CONVERSAO_REMOVIDA or path_l in CONVERSAO_REMOVIDA:
                continue

            if path.startswith('/.well-known'):
                continue

            # Ruido: arquivo, teste, ajax, endereco quebrado. Nao entra em Outras.
            if (path.endswith('.mp3') or path.endswith('.mp4') or path.endswith('.php')
                    or path in ('/stats', '/stats_teste', '/geo', '/%2f')
                    or 'http://' in path or 'https://' in path
                    or path_l in ('/%2f', '/stats_teste')):
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
        'pre_carga_aplicativo_sw': descartados_pre_carga_sw,
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






# ============================================================ GEO (UF e cidade)
def geo_carregar():
    try:
        with open(GEO_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def geo_guardar(cache):
    try:
        os.makedirs(os.path.dirname(GEO_CACHE), exist_ok=True)
        with open(GEO_CACHE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=0)
    except Exception as e:
        print('  AVISO: nao consegui gravar geo_cache:', e)






def _geo_norm(txt):
    """Chave estavel (minuscula, sem acento) + nome como veio p/ exibir."""
    txt = ' '.join(str(txt or '').split())
    if not txt:
        return '', ''
    sem = unicodedata.normalize('NFKD', txt).encode('ascii', 'ignore').decode('ascii')
    return sem.strip().lower(), txt
def geo_processar(res):  # GEO-V4
    """Localizacao REAL: geo.php -> geo_visitas.json (so UF/cidade, sem IP).
    v4 (12/09/2026): so o Brasil entra nas tabelas de Estado e Cidade. De
    fora do Brasil e mostrado so como numero, para nao sumir escondido.
    """
    visitas = {}
    for _caminho in (GEO_VISITAS, GEO_VISITAS_ALT1, GEO_VISITAS_ALT2):
        if not _caminho:
            continue
        try:
            with open(_caminho, 'r', encoding='utf-8') as _f:
                _dados = json.load(_f)
        except Exception:
            continue
        if isinstance(_dados, dict) and _dados:
            for _k, _v in _dados.items():
                try:
                    visitas[_k] = visitas.get(_k, 0) + int(_v)
                except Exception:
                    pass
            if visitas:
                break
    uf_soma = Counter()
    cid_soma = Counter()
    uf_nome = defaultdict(Counter)
    cid_nome = defaultdict(Counter)
    validos = 0
    fora = 0
    lixo = 0
    for chave, n in visitas.items():
        partes = str(chave).split('|')
        pais = partes[0].strip().upper() if len(partes) >= 1 else ''
        estado = partes[1].strip() if len(partes) >= 2 else ''
        mun = partes[2].strip() if len(partes) >= 3 else ''
        try:
            n = int(n)
        except Exception:
            n = 0
        if n <= 0:
            lixo += 1
            continue
        if pais and pais != 'BR':
            fora += n
            continue
        if not estado and not mun:
            lixo += 1
            continue
        validos += n
        k, nome = _geo_norm(estado)
        if k:
            uf_soma[k] += n
            uf_nome[k][nome] += n
        k, nome = _geo_norm(mun)
        if k:
            cid_soma[k] += n
            cid_nome[k][nome] += n
    if validos:
        msg = ('Localizacao real coletada pelo navegador: %d registro(s) '
               'validos do Brasil.' % validos)
        if fora:
            msg += ' %d de fora do Brasil (nao entram na tabela).' % fora
        if lixo:
            msg += ' %d registro(s) zerados ou corrompidos ignorados.' % lixo
    else:
        msg = ('Localizacao real: ainda sem registros do Brasil. Ela comeca a ser '
               'coletada ao abrir qualquer pagina no navegador (1 por sessao).')
    uf = Counter()
    for k, n in uf_soma.items():
        uf[uf_nome[k].most_common(1)[0][0]] += n
    cidade = Counter()
    for k, n in cid_soma.items():
        cidade[cid_nome[k].most_common(1)[0][0]] += n
    return {}, uf, cidade, msg

def geo_tabela(count, rotulo):
    linhas = []
    for i, (nome, n) in enumerate(count.most_common(20), 1):
        medalha = {1: '🥇', 2: '🥈', 3: '🥉'}.get(i, '')
        linhas.append(
            '<tr><td class="num">%s%s</td><td>%s</td><td class="num">%d</td></tr>'
            % (medalha, i, html.escape(nome), n))
    if not linhas:
        return '<tr><td colspan="3">%s ainda sem dados.</td></tr>' % rotulo
    return '\n'.join(linhas)




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













def _v7_analisar(logs=None, paginas=None, pdfs=None, ignorar=None, minutos=None):
    """Catalogo atual sobre logs disponiveis. So paginas iniciam/prolongam sessoes."""
    import os
    import re
    from collections import Counter
    from datetime import datetime
    from urllib.parse import urlsplit
    logs = lista_logs() if logs is None else logs
    paginas = set(PAGINAS) | {'/privacidade', '/leitor'} if paginas is None else set(paginas)
    paginas -= set(INTERNAS_EXCLUIR) | set(LIVROS_REMOVIDOS)
    paginas = {p for p in paginas if not p.startswith('/q-')}
    pdfs = PDF_MAP if pdfs is None else pdfs
    ignorar = IPS_IGNORAR if ignorar is None else ignorar
    minutos = SESSAO_MINUTOS if minutos is None else minutos
    def exigir_v7(ok):
        if not ok:
            raise ValueError('V7: volume de logs acima do limite de teste.')
    arquivos = list(dict.fromkeys(os.path.realpath(p) for p in logs))
    exigir_v7(sum(os.path.getsize(p) for p in arquivos) <= 100 * 1024 * 1024)
    registros = []
    cont = Counter()
    eventos = Counter()
    paginas_cont = Counter()
    vistos = {}
    # Nginx common/combined. Nunca presume status 200 quando o formato muda.
    padrao = re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) HTTP/[^\"]+" (\d{3}) \S+(.*)$')
    for arquivo in arquivos:
        neste_arquivo = Counter()
        with open(arquivo, encoding='utf-8', errors='replace') as f:
            for linha in f:
                cont['linhas_lidas'] += 1
                exigir_v7(cont['linhas_lidas'] <= 250000)
                # Arquivos sobrepostos podem repetir a mesma linha literal.
                # Sem request-id nao e possivel distinguir copia de requisicoes identicas.
                neste_arquivo[linha] += 1
                if neste_arquivo[linha] <= vistos.get(linha, 0):
                    cont['linhas_identicas_ignoradas'] += 1
                    continue
                m = padrao.match(linha.rstrip('\r\n'))
                if not m:
                    cont['formato_nao_reconhecido'] += 1
                    continue
                ip, data, metodo, url, status, resto = m.groups()
                if ip in ignorar:
                    cont['ips_excluidos'] += 1
                    continue
                if metodo != 'GET':
                    cont['outros_metodos'] += 1
                    continue
                if status not in ('200', '206', '304'):
                    cont['status_excluidos'] += 1
                    continue
                campos = re.match(r'^\s+"([^\"]*)"\s+"([^\"]*)"', resto)
                if not campos or campos.group(2) in ('', '-'):
                    cont['sem_user_agent'] += 1
                    continue
                ua = campos.group(2)
                if RE_BOT.search(ua):
                    cont['agentes_filtrados'] += 1
                    continue
                try:
                    dt = datetime.strptime(data, '%d/%b/%Y:%H:%M:%S %z')
                    timestamp = dt.timestamp()
                    path = urlsplit(url).path.rstrip('/') or '/'
                except (ValueError, OverflowError):
                    cont['data_ou_url_invalida'] += 1
                    continue
                if path.endswith('.html'):
                    path = path[:-5]
                if path in ('/index', ''):
                    path = '/'
                path = ALIAS_CONV.get(path, path)
                if path == '/livro08' and timestamp < datetime.fromisoformat('2026-09-02T00:00:00-03:00').timestamp():
                    cont['fora_catalogo_atual'] += 1
                    continue
                if path.startswith('/q-'):
                    if status == '206':
                        cont['status_excluidos'] += 1
                        continue
                    tipo = 'evento'
                elif path.lower() in pdfs:
                    tipo = 'pdf'
                elif path in INTERNAS_EXCLUIR or path.endswith('.php'):
                    cont['internos_ou_php'] += 1
                    continue
                elif path in paginas:
                    if status == '206':
                        cont['status_excluidos'] += 1
                        continue
                    tipo = 'pagina'
                else:
                    cont['outros_recursos_ou_rotas'] += 1
                    continue
                registros.append((timestamp, ip, ua, path, tipo))
        for linha, quantidade in neste_arquivo.items():
            vistos[linha] = max(vistos.get(linha, 0), quantidade)
    registros.sort(key=lambda x: x[0])
    ultimo = {}
    ips_paginas = set()
    primeira = registros[0][0] if registros else None
    ultima = registros[-1][0] if registros else None
    for ts, ip, ua, path, tipo in registros:
        cont[tipo] += 1
        if tipo == 'evento':
            eventos[path] += 1
        elif tipo == 'pagina':
            paginas_cont[path] += 1
            ips_paginas.add(ip)
            chave = (ip, ua)  # estimativa, nao identifica uma pessoa
            if chave not in ultimo or ts - ultimo[chave] > minutos * 60:
                cont['sessoes'] += 1
            ultimo[chave] = ts
    return {'contagens': cont, 'eventos': eventos, 'paginas': paginas_cont,
            'ips_paginas': len(ips_paginas), 'minutos': minutos,
            'inicio': primeira, 'fim': ultima}







# SALMOS_BIBLICA_CARD_HOOK



def _v8_analisar(logs=None, agora=None, antigo=False, limites=None):
    """MISSAO_PAINEL_V8. Ordenacao e deduplicacao em disco privado, sem IP exportado."""
    import hashlib, os, re, sqlite3, tempfile, time, shutil
    from collections import Counter
    from datetime import datetime, timezone, timedelta
    from urllib.parse import urlsplit, parse_qs
    inicio_tempo = time.monotonic()
    max_bytes, max_linhas, max_tempo = limites or (100*1024*1024, 250000, 90)
    zona = timezone(timedelta(hours=-3))
    agora = agora or datetime.now(zona)
    if agora.tzinfo is None:
        raise ValueError('Relogio de teste precisa de fuso.')
    agora = agora.astimezone(zona)
    hoje = agora.date().isoformat()
    ontem = (agora.date()-timedelta(days=1)).isoformat()
    corte = (agora.hour, agora.minute, agora.second)
    arquivos = list(dict.fromkeys(os.path.realpath(p) for p in (lista_logs() if logs is None else logs)))
    if not arquivos:
        raise ValueError('Nenhum log disponivel. Nao ha medicao principal valida.')
    fotos = [os.stat(p) for p in arquivos]
    tamanho = sum(s.st_size for s in fotos)
    if tamanho > max_bytes:
        raise ValueError('Capacidade excedida: %d bytes; teto %d. Principal indisponivel.' % (tamanho,max_bytes))
    paginas = (set(PAGINAS_ANTIGAS) | {p for p in PAGINAS if not p.startswith('/q-')}) if antigo else (set(PAGINAS)|{'/privacidade','/leitor'})-set(LIVROS_REMOVIDOS)
    paginas -= set(INTERNAS_EXCLUIR)
    paginas = {p for p in paginas if not p.startswith('/q-')}
    pdfmap = {p.lower():v for p,v in PDF_MAP.items()}
    eventos_conhecidos = set(CONVERSAO) | {p for p in PAGINAS if p.startswith('/q-')}
    padrao = re.compile(r'^(\S+) \S+ \S+ \[([^\]]+)\] "(\S+) (\S+) HTTP/[^\"]+" (\d{3}) \S+\s+"([^\"]*)"\s+"([^\"]*)"')
    preview = re.compile(r'^WhatsApp(?:[/\s]|$)|meta-externalagent|meta-externalfetcher',re.I)
    c, eventos, ranking, pdfs = Counter(), Counter(), Counter(), Counter()
    c['pre_carga_aplicativo_sw'] = 0
    dias, origens, ips_origens = {}, Counter(), Counter()
    primeira = ultima = log_inicio = log_fim = None
    ate_hoje = ate_ontem = 0
    sal = os.urandom(32)
    with tempfile.TemporaryDirectory(prefix='missao-v8-') as td:
        if shutil.disk_usage(td).free < tamanho*4 + 64*1024*1024:
            raise ValueError('Espaco temporario insuficiente. Nao ampliar limites.')
        db = sqlite3.connect(os.path.join(td,'ordenacao.sqlite'))
        try:
            db.execute('PRAGMA cache_size=-4096'); db.execute('PRAGMA temp_store=FILE')
            db.execute('PRAGMA mmap_size=0'); db.execute('PRAGMA journal_mode=OFF')
            db.set_progress_handler(lambda: int(time.monotonic()-inicio_tempo > max_tempo), 10000)
            db.execute('CREATE TABLE r(id INTEGER PRIMARY KEY, ip BLOB, ident BLOB, ts REAL, origem TEXT, dia TEXT)')
            db.execute('CREATE TABLE s(ip BLOB, origem TEXT, dia TEXT)')
            if len(arquivos)>1:
                db.execute('CREATE TABLE d(h BLOB, f INTEGER, n INTEGER, PRIMARY KEY(h,f)) WITHOUT ROWID')
            for fi,(arquivo,foto) in enumerate(zip(arquivos,fotos)):
                with open(arquivo,'rb') as f:
                    st = os.fstat(f.fileno())
                    if (st.st_dev,st.st_ino,st.st_size)!=(foto.st_dev,foto.st_ino,foto.st_size):
                        raise ValueError('Log mudou antes da leitura; tente outra previa.')
                    restante = foto.st_size
                    while restante:
                        raw = f.readline(min(restante,65537)); restante -= len(raw)
                        if not raw:
                            raise ValueError('Log truncado durante leitura.')
                        c['linhas_lidas'] += 1
                        if c['linhas_lidas'] > max_linhas:
                            raise ValueError('Capacidade excedida: mais de %d linhas. Principal indisponivel.' % max_linhas)
                        if time.monotonic()-inicio_tempo > max_tempo:
                            raise ValueError('Tempo de analise excedido; nao ampliar limites sem medir.')
                        if len(raw)>65536:
                            raise ValueError('Linha maior que 64 KiB; formato exige revisao.')
                        if not raw.endswith(b'\n'):
                            c['linha_final_incompleta']+=1; continue
                        if len(arquivos)>1:
                            h=hashlib.sha256(raw).digest()
                            db.execute('INSERT INTO d VALUES(?,?,1) ON CONFLICT(h,f) DO UPDATE SET n=n+1',(h,fi))
                            n=db.execute('SELECT n FROM d WHERE h=? AND f=?',(h,fi)).fetchone()[0]
                            anterior=db.execute('SELECT MAX(n) FROM d WHERE h=? AND f<?',(h,fi)).fetchone()[0] or 0
                            if n<=anterior:
                                c['linhas_identicas_ignoradas']+=1; continue
                        m=padrao.match(raw.decode('utf-8',errors='replace').rstrip('\r\n'))
                        if not m:
                            c['formato_nao_reconhecido']+=1; continue
                        ip,data,metodo,url,status,ref,ua=m.groups()
                        if ip in IPS_IGNORAR:
                            c['ips_excluidos']+=1; continue
                        try:
                            dt=datetime.strptime(data,'%d/%b/%Y:%H:%M:%S %z').astimezone(zona)
                            ts=dt.timestamp(); path=urlsplit(url).path.rstrip('/') or '/'
                        except (ValueError,OverflowError):
                            c['data_ou_url_invalida']+=1; continue
                        log_inicio=ts if log_inicio is None else min(log_inicio,ts)
                        log_fim=ts if log_fim is None else max(log_fim,ts)
                        if metodo!='GET':
                            c['outros_metodos']+=1; continue
                        if not antigo and _sw_precarga_alvo(metodo, ref, url):
                            c['pre_carga_aplicativo_sw']+=1; continue
                        permitidos=('200','301','302','304','307','308') if antigo else ('200','206','304')
                        if status not in permitidos:
                            c['status_excluidos']+=1; continue
                        if ua in ('','-'):
                            c['sem_user_agent']+=1; continue
                        if RE_BOT.search(ua) or preview.search(ua):
                            c['agentes_filtrados']+=1; continue
                        if ts > agora.timestamp()+300:
                            c['datas_futuras']+=1; continue
                        if path.endswith('.html'): path=path[:-5]
                        if path in ('/index',''): path='/'
                        path=ALIAS_CONV.get(path,path)
                        if not antigo and path=='/livro08' and ts<datetime(2026,9,2,tzinfo=zona).timestamp():
                            c['fora_catalogo']+=1; continue
                        if path in INTERNAS_EXCLUIR or path.endswith('.php'):
                            c['internos_e_php']+=1; continue
                        if not antigo and path.startswith('/q-') and status!='206': tipo='evento'
                        elif not antigo and path.lower() in pdfmap: tipo='pdf'
                        elif path in paginas and status!='206': tipo='pagina'
                        else:
                            c['fora_catalogo']+=1; continue
                        c[tipo]+=1
                        dia=dt.date().isoformat()
                        diario=dias.setdefault(dia,Counter()); diario[tipo]+=1
                        primeira=ts if primeira is None else min(primeira,ts)
                        ultima=ts if ultima is None else max(ultima,ts)
                        if tipo=='evento':
                            ev=path if path in eventos_conhecidos else '/q-outros-nao-catalogados'
                            eventos[ev]+=1; diario[ev]+=1
                        elif tipo=='pdf':
                            pdfs[pdfmap[path.lower()]]+=1
                        else:
                            ranking[path]+=1; diario['pagina:'+path]+=1
                            if (dt.hour,dt.minute,dt.second)<=corte:
                                if dia==hoje: ate_hoje+=1
                                if dia==ontem: ate_ontem+=1
                            try:
                                host=host_de(ref)
                                interna=host in NOSSOS_HOSTS or (ref.startswith('/') and not host)
                                q=parse_qs(urlsplit(url).query)
                                origem='desconhecida' if interna else classificar_origem(ref,(q.get('utm_source') or [''])[0],(q.get('utm_medium') or [''])[0])
                            except ValueError: origem='desconhecida'
                            ipkey=hashlib.sha256(sal+ip.encode()).digest()
                            ident=hashlib.sha256(sal+ip.encode()+b'\0'+ua.encode()).digest()
                            db.execute('INSERT INTO r(ip,ident,ts,origem,dia) VALUES(?,?,?,?,?)',(ipkey,ident,ts,origem,dia))
                    depois=os.stat(arquivo)
                    if (depois.st_dev,depois.st_ino)!=(foto.st_dev,foto.st_ino) or depois.st_size<foto.st_size:
                        raise ValueError('Rotacao/truncamento durante leitura; tente outra previa.')
            anterior_id=None; anterior_ts=None
            for ipkey,ident,ts,origem,dia in db.execute('SELECT ip,ident,ts,origem,dia FROM r ORDER BY ident,ts,id'):
                if ident!=anterior_id or ts-anterior_ts>SESSAO_MINUTOS*60:
                    c['sessoes']+=1; dias[dia]['sessoes']+=1
                    db.execute('INSERT INTO s VALUES(?,?,?)',(ipkey,origem,dia))
                anterior_id,anterior_ts=ident,ts
            ip_total=db.execute('SELECT COUNT(DISTINCT ip) FROM r').fetchone()[0]
            for dia,n in db.execute('SELECT dia,COUNT(DISTINCT ip) FROM r GROUP BY dia'): dias[dia]['ips']=n
            for origem,n,ips in db.execute('SELECT origem,COUNT(*),COUNT(DISTINCT ip) FROM s GROUP BY origem'):
                origens[origem]=n; ips_origens[origem]=ips
        finally:
            db.close()
    return dict(contagens=c,eventos=eventos,paginas=ranking,pdfs=pdfs,dias=dias,origens=origens,ips_origens=ips_origens,
                ips_paginas=ip_total,inicio=primeira,fim=ultima,log_inicio=log_inicio,log_fim=log_fim,
                hoje=hoje,ontem=ontem,ate_hoje=ate_hoje,ate_ontem=ate_ontem,
                bytes=tamanho,limite_bytes=max_bytes,limite_linhas=max_linhas,
                segundos=time.monotonic()-inicio_tempo,agora=agora.isoformat(),arquivos=len(arquivos))


def _v8_html_base(d, legado=None, geo=None, antigo=None, erro=None):
    import html, re
    from datetime import datetime, timezone, timedelta
    zona=timezone(timedelta(hours=-3))
    e=lambda x:html.escape(str(x))
    def tabela(titulos,linhas):
        return '<table><tr>'+''.join('<th>'+e(t)+'</th>' for t in titulos)+'</tr>'+(''.join('<tr>'+''.join('<td>'+e(v)+'</td>' for v in r)+'</tr>' for r in linhas) or '<tr><td>Sem registros nesta base.</td></tr>')+'</table>'
    def card(v,t):return '<div class="card"><strong>'+e(v)+'</strong><br>'+e(t)+'</div>'
    def data(t):return datetime.fromtimestamp(t,zona).strftime('%d/%m/%Y %H:%M') if t is not None else 'sem registros'
    estilo='body{font:16px system-ui;background:#0e1a2e;color:#f4f0e7;max-width:1120px;margin:auto;padding:22px}h1,h2,strong{color:#e3c877}.cards{display:flex;flex-wrap:wrap;gap:12px}.card{background:#172c46;padding:18px;flex:1;min-width:145px}.card strong{font-size:28px}table{width:100%;border-collapse:collapse;margin:16px 0;display:block;overflow-x:auto}td,th{text-align:left;padding:10px;border-bottom:1px solid #38516b}section,details{margin:24px 0;padding:16px;background:#12243a}summary{cursor:pointer;font-weight:bold}.aviso{padding:18px;background:#634018;color:white}.erro{padding:24px;background:#8c2020;color:white;font-size:20px}.nota{color:#c3cfdf;font-size:14px}a{color:#e3c877}@media(max-width:600px){body{padding:10px}td,th{padding:6px;font-size:13px}}'
    out='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Painel da Missão V8</title><style>'+estilo+'</style><h1>Missão com Deus: visão da missão</h1><p>Medição V8: páginas, ações e PDFs separados. /palavra permanece interna.</p>'
    if erro:
        return out+'<div class="erro"><b>MEDIÇÃO PRINCIPAL INDISPONÍVEL.</b><p>Não há totais principais válidos desta execução. O legado não substitui a medição atual.</p><p>'+e(erro)+'</p></div><p>Gerado em '+e(datetime.now(zona).strftime('%d/%m/%Y %H:%M'))+' (Brasília). Confira o terminal. Não interprete ausência de dados como zero.</p></html>'
    c=d['contagens']; hoje=d['dias'].get(d['hoje'],{})
    ocupacao=max(d['bytes']/d['limite_bytes'],c['linhas_lidas']/d['limite_linhas'])*100
    out+='<p>Gerado em '+e(data(datetime.fromisoformat(d['agora']).timestamp()))+' (Brasília). Registros aceitos: '+e(data(d['inicio']))+' até '+e(data(d['fim']))+'.</p>'
    out+='<section><h2>Capacidade e cobertura</h2><p'+(' class="aviso"' if ocupacao>=80 else '')+'><b>'+e('ATENÇÃO: capacidade em 80% ou mais. ' if ocupacao>=80 else 'Capacidade dentro dos limites. ')+'</b>'+e('%d/%d linhas; %.2f/%.0f MiB; %.1f%% do teto mais próximo. %d arquivo(s), %.2f s.' % (c['linhas_lidas'],d['limite_linhas'],d['bytes']/1048576,d['limite_bytes']/1048576,ocupacao,d['arquivos'],d['segundos']))+'</p><p class="nota">Leitura limitada ao tamanho inicial de cada arquivo. Novas linhas entram na próxima geração. Há ordenação temporária em disco; limites de volume e tempo continuam protegendo a VPS. Logs não garantem cobertura contínua nem mostram acessos servidos sem chegar ao servidor.</p></section>'
    out+='<section><h2>Revisão da medição: padrão de pré-carga do aplicativo</h2><p>Esta geração exclui GET com Referer próprio de caminho exato /sw.js somente quando o destino pertence à lista de pré-carga do SW auditado. Eventos /q-*, PHP, PDFs e destinos fora da lista são preservados por este critério. Referer de SW sozinho também pode aparecer em ações reais intermediadas pelo aplicativo, portanto não é prova universal de pré-carga.</p><p>O histórico disponível foi recalculado com esse critério conservador no V8 e na base V6 usada pelo leituras.json. Painéis gerados antes desta revisão usavam critérios diferentes e não devem ser comparados diretamente com os novos totais. As semanas mostradas nesta geração usam o mesmo filtro, mantendo ressalvas de cobertura. Versões históricas do SW podem ter tido outras listas; os logs disponíveis não resolvem toda ambiguidade.</p><p class="nota">O critério vem antes dos filtros de status e agente, depois de método/data e IPs excluídos no V8. Pode absorver descartes anteriores, inclusive manifestos e erros. O contador não é a redução de páginas nem confirmação individual de pré-carga. Não apaga logs, não altera o aplicativo e não comprova leitura humana, instalações voluntárias ou vendas.</p></section>'
    out+='<section><h2>Movimento público: mesma base</h2><div class="cards">'+''.join(card(v,t) for v,t in ((c['pagina'],'Acessos a páginas do catálogo'),(c['sessoes'],'Sessões estimadas de páginas'),(d['ips_paginas'],'IPs distintos em páginas'),('%.2f'%(c['pagina']/c['sessoes']) if c['sessoes'] else 'não se aplica','Páginas por sessão estimada'),(c['evento'],'Eventos /q-*'),(c['pdf'],'Requisições de PDF')) )+'</div><p class="nota">Só páginas iniciam ou prolongam sessões, após mais de '+e(SESSAO_MINUTOS)+' minutos sem página. IP + navegador não identificam pessoas. Filtros não garantem tráfego humano. PDF pode ser parcial (206), não download completo; evento não comprova compra.</p>'
    out+='<h3>Hoje e ontem: somente páginas</h3>'+tabela(['Dia','Páginas até o mesmo horário'],[(d['hoje'],d['ate_hoje']),(d['ontem'],d['ate_ontem'])])
    base_ok=d['log_inicio'] is not None and d['log_inicio']<=datetime.fromisoformat(d['ontem']).replace(tzinfo=zona).timestamp()
    if '2026-10-19' in (d['hoje'],d['ontem']): msg='Comparação percentual suspensa por precaução: há relato de possível lacuna em 19/10. Sua duração não foi confirmada.'
    elif not base_ok: msg='Comparação percentual indisponível: os logs não alcançam o início de ontem.'
    elif not d['ate_ontem']: msg='Comparação percentual indisponível: ontem não tem páginas nessa janela.'
    else: msg='Variação de páginas até o mesmo horário: %+.1f%%. Não é crescimento de pessoas; depende da cobertura dos logs.'%((d['ate_hoje']/d['ate_ontem']-1)*100)
    out+='<p class="aviso">'+e(msg)+'</p>'+tabela(['Dia','Páginas','Eventos','PDFs (requisições)','Sessões iniciadas','IPs em páginas'],[(dia,x.get('pagina',0),x.get('evento',0),x.get('pdf',0),x.get('sessoes',0),x.get('ips',0)) for dia,x in sorted(d['dias'].items(),reverse=True)[:14]])+'</section>'
    out+='<section><h2>Leitura e caminhos públicos</h2><p>Acessos a páginas, não capítulos concluídos. '+e(len(LIVROS_NO_AR))+' livros no catálogo atual.</p>'+tabela(['Página','Acessos','Hoje'],[(PAGINAS.get(p,p),n,hoje.get('pagina:'+p,0)) for p,n in d['paginas'].most_common()])
    # Hoje por livro vem dos contadores diarios especificos, nao da base legada.
    out+='<p class="nota">Salmos, Motivação Bíblica e os guias estão no ranking, calculados diretamente dos dados, sem procurar números no HTML. Guia Pais e Filhos mede acesso à página, não quiz concluído.</p></section>'
    nomes={p:info[1] for p,info in CONVERSAO.items()}
    nomes.update({p:n for p,n in PAGINAS.items() if p.startswith('/q-')})
    nomes.update({'/q-semeador':'Cliques legados de ofertas (histórico, não vendas)','/q-guardar':'Aberturas registradas da página de acesso','/q-guardar-kiwify':'Cliques para o checkout pela página de acesso','/q-outros-nao-catalogados':'Outros eventos /q-* não catalogados'})
    chaves=list(dict.fromkeys(['/q-termo-v2-inicio','/q-termo-v2-fim','/q-guardar','/q-guardar-kiwify']+list(d['eventos'])))
    out+='<section><h2>Ações registradas</h2>'+tabela(['Ação','Total','Hoje'],[(nomes.get(p,p),d['eventos'][p],hoje.get(p,0)) for p in chaves])+'<p class="nota">Início e resultado V2 são tentativas por abertura da página, não pessoas. Requisições independentes podem falhar; marcadores podem ser acessados diretamente. Cliques não são pagamentos. Não se calcula taxa de compra dividindo eventos por IPs.</p><h3>PDFs solicitados</h3>'+tabela(['Material','Requisições 200/206/304'],[(re.sub(r'^Bônus \d+: ', '', DL_NOMES.get(p,p)),n) for p,n in d['pdfs'].most_common()])+'<p class="nota">A tabela identifica materiais solicitados; não confirma bônus, entrega ou oferta comercial atual.</p></section>'
    rotulos={k:v[1] for k,v in ORIGENS.items()}
    rotulos['desconhecida']='Origem não identificada (referência interna na abertura da sessão)'
    out+='<details><summary>Origens das sessões públicas</summary>'+tabela(['Origem inferida','Sessões','IPs distintos nesta origem'],[(rotulos.get(k,k),n,d['ips_origens'][k]) for k,n in d['origens'].most_common()])+'<p class="nota">A origem vem da primeira página da sessão. Um IP pode aparecer em mais de uma origem; não somar como pessoas. Referência interna pode ocorrer após pausa de mais de 30 minutos, não apenas no começo do log. Aplicativos podem omitir a origem; direto não comprova endereço digitado.</p></details>'
    out+='<details><summary>Geografia: base separada</summary><p>'+e((geo or {}).get('msg','Sem leitura geográfica nesta execução.'))+'</p><p class="nota">Base local coletada pelo navegador, acumulada em período próprio não registrado aqui. Não equivale a IPs ou pessoas e não deve ser comparada diretamente às sessões. Precisão, consentimento e adequação para campanhas exigem avaliação própria.</p>'+tabela(['Estado','Registros'],(geo or {}).get('uf',{}).most_common(20) if hasattr((geo or {}).get('uf',{}),'most_common') else [])+tabela(['Cidade','Registros'],(geo or {}).get('cidade',{}).most_common(20) if hasattr((geo or {}).get('cidade',{}),'most_common') else [])+'</details>'
    if antigo and 'contagens' in antigo:
        out+='<details><summary>Endereço antigo: base separada, não somar</summary>'+tabela(['Medida','Total'],[('Requisições aceitas em caminhos reconhecidos',antigo['contagens']['pagina']),('Sessões estimadas',antigo['contagens']['sessoes']),('IPs distintos em páginas',antigo['ips_paginas']),('Fora do catálogo, sem afirmar que sejam ataques',antigo['contagens']['fora_catalogo'])])+'<p class="nota">GET com 200/301/302/304/307/308 e filtros de agentes. Caminhos desconhecidos não são chamados de ataques por conterem dev ou test. /devocional só contará se sua existência histórica for confirmada e incluída no catálogo. Sem perfil antivarredura do cálculo antigo, os totais podem diferir; não comprovam tráfego humano.</p></details>'
    elif antigo: out+='<details><summary>Endereço antigo</summary><p>'+e(antigo.get('erro','Sem medição.'))+'</p></details>'
    if legado:
        out+='<details><summary>Legado V6: critérios antigos, não usar como medição principal</summary><p>Recalculado pelos critérios anteriores; não é um arquivo congelado. Inclui misturas conhecidas de recursos/ações. Não comparar diretamente com V8.</p>'+tabela(['Indicador antigo','Total'],[('Total de registros aceitos V6',legado[1]),('Sessões V6',legado[24]['total_visitas']),('IPs V6',legado[15])])+'<p class="nota">A variação, a razão de páginas por visita e a suposta taxa antiga não são exibidas por terem bases incompatíveis ou interpretação inadequada. O histórico permanece nos logs e no backup. leituras.json continua derivado do legado V6, agora também com exclusão conservadora do padrão de pré-carga da lista auditada. Outras diferenças de critérios entre V6 e V8 permanecem.</p></details>'
    out+='<section><h2>Contexto para interpretar a missão</h2><ul><li>02/09/2026: catálogo atual; acessos anteriores ao antigo Livro 08 não são atribuídos ao Pais e Filhos.</li><li>30/09/2026: mudança informada no acesso de cinco livros para cerca de 40% aberto. Antes/depois não medem a mesma oportunidade de leitura. Não há ajuste artificial dos números.</li><li>19/10/2026: possível lacuna relatada; duração e causa ainda não verificadas nesta revisão.</li></ul></section>'
    out+='<details><summary>Critérios e descartes auditáveis</summary>'+tabela(['Critério','Registros'],sorted((('Padrão de pré-carga do aplicativo (lista auditada)' if k=='pre_carga_aplicativo_sw' else k),v) for k,v in c.items()))+'<p class="nota">Repetições no mesmo arquivo são mantidas. Entre arquivos, vale a maior multiplicidade de linhas idênticas (hash SHA256 em banco temporário). Sem request-id, isso pode juntar requisições legítimas idênticas. /palavra, /stats, /mural e PHP ficam fora das páginas públicas. Prévias reconhecidas do WhatsApp/Meta são filtradas; não há garantia de identificar todos os robôs.</p></details><footer>Painel V8. Noindex não é autenticação. Nenhum e-mail ou resposta de quiz é usado nesta análise.</footer></html>'
    return out


def _v8_coletar():
    """Somente leitura. Sem main legado, APIs, pixels ou gravacoes."""
    import os
    from collections import Counter
    d=_v8_analisar()
    legado,err=analisar()
    if err: raise ValueError('Leitura legada indisponivel; preservar leituras.json: '+str(err))
    geo={'uf':Counter(),'cidade':Counter(),'msg':'Base geográfica local não disponível.'}
    caminhos=[p for p in (GEO_VISITAS,GEO_VISITAS_ALT1,GEO_VISITAS_ALT2) if p and os.path.isfile(p)]
    if caminhos and all(os.path.getsize(p)<=5*1024*1024 for p in caminhos):
        try:
            _,uf,cid,msg=geo_processar(legado); geo=dict(uf=uf,cidade=cid,msg=msg)
        except Exception: geo['msg']='Não foi possível ler a base geográfica local; nenhum serviço externo foi consultado.'
    antigo={'erro':'Log do endereço antigo não disponível; não há total presumido.'}
    for p in dict.fromkeys([LOG_ANTIGO]+CANDIDATOS_LOG_ANTIGO):
        if p and os.path.isfile(p):
            try: antigo=_v8_analisar(logs=[p],antigo=True)
            except Exception as ex: antigo={'erro':'Medição separada indisponível: '+str(ex)}
            break
    return d,legado,geo,antigo


def _v8_gravar(caminho,dados):
    import os, stat, tempfile
    from pathlib import Path
    p=Path(caminho)
    if p.is_symlink(): raise ValueError('Arquivo de saida por link recusado: '+p.name)
    meta=p.stat() if p.exists() else None
    fd,nome=tempfile.mkstemp(prefix='.'+p.name+'.v8-',dir=str(p.parent))
    try:
        with os.fdopen(fd,'wb') as f: f.write(dados); f.flush(); os.fsync(f.fileno())
        if meta: os.chown(nome,meta.st_uid,meta.st_gid)
        os.chmod(nome,stat.S_IMODE(meta.st_mode) if meta else 0o644)
        os.replace(nome,str(p))
    finally:
        if os.path.exists(nome): os.unlink(nome)


def _v8_main():
    import fcntl, json, os
    from datetime import datetime
    from pathlib import Path
    p=Path(__file__).resolve().parent/'.painel_v8.lock'
    with p.open('a') as lock:
        try: fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            print('Painel V8: outra geracao em andamento; esta execucao nao publicou.'); return
        try:
            d,legado,geo,antigo=_v8_coletar()
            doc=_v8_html(d,legado,geo,antigo)
            livros={p:int(legado[0].get(p,0)) for p in LIVROS_NO_AR}
            top3=[p for p,n in sorted(livros.items(),key=lambda x:-x[1]) if n>0][:3]
            leituras=dict(atualizado=datetime.now().strftime('%d/%m/%Y %H:%M'),livros=livros,top3=top3)
            _v8_gravar(LEITURAS,json.dumps(leituras,ensure_ascii=False).encode())
        except Exception as ex:
            doc=_v8_html(None,erro=str(ex)); print('ERRO PRINCIPAL V8:',ex)
        _v8_gravar(OUT,doc.encode('utf-8'))
        print('Painel V8 gerado em',OUT)


def _foco_periodos(d):
    from datetime import datetime,timedelta,timezone
    zona=timezone(timedelta(hours=-3))
    momento=datetime.fromisoformat(d['agora'])
    if momento.tzinfo is None: raise ValueError('Relogio sem fuso.')
    fim=momento.astimezone(zona).date()-timedelta(days=1)
    inicio=fim-timedelta(days=6)
    anterior_fim=inicio-timedelta(days=1)
    anterior_inicio=anterior_fim-timedelta(days=6)
    def linha(x):
        return dict(paginas=int(x.get('pagina',0)),sessoes=int(x.get('sessoes',0)),
                    livros=sum(int(x.get('pagina:'+p,0)) for p in LIVROS_NO_AR),
                    eventos=int(x.get('evento',0)),pdf=int(x.get('pdf',0)),
                    guardar=int(x.get('pagina:/guardar',0)),
                    abertura=int(x.get('/q-guardar',0)),checkout=int(x.get('/q-guardar-kiwify',0)))
    def periodo(a,b):
        datas=[(a+timedelta(days=i)).isoformat() for i in range((b-a).days+1)]
        itens=[linha(d['dias'].get(dia,{})) for dia in datas]
        totais={k:sum(x[k] for x in itens) for k in itens[0]}
        return dict(inicio=a.isoformat(),fim=b.isoformat(),totais=totais,
                    sem_registros=[dia for dia in datas if dia not in d['dias']])
    recente=periodo(inicio,fim); anterior=periodo(anterior_inicio,anterior_fim)
    avisos=[]
    if recente['sem_registros'] or anterior['sem_registros']:
        avisos.append('Há dias sem registros aceitos em uma das janelas. Zero registrado não prova ausência de público; comparação percentual indisponível.')
    if d['log_inicio'] is None or datetime.fromtimestamp(d['log_inicio'],zona).date()>anterior_inicio:
        avisos.append('Os logs não alcançam o início da janela anterior; comparação percentual indisponível.')
    if d['log_fim'] is None or datetime.fromtimestamp(d['log_fim'],zona).date()<fim:
        avisos.append('Os logs não alcançam o último dia encerrado; comparação percentual indisponível.')
    incompleto=bool(avisos)
    if anterior_inicio.isoformat()<='2026-10-19'<=fim.isoformat():
        avisos.append('19/10/2026 tem possível lacuna relatada, sem duração confirmada. Variações são apenas dos registros disponíveis, não crescimento certificado de pessoas.')
    for data,texto in [('2026-09-02','mudança do catálogo'),('2026-09-30','mudança informada na abertura de cinco livros')]:
        if anterior_inicio.isoformat()<=data<=fim.isoformat():
            avisos.append(data+': '+texto+'. As oportunidades de acesso podem não ser equivalentes.')
    total=dict(paginas=d['contagens']['pagina'],sessoes=d['contagens']['sessoes'],
               livros=sum(d['paginas'].get(p,0) for p in LIVROS_NO_AR),
               eventos=d['contagens']['evento'],pdf=d['contagens']['pdf'],
               guardar=d['paginas'].get('/guardar',0),abertura=d['eventos'].get('/q-guardar',0),
               checkout=d['eventos'].get('/q-guardar-kiwify',0))
    diarios=[]
    for i in range(14):
        dia=(fim-timedelta(days=i)).isoformat()
        diarios.append(dict(dia=dia,valores=linha(d['dias'].get(dia,{})),presente=dia in d['dias']))
    return dict(recente=recente,anterior=anterior,hoje=linha(d['dias'].get(d['hoje'],{})),
                total=total,avisos=avisos,incompleto=incompleto,diarios=diarios)


def _foco_html(d):
    import html
    from datetime import datetime
    f=_foco_periodos(d)
    e=lambda x:html.escape(str(x))
    numero=lambda n:format(int(n),',').replace(',','.')
    data=lambda s:datetime.fromisoformat(s).strftime('%d/%m/%Y')
    def variacao(k):
        atual=f['recente']['totais'][k]; base=f['anterior']['totais'][k]
        if f['incompleto']: return 'Indisponível: janela incompleta'
        if not base: return 'Sem base percentual (anterior zero)'
        return ('%+.1f%% observado'%((atual/base-1)*100)).replace('.',',')
    def tabela(titulos,linhas):
        return '<table><tr>'+''.join('<th>'+e(t)+'</th>' for t in titulos)+'</tr>'+''.join('<tr>'+''.join('<td>'+e(v)+'</td>' for v in r)+'</tr>' for r in linhas)+'</table>'
    def faixa(x):return data(x['inicio'])+' a '+data(x['fim'])
    ocupacao=max(d['bytes']/d['limite_bytes'],d['contagens']['linhas_lidas']/d['limite_linhas'])*100
    estado='atencao' if ocupacao>=80 or not d['contagens']['pagina'] else 'operacao'
    msg='Atenção à capacidade ou ausência de páginas reconhecidas.' if estado=='atencao' else 'Medição gerada dentro dos limites nesta execução.'
    css='''<style>
#resumo-missao,#sustento-missao{border:1px solid #36526e;border-radius:12px}
.foco-grade{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px;margin:16px 0}
.foco-cartao{padding:18px;border:1px solid #557ca3;border-radius:10px;background:#173858;color:#f4f7fb}
.foco-cartao strong{display:block;color:#fff;font-size:30px;margin:8px 0}
.foco-cartao small{display:block;margin-top:8px;color:#dbe6f1}
.foco-operacao{padding:14px;background:#143f31;border-left:5px solid #69d2a1;color:#ecfff5}
.foco-atencao{padding:14px;background:#583d16;border-left:5px solid #ffc568;color:#fff3dd}
.foco-info{padding:14px;background:#173858;border-left:5px solid #82bdff;color:#eff6ff}
.foco-nao-informado{background:#303746;border-color:#a0aec0}
.foco-nao-informado strong{font-size:21px}
.foco-comercial{border-top:5px solid #cba0ff!important}
#sustento-missao h2{color:#e0c6ff}
</style>'''
    out=css+'<section id="resumo-missao"><h2>Visão rápida da missão</h2>'
    out+='<p class="foco-'+estado+'"><b>Operação:</b> '+e(msg)+' '+e(('%.1f'%ocupacao).replace('.',',')+'% do teto mais próximo.')+'</p>'
    out+='<p><b>Sete dias civis encerrados:</b> '+e(faixa(f['recente']))+'<br><b>Comparação:</b> '+e(faixa(f['anterior']))+'. Hoje ('+e(data(d['hoje']))+') fica fora dessas duas janelas.</p>'
    out+=tabela(['Indicador',faixa(f['anterior']),faixa(f['recente']),'Variação de registros'],[(rotulo,numero(f['anterior']['totais'][k]),numero(f['recente']['totais'][k]),variacao(k)) for k,rotulo in [('paginas','Acessos às páginas do catálogo'),('sessoes','Sessões iniciadas'),('livros','Acessos às páginas dos livros'),('eventos','Ações /q-* registradas'),('pdf','Requisições de PDF')]])
    if f['avisos']:out+='<div class="foco-atencao"><b>Comparação com ressalvas</b><ul>'+''.join('<li>'+e(a)+'</li>' for a in f['avisos'])+'</ul></div>'
    out+='<p class="nota">Cores não dão nota espiritual nem certificam público humano. Mais páginas não provam leitura concluída. Sessões são estimadas; PDFs podem ser parciais. IPs diários não são somados como pessoas da semana. A ausência de alerta conhecido não garante cobertura contínua.</p></section>'
    resumo=out[len(css):]
    out=css+'<section id="sustento-missao" class="foco-comercial"><h2>Sustento da missão: /guardar e checkout</h2><p>Observar separadamente a procura pelo acesso completo e os cliques de saída para o pagamento.</p><div class="foco-grade">'
    for k,titulo,nota in [('guardar','Acessos à página /guardar','Requisições aceitas à página, não pessoas.'),('checkout','Cliques de saída para o checkout','Marcador /q-guardar-kiwify; não comprova chegada à Kiwify ou pagamento.')]:
        out+='<div class="foco-cartao"><b>'+e(titulo)+'</b><strong>'+numero(f['total'][k])+'</strong><span>No período acumulado</span><small>Hoje: '+numero(f['hoje'][k])+' | Últimos 7 dias encerrados: '+numero(f['recente']['totais'][k])+'</small><small>'+e(nota)+'</small></div>'
    out+='<div class="foco-cartao foco-nao-informado"><b>Vendas aprovadas e receita</b><strong>Não informadas</strong><small>Não significa zero vendas. Conferir na plataforma de pagamentos. Nenhum dado de pagamento foi integrado nesta revisão.</small></div></div>'
    out+=tabela(['Etapa observada','Acumulado','Hoje',faixa(f['anterior']),faixa(f['recente']),'Variação observada'],[(rotulo,numero(f['total'][k]),numero(f['hoje'][k]),numero(f['anterior']['totais'][k]),numero(f['recente']['totais'][k]),variacao(k)) for k,rotulo in [('livros','Páginas de livros (contexto)'),('guardar','Acessos HTTP à /guardar'),('abertura','Marcador de abertura /q-guardar'),('checkout','Clique de saída /q-guardar-kiwify')]])
    out+='<p class="foco-info"><b>Como ler:</b> /guardar é uma página; /q-guardar é um evento de abertura; /q-guardar-kiwify é um evento de clique. As bases e a instrumentação podem diferir. Cliques legados /q-semeador não são somados aos cliques atuais do checkout.</p>'
    r=f['recente']['totais']; a=f['anterior']['totais']
    if f['incompleto']: observacao='Ainda não há janela suficiente para avaliar a evolução semanal deste bloco.'
    elif not r['checkout'] and r['guardar']: observacao='Há acessos à /guardar, mas nenhum clique de saída registrado na semana. É um ponto de atenção, não prova de abandono ou zero vendas.'
    elif not r['guardar'] and r['checkout']: observacao='Há cliques de saída sem acesso à /guardar registrado na mesma semana. Verificar limites de janela, cache e instrumentação; não presumir erro ou venda.'
    elif r['livros']>a['livros'] and r['checkout']<=a['checkout']: observacao='Os acessos às páginas dos livros aumentaram, mas os cliques de saída para o checkout não aumentaram. Merece acompanhamento, sem atribuir causa automaticamente.'
    elif r['checkout']>a['checkout']: observacao='Há mais cliques de saída registrados para o checkout. Isso não comprova aumento de vendas.'
    else: observacao='Compare a evolução da leitura, dos acessos à oferta e dos cliques de saída. Não é possível concluir a trajetória de cada pessoa pelos totais.'
    out+='<p class="foco-atencao"><b>Ponto de observação:</b> '+e(observacao)+'</p>'
    out+='<p class="nota">Este bloco não identifica quem ficou somente na leitura, quem abandonou a oferta ou quem comprou. Não é funil pareado de pessoas. Não calcula taxa de compra com cliques, IPs ou acesso à página de obrigado. Pode incluir testes e automações não reconhecidas. As ressalvas de cobertura do resumo semanal também valem aqui.</p>'
    out+='<details><summary>/guardar e checkout: dia a dia (últimos 14 dias encerrados)</summary>'+tabela(['Dia','Páginas de livros','Acessos /guardar','Aberturas /q-guardar','Cliques de saída','Cobertura'],[(data(x['dia']),numero(x['valores']['livros']),numero(x['valores']['guardar']),numero(x['valores']['abertura']),numero(x['valores']['checkout']),'Há registros aceitos; continuidade não garantida' if x['presente'] else 'Sem registros aceitos neste dia') for x in f['diarios']])+'</details></section>'
    return out+resumo


def _v8_html(d,legado=None,geo=None,antigo=None,erro=None):
    import html
    from datetime import datetime,timezone,timedelta
    pagina=_v8_html_base(d,legado,geo,antigo,erro)
    if erro or d is None:return pagina
    e=lambda v:html.escape(str(v))
    numero=lambda v:format(int(v),',').replace(',','.')
    zona=timezone(timedelta(hours=-3))
    momento=datetime.fromisoformat(d['agora']).astimezone(zona)
    f=_foco_periodos(d)
    def data(s):return datetime.fromisoformat(s).strftime('%d/%m')
    def faixa(x):return data(x['inicio'])+' a '+data(x['fim'])
    def instante(ts):
        return datetime.fromtimestamp(ts,zona).strftime('%d/%m/%Y') if ts is not None else 'sem registros'
    def tabela(titulos,linhas):
        return '<div class="resumo-tabela"><table><thead><tr>'+''.join('<th scope="col">'+e(v)+'</th>' for v in titulos)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+e(v)+'</td>' for v in r)+'</tr>' for r in linhas)+'</tbody></table></div>'
    # Reaproveita integralmente as tabelas e os criterios originais, agora fechados.
    grupos={
        'Capacidade e cobertura':'Funcionamento do painel e limites',
        'Revisão da medição: padrão de pré-carga do aplicativo':'Filtro do aplicativo: como funciona',
        'Movimento público: mesma base':'Visitas ao site, sessões e últimos dias',
        'Leitura e caminhos públicos':'Todas as páginas: acessos e hoje',
        'Ações registradas':'Ações, compartilhamentos e PDFs',
        'Contexto para interpretar a missão':'Mudanças do site e histórico da medição',
    }
    ancora='<section><h2>Capacidade e cobertura</h2>'
    if pagina.count(ancora)!=1:raise ValueError('Estrutura do painel diferente da aprovada.')
    cabeca=pagina[:pagina.index('<h1>')].replace('<title>Painel da Missão V8</title>','<title>Resumo da Missão</title>')
    detalhes=pagina[pagina.index(ancora):].partition('<footer>')[0]
    if detalhes.count('<section>')!=len(grupos) or detalhes.count('</section>')!=len(grupos):
        raise ValueError('Secoes do painel diferentes da fonte conferida.')
    for titulo,resumo in grupos.items():
        chave='<section><h2>'+titulo+'</h2>'
        if detalhes.count(chave)!=1:raise ValueError('Secao esperada ausente.')
        detalhes=detalhes.replace(chave,'<details class="resumo-detalhe"><summary>'+e(resumo)+'</summary>',1)
    detalhes=detalhes.replace('</section>','</details>')
    css='''<style>
body{max-width:1120px;padding:24px;color:#e9eef6}h1{font-size:28px;margin:0 0 6px}h2{font-size:21px;margin:0 0 12px}p{line-height:1.55}.resumo-sub{color:#b9c8da;margin:4px 0 16px;font-size:14px}.resumo-grade{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:20px 0 12px}.resumo-card{background:#172c46;border:1px solid #37536f;border-radius:12px;padding:18px;min-width:0}.resumo-card h2{font-size:15px;color:#e9eef6;line-height:1.35;min-height:40px}.resumo-card strong{display:block;color:#f2d28c;font-size:36px;line-height:1.2}.resumo-card small{display:block;color:#b9c8da;margin-top:5px}.resumo-card p{margin:14px 0 0;font-weight:bold}.resumo-venda{border-color:#9e83b9}.resumo-nota{font-size:13px;color:#b9c8da;margin:9px 0}.resumo-pagamentos{font-size:14px;padding:12px 16px;background:#202b40;border-radius:8px;margin:14px 0 22px}.resumo-semana{border:1px solid #37536f;border-radius:12px;margin:20px 0;padding:18px}.resumo-tabela{overflow-x:auto}table{display:block;max-width:100%;overflow-x:auto;width:100%;margin:10px 0;font-variant-numeric:tabular-nums}.resumo-tabela table{display:table;min-width:480px}th{color:#d7e2ee;font-size:13px}td,th{padding:11px 10px}th:not(:first-child),td:not(:first-child){text-align:right}th:first-child,td:first-child{text-align:left}.resumo-alerta{padding:12px 16px;border-left:4px solid #e4ba6b;background:#493819;color:#fff0d3;font-size:14px}.resumo-detalhe,details{border:1px solid #2e465f;border-radius:9px;margin:10px 0;padding:15px;background:#12243a}summary{line-height:1.4;color:#d8e3ef}summary:focus-visible,a:focus-visible{outline:3px solid #f2d28c;outline-offset:4px}.resumo-detalhe[open],details[open]{padding-bottom:20px}.resumo-rodape{font-size:12px;color:#aebed0;margin-top:22px}#resumo-tecnico .foco-grade{grid-template-columns:1fr}#resumo-tecnico .foco-cartao{min-width:0;overflow-wrap:anywhere}
@media(max-width:900px){.resumo-grade{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:480px){body{padding:14px}h1{font-size:24px}.resumo-grade{gap:9px}.resumo-card{padding:13px}.resumo-card strong{font-size:30px}.resumo-card h2{font-size:14px}.resumo-semana{padding:13px}td,th{padding:9px 7px;font-size:12px}.resumo-semana .resumo-tabela table{display:block;min-width:0}.resumo-semana thead{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap}.resumo-semana tbody{display:block}.resumo-semana tbody tr{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));row-gap:9px;padding:12px 0;border-bottom:1px solid #38516b}.resumo-semana td{display:block;border:0;padding:0;text-align:left!important;font-size:16px}.resumo-semana td:first-child{grid-column:1/-1;font-size:13px;font-weight:bold}.resumo-semana td:not(:first-child)::before{display:block;font-size:10px;color:#b9c8da;margin-bottom:4px}.resumo-semana td:nth-child(2)::before{content:'Anterior'}.resumo-semana td:nth-child(3)::before{content:'7 dias completos'}.resumo-semana td:nth-child(4)::before{content:'Diferença'}}
</style>'''
    out=cabeca+css+'<main><h1>Missão com Deus</h1><p class="resumo-sub">Resumo dos acessos e do sustento da missão<br>Atualizado em '+e(momento.strftime('%d/%m/%Y às %H:%M'))+' (Brasília)</p>'
    ocupacao=max(d['bytes']/d['limite_bytes'],d['contagens']['linhas_lidas']/d['limite_linhas'])
    if ocupacao>=.8:out+='<p class="resumo-alerta"><b>Atenção:</b> o painel está próximo do limite de processamento. Consulte "Funcionamento do painel e limites".</p>'
    if not d['contagens']['pagina']:out+='<p class="resumo-alerta">Nenhum acesso a página foi reconhecido neste período. Confira os detalhes antes de concluir que não houve movimento.</p>'
    out+='<p class="resumo-nota">Totais acumulados de '+e(instante(d['inicio']))+' a '+e(instante(d['fim']))+'. "Hoje" é '+e(momento.strftime('%d/%m'))+'.</p><div class="resumo-grade">'
    for k,titulo in [('livros','Acessos aos livros'),('guardar','Página de acesso completo'),('checkout','Cliques para pagamento'),('pdf','PDFs solicitados')]:
        classe=' resumo-venda' if k in ('guardar','checkout') else ''
        out+='<article class="resumo-card'+classe+'"><h2>'+e(titulo)+'</h2><strong>'+numero(f['total'][k])+'</strong><small>No período acumulado</small><p>Hoje: '+numero(f['hoje'][k])+'</p></article>'
    out+='</div><p class="resumo-nota">São registros, não pessoas. Cliques não confirmam pagamento; pedidos de PDF podem ser parciais.</p>'
    out+='<p class="resumo-pagamentos"><b>Vendas e receita:</b> conferir na Kiwify. Esses dados ainda não estão integrados ao painel.</p>'
    out+='<section class="resumo-semana"><h2>Como foi a última semana?</h2><p class="resumo-sub">Últimos 7 dias completos: '+e(faixa(f['recente']))+'<br>Semana anterior: '+e(faixa(f['anterior']))+'. Hoje fica fora da comparação.</p>'
    linhas=[]
    for k,nome in [('livros','Acessos aos livros'),('guardar','Página de acesso completo'),('checkout','Cliques para pagamento'),('pdf','PDFs solicitados')]:
        antes=f['anterior']['totais'][k];depois=f['recente']['totais'][k]
        diferenca='Não comparar' if f['incompleto'] else ('%+d'%(depois-antes) if depois!=antes else 'Sem mudança')
        linhas.append((nome,numero(antes),numero(depois),diferenca))
    out+=tabela(['Registro','Semana anterior','Últimos 7 dias','Diferença'],linhas)
    if f['avisos']:
        out+='<p class="resumo-alerta">Há ressalvas na cobertura dos dados. A comparação é apenas dos registros disponíveis.</p><details><summary>Ver cuidados desta comparação</summary><ul>'+''.join('<li>'+e(a)+'</li>' for a in f['avisos'])+'</ul></details>'
    out+='</section><details id="resumo-livros"><summary>Livros: acessos por obra</summary>'
    ordem=sorted(LIVROS_NO_AR,key=lambda p:(-d['paginas'].get(p,0),p))
    linhas=[]
    for p in ordem:
        hoje=d['dias'].get(d['hoje'],{}).get('pagina:'+p,0)
        semana=sum(v.get('pagina:'+p,0) for dia,v in d['dias'].items() if f['recente']['inicio']<=dia<=f['recente']['fim'])
        linhas.append((PAGINAS.get(p,p),numero(hoje),numero(semana),numero(d['paginas'].get(p,0))))
    out+=tabela(['Livro','Hoje','Últimos 7 dias','Acumulado'],linhas)+'</details>'
    out+='<details><summary>Acesso completo e pagamento: dia a dia</summary>'+tabela(['Dia','Livros','Página de acesso','Cliques para pagamento'],[(data(x['dia']),numero(x['valores']['livros']),numero(x['valores']['guardar']),numero(x['valores']['checkout'])) for x in f['diarios']])+'<p class="resumo-nota">Dias sem registros não comprovam ausência de público. Não é um acompanhamento individual de compradores.</p></details>'
    extras=[]
    for resumo in ('Todas as páginas: acessos e hoje','Ações, compartilhamentos e PDFs'):
        tag='<details class="resumo-detalhe"><summary>'+e(resumo)+'</summary>'
        inicio=detalhes.index(tag);fim=detalhes.index('</details>',inicio)+len('</details>')
        extras.append(detalhes[inicio:fim]);detalhes=detalhes[:inicio]+detalhes[fim:]
    out+='<h2 style="margin-top:28px">Consultar mais detalhes</h2>'+''.join(extras)
    out+='<details id="resumo-tecnico"><summary>Origens, geografia e dados técnicos</summary>'+detalhes
    out+='<details><summary>Comparações completas e abertura do acesso</summary>'+_foco_html(d)+'</details></details>'
    return out+'</main><footer class="resumo-rodape">Painel de acompanhamento da missão. Os critérios e limites continuam disponíveis acima.</footer></html>'


# VISAO_MISSAO_V3: primeira tela "visão da semana". Usa os mesmos dados e critérios do V8.
VENDAS_ARQ = os.environ.get('STATS_VENDAS', '/home/deploy/vendas_semana.txt')
_VM_LACUNAS = {'2026-10-19': 'reinício do servidor'}
_VM_CRON_MIN = 15

_VM_CSS = ('<style>'
    '.vm{max-width:1080px;margin:0 auto;color:#eef2f8;font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}'
    '.vm *{box-sizing:border-box}'
    '.vm .vm-k{color:#e0b45a;font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 6px}'
    '.vm .vm-h1{font-family:Georgia,"Times New Roman",serif;font-size:38px;line-height:1.1;margin:0 0 8px;color:#fff}'
    '.vm .vm-h2{font-family:Georgia,"Times New Roman",serif;font-size:24px;margin:42px 0 6px;color:#fff}'
    '.vm .vm-s{color:#b4c3d6;font-size:15px;line-height:1.5;margin:0 0 16px}'
    '.vm .vm-frase{background:#162a44;border:1px solid #2a4466;border-radius:14px;padding:20px 22px;'
    'font-family:Georgia,"Times New Roman",serif;font-size:22px;line-height:1.4;margin:20px 0 0;color:#eef2f8}'
    '.vm .vm-frase b{color:#e0b45a}'
    '.vm .vm-g{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}'
    '.vm .vm-c{background:#162a44;border:1px solid #2a4466;border-radius:14px;padding:18px}'
    '.vm .vm-c h3{margin:0 0 10px;font-size:15px;color:#b4c3d6;font-weight:600}'
    '.vm .vm-n{font-size:42px;font-weight:700;line-height:1;color:#fff}'
    '.vm .vm-d{margin-top:12px;font-size:15px;line-height:1.4}'
    '.vm .vm-up{color:#7cc4ff;font-weight:600}.vm .vm-dn{color:#ffb066;font-weight:600}.vm .vm-m{color:#b4c3d6}'
    '.vm .vm-tw{overflow-x:auto}'
    '.vm .vm-t{width:100%;border-collapse:collapse;font-size:15px}'
    '.vm .vm-t th,.vm .vm-t td{padding:11px 10px;border-bottom:1px solid #2a4466;text-align:right;color:#eef2f8;background:none}'
    '.vm .vm-t th:first-child,.vm .vm-t td:first-child{text-align:left}'
    '.vm .vm-t th{color:#b4c3d6;font-weight:600;font-size:13px}'
    '.vm .vm-t .vm-hi td{background:#1d3558}'
    '.vm .vm-t .vm-gr td{color:#e0b45a;font-size:12px;letter-spacing:.08em;text-transform:uppercase;text-align:left;background:none;padding-top:18px}'
    '.vm .vm-cx{background:#162a44;border:1px solid #2a4466;border-radius:14px;padding:18px 18px 12px;margin-top:14px}'
    '.vm .vm-cx h3{margin:0 0 4px;font-size:16px;color:#fff}'
    '.vm .vm-bars{display:flex;align-items:flex-end;gap:4px;height:150px;border-bottom:1px solid #2a4466;margin-top:12px}'
    '.vm .vm-b{flex:1;min-width:0;display:flex;flex-direction:column;justify-content:flex-end;align-items:center}'
    '.vm .vm-b span{font-size:11px;color:#b4c3d6;margin-bottom:3px}'
    '.vm .vm-b i{display:block;width:100%;background:#e0b45a;border-radius:3px 3px 0 0}'
    '.vm .vm-b.vm-az i{background:#7cc4ff}.vm .vm-b.vm-cz i{background:#6b7f9a}'
    '.vm .vm-lab{display:flex;gap:4px;margin-top:5px}'
    '.vm .vm-lab span{flex:1;min-width:0;text-align:center;font-size:11px;color:#b4c3d6}'
    '.vm .vm-nota{font-size:14px;line-height:1.5;color:#b4c3d6;margin:10px 0 0}'
    '.vm .vm-bar{height:8px;background:#e0b45a;border-radius:4px;min-width:2px;margin-top:6px}'
    '.vm .vm-lista{margin:12px 0 0;padding-left:22px;line-height:1.55;font-size:16px;color:#eef2f8}'
    '.vm .vm-lista li{margin-bottom:12px}'
    '.vm .vm-ph{border:2px dashed #e0b45a;border-radius:12px;padding:14px 16px;margin-top:8px;color:#e0b45a;font-size:15px}'
    '.vm .vm-fresco{background:#143f31;border-left:5px solid #69d2a1;color:#ecfff5;padding:14px 16px;border-radius:8px;margin:14px 0 4px;line-height:1.5;font-size:15px}'
    '.vm .vm-fresco.vm-velho{background:#5a1f26;border-left-color:#ff8a8a;color:#ffecec}'
    '.vm .vm-fresco b{font-size:17px}'
    '.vm .vm-alerta{background:#583d16;border-left:5px solid #ffc568;color:#fff3dd;padding:14px;border-radius:6px;margin:16px 0}'
    '.vm .vm-verso{margin:44px 0 0;font-family:Georgia,"Times New Roman",serif;font-style:italic;font-size:17px;color:#e8d9a8;line-height:1.5}'
    '.vm .vm-rod{margin-top:8px;font-size:13px;color:#b4c3d6;line-height:1.5}'
    '@media(max-width:520px){.vm .vm-h1{font-size:30px}.vm .vm-frase{font-size:19px}.vm .vm-n{font-size:36px}}'
    '</style>')


def _vm_n(n):
    return format(int(n), ',').replace(',', '.')


def _vm_dec(x, casas=1):
    return format(x, '.%df' % casas).replace('.', ',')


def _vm_var(atual, anterior):
    if not anterior:
        return None
    return (atual / float(anterior) - 1) * 100


def _vm_pct(p):
    return ('+' if p > 0 else ('−' if p < 0 else '')) + _vm_dec(abs(p), 1) + '%'


def _vm_dd(iso):
    return iso[8:10] + '/' + iso[5:7]


def _vm_linha(x):
    return dict(sessoes=int(x.get('sessoes', 0)),
                livros=sum(int(x.get('pagina:' + p, 0)) for p in LIVROS_NO_AR),
                guardar=int(x.get('pagina:/guardar', 0)),
                checkout=int(x.get('/q-guardar-kiwify', 0)))


def _vm_cartao(titulo, atual, anterior, incompleto, absoluto=False):
    if incompleto:
        dif = '<span class="vm-m">Não comparar: registros incompletos</span>'
    else:
        p = _vm_var(atual, anterior)
        if absoluto or p is None or anterior < 30:
            delta = atual - anterior
            if delta > 0:
                dif = '<span class="vm-up">▲ +%s</span>' % _vm_n(delta)
            elif delta < 0:
                dif = '<span class="vm-dn">▼ −%s</span>' % _vm_n(-delta)
            else:
                dif = '<span class="vm-m">= sem mudança</span>'
            dif += '<br><span class="vm-m">semana anterior: %s (números pequenos)</span>' % _vm_n(anterior)
        else:
            if p > 0:
                dif = '<span class="vm-up">▲ %s</span>' % _vm_pct(p)
            elif p < 0:
                dif = '<span class="vm-dn">▼ %s</span>' % _vm_pct(p)
            else:
                dif = '<span class="vm-m">= sem mudança</span>'
            dif += '<br><span class="vm-m">semana anterior: %s</span>' % _vm_n(anterior)
    return ('<div class="vm-c"><h3>%s</h3><div class="vm-n">%s</div><div class="vm-d">%s</div></div>'
            % (titulo, _vm_n(atual), dif))


def _vm_estado(p):
    if p is None:
        return None
    if p >= 10:
        return 'sobe'
    if p <= -10:
        return 'cai'
    return 'estavel'


def _vm_frase(f):
    r, a = f['recente']['totais'], f['anterior']['totais']
    if f['incompleto']:
        return 'Comparação semanal indisponível: os registros não cobrem as duas semanas.'
    ps = _vm_var(r['sessoes'], a['sessoes'])
    pl = _vm_var(r['livros'], a['livros'])
    es, el = _vm_estado(ps), _vm_estado(pl)
    if es is None or el is None:
        return 'Sem base na semana anterior para comparar.'
    s, l = _vm_pct(ps), _vm_pct(pl)
    frases = {
        ('sobe', 'cai'): 'Chegou <b>mais gente</b> (%s de sessões), mas <b>menos livros foram abertos</b> (%s).',
        ('sobe', 'sobe'): 'Chegou <b>mais gente</b> (%s de sessões) e <b>mais livros foram abertos</b> (%s).',
        ('sobe', 'estavel'): 'Chegou <b>mais gente</b> (%s de sessões), e os livros abertos ficaram estáveis (%s).',
        ('cai', 'cai'): 'Chegou <b>menos gente</b> (%s de sessões) e <b>menos livros foram abertos</b> (%s).',
        ('cai', 'sobe'): 'Chegou <b>menos gente</b> (%s de sessões), mas <b>mais livros foram abertos</b> (%s).',
        ('cai', 'estavel'): 'Chegou <b>menos gente</b> (%s de sessões), e os livros abertos ficaram estáveis (%s).',
        ('estavel', 'cai'): 'A chegada de gente ficou estável (%s de sessões), mas <b>menos livros foram abertos</b> (%s).',
        ('estavel', 'sobe'): 'A chegada de gente ficou estável (%s de sessões), e <b>mais livros foram abertos</b> (%s).',
        ('estavel', 'estavel'): 'A chegada de gente (%s de sessões) e os livros abertos (%s) ficaram estáveis.',
    }
    texto = frases[(es, el)] % (s, l)
    pg = _vm_var(r['guardar'], a['guardar'])
    if pg is not None and a['guardar'] >= 30:
        eg = _vm_estado(pg)
        verbo = {'sobe': 'subiu', 'cai': 'caiu', 'estavel': 'ficou estável'}[eg]
        texto += ' A procura pela página de acesso %s (%s).' % (verbo, _vm_pct(pg))
    return texto


def _vm_barras(dias, valores, azuis, rotulo_aria, cinzas=None):
    import html
    cinzas = set(_VM_LACUNAS) if cinzas is None else cinzas
    maximo = max(valores) if valores and max(valores) > 0 else 1
    barras, rotulos = '', ''
    for dia, v in zip(dias, valores):
        h = max(2, int(round(v / float(maximo) * 110))) if v > 0 else 1
        cls = ' vm-cz' if dia in cinzas else (' vm-az' if dia in azuis else '')
        barras += '<div class="vm-b%s"><span>%s</span><i style="height:%dpx"></i></div>' % (cls, _vm_n(v), h)
        rotulos += '<span>%s</span>' % dia[8:10]
    return ('<div class="vm-bars" role="img" aria-label="%s">%s</div><div class="vm-lab">%s</div>'
            % (html.escape(rotulo_aria), barras, rotulos))


def _vm_semanas(d, f):
    from datetime import date, datetime, timedelta, timezone
    zona = timezone(timedelta(hours=-3))
    fim = date.fromisoformat(f['recente']['fim'])
    if d['log_inicio'] is None:
        return []
    inicio_log = datetime.fromtimestamp(d['log_inicio'], zona).date()
    saida = []
    for k in range(8):
        fim_k = fim - timedelta(days=7 * k)
        ini_k = fim_k - timedelta(days=6)
        if ini_k < inicio_log:
            break
        soma = dict(sessoes=0, livros=0, guardar=0, checkout=0)
        for i in range(7):
            x = _vm_linha(d['dias'].get((ini_k + timedelta(days=i)).isoformat(), {}))
            for chave in soma:
                soma[chave] += x[chave]
        soma['inicio'] = ini_k.isoformat()
        soma['fim'] = fim_k.isoformat()
        soma['lacuna'] = any(ini_k.isoformat() <= g <= fim_k.isoformat() for g in _VM_LACUNAS)
        saida.append(soma)
    saida.reverse()
    return saida


def _vm_vendas_html():
    import html
    import re
    linhas = []
    try:
        with open(VENDAS_ARQ, 'r', encoding='utf-8') as arq:
            for lin in arq:
                lin = lin.strip()
                if not lin or lin.startswith('#'):
                    continue
                p = [x.strip() for x in lin.split(';')]
                if len(p) >= 2 and re.match(r'^\d{4}-\d{2}-\d{2}$', p[0]) and re.match(r'^\d{1,5}$', p[1]):
                    rec = p[2] if len(p) > 2 and re.match(r'^[0-9.,]{1,12}$', p[2]) else ''
                    linhas.append((p[0], int(p[1]), rec))
    except OSError:
        pass
    if not linhas:
        return ('<div class="vm-ph">[VENDAS APROVADAS NA KIWIFY NESTA SEMANA: informar]</div>'
                '<p class="vm-nota">Para o painel mostrar as vendas, crie o arquivo ' + html.escape(VENDAS_ARQ) +
                ' com uma linha por semana: AAAA-MM-DD;vendas;receita (data de início da semana).</p>')
    corpo = ''.join('<tr><td>Semana de %s</td><td>%s</td><td>%s</td></tr>' %
                    (_vm_dd(dia), _vm_n(v), ('R$ ' + html.escape(rec)) if rec else 'não informada')
                    for dia, v, rec in linhas[-8:])
    return ('<div class="vm-tw"><table class="vm-t"><thead><tr><th scope="col">Semana</th>'
            '<th scope="col">Vendas aprovadas</th><th scope="col">Receita</th></tr></thead><tbody>' + corpo +
            '</tbody></table></div><p class="vm-nota">Informado por você, a partir da Kiwify. O painel não confere estes números.</p>')


def _vm_frescor(d, momento, zona):
    from datetime import datetime
    fim = d.get('fim')
    ate = datetime.fromtimestamp(fim, zona).strftime('%d/%m/%Y às %H:%M:%S') if fim else 'sem registros'
    return ('<div class="vm-fresco" id="vm-fresco" data-gerado="%s" data-limite="%d">'
            '<b>Atualizado em %s</b> <span id="vm-idade"></span><br>'
            '<span>Registros do servidor até %s. Acessos depois dessa hora entram na próxima atualização, '
            'que o cron faz sozinho a cada %d minutos.</span></div>'
            '<script>(function(){try{var e=document.getElementById("vm-fresco");if(!e)return;'
            'var g=new Date(e.getAttribute("data-gerado")),lim=parseInt(e.getAttribute("data-limite"),10);'
            'function atualiza(){var m=Math.floor((new Date()-g)/60000),s=document.getElementById("vm-idade");'
            'if(isNaN(m)||!s)return;'
            's.textContent=m<1?"(agora há pouco)":(m<60?"(há "+m+" min)":"(há "+Math.floor(m/60)+" h "+(m%%60)+" min)");'
            'if(m>lim){e.className="vm-fresco vm-velho";s.textContent+=" Atenção: este painel está parado há mais de "+lim+" minutos. '
            'O cron pode estar parado, ou o seu navegador mostra uma cópia antiga. Atualize a página.";}}'
            'atualiza();setInterval(atualiza,30000);}catch(x){}})();</script>'
            % (momento.isoformat(), _VM_CRON_MIN * 3, momento.strftime('%d/%m/%Y às %H:%M:%S'), ate, _VM_CRON_MIN))


def _vm_bloco(d):
    import html
    from datetime import datetime, timezone, timedelta
    zona = timezone(timedelta(hours=-3))
    e = html.escape
    f = _foco_periodos(d)
    r, a = f['recente']['totais'], f['anterior']['totais']
    inc = f['incompleto']
    momento = datetime.fromisoformat(d['agora']).astimezone(zona)
    out = '<div class="vm"><p class="vm-k">Missão com Deus</p><h1 class="vm-h1">Visão da semana</h1>'
    out += ('<p class="vm-s">Últimos 7 dias completos: %s a %s. Comparados com %s a %s. '
            'Registros de acesso, não pessoas. Horários de Brasília.</p>' % (_vm_dd(f['recente']['inicio']), _vm_dd(f['recente']['fim']),
                                                                             _vm_dd(f['anterior']['inicio']), _vm_dd(f['anterior']['fim'])))
    out += _vm_frescor(d, momento, zona)
    ocupacao = max(d['bytes'] / float(d['limite_bytes']), d['contagens']['linhas_lidas'] / float(d['limite_linhas'])) * 100
    if ocupacao >= 80:
        out += ('<p class="vm-alerta"><b>Atenção:</b> o painel usa %.0f%% do limite de leitura dos registros. '
                'Avise o responsável técnico para revisar os limites com teste.</p>' % ocupacao)
    if not d['contagens']['pagina']:
        out += '<p class="vm-alerta">Nenhum acesso a página foi reconhecido neste período. Confira os detalhes antes de concluir que não houve movimento.</p>'
    out += '<p class="vm-frase">%s</p>' % _vm_frase(f)

    out += '<h2 class="vm-h2">O caminho da missão: semana contra semana</h2>'
    out += '<p class="vm-s">Da chegada até o pagamento. São registros, não pessoas, e cliques não são vendas.</p><div class="vm-g">'
    out += _vm_cartao('Chegaram (sessões)', r['sessoes'], a['sessoes'], inc)
    out += _vm_cartao('Livros abertos', r['livros'], a['livros'], inc)
    out += _vm_cartao('Página de acesso completo', r['guardar'], a['guardar'], inc)
    out += _vm_cartao('Cliques para pagar', r['checkout'], a['checkout'], inc, absoluto=True)
    out += '</div>'

    out += '<h2 class="vm-h2">A cada 100 sessões</h2>'
    out += '<p class="vm-s">Mostra o que a alta de visitas esconde: quanto da chegada vira leitura e procura pelo acesso.</p>'

    def por100(v, s):
        return (v * 100.0 / s) if s else None

    def celula(x, casas):
        return _vm_dec(x, casas) if x is not None else 'n/d'

    linhas = ''
    for nome, chave, casas, destaque in (('Livros abertos', 'livros', 1, True), ('Página de acesso completo', 'guardar', 1, False),
                                         ('Cliques para pagar', 'checkout', 2, False)):
        x0, x1 = por100(a[chave], a['sessoes']), por100(r[chave], r['sessoes'])
        seta = ''
        if not inc and x0 is not None and x1 is not None and round(x1, casas) != round(x0, casas):
            seta = ' <span class="%s">%s</span>' % (('vm-up', '▲') if x1 > x0 else ('vm-dn', '▼'))
        linhas += '<tr%s><td>%s</td><td>%s</td><td>%s%s</td></tr>' % (' class="vm-hi"' if destaque else '', nome,
                                                                      celula(x0, casas), ('<b>%s</b>' % celula(x1, casas)) if destaque else celula(x1, casas), seta)
    out += ('<div class="vm-tw"><table class="vm-t"><thead><tr><th scope="col">Registro</th><th scope="col">Semana anterior</th>'
            '<th scope="col">Últimos 7 dias</th></tr></thead><tbody>' + linhas + '</tbody></table></div>')
    out += '<p class="vm-nota">Razão entre registros e sessões, da mesma medição. Não é taxa de pessoas.</p>'

    # dia a dia
    diarios = list(reversed(f['diarios']))
    dias = [x['dia'] for x in diarios]
    sess = [x['valores']['sessoes'] for x in diarios]
    livs = [x['valores']['livros'] for x in diarios]
    positivos = sorted(v for v in sess if v > 0)
    mediana = positivos[len(positivos) // 2] if positivos else 0
    azuis = set(dia for dia, v in zip(dias, sess) if mediana and v >= 1.5 * mediana)
    out += '<h2 class="vm-h2">Dia a dia</h2><p class="vm-s">Os 14 últimos dias encerrados, de %s a %s.</p>' % (_vm_dd(dias[0]), _vm_dd(dias[-1]))
    out += ('<div class="vm-cx"><h3>Sessões por dia</h3>' +
            _vm_barras(dias, sess, azuis, 'Sessões por dia, de %s a %s. Maior valor: %s.' % (_vm_dd(dias[0]), _vm_dd(dias[-1]), _vm_n(max(sess)))) + '</div>')
    out += ('<div class="vm-cx"><h3>Livros abertos por dia</h3>' +
            _vm_barras(dias, livs, azuis, 'Livros abertos por dia, de %s a %s. Maior valor: %s.' % (_vm_dd(dias[0]), _vm_dd(dias[-1]), _vm_n(max(livs)))))
    topo = max(range(len(sess)), key=lambda i: sess[i])
    notas = 'No dia de maior movimento (%s) vieram %s sessões e foram abertos %s livros.' % (_vm_dd(dias[topo]), _vm_n(sess[topo]), _vm_n(livs[topo]))
    if azuis:
        notas += ' Barras azuis: dias com sessões de pelo menos 1,5 vez a mediana.'
    for g, motivo in _VM_LACUNAS.items():
        if g in dias:
            notas += ' Barra cinza: %s, possível lacuna no registro (%s).' % (_vm_dd(g), motivo)
    out += '<p class="vm-nota">%s</p></div>' % e(notas)

    # semanas
    semanas = _vm_semanas(d, f)
    if len(semanas) >= 3:
        out += '<h2 class="vm-h2">As últimas semanas</h2><p class="vm-s">Cada barra é uma semana de 7 dias. Uma semana sozinha engana: olhe a tendência.</p>'
        rot = [s['fim'] for s in semanas]
        cinz = set(s['fim'] for s in semanas if s['lacuna'])
        out += ('<div class="vm-cx"><h3>Sessões por semana</h3>' +
                _vm_barras(rot, [s['sessoes'] for s in semanas], set(), 'Sessões por semana, das últimas %d semanas.' % len(semanas), cinz) + '</div>')
        out += ('<div class="vm-cx"><h3>Livros abertos por semana</h3>' +
                _vm_barras(rot, [s['livros'] for s in semanas], set(), 'Livros abertos por semana, das últimas %d semanas.' % len(semanas), cinz) +
                '<p class="vm-nota">Os rótulos mostram o último dia de cada semana (dia do mês). Semana mais à direita: %s a %s. '
                'A partir de 30/09/2026, cinco livros passaram a abrir só cerca de 40%%: semanas antes e depois não medem a mesma oportunidade.</p></div>'
                % (_vm_dd(semanas[-1]['inicio']), _vm_dd(semanas[-1]['fim'])))

    # livros por obra
    hoje = d['dias'].get(d['hoje'], {})
    obras = []
    for p in LIVROS_NO_AR:
        sem = sum(d['dias'].get(dia, {}).get('pagina:' + p, 0) for dia in dias[7:])
        ant = sum(d['dias'].get(dia, {}).get('pagina:' + p, 0) for dia in dias[:7])
        obras.append((PAGINAS.get(p, p), int(hoje.get('pagina:' + p, 0)), int(sem), int(d['paginas'].get(p, 0)), int(ant)))
    obras.sort(key=lambda x: (-x[2], -x[3]))
    maxsem = max([o[2] for o in obras] + [1])
    soma_total = sum(o[3] for o in obras)
    corpo = ''.join('<tr><td>%s<div class="vm-bar" style="width:%d%%"></div></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                    (e(n), int(round(s * 100.0 / maxsem)), _vm_n(h), _vm_n(s), _vm_n(an), _vm_n(t),
                     (_vm_dec(t * 100.0 / soma_total, 1) + '%') if soma_total else 'n/d') for n, h, s, t, an in obras)
    corpo += ('<tr class="vm-hi"><td><b>Todos os livros</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td><td><b>%s</b></td></tr>' %
              (_vm_n(sum(o[1] for o in obras)), _vm_n(sum(o[2] for o in obras)), _vm_n(sum(o[4] for o in obras)), _vm_n(soma_total),
               '100%' if soma_total else 'n/d'))
    out += '<h2 class="vm-h2">Livros por obra</h2><p class="vm-s">Quais livros as pessoas mais abrem, e como cada um se mexeu de uma semana para outra. Ordenados pelos últimos 7 dias.</p>'
    out += ('<div class="vm-tw"><table class="vm-t"><thead><tr><th scope="col">Livro</th><th scope="col">Hoje</th><th scope="col">7 dias</th>'
            '<th scope="col">Semana anterior</th><th scope="col">Total</th><th scope="col">% do total</th></tr></thead><tbody>' + corpo + '</tbody></table></div>')
    out += ('<p class="vm-nota">A barra compara as obras nos últimos 7 dias. A coluna %% do total mostra a proporção de cada livro entre os %d, '
            'desde o início dos registros. Acessos a páginas de livro, não capítulos concluídos. Os downloads automáticos do aplicativo já foram descontados. '
            'Os números por livro são pequenos: uma semana sozinha não define crescimento.</p>' % len(obras))

    # Salmos, Motivação Bíblica, guias, plays e compartilhamentos
    def soma(chave, lista):
        return sum(int(d['dias'].get(dia, {}).get(chave, 0)) for dia in lista)

    def linha_item(rotulo, chave, total):
        return ('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                (e(rotulo), _vm_n(hoje.get(chave, 0)), _vm_n(soma(chave, dias[7:])), _vm_n(soma(chave, dias[:7])), _vm_n(total)))

    corpo2 = '<tr class="vm-gr"><td colspan="5">Páginas</td></tr>'
    for rot, cam in (('Salmos', '/salmos'), ('Motivação Bíblica', '/biblica'),
                     ('Guia Pais e Filhos (quiz)', '/guia-pais-filhos'), ('Filhos e Pais: O Espelho', '/guia-pais-filhos-espelho')):
        corpo2 += linha_item(PAGINAS.get(cam, rot) if cam in ('/salmos', '/biblica') else rot, 'pagina:' + cam, d['paginas'].get(cam, 0))
    corpo2 += '<tr class="vm-gr"><td colspan="5">Plays e compartilhamentos</td></tr>'
    for rot, cam in (('Palavra de hoje: plays (página interna)', '/q-palavra-play'),
                     ('Palavra compartilhada (página interna)', '/q-palavra-share'),
                     ('Livros compartilhados', '/q-livro-share'),
                     ('Cliques no WhatsApp', '/q-whats'),
                     ('Fale com a Laura (banner da Home)', '/q-laura'),
                     ('Fale com a Laura (área de alunos)', '/q-codigo')):
        corpo2 += linha_item(rot, cam, d['eventos'].get(cam, 0))
    out += '<h2 class="vm-h2">Salmos, Motivação Bíblica e compartilhamentos</h2><p class="vm-s">Além dos livros: o que as pessoas procuram e compartilham.</p>'
    out += ('<div class="vm-tw"><table class="vm-t"><thead><tr><th scope="col">Item</th><th scope="col">Hoje</th><th scope="col">7 dias</th>'
            '<th scope="col">Semana anterior</th><th scope="col">Total</th></tr></thead><tbody>' + corpo2 + '</tbody></table></div>')
    out += ('<p class="vm-nota">Números pequenos: compare com cautela. A página /palavra é interna, então os plays e compartilhamentos dela '
            'mostram o uso da própria casa, não de leitores. Um clique em compartilhar não prova que a mensagem chegou. '
            'Páginas são acessos, não leitura concluída.</p>')

    # acesso e pagamento dia a dia
    linhas = ''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                     (_vm_dd(x['dia']), _vm_n(x['valores']['livros']), _vm_n(x['valores']['guardar']), _vm_n(x['valores']['checkout']))
                     for x in f['diarios'])
    out += ('<details style="margin-top:14px"><summary style="cursor:pointer;color:#b4c3d6">Página de acesso e pagamento: dia a dia</summary>'
            '<div class="vm-tw"><table class="vm-t"><thead><tr><th scope="col">Dia</th><th scope="col">Livros</th><th scope="col">Página de acesso</th>'
            '<th scope="col">Cliques para pagar</th></tr></thead><tbody>' + linhas + '</tbody></table></div></details>')

    out += '<h2 class="vm-h2">O que acompanhar toda semana</h2><ol class="vm-lista">'
    out += '<li><b>Sessões.</b> Mostram a chegada de gente.</li>'
    out += '<li><b>Livros abertos a cada 100 sessões.</b> Se cai, chegou gente que não entra nos livros.</li>'
    out += '<li><b>Livros por obra.</b> Quais sobem e quais caem.</li>'
    out += '<li><b>Salmos, Motivação Bíblica e compartilhamentos.</b> O que as pessoas procuram além dos livros e o que repassam.</li>'
    out += '<li><b>Página de acesso e cliques para pagar.</b> Os números são pequenos: olhe os dois juntos, sem concluir por uma semana só.</li>'
    out += '<li><b>Vendas aprovadas na Kiwify.</b> É o que mais importa, e o painel não tem esse dado. ' + _vm_vendas_html() + '</li>'
    out += ('<li><b>Origem das visitas.</b> Fica em Origens, geografia e dados técnicos. Nos links dos Reels, use ?utm_source=instagram '
            'e ?utm_source=tiktok para o painel enxergar de onde vem.</li></ol>')

    out += '<h2 class="vm-h2">Como ler este painel</h2>'
    out += ('<p class="vm-s">Sessões, aberturas e cliques são registros do servidor, não pessoas. Clique para pagamento não é venda. '
            'Dias com possível lacuna aparecem em cinza. Semanas anteriores a 21/10/2026 foram recalculadas sem os downloads automáticos '
            'do aplicativo, e os painéis antigos não se comparam com este.</p>')
    out += ('<p class="vm-verso">“Eu plantei, Apolo regou; mas Deus deu o crescimento.” 1 Coríntios 3:6 (ACF)</p>'
            '<p class="vm-rod">Os números são registros. A honra é do Senhor.</p></div>')
    return out, f, obras, semanas, dias, sess, livs


def _vm_conferir(f, obras, dias, sess, livs):
    falhas = []
    if sum(o[2] for o in obras) != f['recente']['totais']['livros']:
        falhas.append('livros por obra (7 dias) não fecha com o total semanal')
    if sum(o[4] for o in obras) != f['anterior']['totais']['livros']:
        falhas.append('livros por obra (semana anterior) não fecha com o total semanal')
    if sum(livs[7:]) != f['recente']['totais']['livros'] or sum(livs[:7]) != f['anterior']['totais']['livros']:
        falhas.append('barras diárias de livros não fecham com as semanas')
    if sum(sess[7:]) != f['recente']['totais']['sessoes'] or sum(sess[:7]) != f['anterior']['totais']['sessoes']:
        falhas.append('barras diárias de sessões não fecham com as semanas')
    return falhas


def _visao_montar(pagina, d):
    ini = '<main><h1>Missão com Deus</h1>'
    fim = '<h2 style="margin-top:28px">Consultar mais detalhes</h2>'
    if pagina.count(ini) != 1 or pagina.count(fim) != 1:
        raise ValueError('estrutura do resumo anterior diferente da esperada')
    bloco, f, obras, semanas, dias, sess, livs = _vm_bloco(d)
    falhas = _vm_conferir(f, obras, dias, sess, livs)
    if falhas:
        raise ValueError('conferência interna falhou: ' + '; '.join(falhas))
    a = pagina.index(ini)
    b = pagina.index(fim)
    novo = pagina[:a] + _VM_CSS + '<main>' + bloco + pagina[b:]
    return novo.replace('<title>Resumo da Missão</title>', '<title>Missão com Deus: visão da semana</title>', 1)


_v8_html_resumo_anterior = _v8_html


def _v8_html(d, legado=None, geo=None, antigo=None, erro=None):
    pagina = _v8_html_resumo_anterior(d, legado, geo, antigo, erro)
    if erro or d is None:
        return pagina
    try:
        return _visao_montar(pagina, d)
    except Exception as ex:
        print('VISAO: usando o resumo anterior. Motivo:', ex)
        return pagina


if __name__ == '__main__':
    _v8_main()
