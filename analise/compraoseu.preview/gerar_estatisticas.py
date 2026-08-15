# -*- coding: utf-8 -*-
"""
Gera o painel de estatísticas de acesso do site compraoseu.com.

Lê o log do Nginx (padrão aaPanel) e conta os acessos por página:
- /            -> Home
- /livro01 ... /livro10 -> cada livro
- /quiz        -> quiz

Inclui:
- Acessos de HOJE (até agora) e de ONTEM, com comparação (%);
- Acessos por página, com coluna "Hoje";
- Acessos por dia (últimos 7).

IMPORTANTE: o painel é uma "fotografia" do momento em que o script roda.
Para atualizar sozinho, agende no aaPanel:
  Cron -> Shell -> a cada 1h:  python3 /home/deploy/gerar_estatisticas.py

Gera: /www/wwwroot/compraoseu.com/stats.html
"""
import os
import re
import html
from collections import Counter, OrderedDict
from datetime import datetime, timedelta

LOG = '/www/wwwlogs/compraoseu.com.log'
OUT = '/www/wwwroot/compraoseu.com/stats.html'

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
    ('/quiz', 'Quiz — Autoavaliação'),
])

RE_LINHA = re.compile(r'^(\S+) .*?\[([^\]]+)\] "GET (\S+) HTTP')
RE_EXT = re.compile(r'\.(png|jpg|jpeg|gif|svg|ico|css|js|woff2?|webp|xml|json|txt|webmanifest)$', re.I)


def analisar():
    contagens = Counter()          # total por página
    contagens_hoje = Counter()     # hoje por página
    total_geral = 0
    data_inicio = None
    data_fim = None
    por_dia = Counter()

    agora = datetime.now()
    hoje_str = agora.strftime('%d/%m/%Y')
    ontem = (agora - timedelta(days=1)).strftime('%d/%m/%Y')
    data_ontem = agora.date() - timedelta(days=1)
    acessos_ontem_mesmo_horario = 0

    if not os.path.exists(LOG):
        return None, 'Log não encontrado: ' + LOG

    with open(LOG, 'r', encoding='utf-8', errors='ignore') as f:
        for linha in f:
            m = RE_LINHA.match(linha)
            if not m:
                continue
            ip, data, url = m.group(1), m.group(2), m.group(3)
            if RE_EXT.search(url):
                continue
            path = url.split('?')[0].rstrip('/')
            if path == '':
                path = '/'
            if path.startswith('/livro') or path == '/' or path == '/quiz':
                contagens[path] += 1
            else:
                contagens['/outros:' + path] += 1
            total_geral += 1
            try:
                dt = datetime.strptime(data.split(' ')[0], '%d/%b/%Y:%H:%M:%S')
                chave_dia = dt.strftime('%d/%m/%Y')
                por_dia[chave_dia] += 1
                if chave_dia == hoje_str and (path.startswith('/livro') or path == '/' or path == '/quiz'):
                    contagens_hoje[path] += 1
                if dt.date() == data_ontem and (dt.hour, dt.minute) <= (agora.hour, agora.minute):
                    acessos_ontem_mesmo_horario += 1
                if data_inicio is None or dt < data_inicio:
                    data_inicio = dt
                if data_fim is None or dt > data_fim:
                    data_fim = dt
            except Exception:
                pass

    total_hoje = por_dia.get(hoje_str, 0)
    total_ontem = por_dia.get(ontem, 0)
    # Variação JUSTA: hoje (parcial) contra ONTEM ATÉ O MESMO HORÁRIO.
    # Comparar o parcial com o dia inteiro de ontem é injusto (mostra queda
    # falsa no início do dia); esta comparação é a que reflete o ritmo real.
    if acessos_ontem_mesmo_horario > 0:
        variacao = ((total_hoje - acessos_ontem_mesmo_horario) / acessos_ontem_mesmo_horario) * 100
    else:
        variacao = 100.0 if total_hoje > 0 else 0.0
    # Projeção honesta do dia: ritmo atual (por hora) estendido para 24h
    horas_decorridas = agora.hour + agora.minute / 60.0
    if horas_decorridas > 0:
        projecao = int(round(total_hoje / horas_decorridas * 24))
    else:
        projecao = total_hoje

    return (contagens, total_geral, data_inicio, data_fim, por_dia,
            contagens_hoje, total_hoje, total_ontem, variacao, hoje_str, ontem,
            acessos_ontem_mesmo_horario, projecao), None


def montar_html(res):
    (contagens, total_geral, data_inicio, data_fim, por_dia,
     contagens_hoje, total_hoje, total_ontem, variacao, hoje_str, ontem,
     ontem_mesmo_horario, projecao) = res

    # Seta de variação
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
          <td><a href="https://compraoseu.com{path}">{html.escape(nome)}</a><br><span class="url">{path}</span></td>
          <td class="num">{n} {hoje_txt}</td>
          <td class="num">{pct:.1f}%</td>
          <td><div class="barra"><div class="fill" style="width:{min(100,pct)}%"></div></div></td>
        </tr>""")

    dias = por_dia.most_common(7)
    dias.sort(key=lambda x: x[0], reverse=True)  # mais recente primeiro
    linhas_dias = '\n'.join(
        f'<tr><td>{d}</td><td class="num">{n}</td></tr>' for d, n in dias
    ) or '<tr><td colspan="2">Sem dados diários</td></tr>'

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
  footer {{ text-align:center; color:#7f92ad; font-size:.78rem; margin-top:40px; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>📊 Estatísticas de Acesso</h1>
  <p class="sub">Portal O Despertar · compraoseu.com · gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>

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
  <p style="font-size:.8rem;color:#9fb0c8;margin:-18px 0 24px;">Comparação justa: hoje (parcial) contra ontem até o mesmo horário do dia. A projeção estima o total do dia pelo ritmo atual. (O número de ontem completo é mostrado apenas como referência.)</p>

  <div class="cards">
    <div class="card destaque"><div class="v">{total_home}</div><div class="l">Visitas à Home</div></div>
    <div class="card destaque"><div class="v">{total_livros}</div><div class="l">Acessos aos livros</div></div>
    <div class="card"><div class="v">{livros_lidos}</div><div class="l">Livros lidos</div></div>
    <div class="card"><div class="v">{contagens.get('/quiz',0)}</div><div class="l">Quiz</div></div>
  </div>

  <h2>🏆 Ranking (Home + Livros + Quiz)</h2>
  <table>
    <tr><th>#</th><th>Página</th><th>Acessos (total · hoje)</th><th>%</th><th>Distribuição</th></tr>
    {''.join(linhas)}
  </table>

  <h2>📅 Acessos por dia (últimos 7)</h2>
  <table>
    <tr><th>Dia</th><th>Acessos</th></tr>
    {linhas_dias}
  </table>

  <h2>📄 Outras páginas acessadas</h2>
  <table>
    <tr><th>Página</th><th>Acessos</th></tr>
    {linhas_outros}
  </table>

  <footer>Período registrado: {periodo} · Missão com Deus · Coleção do Despertar<br>
  Painel atualizado pelo script (cron). Página protegida (noindex) — apenas para o administrador.</footer>
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
    print('   Acesse: https://compraoseu.com/stats.html')


if __name__ == '__main__':
    main()
