# -*- coding: utf-8 -*-
"""
Trava impressao e copia nos PDF da pasta livros (e na raiz).
Abrir continua sem senha. Print da tela ninguem impede.

  pip3 install pypdf
  cd /www/wwwroot/missaocomdeus.com.br
  python3 PROTEGER_PDFS.py
"""
import os
import glob

SITE = "/www/wwwroot/missaocomdeus.com.br"
SENHA_DONO = "MissaoComDeus2026"
# Ficam ABERTOS (sem trava): Devocional e e-book infantil
LIVRES = (
    "um-segundo-com-deus",
    "jesus-quer-falar",
    "livro04",
    "livro06",
)

def trancar(w, senha):
    import inspect
    params = inspect.signature(type(w).encrypt).parameters
    kwargs = {}
    if "user_password" in params:
        kwargs["user_password"] = ""
        kwargs["owner_password"] = senha
    else:
        kwargs["user_pwd"] = ""
        kwargs["owner_pwd"] = senha
    if "permissions_flag" in params:
        try:
            from pypdf.constants import UserAccessPermissions as P
            kwargs["permissions_flag"] = P(0)
        except Exception:
            kwargs["permissions_flag"] = 0
    if "algorithm" in params:
        kwargs["algorithm"] = "AES-256"
    w.encrypt(**kwargs)


def main():
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        print("ERRO: rode antes:  pip3 install pypdf")
        return
    caminhos = []
    for pasta in (
        os.path.join(SITE, "livros"),
        os.path.join(SITE, "ebooks"),
        SITE,
    ):
        caminhos += glob.glob(os.path.join(pasta, "*.pdf"))
        caminhos += glob.glob(os.path.join(pasta, "*.PDF"))
    if not caminhos:
        print("Nenhum PDF encontrado")
        return
    for path in sorted(set(caminhos)):
        nome = os.path.basename(path)
        chave = nome.lower().replace("_", "-")
        if any(x in chave for x in LIVRES):
            print("LIVRE", nome)
            continue
        try:
            r = PdfReader(path)
            w = PdfWriter()
            for pag in r.pages:
                w.add_page(pag)
            if r.metadata:
                w.add_metadata(r.metadata)
            trancar(w, SENHA_DONO)
            tmp = path + ".tmp"
            with open(tmp, "wb") as f:
                w.write(f)
            os.replace(tmp, path)
            print("OK", nome)
        except Exception as e:
            print("FALHOU", nome, e)
    print("Pronto. Abrir sim. Imprimir/copiar o leitor bloqueia. Print da tela nao.")


if __name__ == "__main__":
    main()
