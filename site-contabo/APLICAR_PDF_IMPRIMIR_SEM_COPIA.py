#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDFs dos livros: imprimir SIM, copiar NAO.
Quem quiser o texto, digita. Abre sem senha.
A senha do dono fica num arquivo no servidor. Nao cole no chat.

  cd /www/wwwroot/missaocomdeus.com.br
  python3 APLICAR_PDF_IMPRIMIR_SEM_COPIA.py

Digite o nome. Nao clique se o Terminal mostrar colchete azul.
"""
import datetime
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

SITE = Path("/www/wwwroot/missaocomdeus.com.br")
EBOOKS = SITE / "ebooks"
SENHA_ARQ = Path("/home/deploy/pdf-owner-nao-colar.txt")
STAMP = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def log(msg):
    print(msg)


def dono():
    SENHA_ARQ.parent.mkdir(parents=True, exist_ok=True)
    if SENHA_ARQ.exists():
        s = SENHA_ARQ.read_text(encoding="utf-8").strip()
        if s:
            return s
    s = secrets.token_urlsafe(18)
    SENHA_ARQ.write_text(s + "\n", encoding="utf-8")
    try:
        SENHA_ARQ.chmod(0o600)
    except OSError:
        pass
    log("Senha do dono gravada em /home/deploy/pdf-owner-nao-colar.txt")
    log("Anote no caderno. Nao cole neste chat.")
    return s


def garante_pikepdf():
    try:
        import pikepdf  # noqa: F401
        return True
    except ImportError:
        log("Instalando pikepdf (uma vez)...")
        r = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", "pikepdf"],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            log("Nao consegui instalar pikepdf. Nao gravei os PDFs.")
            log("No Terminal, se quiser: pip3 install pikepdf")
            return False
        try:
            import pikepdf  # noqa: F401
            return True
        except ImportError:
            log("pikepdf nao entrou. Nao gravei.")
            return False


def aplica(pdf_path, owner, pasta_bak):
    import pikepdf
    from pikepdf import Encryption, Permissions

    perms = Permissions(
        accessibility=True,
        extract=False,
        modify_annotation=False,
        modify_assembly=False,
        modify_form=False,
        modify_other=False,
        print_lowres=True,
        print_highres=True,
    )
    try:
        pdf = pikepdf.open(pdf_path)
    except pikepdf.PasswordError:
        log("Ja tinha senha, nao mexi: " + pdf_path.name)
        return False
    bak = pasta_bak / pdf_path.name
    if not bak.exists():
        shutil.copy2(pdf_path, bak)
    tmp = pdf_path.with_name(pdf_path.stem + ".tmp-perm.pdf")
    pdf.save(
        tmp,
        encryption=Encryption(user="", owner=owner, allow=perms),
    )
    pdf.close()
    tmp.replace(pdf_path)
    log("OK  " + pdf_path.name + "  imprimir sim, copiar nao")
    return True


def main():
    log("Arquivo: APLICAR_PDF_IMPRIMIR_SEM_COPIA.py  (sem colchete)")
    if not EBOOKS.exists():
        log("Nao achei a pasta ebooks. Nao gravei.")
        return
    pdfs = sorted(p for p in EBOOKS.glob("*.pdf") if p.is_file())
    if not pdfs:
        log("Nenhum PDF na pasta ebooks. Nao gravei.")
        return
    log("Achei %d PDF(s)." % len(pdfs))
    if not garante_pikepdf():
        return
    owner = dono()
    pasta_bak = EBOOKS / ("backup-pdf-antes-perm-" + STAMP)
    pasta_bak.mkdir(parents=True, exist_ok=True)
    log("backup  " + str(pasta_bak))
    n = 0
    for p in pdfs:
        if aplica(p, owner, pasta_bak):
            n += 1
    log("Fim. PDFs ajustados: %d" % n)
    log("Imprimir: sim. Copiar texto: nao. Foto da tela o PDF tambem nao trava.")


if __name__ == "__main__":
    main()
