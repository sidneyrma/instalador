# -*- coding: utf-8 -*-
"""
DESPROTEGER_PDFS.py
Missao com Deus - REMOVER a protecao de copiar/imprimir dos PDFs.

Este e o REVERSO do PROTEGER_PDFS.py:
  - Abre cada PDF travado com a senha de dono.
  - Reescreve o arquivo SEM senha de usuario e SEM protecao.
  - Apagar as travas de "copiar/colar" e de "imprimir".
  - Volta ao estado ABERTO (leitura, copia e impressao liberadas).
  - Antes de alterar, guarda uma copia segura do arquivo travado:
      NOME.pdf.protegido.bak
    (se o programa precisar ser refeito, essa copia permite voltar ao estado travado)

  REVERSO TOTAL / SEM SOBRESCRITA PERIGOSA:
  - Nao faz backup de arquivos que ja estao abertos.
  - Nao altera PDFs que nao conseguem ser abertos com a senha de dono.
  - Cada PDF reescrito e substituido apenas DEPOIS de ser salvo com sucesso
    em um arquivo temporario (.tmp).

Como usar (aaPanel, 2 linhas):
  cd /www/wwwroot/missaocomdeus.com.br
  python3 DESPROTEGER_PDFS.py

Em outro diretorio (testar sem tocar no site):
  SITE=/tmp/meus_pdfs python3 DESPROTEGER_PDFS.py
"""
import os
import glob
import sys

SITE = os.environ.get('SITE', '/www/wwwroot/missaocomdeus.com.br')
SENHA_DONO = "MissaoComDeus2026"

# Pastas varridas no PROTEGER_PDFS.py
PASTAS = ("livros", "ebooks", ".")


def tentar_desbloquear(reader):
    """Retorna True se conseguir ler as paginas com a senha de dono."""
    try:
        from pypdf import PasswordType
        tipo = reader.decrypt(SENHA_DONO)
        return tipo in (
            PasswordType.OWNER_PASSWORD,
            PasswordType.USER_PASSWORD,
        )
    except Exception:
        pass

    # Compatibilidade com versoes antigas do pypdf/PyPDF2.
    try:
        resultado = reader.decrypt(SENHA_DONO)
        return bool(resultado)
    except Exception:
        return False


def escrever_sem_protecao(reader, destino_final):
    """Copia todas as paginas/metadados e grava um PDF SEM senha/bloqueio."""
    from pypdf import PdfWriter

    writer = PdfWriter()
    for pagina in reader.pages:
        writer.add_page(pagina)
    if reader.metadata:
        writer.add_metadata(reader.metadata)

    # Sem chamar writer.encrypt() => arquivo final 100% aberto.
    tmp = destino_final + ".tmp"
    with open(tmp, "wb") as f:
        writer.write(f)
    os.replace(tmp, destino_final)


def main():
    try:
        from pypdf import PdfReader
    except ImportError:
        print("ERRO: rode antes:  pip3 install pypdf")
        sys.exit(1)

    if not os.path.isdir(SITE):
        print("ERRO: pasta nao encontrada:", SITE)
        sys.exit(1)

    caminhos = []
    for pasta_rel in PASTAS:
        pasta = os.path.join(SITE, pasta_rel)
        if not os.path.isdir(pasta):
            continue
        caminhos += glob.glob(os.path.join(pasta, "*.pdf"))
        caminhos += glob.glob(os.path.join(pasta, "*.PDF"))

    if not caminhos:
        print("Nenhum PDF encontrado em", SITE)
        return

    feitos = 0
    abertos = 0
    falhas = 0
    for path in sorted(set(caminhos)):
        nome = os.path.basename(path)
        try:
            reader = PdfReader(path)
            if not reader.is_encrypted:
                print("ABERTO", nome)
                abertos += 1
                continue

            if not tentar_desbloquear(reader):
                print("FALHOU", nome, "(senha de dono nao abriu; arquivo NAO foi alterado)")
                falhas += 1
                continue

            # Guarda uma copia do arquivo TRAVADO (apenas no primeiro revert).
            bak = path + ".protegido.bak"
            if not os.path.exists(bak):
                import shutil
                shutil.copy2(path, bak)
                print("  backup do travado:", os.path.basename(bak))

            escrever_sem_protecao(reader, path)
            print("OK", nome)
            feitos += 1
        except Exception as e:
            print("FALHOU", nome, e)
            falhas += 1

    print("---")
    print("Desprotegidos:", feitos)
    print("Ja estavam abertos:", abertos)
    print("Nao alterados:", falhas)
    print("Pronto. PDFs reescritos sem trava de copiar/imprimir.")


if __name__ == "__main__":
    main()