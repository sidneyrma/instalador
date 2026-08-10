# -*- coding: utf-8 -*-
"""Auditoria de alta conversão das páginas criadas pelo Claude (compraoseu.preview)"""
import re, os

BASE = '/tmp/compraoseu_preview'
PAGINAS = ['home', 'evolucao', 'anestesia', 'devocional']

# mapeamento checkout -> preço esperado
CHECKOUTS = {
    'iVfp2bi': '49,00',
    'ptH32K9': '19,90',
    'NCf1jh4': '19,90',
    'CF9nhFx': '9,90',
    'F106343306J': '97,00',
}

# nomes de ícones Material que indicam ícone quebrado
ICONES_QBRADOS = ['shopping_bag','expand_more','play_circle','verified','timer','lock_open',
                  'auto_stories','psychology','history_edu','account_tree','cloud_off',
                  'target','self_improvement','visibility','vpn_key','account_balance',
                  'devices','check_circle','key','bolt','menu_book','prayer_times',
                  'family_restroom','gavel','biotech','all_inclusive','storm','door_open',
                  'exit_to_app','hub','grid_guides','shield_with_heart','psychology_alt',
                  'crisis_alert','auto_fix_high','timer']

def analisar(pag):
    head = open(f'{BASE}/{pag}_HEAD.html', encoding='utf-8').read()
    body = open(f'{BASE}/{pag}_BODY.html', encoding='utf-8').read()
    r = {'pag': pag}

    # 1. Checkouts presentes e preços próximos
    links = set(re.findall(r'(?:pay\.kiwify\.com\.br|go\.hotmart\.com)/([A-Za-z0-9?=]+)', body + ' ' + head))
    r['checkouts'] = sorted(set(l.split('?')[0] for l in links))

    # 2. Ícones quebrados no BODY
    achados = [ic for ic in ICONES_QBRADOS if re.search(r'\b'+ic+r'\b', body)]
    r['icones_quebrados'] = achados

    # 3. Cronômetro falso
    r['cronometro'] = 'CRONÔMETRO' in body.upper() or 'timer' in body.lower() or re.search(r'00:\d\d:\d\d', body) is not None

    # 4. Garantia
    r['garantia'] = '7 DIAS' in body.upper() or '7 dias' in body.lower() or 'garantia' in body.lower()

    # 5. Prova social (placeholders vs inventados)
    r['depo_placeholder'] = 'ilustrativo' in body.lower() or 'substitua' in body.lower() or 'coloque aqui' in body.lower() or 'nome do aluno' in body.lower()
    r['10k'] = '10k' in body.lower()

    # 6. O que você recebe
    r['recebe'] = 'você recebe' in body.lower() or 'voce recebe' in body.lower()

    # 7. CTAs (class btn / botão)
    r['ctas'] = body.count('class="btn') + body.count('class=\'btn') + body.count('btn">') 

    # 8. Cores da identidade
    r['cor_navy'] = '#0e1a2e' in head.lower()
    r['cor_ouro'] = '#c9a24b' in head.lower()

    # 9. CTA repetido (conta ocorrências de palavras de compra)
    r['quero/garantir/adquirir'] = sum(body.lower().count(x) for x in ['quero meu','garantir','adquirir','quero meu acesso','quero minha'])

    # 10. WhatsApp
    r['whatsapp'] = 'wa.me' in body

    # 11. Emojis usados
    emojis = re.findall(r'[\U0001F300-\U0001FAFF\u2600-\u27BF]', body)
    r['emojis'] = len(emojis)

    return r

print('='*80)
print('AUDITORIA DE ALTA CONVERSÃO — páginas do Claude (compraoseu.preview)')
print('='*80)
for p in PAGINAS:
    r = analisar(p)
    print(f"\n--- {r['pag'].upper()} ---")
    print(f"  Checkouts encontrados: {r['checkouts']}")
    print(f"  Ícones quebrados: {r['icones_quebrados'] if r['icones_quebrados'] else 'NENHUM ✓'}")
    print(f"  Cronômetro falso: {'SIM ✗' if r['cronometro'] else 'não ✓'}")
    print(f"  Garantia 7 dias: {'SIM ✓' if r['garantia'] else 'NÃO ✗'}")
    print(f"  Depoimento placeholder: {'SIM ✓' if r['depo_placeholder'] else 'sem placeholder (verificar)'}")
    print(f"  '10k+': {'SIM ✗' if r['10k'] else 'não ✓'}")
    print(f"  Bloco 'o que recebe': {'SIM ✓' if r['recebe'] else 'NÃO ✗'}")
    print(f"  Nº CTAs (botões): {r['ctas']}")
    print(f"  Cores marca (navy/ouro): {'SIM ✓' if r['cor_navy'] and r['cor_ouro'] else 'parcial/não'}")
    print(f"  Palavras de compra (CTAs repetidos): {r['quero/garantir/adquirir']}")
    print(f"  WhatsApp: {'SIM ✓' if r['whatsapp'] else 'não'}")
    print(f"  Emojis usados: {r['emojis']}")
