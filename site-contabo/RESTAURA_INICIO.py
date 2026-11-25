#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Restaura cada arquivo ao PRIMEIRO backup (mais antigo).
Nao mexe em .env (chave 64 do painel fica).
Nao apaga a API oficial nem o banco.

  cd /www/wwwroot/missaocomdeus.com.br
  python3 RESTAURA_INICIO.py
"""
import re
from pathlib import Path
from shutil import copy2

RAIZ = Path("/home/deploy/conectai")
PAT = re.compile(r"^(?P<stem>.+)\.bak-[A-Za-z0-9]+-\d{8}-\d{6}$")


def main():
    print("Arquivo: RESTAURA_INICIO.py  (sem colchete)")
    grupos = {}
    for bak in RAIZ.rglob("*"):
        if not bak.is_file():
            continue
        if ".env.bak" in bak.name:
            print("pula env:", bak.name)
            continue
        m = PAT.match(bak.name)
        if not m:
            continue
        dest = bak.with_name(m.group("stem"))
        grupos.setdefault(str(dest), []).append(bak)
    n = 0
    for dest_s, baks in sorted(grupos.items()):
        dest = Path(dest_s)
        escolhido = min(baks, key=lambda p: p.stat().st_mtime)
        copy2(escolhido, dest)
        n += 1
        print("OK", dest.name, "<-", escolhido.name)
    print("Arquivos restaurados:", n)
    print("Nao mexi em .env")
    print("Depois: prisma generate na api_oficial e pm2 restart backend + apioficial, sem --update-env")


if __name__ == "__main__":
    main()
