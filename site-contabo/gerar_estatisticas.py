# -*- coding: utf-8 -*-
import os, re, html
from collections import Counter, OrderedDict
from datetime import datetime, timedelta

LOG     = '/www/wwwlogs/compraoseu.com.log'
OUT     = '/www/wwwroot/compraoseu.com/stats.html'
OUT2    = '/www/wwwroot/missaocomdeus.com.br/stats.html'
DOMINIO = 'missaocomdeus.com.br'

PAGINAS = OrderedDict([
    ('/',        'Home (inicio)'),
    ('/livro01', 'Livro 01 - O Verbo que Transforma'),
    ('/livro02', 'Livro 02 - A Sabedoria dos Mestres'),
    ('/livro03', 'Livro 03 - A Mente Renovada'),
    ('/livro04', 'Livro 04 - Um Segundo com Deus'),
    ('/livro05', 'Livro 05 - Evolucao da Alma'),
    ('/livro06', 'Livro 06 - Jesus Quer Falar com Seu Filho'),
    ('/livro07', 'Livro 07 - O Caminho do Despertar'),
    ('/livro08', 'Livro 08 - O Arquiteto da Realidade'),
    ('/livro09', 'Livro 09 - Anestesia Mental'),
    ('/livro10', 'Livro 10 - O Despertar do Observador'),
    ('/livro11', 'Livro 11 - O Novo Testamento como nunca lido'),
    ('/livro12', 'Livro 12 - Afirmacoes, Declaracoes e Oracoes'),
    ('/quiz',    'Quiz - Autoavaliacao'),
])

PAGINAS_LEGITIMAS = ['/enquete.php', '/enquete', '/stats', '/stats.html', '/leitor']

RE_LINHA   = re.compile(r'^(\S+) .*?\[([^\]]+)\] "GET (\S+) HTTP')
RE_EXT     = re.compile(r'\.(png|jpg|jpeg|gif|svg|ico|css|js|woff2?|webp|xml|json|txt|webmanifest)$', re.I)
RE_BOT_URL = re.compile(
    r'/(wp-|xmlrpc|\.env|\.git|\.aws|info\.php|phpinfo|\.htaccess|admin\.php'
    r'|222\.php|1\.php|shell|cmd\.php|\.bak|\.sql|\.yml|\.yaml|config\.php'
    r'|actuator|telescope|this_is_a_new|filemanager)', re.I)
RE_BOT_UA  = re.compile(
    r'(bot|crawler|spider|scanner|curl|wget|python-requests|Go-http-client'
    r'|sqlmap|nikto|nmap|masscan|ZmEu|acunetix|java/|okhttp|headless'
    r'|GPTBot|CCBot|Ahrefs|Semrush|YandexBot|Googlebot|bingbot)', re.I)


def fmt(n):
    return '{:,}'.format(int(n)).replace(',','.')
def eh_bot(path, ua):
    if path in ('/', ''): return False
    if RE_BOT_URL.search(path): return True
    if ua and RE_BOT_UA.search(ua): return True
    return False

def analisar():
    contagens = Counter()
    contagens_hoje = Counter()
    contagens_ataques = Counter()
    contagens_legitimas = Counter()
    total_geral = total_real = total_bots = 0
    data_inicio = data_fim = None
    por_dia = Counter()
    por_dia_real = Counter()
    agora      = datetime.now()
    hoje_str   = agora.strftime('%d/%m/%Y')
    ontem_str  = (agora - timedelta(days=1)).strftime('%d/%m/%Y')
    data_ontem = agora.date() - timedelta(days=1)
    ontem_mesmo_horario = 0
    ontem_mesmo_horario_real = 0
    if not os.path.exists(LOG):
        return None, 'Log nao encontrado: ' + LOG
    with open(LOG, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            m = RE_LINHA.match(linha)
            if not m: continue
            ip, data_raw, url = m.group(1), m.group(2), m.group(3)
            if RE_EXT.search(url): continue
            path = url.split('?')[0].rstrip('/')
            if path == '': path = '/'
            ua  = linha.rsplit('"', 2)[-2] if linha.count('"') >= 4 else ''
            bot = eh_bot(path, ua)
            total_geral += 1
            if bot:
                total_bots += 1
                contagens_ataques[path] += 1
            else:
                total_real += 1
                if path in PAGINAS:
                    contagens[path] += 1
                elif any(path.startswith(p) for p in PAGINAS_LEGITIMAS):
                    contagens_legitimas[path] += 1
            try:
                dt    = datetime.strptime(data_raw.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
                chave = dt.strftime('%d/%m/%Y')
                por_dia[chave] += 1
                if not bot: por_dia_real[chave] += 1
                if chave == hoje_str and path in PAGINAS:
                    contagens_hoje[path] += 1
                if dt.date() == data_ontem and (dt.hour, dt.minute) <= (agora.hour, agora.minute):
                    ontem_mesmo_horario += 1
                    if not bot: ontem_mesmo_horario_real += 1
                if data_inicio is None or dt < data_inicio: data_inicio = dt
                if data_fim    is None or dt > data_fim:    data_fim    = dt
            except: pass
    total_hoje      = por_dia.get(hoje_str,  0)
    total_ontem     = por_dia.get(ontem_str, 0)
    total_hoje_real = por_dia_real.get(hoje_str, 0)
    if ontem_mesmo_horario > 0:
        variacao = (total_hoje - ontem_mesmo_horario) / ontem_mesmo_horario * 100
    else:
        variacao = 100.0 if total_hoje > 0 else 0.0
    if ontem_mesmo_horario_real > 0:
        variacao_real = (total_hoje_real - ontem_mesmo_horario_real) / ontem_mesmo_horario_real * 100
    else:
        variacao_real = 100.0 if total_hoje_real > 0 else 0.0
    horas = agora.hour + agora.minute / 60.0
    projecao      = int(round(total_hoje      / horas * 24)) if horas > 0 else 0
    projecao_real = int(round(total_hoje_real / horas * 24)) if horas > 0 else 0
    return (contagens, contagens_hoje, contagens_ataques, contagens_legitimas,
            total_geral, total_real, total_bots, data_inicio, data_fim,
            por_dia, por_dia_real, total_hoje, total_ontem, ontem_mesmo_horario,
            variacao, projecao, total_hoje_real, variacao_real, projecao_real,
            hoje_str, ontem_str), None

CSS = """
:root{--navy:#0e1a2e;--gold:#c9a24b;--green:#7fe0a3;--red:#e07b6b;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Segoe UI",system-ui,sans-serif;background:var(--navy);color:#e8ecf3;line-height:1.5;}
.wrap{max-width:980px;margin:0 auto;padding:24px 16px 60px;}
h1{color:var(--gold);font-size:1.6rem;margin-bottom:4px;}
.sub{color:#9fb0c8;font-size:.9rem;margin-bottom:24px;}
.badge{font-size:.65rem;background:rgba(201,162,75,.2);color:var(--gold);padding:2px 8px;border-radius:4px;margin-left:8px;vertical-align:middle;}
.badge-red{background:rgba(224,123,107,.15);color:var(--red);}
.badge-green{background:rgba(127,224,163,.15);color:var(--green);}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;margin-bottom:24px;}
.card{background:#16283f;border:1px solid rgba(201,162,75,.25);border-radius:10px;padding:16px;text-align:center;}
.card .v{font-size:1.6rem;font-weight:700;color:var(--gold);}
.card .l{font-size:.75rem;color:#9fb0c8;text-transform:uppercase;letter-spacing:.06em;}
.card .periodo{font-size:.62rem;color:#4a6a8a;margin-top:3px;}
.card.destaque{border-color:var(--gold);background:linear-gradient(180deg,#1a2c47,#16283f);}
.card.verde{border-color:var(--green);}
.card.vermelho{border-color:var(--red);}
table{width:100%;border-collapse:collapse;background:#16283f;border-radius:10px;overflow:hidden;margin-bottom:24px;}
th{background:rgba(201,162,75,.15);color:var(--gold);text-align:left;padding:10px 12px;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;}
td{padding:10px 12px;border-top:1px solid rgba(201,162,75,.1);font-size:.92rem;vertical-align:middle;}
.num{text-align:center;white-space:nowrap;}
.url{color:#7f92ad;font-size:.75rem;}
.barra{background:#0e1a2e;border-radius:6px;height:10px;overflow:hidden;min-width:80px;}
.fill{background:linear-gradient(90deg,#c9a24b,#e3c877);height:100%;border-radius:6px;}
h2{color:var(--gold);font-size:1.1rem;margin:32px 0 10px;}
.bloco-comp{background:#16283f;border:1px solid rgba(201,162,75,.2);border-radius:10px;padding:16px 20px;margin-bottom:16px;display:flex;gap:20px;flex-wrap:wrap;align-items:center;}
.bloco-comp .item{flex:1;min-width:120px;}
.bloco-comp .rot{font-size:.72rem;color:#9fb0c8;text-transform:uppercase;letter-spacing:.05em;}
.bloco-comp .val{font-size:1.4rem;font-weight:700;color:#fff;}
.bloco-comp .val.gold{color:var(--gold);}
.bloco-comp .val.green{color:var(--green);}
.bloco-comp .val.red{color:var(--red);}
.nota{font-size:.78rem;color:#9fb0c8;margin:6px 0 20px;line-height:1.6;}
.nota b{color:#e3c877;}
hr{border:none;border-top:1px solid rgba(201,162,75,.15);margin:32px 0;}
footer{text-align:center;color:#7f92ad;font-size:.78rem;margin-top:40px;}
"""

def gerar():
    res, err = analisar()
    if err:
        print('ERRO:', err)
        return
    (contagens, contagens_hoje, contagens_ataques, contagens_legitimas,
     total_geral, total_real, total_bots, data_inicio, data_fim,
     por_dia, por_dia_real, total_hoje, total_ontem, ontem_mesmo_horario,
     variacao, projecao, total_hoje_real, variacao_real, projecao_real,
     hoje_str, ontem_str) = res

    agora     = datetime.now()
    gerado_em = agora.strftime('%d/%m/%Y %H:%M')
    hora_atual = agora.strftime('%H:%M')
    seta      = '↑' if variacao      > 0 else ('↓' if variacao      < 0 else '↓')
    seta_real = '↑' if variacao_real > 0 else ('↓' if variacao_real < 0 else '↓')
    var_cor      = 'green' if variacao      >= 0 else 'red'
    var_real_cor = 'green' if variacao_real >= 0 else 'red'
    total_home   = contagens.get('/', 0)
    total_livros = sum(contagens.get(p, 0) for p in PAGINAS if p.startswith('/livro'))
    livros_lidos = sum(1 for p in PAGINAS if p.startswith('/livro') and contagens.get(p, 0) > 0)
    taxa_humana  = '{:.1f}%'.format(total_real / total_geral * 100) if total_geral else '0%'
    periodo = '-'
    if data_inicio and data_fim:
        periodo = '{} ate {}'.format(
            data_inicio.strftime('%d/%m/%Y'),
            data_fim.strftime('%d/%m/%Y %H:%M'))

    itens = sorted(
        [(p, contagens.get(p,0), PAGINAS[p], contagens_hoje.get(p,0)) for p in PAGINAS],
        key=lambda x: -x[1])
    max_n = itens[0][1] if itens and itens[0][1] > 0 else 1

    linhas_ranking = ''
    for i, (path, n, nome, n_hoje) in enumerate(itens, 1):
        pct_barra = n / max_n * 100
        pct_num   = n / total_geral * 100 if total_geral else 0
        medalha   = {1:'#1',2:'#2',3:'#3'}.get(i, str(i))
        hoje_txt  = '<span style="color:#7fe0a3">+' + str(n_hoje) + ' hoje</span>' if n_hoje else ''
        linhas_ranking += (
            '<tr>'
            '<td class="num">' + medalha + '</td>'
            '<td><a href="https://' + DOMINIO + path + '" target="_blank">' + nome + '</a>'
            '<br><span class="url">' + path + '</span></td>'
            '<td class="num">' + str(n) + ' ' + hoje_txt + '</td>'
            '<td class="num">{:.1f}%</td>'.format(pct_num) +
            '<td><div class="barra"><div class="fill" style="width:{:.1f}%"></div></div></td>'.format(pct_barra) +
            '</tr>\n')

    linhas_dias = ''
    for d, n in sorted(por_dia.items(), key=lambda x: x[0], reverse=True)[:7]:
        real = por_dia_real.get(d, 0)
        pct  = '{:.0f}%'.format(real/n*100) if n else '0%'
        dest = ' style="color:var(--gold);font-weight:700"' if d == hoje_str else ''
        label = ' (hoje)' if d == hoje_str else ''
        linhas_dias += (
            '<tr><td' + dest + '>' + d + label + '</td>'
            '<td class="num">' + str(n) + '</td>'
            '<td class="num" style="color:#7fe0a3">' + str(real) + '</td>'
            '<td class="num">' + pct + '</td></tr>\n')

    linhas_legitimas = ''
    for path, n in sorted(contagens_legitimas.items(), key=lambda x: -x[1])[:10]:
        linhas_legitimas += '<tr><td>' + html.escape(path) + '</td><td class="num">' + str(n) + '</td></tr>\n'
    if not linhas_legitimas:
        linhas_legitimas = '<tr><td colspan="2" style="color:#9fb0c8">Nenhuma pagina adicional</td></tr>'

    linhas_ataques = ''
    for path, n in sorted(contagens_ataques.items(), key=lambda x: -x[1])[:15]:
        linhas_ataques += (
            '<tr><td style="color:#e07b6b">' + html.escape(path) + '</td>'
            '<td class="num">' + str(n) + '</td>'
            '<td class="num" style="color:#7fe0a3">Bloqueado</td></tr>\n')
    if not linhas_ataques:
        linhas_ataques = '<tr><td colspan="3" style="color:#9fb0c8">Nenhum ataque registrado</td></tr>'

    doc = (
        '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="noindex, nofollow">\n'
        '<title>Estatisticas - Portal O Despertar</title>\n'
        '<style>' + CSS + '</style>\n'
        '</head>\n<body>\n<div class="wrap">\n'
        '<h1>Estatisticas de Acesso</h1>\n'
        '<p class="sub">Portal O Despertar &middot; ' + DOMINIO + ' &middot; gerado em ' + gerado_em + '</p>\n'

        '<h2>Desempenho de Hoje <span class="badge">parcial ate ' + hora_atual + '</span></h2>\n'
        '<div class="bloco-comp">'
        '<div class="item"><div class="rot">Acessos brutos hoje</div><div class="val gold">' + fmt(total_hoje) + '</div></div>'
        '<div class="item"><div class="rot">Visitas humanas hoje</div><div class="val green">' + fmt(total_hoje_real) + '</div></div>'
        '<div class="item"><div class="rot">Ontem ate este horario</div><div class="val">' + fmt(ontem_mesmo_horario) + '</div></div>'
        '<div class="item"><div class="rot">Variacao bruta</div><div class="val ' + var_cor + '">' + seta + ' {:.1f}%</div></div>'.format(variacao) +
        '<div class="item"><div class="rot">Projecao bruta</div><div class="val gold">~' + fmt(projecao) + '</div></div>'
        '<div class="item"><div class="rot">Projecao real</div><div class="val green">~' + fmt(projecao_real) + '</div></div>'
        '</div>\n'
        '<p class="nota">Comparacao justa: hoje parcial vs ontem ate ' + hora_atual + '. '
        '<b>Visitas humanas</b> excluem bots. '
        'Variacao real: <b>' + seta_real + ' {:.1f}%</b></p>\n'.format(variacao_real) +

        '<hr>\n'
        '<h2>Resumo do Periodo <span class="badge">acumulado de ' + periodo + '</span></h2>\n'
        '<div class="cards">'
        '<div class="card destaque"><div class="v">' + fmt(total_geral) + '</div><div class="l">Total bruto</div><div class="periodo">requisicoes no periodo</div></div>'
        '<div class="card verde"><div class="v" style="color:var(--green)">' + fmt(total_real) + '</div><div class="l">Visitas humanas</div><div class="periodo">acumulado no periodo</div></div>'
        '<div class="card vermelho"><div class="v" style="color:var(--red)">' + fmt(total_bots) + '</div><div class="l">Bots bloqueados</div><div class="periodo">acumulado no periodo</div></div>'
        '<div class="card"><div class="v">' + taxa_humana + '</div><div class="l">Taxa humana</div><div class="periodo">do total de acessos</div></div>'
        '</div>\n'

        '<hr>\n'
        '<h2>Conteudos Acessados <span class="badge">visualizacoes acumuladas no periodo</span></h2>\n'
        '<div class="cards">'
        '<div class="card destaque"><div class="v">' + fmt(total_home) + '</div><div class="l">Visualizacoes da Home</div><div class="periodo">acumulado no periodo</div></div>'
        '<div class="card destaque"><div class="v">' + fmt(total_livros) + '</div><div class="l">Visualizacoes dos Livros</div><div class="periodo">acumulado no periodo</div></div>'
        '<div class="card"><div class="v">' + str(livros_lidos) + '</div><div class="l">Livros com leitores</div><div class="periodo">de 12 disponiveis</div></div>'
        '<div class="card"><div class="v">' + str(contagens.get('/quiz',0)) + '</div><div class="l">Quiz</div><div class="periodo">acumulado no periodo</div></div>'
        '</div>\n'
        '<p class="nota"><b>Visualizacoes nao sao pessoas unicas.</b> '
        'Uma pessoa que abre a Home e 3 livros gera 4 visualizacoes.</p>\n'

        '<hr>\n'
        '<h2>Ranking dos Livros <span class="badge">acumulado no periodo</span></h2>\n'
        '<table><tr><th>#</th><th>Pagina</th><th>Visualizacoes (total / hoje)</th><th>%</th><th>Proporcao</th></tr>\n'
        + linhas_ranking +
        '</table>\n'

        '<h2>Acessos por Dia <span class="badge">ultimos 7 dias</span></h2>\n'
        '<table><tr><th>Dia</th><th>Acessos brutos</th><th>Visitas humanas</th><th>% humano</th></tr>\n'
        + linhas_dias +
        '</table>\n'

        '<hr>\n'
        '<h2>Outras Paginas Legitimas <span class="badge">acumulado</span></h2>\n'
        '<table><tr><th>Pagina</th><th>Acessos</th></tr>\n'
        + linhas_legitimas +
        '</table>\n'

        '<h2>Tentativas de Ataque Bloqueadas <span class="badge badge-red">seguranca</span></h2>\n'
        '<table><tr><th>Rota atacada</th><th>Tentativas</th><th>Status</th></tr>\n'
        + linhas_ataques +
        '</table>\n'

        '<footer>Periodo: ' + periodo + ' &middot; Portal O Despertar &middot; ' + DOMINIO + '<br>\n'
        'Atualizado pelo cron &middot; Protegido (noindex) &middot; Apenas para o administrador</footer>\n'
        '</div>\n</body>\n</html>')

    for saida in [OUT, OUT2]:
        if os.path.isdir(os.path.dirname(saida)):
            with open(saida, 'w', encoding='utf-8') as f:
                f.write(doc)
            print('OK: ' + saida)

if __name__ == '__main__':
    gerar()
