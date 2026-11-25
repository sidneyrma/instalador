#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Volta ActionsWebhook, wbotMessageListener, OpenAiService e ReceivedWhatsApp
ao estado em que o Oi gerava o cumprimento e o envio oficial funcionava.
Nao mexe no Prisma nem no JSON de envio.

  cd /www/wwwroot/missaocomdeus.com.br
  python3 RESTAURA_ANTES_GPT.py
"""
import glob
from pathlib import Path
from shutil import copy2

ROOTS = [
    Path("/home/deploy/conectai/backend/dist/services/WebhookService"),
    Path("/home/deploy/conectai/backend/dist/services/WbotServices"),
    Path("/home/deploy/conectai/backend/dist/services/IntegrationsServices"),
    Path("/home/deploy/conectai/backend/dist/services/WhatsAppOficial"),
]


def mais_antigo(pasta: Path, globpat: str):
    files = sorted(pasta.glob(globpat), key=lambda p: p.stat().st_mtime)
    return files[0] if files else None


def main():
    print("Arquivo: RESTAURA_ANTES_GPT.py  (sem colchete)")
    pares = [
        (
            Path("/home/deploy/conectai/backend/dist/services/WebhookService/ActionsWebhookService.js"),
            "ActionsWebhookService.js.bak-semola-*",
        ),
        (
            Path("/home/deploy/conectai/backend/dist/services/WbotServices/wbotMessageListener.js"),
            "wbotMessageListener.js.bak-continua-*",
        ),
        (
            Path("/home/deploy/conectai/backend/dist/services/IntegrationsServices/OpenAiService.js"),
            "OpenAiService.js.bak-gpt3-*",
        ),
        (
            Path("/home/deploy/conectai/backend/dist/services/WhatsAppOficial/ReceivedWhatsApp.js"),
            "ReceivedWhatsApp.js.bak-gpt-*",
        ),
    ]
    for dest, pat in pares:
        bak = mais_antigo(dest.parent, pat)
        if not bak:
            print("Nao achei", pat)
            continue
        copy2(bak, dest)
        print("restaurou", dest.name, "<-", bak.name)
    print("Nao mexe em send JSON nem bolha nem prisma.")
    print("Reinicie o backend sem --update-env.")


if __name__ == "__main__":
    main()
