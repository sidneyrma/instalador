# -*- coding: utf-8 -*-
"""
Painel de estatísticas v2 — compraoseu.com (MODO PRUDENTE)

Novidades em relação à v1 (as "sugestões 1 e 2" da auditoria de 18/08):

SUGESTÃO 1 — FILTROS (contar só gente de verdade):
  a) Só conta respostas 200/304 (página realmente entregue). Ataques
     bloqueados (444), erros (404) e redirecionamentos ficam DE FORA.
  b) Só conta se o User-Agent NÃO for robô (Googlebot, Bingbot, curl,
     python, scanners, prévias de WhatsApp/Facebook etc.).
  c) User-Agent vazio ("-") é descartado (navegador real sempre se identifica).

SUGESTÃO 2 — VISITANTES ÚNICOS (o número mais próximo de "pessoas"):
  Conta IPs diferentes por dia (hoje, ontem e total). 1 pessoa que lê
  5 livros continua sendo 1 visitante — como as plataformas profissionais.

TRANSPARÊNCIA: o painel também mostra quantas requisições foram
descartadas (robôs declarados e ataques/erros), para nada ficar escondido.

Para atualizar sozinho, agende no aaPanel (igual à v1):
  Cron -> Shell -> a cada 1h:  python3 /home/deploy/gerar_estatisticas.py

Gera: /www/wwwroot/compraoseu.com/stats.html
"""
import os
import re
import html
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime, timedelta

LOG = os.environ.get('STATS_LOG', '/www/wwwlogs/missaocomdeus.com.br.log')
OUT = os.environ.get('STATS_OUT', '/www/wwwroot/missaocomdeus.com.br/stats.html')

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

# Linha completa do log (formato padrão aaPanel/Nginx "combined"):
# IP - - [data] "GET url HTTP/1.x" status bytes "referer" "user-agent"
RE_COMPLETA = re.compile(
    r'^(\S+) \S+ \S+ \[([^\]]+)\] "GET (\S+) HTTP[^"]*" (\d{3}) \S+ "[^"]*" "([^"]*)"')
# Reserva (formato antigo, sem UA) — usada só se a completa não casar
RE_SIMPLES = re.compile(r'^(\S+) .*?\[([^\]]+)\] "GET (\S+) HTTP')
RE_EXT = re.compile(
    r'\.(png|jpg|jpeg|gif|svg|ico|css|js|woff2?|webp|xml|json|txt|webmanifest)$', re.I)

# Robôs declarados e ferramentas de máquina (não são leitores)
RE_BOT = re.compile(
    r'bot|crawl|spider|slurp|scan|monitor|probe|python|curl|wget|httpclient|'
    r'go-http|libwww|java/|okhttp|headless|lighthouse|pingdom|uptime|'
    r'facebookexternalhit|whatsapp|telegrambot|twitterbot|linkedinbot|'
    r'semrush|ahrefs|mj12|dotbot|petalbot|bytespider|zgrab|masscan|nuclei', re.I)


def analisar():
    contagens = Counter()
    contagens_hoje = Counter()
    total_geral = 0
    data_inicio = None
    data_fim = None
    por_dia = Counter()
    visitantes_por_dia = defaultdict(set)   # dia -> {ips humanos}
    visitantes_total = set()
    descartados_robos = 0                   # user-agent de robô
    descartados_erros = 0                   # 444/404/etc (ataques e erros)
    robos_por_dia = Counter()
    erros_por_dia = Counter()

    agora = datetime.now()
    hoje_str = agora.strftime('%d/%m/%Y')
    ontem = (agora - timedelta(days=1)).strftime('%d/%m/%Y')
    data_ontem = agora.date() - timedelta(days=1)
    acessos_ontem_mesmo_horario = 0

    if not os.path.exists(LOG):
        return None, 'Log não encontrado: ' + LOG

    with open(LOG, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            m = RE_COMPLETA.match(linha)
            if m:
                ip, data, url, status, ua = (m.group(1), m.group(2), m.group(3),
                                             m.group(4), m.group(5))
            else:
                m = RE_SIMPLES.match(linha)
                if not m:
                    continue
                ip, data, url = m.group(1), m.group(2), m.group(3)
                status, ua = '200', 'desconhecido'
            if RE_EXT.search(url):
                continue

            # dia da linha (para registrar também os descartes por dia)
            chave_dia = None
            dt = None
            try:
                dt = datetime.strptime(data.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
                chave_dia = dt.strftime('%d/%m/%Y')
            except Exception:
                pass

            # ---------- SUGESTÃO 1: FILTROS ----------
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
            # -----------------------------------------

            path = url.split('?')[0].rstrip('/')
            if path == '':
                path = '/'
            if path.endswith('.html'):
                path = path[:-5]
                if path == '/index':
                    path = '/'
            if path in PAGINAS or path.startswith('/livro'):
                contagens[path] += 1
            else:
                contagens['/outros:' + path] += 1
            total_geral += 1

            if dt is not None:
                por_dia[chave_dia] += 1
                # ---------- SUGESTÃO 2: VISITANTES ÚNICOS ----------
                visitantes_por_dia[chave_dia].add(ip)
                visitantes_total.add(ip)
                # ----------------------------------------------------
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
    if horas_decorridas > 0:
        projecao = int(round(total_hoje / horas_decorridas * 24))
    else:
        projecao = total_hoje

    unicos_hoje = len(visitantes_por_dia.get(hoje_str, set()))
    unicos_ontem = len(visitantes_por_dia.get(ontem, set()))
    unicos_total = len(visitantes_total)

    return (contagens, total_geral, data_inicio, data_fim, por_dia,
            contagens_hoje, total_hoje, total_ontem, variacao, hoje_str, ontem,
            acessos_ontem_mesmo_horario, projecao,
            unicos_hoje, unicos_ontem, unicos_total, visitantes_por_dia,
            descartados_robos, descartados_erros, robos_por_dia, erros_por_dia), None


def montar_html(res):
    (contagens, total_geral, data_inicio, data_fim, por_dia,
     contagens_hoje, total_hoje, total_ontem, variacao, hoje_str, ontem,
     ontem_mesmo_horario, projecao,
     unicos_hoje, unicos_ontem, unicos_total, visitantes_por_dia,
     descartados_robos, descartados_erros, robos_por_dia, erros_por_dia) = res

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
          <td><a href="https://missaocomdeus.com.br{path}">{html.escape(nome)}</a><br><span class="url">{path}</span></td>
          <td class="num">{n} {hoje_txt}</td>
          <td class="num">{pct:.1f}%</td>
          <td><div class="barra"><div class="fill" style="width:{min(100,pct)}%"></div></div></td>
        </tr>""")

    dias = por_dia.most_common(7)
    dias.sort(key=lambda x: x[0], reverse=True)
    linhas_dias = '\n'.join(
        f'<tr><td>{d}</td><td class="num">{n}</td>'
        f'<td class="num" style="color:#7fe0a3">{len(visitantes_por_dia.get(d, set()))}</td>'
        f'<td class="num" style="color:#9fb0c8">{robos_por_dia.get(d, 0) + erros_por_dia.get(d, 0)}</td></tr>'
        for d, n in dias
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

    periodo = '—'
    if data_inicio and data_fim:
        periodo = f'{data_inicio.strftime("%d/%m/%Y %H:%M")} até {data_fim.strftime("%d/%m/%Y %H:%M")}'

    html_doc = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>📊 Estatísticas de Acesso — Portal O Despertar</title>
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
  .card.destaque {{ border-color:var(--gold); background:linear-gradient(180deg,#1a2c47,#16283f); }}
  .card.humano .v {{ color:#7fe0a3; }}
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
</style>
</head>
<body>
<div class="wrap">
  <h1>📊 Estatísticas de Acesso <span class="selo-filtro">✅ v2 — só leitores reais</span></h1>
  <p class="sub">Portal O Despertar · missaocomdeus.com.br · gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>

  <div class="comparacao">
    <div class="bloco">
      <div class="rot">Ontem completo ({ontem})</div>
      <div class="val">{total_ontem}</div>
    </div>
    <div class="bloco">
      <div class="rot">Hoje até agora ({hoje_str})</div>
      <div class="val gold">{total_hoje}</div>
    </div>
    <div class="bloco">
      <div class="rot">Ontem até este horário</div>
      <div class="val">{ontem_mesmo_horario}</div>
    </div>
    <div class="bloco">
      <div class="rot">Variação (justa)</div>
      <div class="val gold">{seta} {variacao:+.1f}%</div>
    </div>
    <div class="bloco">
      <div class="rot">Projeção do dia</div>
      <div class="val gold">~{projecao}</div>
    </div>
    <div class="bloco">
      <div class="rot">Total geral</div>
      <div class="val">{total_geral}</div>
    </div>
  </div>

  <div class="comparacao" style="border-color:rgba(127,224,163,.4);">
    <div class="bloco">
      <div class="rot">👤 Visitantes únicos HOJE</div>
      <div class="val verde">{unicos_hoje}</div>
    </div>
    <div class="bloco">
      <div class="rot">👤 Visitantes únicos ONTEM</div>
      <div class="val verde">{unicos_ontem}</div>
    </div>
    <div class="bloco">
      <div class="rot">👤 Visitantes únicos TOTAL</div>
      <div class="val verde">{unicos_total}</div>
    </div>
    <div class="bloco">
      <div class="rot">🤖 Robôs descartados</div>
      <div class="val" style="font-size:1.1rem;">{descartados_robos}</div>
    </div>
    <div class="bloco">
      <div class="rot">🛡️ Ataques/erros descartados</div>
      <div class="val" style="font-size:1.1rem;">{descartados_erros}</div>
    </div>
  </div>
  <p style="font-size:.8rem;color:#9fb0c8;margin:-18px 0 24px;">Contagem prudente: só entram páginas realmente entregues (código 200/304) a navegadores de gente (robôs declarados, prévias de link e ataques ficam de fora — os descartes aparecem aí em cima, com transparência). "Visitantes únicos" = IPs diferentes no dia: o número mais próximo de PESSOAS.</p>

  <div class="cards">
    <div class="card destaque"><div class="v">{total_home}</div><div class="l">Visitas à Home</div></div>
    <div class="card destaque"><div class="v">{total_livros}</div><div class="l">Acessos aos livros</div></div>
    <div class="card"><div class="v">{livros_lidos}</div><div class="l">Livros lidos</div></div>
    <div class="card"><div class="v">{contagens.get('/guia-pais-filhos',0)}</div><div class="l">Quiz Pais e Filhos</div></div>
    <div class="card humano"><div class="v">{unicos_total}</div><div class="l">Pessoas (IPs únicos)</div></div>
  </div>

  <h2>🏆 Ranking (Home + Livros + Quiz)</h2>
  <table>
    <tr><th>#</th><th>Página</th><th>Acessos (total · hoje)</th><th>%</th><th>Distribuição</th></tr>
    {''.join(linhas)}
  </table>

  <h2>📅 Acessos por dia (últimos 7)</h2>
  <table>
    <tr><th>Dia</th><th>Páginas vistas (humanos)</th><th>👤 Visitantes únicos</th><th>🤖 Descartados</th></tr>
    {linhas_dias}
  </table>

  <h2>📄 Outras páginas acessadas</h2>
  <table>
    <tr><th>Página</th><th>Acessos</th></tr>
    {linhas_outros}
  </table>

  <footer>Período registrado: {periodo} · Missão com Deus · Coleção do Despertar<br>
  Painel v2 (filtros de robôs + visitantes únicos) atualizado pelo script (cron). Página protegida (noindex) — apenas para o administrador.</footer>
</div>
</body>
</html>"""
    return html_doc


def main():
    res, err = analisar()
    if err:
        print('ERRO:', err)
        return
    doc = montar_html(res)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(doc)
    print('✅ stats.html gerado em', OUT)
    print('   Acesse: https://missaocomdeus.com.br/stats.html')


if __name__ == '__main__':
    main()
