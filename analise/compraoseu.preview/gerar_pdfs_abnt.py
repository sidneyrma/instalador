# -*- coding: utf-8 -*-
"""
Gera os PDFs ABNT protegidos dos livros da Coleção do Despertar.

Formato: livro físico 16x23 cm (padrão ABNT de editoras brasileiras)
  - margens: 3 cm (superior/esquerda), 2 cm (inferior/direita)
  - fonte: Times New Roman 12pt, entrelinha 1,5
  - capa, folha de rosto, créditos, sumário com paginação, capítulos
Proteção: PDF com senha de dono que BLOQUEIA cópia e impressão
  (owner password sem permissões de copy/print; usuário pode apenas ler).

Livros gerados (sem imagens):
  - livro01 O Ouro das Palavras
  - livro02 O Livro Proibido dos Mestres
  - livro03 A Mente de Cristo
  - livro05 Evolução da Alma
  - livro07 O Caminho do Despertar
  - livro08 Você e o Universo
  - livro09 Anestesia Mental
  - livro10 O Despertar do Observador

Saída: edicoes/abnt/<slug>.pdf
"""
import re, html, os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.lib import pdfencrypt

HERE = Path(__file__).parent
PAGINAS = HERE.parent.parent / "paginas"
OUT_DIR = HERE.parent.parent / "edicoes" / "abnt"

# Livros: (arquivo html, slug, título, autor/editora, subtítulo)
LIVROS = [
    ("livro01_preview.html", "livro01", "O Verbo que Transforma",
     "Coleção do Despertar", "O Poder Criador da Palavra e da Fé"),
    ("livro02_preview.html", "livro02", "A Sabedoria dos Mestres",
     "Coleção do Despertar", "O Despertar do Conhecimento que Liberta a Alma"),
    ("livro03_preview.html", "livro03", "A Mente de Cristo",
     "Baseado nos ensinamentos de Emmet Fox", "Como Pensar com o Espírito e não com o Mundo"),
    ("livro05_preview.html", "livro05", "Evolução da Alma",
     "Coleção do Despertar", "Caminhos para o Autoconhecimento, Fé e Transformação Pessoal"),
    ("livro07_preview.html", "livro07", "O Caminho do Despertar",
     "Coleção do Despertar", "A Jornada Solitária da Alma"),
    ("livro08_preview.html", "livro08", "O Arquiteto da Realidade",
     "Coleção do Despertar", "O Poder da Mente que Cria o Mundo que Você Vive"),
    ("livro09_preview.html", "livro09", "Anestesia Mental",
     "Coleção do Despertar", "e seus Algoritmos da Escravidão"),
    ("livro10_preview.html", "livro10", "O Despertar do Observador",
     "Coleção do Despertar", "As Leis Invisíveis que Moldam a Realidade"),
]


def extrair_estrutura(html_path):
    """Extrai do HTML: [(tipo, texto)] com tipos cap-num, cap-titulo, parte, secao, p."""
    raw = html_path.read_text(encoding="utf-8")
    # isola o <main class="leitura">
    m = re.search(r'<main class="leitura">(.*?)</main>', raw, re.DOTALL)
    if not m:
        return []
    corpo = m.group(1)
    blocos = []
    # seções
    for sec in re.finditer(r'<section class="capitulo[^"]*" id="[^"]*">(.*?)</section>', corpo, re.DOTALL):
        conteudo = sec.group(1)
        # navegação (remover)
        conteudo = re.sub(r'<nav class="cap-nav">.*?</nav>', '', conteudo, flags=re.DOTALL)
        # cap-num
        mnum = re.search(r'<p class="cap-num">(.*?)</p>', conteudo, re.DOTALL)
        if mnum:
            blocos.append(("cap-num", html.unescape(re.sub(r'<[^>]+>', '', mnum.group(1))).strip()))
        # títulos
        for h in re.finditer(r'<h2 class="cap-titulo[^"]*"[^>]*>(.*?)</h2>', conteudo, re.DOTALL):
            blocos.append(("cap-titulo", html.unescape(re.sub(r'<[^>]+>', '', h.group(1))).strip()))
        for h in re.finditer(r'<h3 class="secao-titulo"[^>]*>(.*?)</h3>', conteudo, re.DOTALL):
            blocos.append(("secao", html.unescape(re.sub(r'<[^>]+>', '', h.group(1))).strip()))
        # parágrafos
        for p in re.finditer(r'<p>(.*?)</p>', conteudo, re.DOTALL):
            txt = html.unescape(re.sub(r'<[^>]+>', '', p.group(1))).strip()
            if txt:
                blocos.append(("p", txt))
    return blocos


# ---------------- Estilos ABNT ----------------
MARGEM_SUP = 3 * cm
MARGEM_INF = 2 * cm
MARGEM_ESQ = 3 * cm
MARGEM_DIR = 2 * cm

# Formato 16x23 cm (livro físico)
PAG_W = 16 * cm
PAG_H = 23 * cm

ESTILO = ParagraphStyle('abnt', fontName='Times-Roman', fontSize=12,
                        leading=18, alignment=TA_JUSTIFY, firstLineIndent=1.25 * cm)
ESTILO_CAP = ParagraphStyle('cap', fontName='Times-Bold', fontSize=14,
                            leading=18, alignment=TA_LEFT, spaceBefore=18, spaceAfter=10)
ESTILO_SEC = ParagraphStyle('sec', fontName='Times-BoldItalic', fontSize=12,
                            leading=18, alignment=TA_LEFT, spaceBefore=12, spaceAfter=6)
ESTILO_NUM = ParagraphStyle('num', fontName='Times-Bold', fontSize=11,
                            leading=14, alignment=TA_CENTER, spaceAfter=6)
ESTILO_TOC = ParagraphStyle('toc', fontName='Times-Roman', fontSize=12,
                            leading=20, alignment=TA_LEFT)


def gerar_pdf(estrutura, titulo, autor, subtitulo, slug):
    out = OUT_DIR / f"{slug}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)

    # Proteção: bloquear cópia e impressão
    encrypt = pdfencrypt.StandardEncryption(
        userPassword='',            # abre sem senha
        ownerPassword='colegiododespertar2026',
        canPrint=0,
        canCopy=0,
        canModify=0,
    )

    c = canvas.Canvas(str(out), pagesize=(PAG_W, PAG_H), encrypt=encrypt)
    c.setTitle(f"{titulo} — {subtitulo}")
    c.setAuthor("Coleção do Despertar")
    c.setSubject(subtitulo)

    def nova_pagina():
        c.showPage()

    # ---- Capa ----
    c.setFillColorRGB(0.05, 0.10, 0.18)
    c.rect(0, 0, PAG_W, PAG_H, fill=1, stroke=0)
    c.setFillColorRGB(0.79, 0.64, 0.29)
    c.setFont('Times-Bold', 20)
    c.drawCentredString(PAG_W/2, PAG_H - 4*cm, "COLEÇÃO DO DESPERTAR")
    c.setFillColorRGB(0.93, 0.88, 0.80)
    c.setFont('Times-Bold', 26)
    # título quebrado
    titulo_linhas = [titulo]
    c.drawCentredString(PAG_W/2, PAG_H - 6.5*cm, titulo)
    c.setFont('Times-Italic', 15)
    c.drawCentredString(PAG_W/2, PAG_H - 8*cm, subtitulo)
    c.setFont('Times-Roman', 12)
    c.setFillColorRGB(0.79, 0.64, 0.29)
    c.drawCentredString(PAG_W/2, 3*cm, "Leitura protegida · Proibida a cópia e a impressão")
    nova_pagina()

    # ---- Folha de rosto ----
    c.setFillColorRGB(0.1, 0.1, 0.1)
    c.setFont('Times-Bold', 16)
    c.drawCentredString(PAG_W/2, PAG_H - 5*cm, titulo)
    c.setFont('Times-Italic', 12)
    c.drawCentredString(PAG_W/2, PAG_H - 6*cm, subtitulo)
    c.setFont('Times-Roman', 12)
    c.drawCentredString(PAG_W/2, PAG_H - 8*cm, autor)
    nova_pagina()

    # ---- Créditos ----
    c.setFont('Times-Roman', 11)
    cred = [
        f"© 2026 Coleção do Despertar",
        "Todos os direitos reservados.",
        "",
        "Nenhuma parte desta obra pode ser reproduzida, distribuída ou",
        "transmitida por qualquer forma ou meio, incluindo fotocópias,",
        "gravações ou sistemas de armazenamento, sem autorização por",
        "escrito dos detentores dos direitos autorais.",
        "",
        f"Título: {titulo}",
        f"Subtítulo: {subtitulo}",
        f"Editora: Coleção do Despertar · CompraOSeu",
        "Edição: 1ª Edição · 2026",
        "",
        "Este material é protegido contra cópia e impressão.",
        "Leitura apenas online em compraoseu.com",
    ]
    y = PAG_H - 5*cm
    for linha in cred:
        c.drawCentredString(PAG_W/2, y, linha)
        y -= 0.55*cm
    nova_pagina()

    # ---- Sumário (coletar capítulos e partes) ----
    toc_itens = []
    for i in range(len(estrutura)):
        if estrutura[i][0] == "cap-titulo":
            num = estrutura[i-1][1] if i > 0 and estrutura[i-1][0] == "cap-num" else ""
            # só usa numeração se for "Capítulo N"
            if num.startswith("Capítulo"):
                toc_itens.append(("cap", num, estrutura[i][1]))
            else:
                toc_itens.append(("parte", "", estrutura[i][1]))
    c.setFont('Times-Bold', 16)
    c.drawCentredString(PAG_W/2, PAG_H - 3.5*cm, "SUMÁRIO")
    y = PAG_H - 5.5*cm
    for tipo, num, tit in toc_itens:
        if y < 2.5*cm:
            nova_pagina()
            y = PAG_H - 3*cm
        if tipo == "parte":
            c.setFont('Times-Bold', 12)
            c.setFillColorRGB(0.5, 0.4, 0.2)
        else:
            c.setFont('Times-Roman', 12)
            c.setFillColorRGB(0.1, 0.1, 0.1)
        rotulo = f"{num}  {tit}" if num else tit
        c.drawString(MARGEM_ESQ, y, rotulo[:62])
        y -= 0.7*cm
    c.setFillColorRGB(0.1, 0.1, 0.1)
    nova_pagina()

    # ---- Corpo ----
    from reportlab.platypus import Paragraph, Frame, PageTemplate, BaseDocTemplate
    # Usamos canvas simples com quebra manual
    y = PAG_H - MARGEM_SUP
    def escrever(texto, estilo, indentar=True):
        nonlocal y
        # quebra de linha simples com textwrap aproximado
        from reportlab.pdfbase.pdfmetrics import stringWidth
        palavras = texto.split()
        largura = PAG_W - MARGEM_ESQ - MARGEM_DIR
        linha = ""
        for w in palavras:
            teste = (linha + " " + w).strip()
            if stringWidth(teste, estilo.fontName, estilo.fontSize) <= largura:
                linha = teste
            else:
                if y < MARGEM_INF + 0.5*cm:
                    nova_pagina()
                    y = PAG_H - MARGEM_SUP
                x = MARGEM_ESQ + (estilo.firstLineIndent if indentar else 0)
                c.setFont(estilo.fontName, estilo.fontSize)
                c.drawString(x, y, linha)
                y -= estilo.leading
                linha = w
                indentar = True
        if linha:
            if y < MARGEM_INF + 0.5*cm:
                nova_pagina()
                y = PAG_H - MARGEM_SUP
            x = MARGEM_ESQ + (estilo.firstLineIndent if indentar else 0)
            c.setFont(estilo.fontName, estilo.fontSize)
            c.drawString(x, y, linha)
            y -= estilo.leading

    for tipo, txt in estrutura:
        if tipo == "cap-num":
            # centraliza número do capítulo; parte inicia página nova
            if txt.strip().startswith("Coleção do Despertar"):
                nova_pagina(); y = PAG_H - MARGEM_SUP
                c.setFont('Times-BoldItalic', 16)
                c.setFillColorRGB(0.5, 0.4, 0.2)
                c.drawCentredString(PAG_W/2, y, txt.strip())
                c.setFillColorRGB(0.1, 0.1, 0.1)
                y -= 1.2*cm
            else:
                if y < MARGEM_INF + 2*cm:
                    nova_pagina(); y = PAG_H - MARGEM_SUP
                c.setFont('Times-Bold', 12)
                c.drawCentredString(PAG_W/2, y, txt)
                y -= 0.8*cm
        elif tipo == "cap-titulo":
            if y < MARGEM_INF + 2.5*cm:
                nova_pagina(); y = PAG_H - MARGEM_SUP
            escrever(txt, ESTILO_CAP, indentar=False)
            y -= 0.2*cm
        elif tipo == "secao":
            escrever(txt, ESTILO_SEC, indentar=False)
        else:
            escrever(txt, ESTILO)
    c.showPage()
    c.save()
    print(f"✔ {slug}.pdf gerado ({out.stat().st_size//1024} KB)")


def main():
    total = 0
    for arq, slug, titulo, autor, subtitulo in LIVROS:
        html_path = PAGINAS / arq
        if not html_path.exists():
            print(f"⚠ {arq} não encontrado")
            continue
        estrutura = extrair_estrutura(html_path)
        if not estrutura:
            print(f"⚠ {arq} sem estrutura extraída")
            continue
        gerar_pdf(estrutura, titulo, autor, subtitulo, slug)
        total += 1
    print(f"\nTotal de PDFs gerados: {total} em {OUT_DIR}")


if __name__ == '__main__':
    main()
