#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Purifica TODOS os livros do Portal: remove travessões (—), asteriscos (*),
reticências (…) e setas (→) do CONTEÚDO, mantendo a pontuação suave.

Preserva: navegação HTML (← Anterior | Próximo →), <script> (JS do leitor),
<style> (CSS). O JSON-LD também é purificado.

Regras globais:
  1. Referência bíblica: ' " — Nome cap:vers'  ->  ' " (Nome cap:vers)'
  2. Títulos: 'CAPÍTULO 1 — X' / 'Capítulo 1 — X' / 'PARTE I — X' / 'Dia 1 — X'
     -> dois-pontos.
  3. Títulos de capa/JSON: 'Livro — Subtítulo' -> 'Livro: Subtítulo'.
  4. 'Missão com Deus — ...' -> 'Missão com Deus · ...'
  5. '© Coleção do Despertar — Todos os direitos reservados' -> '. '
  6. Citações com autores: ' — Frederick Douglass' -> ' (Frederick Douglass)'
  7. Diálogo: 'Jesus respondeu: — ...' -> 'Jesus respondeu: ...'
  8. Ciclo com setas (livro09): 'x → y → z' -> 'x, y, z'
  9. Reticências: específicas com vírgula onde couber; '…' -> '.' no resto.
 10. Markdown: '**texto**' -> '<strong>texto</strong>'; '*Fim da obra...*' -> '<em>'.

Uso: python3 purificar_todos_livros.py
"""
import re
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]

# Todos os livros (originais, com leitor e publicados)
ARQUIVOS = []
for n in range(1, 12):
    nome = f"livro{n:02d}"
    ARQUIVOS.append(f"paginas/{nome}_preview.html")
    ARQUIVOS.append(f"paginas/{nome}_leitor_preview.html")
    ARQUIVOS.append(f"site-contabo/{nome}.html")

TITULOS_CAPA = [
    ("O Verbo que Transforma — O Poder Criador da Palavra e da Fé",
     "O Verbo que Transforma: O Poder Criador da Palavra e da Fé"),
    ("A Sabedoria dos Mestres — O Despertar do Conhecimento que Liberta a Alma",
     "A Sabedoria dos Mestres: O Despertar do Conhecimento que Liberta a Alma"),
    ("A Mente Renovada — O Pensar com Cristo que Transforma a Vida",
     "A Mente Renovada: O Pensar com Cristo que Transforma a Vida"),
    ("Um Segundo com Deus — Devocional Vol. 01",
     "Um Segundo com Deus: Devocional Vol. 01"),
    ("Devocional Vol. 01 — 30 dias de conexão diária com Deus",
     "Devocional Vol. 01: 30 dias de conexão diária com Deus"),
    ("Sumário — 30 Dias", "Sumário: 30 Dias"),
    ("Evolução da Alma — Caminhos para o Autoconhecimento, Fé e Transformação Pessoal",
     "Evolução da Alma: Caminhos para o Autoconhecimento, Fé e Transformação Pessoal"),
    ("Jesus Quer Falar com Seu Filho — Leitura Online",
     "Jesus Quer Falar com Seu Filho: Leitura Online"),
    ("O Caminho do Despertar — A Jornada Solitária da Alma",
     "O Caminho do Despertar: A Jornada Solitária da Alma"),
    ("O Arquiteto da Realidade — O Poder da Mente que Cria o Mundo que Você Vive",
     "O Arquiteto da Realidade: O Poder da Mente que Cria o Mundo que Você Vive"),
    ("Anestesia Mental — A Hipnose da Sobrevivência",
     "Anestesia Mental: A Hipnose da Sobrevivência"),
    ("Solidão Funcional — O Retiro Estratégico do Guerreiro",
     "Solidão Funcional: O Retiro Estratégico do Guerreiro"),
    ("Exercícios de Ativação — Log de Execução",
     "Exercícios de Ativação: Log de Execução"),
    ("O Despertar do Observador — As Leis Invisíveis que Moldam a Realidade",
     "O Despertar do Observador: As Leis Invisíveis que Moldam a Realidade"),
]

# Substituições específicas por contexto
ESPECIFICAS = [
    # livro04: reticências suaves
    ("esperando… dê o primeiro passo", "esperando. Dê o primeiro passo"),
    ("apenas respire… e permita", "apenas respire, e permita"),
    ("Eu sou teu… totalmente teu", "Eu sou teu, totalmente teu"),
    # livro05: citações com autores e diálogo
    ("“Não há progresso sem luta.” — Frederick Douglass",
     "“Não há progresso sem luta.” (Frederick Douglass)"),
    ("“A felicidade da sua vida depende da qualidade dos seus pensamentos.” — Marco Aurélio",
     "“A felicidade da sua vida depende da qualidade dos seus pensamentos.” (Marco Aurélio)"),
    ("Jesus respondeu: — Eu sou o caminho, a verdade e a vida",
     "Jesus respondeu: Eu sou o caminho, a verdade e a vida"),
    # livro09: ciclo com setas e reticências
    ("estímulo rápido → satisfação rápida → vazio rápido → novo estímulo",
     "estímulo rápido, satisfação rápida, vazio rápido, novo estímulo"),
    ("parece espiritual… mas começou biológico", "parece espiritual, mas começou biológico"),
    ("Isso me governa… ou eu governo isso", "Isso me governa, ou eu governo isso"),
    ("a chave que quebra o código…", "a chave que quebra o código."),
    ("necessidade de validação…", "necessidade de validação."),
    # livro11: frase final em itálico
    ("*Fim da obra. Que o Novo Testamento seja, para você, como nunca lido, e que as Boas Novas de Cristo transformem a sua vida, agora e para sempre.*",
     "<em>Fim da obra. Que o Novo Testamento seja, para você, como nunca lido, e que as Boas Novas de Cristo transformem a sua vida, agora e para sempre.</em>"),
]

RE_REF = re.compile(r'[“"ˮ]\s*—\s*((?:1|2|3)\s*)?([A-Za-zÁÉÍÓÚÂÊÔÃÕÇ][A-Za-zÁÉÍÓÚÂÊÔÃÕÇ]*)\s*(\d+):(\d+)(?:-(\d+))?')

def sub_ref(m):
    num = (m.group(1) or "").strip()
    nome = m.group(2)
    cap, ver = m.group(3), m.group(4)
    fim = "-" + m.group(5) if m.group(5) else ""
    ref = (num + " " if num else "") + nome + " " + cap + ":" + ver + fim
    return '" (' + ref + ')'

RE_TITULO = re.compile(r'\b(CAPÍTULO\s+\d+|Capítulo\s+\d+|PARTE\s+[IVX]+|APRESENTAÇÃO|EPÍLOGO|PRÓLOGO|BÔNUS|Dia\s+\d+)\s*—\s*')

def sub_titulo(m):
    return m.group(1) + ": "

def purificar_texto(texto):
    for antigo, novo in TITULOS_CAPA:
        texto = texto.replace(antigo, novo)
    for antigo, novo in ESPECIFICAS:
        texto = texto.replace(antigo, novo)
    texto = texto.replace("Missão com Deus — Coleção do Despertar", "Missão com Deus · Coleção do Despertar")
    texto = texto.replace("Missão com Deus — CompraOSeu", "Missão com Deus · CompraOSeu")
    texto = texto.replace("© Coleção do Despertar — Todos os direitos reservados",
                          "© Coleção do Despertar. Todos os direitos reservados")
    texto = RE_REF.sub(sub_ref, texto)
    texto = RE_TITULO.sub(sub_titulo, texto)
    # fallback de prosa
    texto = texto.replace(" — ", ", ")
    texto = texto.replace("…", ".")
    texto = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', texto)
    return texto

def purificar_html(html):
    partes = []
    pos = 0
    for m in re.finditer(r'<script(?:\s[^>]*)?>.*?</script>|<style>.*?</style>', html, re.S):
        partes.append(purificar_texto(html[pos:m.start()]))
        bloco = m.group(0)
        if 'application/ld+json' in bloco:
            bloco = re.sub(r'^(<script[^>]*>)(.*)(</script>)$',
                           lambda mm: mm.group(1) + purificar_texto(mm.group(2)) + mm.group(3),
                           bloco, flags=re.S)
        partes.append(bloco)
        pos = m.end()
    partes.append(purificar_texto(html[pos:]))
    return "".join(partes)

def main():
    for rel in ARQUIVOS:
        f = RAIZ / rel
        if not f.exists():
            continue
        html = f.read_text(encoding="utf-8")
        novo = purificar_html(html)
        if novo != html:
            f.write_text(novo, encoding="utf-8")
            print("PURIFICADO:", rel)
    print("Concluído.")

if __name__ == "__main__":
    main()
