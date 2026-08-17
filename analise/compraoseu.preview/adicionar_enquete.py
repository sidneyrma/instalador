#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona a ENQUETE de participação na Home do Portal.

- Pergunta principal: o que o leitor achou da leitura online com marcadores.
- 4 opções de voto com PERCENTUAL ao vivo (endpoint enquete.php no servidor).
- Campo de comentário opcional (qual livro está lendo, dúvidas, sugestões).
- Fallback honesto: se o endpoint PHP não estiver ativo, o voto/comentário
  vai por e-mail (FormSubmit) e a enquete avisa que os percentuais voltam
  quando o servidor ativar o PHP.

Aplica em: paginas/home_preview.html e site-contabo/index.html
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]

CSS_ENQUETE = """
  /* ===== Enquete de participação ===== */
  .enquete-sec{background:var(--cream-2);padding:70px 0;position:relative;overflow:hidden}
  .enquete-sec::before{content:"💬";position:absolute;right:-26px;bottom:-30px;font-size:170px;opacity:.05;transform:rotate(-10deg);pointer-events:none}
  .enquete-box{max-width:680px;margin:0 auto;background:#fff;border:1px solid rgba(201,162,75,.35);border-radius:16px;padding:28px 26px;box-shadow:var(--shadow);position:relative;z-index:1}
  .enquete-box h3{font-family:var(--serif);color:var(--navy);font-size:1.25rem;margin:0 0 6px;line-height:1.3}
  .enquete-box .eq-sub{color:var(--muted);font-size:.9rem;margin:0 0 18px}
  .eq-opcoes{display:flex;flex-direction:column;gap:9px}
  .eq-op{
    display:flex;align-items:center;gap:11px;text-align:left;width:100%;
    background:var(--cream);border:1px solid rgba(201,162,75,.4);border-radius:10px;
    padding:12px 14px;cursor:pointer;font-family:var(--sans);font-size:.95rem;color:var(--navy);
    transition:.15s;position:relative;overflow:hidden;
  }
  .eq-op:hover{border-color:var(--gold);background:#fff;transform:translateY(-1px)}
  .eq-op input{margin:0;accent-color:var(--gold-dark)}
  .eq-op .eq-label{flex:1;min-width:0}
  .eq-op .eq-pct{font-weight:700;color:var(--gold-dark);font-size:.85rem;white-space:nowrap}
  .eq-op .eq-barra{position:absolute;left:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--gold-light),var(--gold-dark));width:0%;transition:width .6s ease;border-radius:3px}
  .eq-op.selecionada{border-color:var(--gold);background:#fffdf5}
  .eq-comentario{margin-top:16px}
  .eq-comentario textarea{width:100%;padding:11px 13px;border:1px solid rgba(201,162,75,.4);border-radius:10px;font-family:var(--sans);font-size:.92rem;color:var(--navy);resize:vertical;min-height:64px}
  .eq-comentario textarea:focus{outline:none;border-color:var(--gold)}
  .eq-acoes{display:flex;align-items:center;gap:12px;margin-top:12px;flex-wrap:wrap}
  .eq-acoes .btn{padding:12px 22px;font-size:.92rem}
  .eq-mensagem{margin-top:14px;font-size:.88rem;color:var(--muted);display:none;align-items:center;gap:8px;line-height:1.5}
  .eq-mensagem.visivel{display:flex}
  .eq-mensagem.ok{color:#2e7d32}
  .eq-resultado{margin-top:16px;display:none}
  .eq-resultado .eq-total{font-size:.8rem;color:var(--muted);text-align:center;margin-top:12px}
  .eq-comentarios{margin-top:14px;border-top:1px dashed rgba(201,162,75,.4);padding-top:12px;display:none}
  .eq-comentarios h4{font-size:.85rem;color:var(--gold-dark);margin:0 0 8px;letter-spacing:.05em;text-transform:uppercase}
  .eq-comentarios .eq-c{font-size:.85rem;color:var(--muted);padding:7px 0;border-bottom:1px dotted rgba(201,162,75,.25)}
  .eq-comentarios .eq-c:last-child{border-bottom:none}
  .eq-aviso{font-size:.75rem;color:var(--muted);margin-top:14px;text-align:center}
"""

HTML_ENQUETE = """
<section class="enquete-sec" id="enquete">
  <div class="wrap">
    <div class="section-head">
      <span class="eyebrow">📊 Participe</span>
      <h2>Sua opinião faz a diferença</h2>
      <p>Leva menos de um minuto e ajuda a melhorar a experiência de todos os leitores.</p>
    </div>
    <div class="enquete-box" id="enquete-box">
      <h3>O que você achou da leitura online com marcadores?</h3>
      <p class="eq-sub">Agora você continua de onde parou, com a fita dourada e as letras no seu tamanho.</p>
      <form id="eq-form">
        <div class="eq-opcoes">
          <label class="eq-op"><input type="radio" name="eq-voto" value="amei"><span class="eq-label">😍 Amei, me ajuda muito a continuar a leitura</span><span class="eq-pct" data-pct="amei"></span><span class="eq-barra" data-barra="amei"></span></label>
          <label class="eq-op"><input type="radio" name="eq-voto" value="gostei"><span class="eq-label">😊 Gostei, é muito prático</span><span class="eq-pct" data-pct="gostei"></span><span class="eq-barra" data-barra="gostei"></span></label>
          <label class="eq-op"><input type="radio" name="eq-voto" value="util"><span class="eq-label">👍 Parece útil, ainda estou descobrindo</span><span class="eq-pct" data-pct="util"></span><span class="eq-barra" data-barra="util"></span></label>
          <label class="eq-op"><input type="radio" name="eq-voto" value="nao_usei"><span class="eq-label">🤔 Ainda não usei a leitura online</span><span class="eq-pct" data-pct="nao_usei"></span><span class="eq-barra" data-barra="nao_usei"></span></label>
        </div>
        <div class="eq-comentario">
          <textarea id="eq-comentario" placeholder="Conte mais (opcional): qual livro você está lendo? Está gostando? Tem alguma dúvida ou sugestão?"></textarea>
        </div>
        <div class="eq-acoes">
          <button type="submit" class="btn btn-gold" id="eq-enviar">Votar e participar</button>
        </div>
      </form>
      <div class="eq-mensagem" id="eq-mensagem"></div>
      <div class="eq-resultado" id="eq-resultado"></div>
      <div class="eq-comentarios" id="eq-comentarios"></div>
      <p class="eq-aviso">🔒 Votação anônima. Usamos apenas para entender melhor os nossos leitores e melhorar o portal.</p>
    </div>
  </div>
</section>
"""

JS_ENQUETE = """
<script>
(function(){
  "use strict";
  var OPCOES = { amei:"😍 Amei, me ajuda muito", gostei:"😊 Gostei, é muito prático", util:"👍 Parece útil", nao_usei:"🤔 Ainda não usei" };
  var jaVotou = false;
  try{ jaVotou = localStorage.getItem("despertar_enquete_votada") === "1"; }catch(e){}
  var form = document.getElementById("eq-form");
  var msg = document.getElementById("eq-mensagem");
  var resultDiv = document.getElementById("eq-resultado");
  var comDiv = document.getElementById("eq-comentarios");

  function aplicarResultados(d){
    var tot = d.votos || 0;
    for (var chave in OPCOES){
      var pctEl = document.querySelector('[data-pct="' + chave + '"]');
      var barEl = document.querySelector('[data-barra="' + chave + '"]');
      var p = (d.percentuais && d.percentuais[chave]) ? d.percentuais[chave] : 0;
      if(pctEl){ pctEl.textContent = tot > 0 ? p + "%" : ""; }
      if(barEl){ barEl.style.width = (tot > 0 ? p : 0) + "%"; }
    }
    var totalEl = document.querySelector(".eq-total");
    if(totalEl){ totalEl.textContent = tot + (tot === 1 ? " voto" : " votos"); }
    // comentários recentes
    if(d.comentarios && d.comentarios.length){
      var h = "";
      d.comentarios.forEach(function(c){ h += '<div class="eq-c">💬 ' + c.texto + ' <span style="color:var(--gold-dark)">· ' + c.data + '</span></div>'; });
      comDiv.innerHTML = '<h4>Comentários dos leitores</h4>' + h;
      comDiv.style.display = "block";
    }
  }

  function carregar(){
    fetch("enquete.php", { cache:"no-store" })
      .then(function(r){ if(!r.ok){ throw new Error("offline"); } return r.json(); })
      .then(function(d){
        aplicarResultados(d);
        var box = document.querySelector(".enquete-box");
        var nota = document.createElement("p");
        nota.className = "eq-total";
        nota.textContent = (d.votos || 0) + (d.votos === 1 ? " voto até agora" : " votos até agora");
        box.appendChild(nota);
      })
      .catch(function(){
        // Fallback honesto: PHP indisponível -> voto segue por e-mail
        msg.textContent = "📧 A votação ao vivo ainda não está ativa neste momento. Seu voto e comentário podem ser enviados por e-mail normalmente.";
        msg.className = "eq-mensagem visivel";
      });
  }

  form.addEventListener("submit", function(e){
    e.preventDefault();
    var escolhido = form.querySelector('input[name="eq-voto"]:checked');
    if(!escolhido){
      msg.textContent = "🙏 Toque em uma das opções acima para votar.";
      msg.className = "eq-mensagem visivel";
      return;
    }
    if(jaVotou){
      msg.textContent = "💛 Você já participou! Obrigado por contribuir.";
      msg.className = "eq-mensagem visivel ok";
      return;
    }
    var voto = escolhido.value;
    var comentario = document.getElementById("eq-comentario").value.trim();

    var payload = { voto: voto };
    if(comentario){ payload.comentario = comentario; }

    fetch("enquete.php", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
    .then(function(r){ return r.json().then(function(d){ return {ok:r.ok, d:d}; }); })
    .then(function(res){
      if(res.ok){
        aplicarResultados(res.d);
        msg.textContent = "💛 Obrigado por participar! Seu voto foi registrado.";
        msg.className = "eq-mensagem visivel ok";
        try{ localStorage.setItem("despertar_enquete_votada", "1"); }catch(err){}
        form.querySelectorAll('input[name="eq-voto"]').forEach(function(i){ i.disabled = true; });
      }else{
        throw new Error(res.d && res.d.erro ? res.d.erro : "erro");
      }
    })
    .catch(function(err){
      // Fallback: envia por e-mail via FormSubmit
      var url = "https://formsubmit.co/ajax/compraoseu.com@gmail.com";
      var dados = {
        _subject: "📊 Voto na enquete do Portal",
        _template: "table",
        _captcha: "false",
        Voto: OPCOES[voto] || voto,
        Comentario: comentario || "(sem comentário)"
      };
      fetch(url, { method:"POST", headers:{ "Content-Type":"application/json", "Accept":"application/json" }, body: JSON.stringify(dados) })
        .then(function(){ msg.textContent = "💛 Obrigado! Seu voto foi enviado (por e-mail). Os percentuais ao vivo voltam quando ativarmos a votação no servidor."; msg.className = "eq-mensagem visivel ok"; })
        .catch(function(){ msg.textContent = "🙏 Obrigado pela sua participação! Se quiser, envie seu voto para contato@compraoseu.com."; msg.className = "eq-mensagem visivel ok"; });
      try{ localStorage.setItem("despertar_enquete_votada", "1"); }catch(err){}
    });
  });

  carregar();
})();
</script>
"""


def aplicar(arquivo):
    html = arquivo.read_text(encoding="utf-8")
    if 'id="enquete"' in html:
        print("  (já tem enquete, pulando):", arquivo.name)
        return
    # CSS antes de </style>
    assert "</style>" in html
    html = html.replace("</style>", CSS_ENQUETE + "\n</style>", 1)
    # HTML antes da trilogia
    alvo = '<section id="trilogia" class="dark">'
    assert alvo in html, "seção trilogia não encontrada em " + arquivo.name
    html = html.replace(alvo, HTML_ENQUETE + "\n" + alvo, 1)
    # JS antes de </body>
    assert "</body>" in html
    html = html.replace("</body>", JS_ENQUETE + "\n</body>", 1)
    arquivo.write_text(html, encoding="utf-8")
    print("  OK:", arquivo.name)


def main():
    aplicar(RAIZ / "paginas" / "home_preview.html")
    aplicar(RAIZ / "site-contabo" / "index.html")


if __name__ == "__main__":
    main()
    print("Concluído.")
