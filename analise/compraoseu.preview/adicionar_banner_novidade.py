#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona o banner de NOVIDADE da leitura online na Home do Portal.

Texto: "Agora você pode ler nossos livros online e, sempre que abrir
novamente, continuar do ponto em que parou. Letras no seu tamanho,
tela confortável e fita dourada para marcar o lugar."

Aplica em:
  paginas/home_preview.html
  site-contabo/index.html
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]

CSS_BANNER = """
  /* ===== Banner de novidade da leitura ===== */
  #banner-novidade{background:linear-gradient(135deg,var(--navy) 0%,var(--navy-3) 100%);border-top:3px solid var(--gold);border-bottom:1px solid rgba(201,162,75,.35);padding:26px 0;position:relative;overflow:hidden}
  #banner-novidade::after{content:"📖";position:absolute;right:-18px;bottom:-24px;font-size:150px;opacity:.06;transform:rotate(-12deg);pointer-events:none}
  .bn-inner{display:flex;align-items:center;gap:18px;max-width:64rem;margin:0 auto;padding:0;position:relative;z-index:1}
  .bn-icone{font-size:2.1rem;flex-shrink:0;background:rgba(201,162,75,.14);border:1px solid rgba(201,162,75,.45);border-radius:50%;width:64px;height:64px;display:flex;align-items:center;justify-content:center}
  .bn-texto{flex:1;min-width:0;color:var(--cream-2)}
  .bn-texto strong{display:block;font-family:var(--serif);font-size:1.15rem;color:var(--gold-light);margin-bottom:4px;letter-spacing:.02em}
  .bn-texto span{display:block;font-size:.92rem;line-height:1.55;color:rgba(246,241,231,.85);max-width:46rem}
  .bn-cta{flex-shrink:0;background:linear-gradient(135deg,var(--gold-light),var(--gold-dark));color:var(--navy);font-weight:700;font-size:.85rem;padding:12px 20px;border-radius:10px;text-decoration:none;box-shadow:0 10px 22px -8px rgba(184,134,11,.55);white-space:nowrap}
  .bn-cta:hover{transform:translateY(-1px)}
  @media (max-width:640px){
    .bn-inner{flex-direction:column;text-align:center}
    .bn-texto span{max-width:100%}
  }
"""

BANNER = """
<div id="banner-novidade">
  <div class="wrap">
    <div class="bn-inner">
      <span class="bn-icone">✨</span>
      <div class="bn-texto">
        <strong>Novidade: leitura que não se perde</strong>
        <span>Agora você pode ler nossos livros online e, sempre que abrir novamente, continuar exatamente do ponto em que parou. Letras no seu tamanho, tela confortável e fita dourada para marcar o lugar.</span>
      </div>
      <a class="bn-cta" href="#biblioteca">Explorar os livros →</a>
    </div>
  </div>
</div>
"""


def aplicar(arquivo):
    html = arquivo.read_text(encoding="utf-8")
    if "banner-novidade" in html:
        print("  (já tem banner, pulando):", arquivo.name)
        return
    # CSS antes de </style>
    assert "</style>" in html
    html = html.replace("</style>", CSS_BANNER + "\n</style>", 1)
    # Banner antes da biblioteca
    alvo = '<section class="biblioteca" id="biblioteca">'
    assert alvo in html, "seção biblioteca não encontrada em " + arquivo.name
    html = html.replace(alvo, BANNER + "\n" + alvo, 1)
    arquivo.write_text(html, encoding="utf-8")
    print("  OK:", arquivo.name)


def main():
    aplicar(RAIZ / "paginas" / "home_preview.html")
    aplicar(RAIZ / "site-contabo" / "index.html")


if __name__ == "__main__":
    main()
    print("Concluído.")
