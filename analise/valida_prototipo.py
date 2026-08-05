# -*- coding: utf-8 -*-
import sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.erros = []; self.stack = []
        self.void = {'meta','link','br','hr','img','input','wbr'}
    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        else:
            self.erros.append(f"</{tag}> inesperado (pilha: {self.stack[-3:]})")

p = P()
p.feed(open('analise/prototipo_devocional.html', encoding='utf-8').read())
print("tags nao fechadas:", p.stack or "nenhuma")
print("erros:", p.erros or "nenhum")
t = open('analise/prototipo_devocional.html', encoding='utf-8').read()
print("CTAs:", t.count('class="btn"'))
print("checkout Kiwify:", t.count('CF9nhFx'))
print("WhatsApp:", t.count('wa.me'))
print("capa:", t.count('umsegundocdeusjpg.jpg'))
