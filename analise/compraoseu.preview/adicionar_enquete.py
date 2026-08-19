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
  .eq-email{margin-top:10px}
  .eq-email input{width:100%;padding:11px 13px;border:1px solid rgba(201,162,75,.4);border-radius:10px;font-family:var(--sans);font-size:.92rem;color:var(--navy)}
  .eq-email input:focus{outline:none;border-color:var(--gold)}
  .eq-acoes{display:flex;align-items:center;gap:12px;margin-top:12px;flex-wrap:wrap}
  .eq-acoes .btn{padding:12px 22px;font-size:.92rem}
  .eq-mensagem{margin-top:14px;font-size:.88rem;color:var(--muted);display:none;align-items:center;gap:8px;line-height:1.5}
  .eq-mensagem.visivel{display:flex}
  .eq-mensagem.ok{color:#2e7d32}
  .eq-resultado{margin-top:16px;display:none}
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
      <h3>Qual é a maior batalha da sua mente hoje?</h3>
      <p class="eq-sub">Responda com o coração aberto. Não há resposta certa ou errada, apenas um convite para olhar para dentro.</p>
      <form id="eq-form">
        <div class="eq-opcoes">
          <label class="eq-op"><input type="radio" name="eq-voto" value="ansiedade"><span class="eq-label">😰 Ansiedade e preocupação</span><span class="eq-pct" data-pct="ansiedade"></span><span class="eq-barra" data-barra="ansiedade"></span></label>
          <label class="eq-op"><input type="radio" name="eq-voto" value="magoas"><span class="eq-label">😔 Mágoas e lembranças do passado</span><span class="eq-pct" data-pct="magoas"></span><span class="eq-barra" data-barra="magoas"></span></label>
          <label class="eq-op"><input type="radio" name="eq-voto" value="medo"><span class="eq-label">😨 Medo do futuro</span><span class="eq-pct" data-pct="medo"></span><span class="eq-barra" data-barra="medo"></span></label>
          <label class="eq-op"><input type="radio" name="eq-voto" value="paz"><span class="eq-label">🕊️ Falta de paz e propósito</span><span class="eq-pct" data-pct="paz"></span><span class="eq-barra" data-barra="paz"></span></label>
        </div>
        <div class="eq-comentario">
          <textarea id="eq-comentario" placeholder="Quer compartilhar? (opcional) O que você tem feito para vencer essa batalha?"></textarea>
        </div>
        <div class="eq-email">
          <input type="email" id="eq-email" placeholder="Seu e-mail (opcional) — se quiser uma resposta" autocomplete="email">
        </div>
        <div class="eq-acoes">
          <button type="submit" class="btn btn-gold" id="eq-enviar">Votar e participar</button>
        </div>
      </form>
      <div class="eq-mensagem" id="eq-mensagem"></div>
      <div class="eq-resultado" id="eq-resultado"></div>
      <div class="eq-comentarios" id="eq-comentarios"></div>
      <p class="eq-aviso">🔒 Votação anônima. Quem deixar o e-mail recebe resposta. Para conversar na hora, fale conosco no <a href="https://wa.me/5528999111493?text=Ol%C3%A1%2C%20escrevi%20na%20enquete%20do%20Portal%20e%20quero%20tirar%20uma%20d%C3%BAvida" style="color:var(--gold-dark);font-weight:700;text-decoration:underline">WhatsApp 💬</a>.</p>
    </div>
  </div>
</section>
"""

JS_ENQUETE = """
<script>
(function(){
  "use strict";
  var OPCOES = { ansiedade:"😰 Ansiedade e preocupação", magoas:"😔 Mágoas e lembranças do passado", medo:"😨 Medo do futuro", paz:"🕊️ Falta de paz e propósito" };
  var jaVotou = false;
  try{ jaVotou = localStorage.getItem("despertar_enquete_votada_v2") === "1"; }catch(e){}
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
    // comentários recentes
    if(d.comentarios && d.comentarios.length){
      var h = "";
      d.comentarios.forEach(function(c){ h += '<div class="eq-c">💬 ' + c.texto + ' <span style="color:var(--gold-dark)">· ' + c.data + '</span></div>'; });
      comDiv.innerHTML = '<h4>Comentários dos leitores</h4>' + h;
      comDiv.style.display = "block";
    }
    // SEGUNDA CAMADA (pós-resultado): convite a compartilhar leitura que ajudou
    var convite = document.getElementById("eq-convite2");
    if(!convite && tot > 0){
      convite = document.createElement("div");
      convite.id = "eq-convite2";
      convite.style.cssText = "margin-top:14px;padding:12px 14px;background:rgba(201,162,75,.08);border:1px dashed rgba(201,162,75,.4);border-radius:10px;font-size:.88rem;color:var(--navy);text-align:center;";
      convite.innerHTML = "💛 <b>" + tot + "% também lutam com isso.</b> E você, já leu algo que te ajudou nessa batalha? <a href=\"#enquete\" onclick=\"document.getElementById('eq-comentario').focus();return false;\" style=\"color:var(--gold-dark);font-weight:700;text-decoration:underline\">Compartilhe aqui</a> (opcional).";
      var box = document.querySelector(".enquete-box");
      if(box){ box.appendChild(convite); }
    }

  function carregar(){
    // A contagem de votos fica OCULTA na página (pedido do autor).
    // Antes de votar, nada é exibido; após o voto, os percentuais aparecem.
    fetch("enquete.php", { cache:"no-store" })
      .then(function(r){ if(!r.ok){ throw new Error("offline"); } return r.json(); })
      .then(function(){ /* silencioso: só confirma que o endpoint está ativo */ })
      .catch(function(){
        // Fallback honesto: PHP indisponível -> voto segue por e-mail
        msg.textContent = "📧 A votação ao vivo ainda não está ativa neste momento. Seu voto e comentário podem ser enviados por e-mail normalmente.";
        msg.className = "eq-mensagem visivel";
      });
  }

  // Modo mensagem: quem já votou pode enviar apenas uma mensagem/comentário
  // (sem contabilizar voto). O sistema detecta e mostra só o campo de texto.
  function modoMensagem(){
    var opcoes = document.querySelectorAll('.eq-opcoes .eq-op');
    var rotulo = document.querySelector('.eq-sub');
    var botao = document.getElementById("eq-enviar");
    opcoes.forEach(function(op){ op.style.display = "none"; });
    if(rotulo){ rotulo.innerHTML = "💬 Quer enviar uma mensagem sobre os livros ou a leitura? Fique à vontade! Ou <a href=\"https://wa.me/5528999111493?text=Ol%C3%A1%2C%20quero%20falar%20sobre%20os%20livros%20do%20Portal\" style=\"color:var(--gold-dark);font-weight:700;text-decoration:underline\">converse no WhatsApp</a>."; }
    if(botao){ botao.textContent = "💬 Enviar mensagem"; }
    var ta = document.getElementById("eq-comentario");
    if(ta){ ta.placeholder = "Escreva sua mensagem ou dúvida sobre os livros..."; }
  }
  if(jaVotou){ modoMensagem(); }

  form.addEventListener("submit", function(e){
    e.preventDefault();
    var comentario = document.getElementById("eq-comentario").value.trim();

    if(jaVotou){
      // Quem já votou: envia SÓ a mensagem (sem voto)
      if(!comentario){
        msg.textContent = "✍️ Escreva sua mensagem antes de enviar.";
        msg.className = "eq-mensagem visivel";
        return;
      }
      var email = document.getElementById("eq-email").value.trim();
      var payload = { comentario: comentario };
      if(email){ payload.email = email; }
      enviar(payload, "💛 Mensagem enviada! Obrigado por escrever para nós.", true);
      return;
    }

    var escolhido = form.querySelector('input[name="eq-voto"]:checked');
    if(!escolhido){
      msg.textContent = "🙏 Toque em uma das opções acima para votar.";
      msg.className = "eq-mensagem visivel";
      return;
    }
    var voto = escolhido.value;
    var email = document.getElementById("eq-email").value.trim();
    var payload = { voto: voto };
    if(comentario){ payload.comentario = comentario; }
    if(email){ payload.email = email; }
    enviar(payload, "💛 Obrigado por participar! Seu voto foi registrado.", false);
  });

  // Envia o e-mail de notificação (FormSubmit) — SEMPRE, em paralelo com o
  // salvamento no PHP, para o autor receber cada voto/comentário.
  function notificarEmail(payload, soMensagem){
    // 1º: tenta o nosso servidor (notificar.php) — controle total
    var nosso = {
      voto: payload.voto || "",
      mensagem: payload.comentario || "",
      email: payload.email || "",
      so_mensagem: soMensagem ? 1 : 0
    };
    fetch("notificar.php", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(nosso)
    }).catch(function(){
      // Fallback: se o mail() do servidor falhar, usa FormSubmit
      var url = "https://formsubmit.co/ajax/compraoseu.com@gmail.com";
      var dados = {
        _subject: soMensagem ? "💬 Mensagem do Portal (enquete)" : "📊 Voto na enquete do Portal",
        _template: "table",
        _captcha: "false",
        Mensagem: payload.comentario || "(sem mensagem)",
        Voto: payload.voto ? (OPCOES[payload.voto] || payload.voto) : "(sem voto, só mensagem)",
        "E-mail do leitor (para responder)": payload.email || "(não informado)"
      };
      fetch(url, { method:"POST", headers:{ "Content-Type":"application/json", "Accept":"application/json" }, body: JSON.stringify(dados) }).catch(function(){});
    });
  }

  function enviar(payload, textoOk, soMensagem){
    fetch("enquete.php", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
    .then(function(r){ return r.json().then(function(d){ return {ok:r.ok, d:d}; }); })
    .then(function(res){
      if(res.ok){
        aplicarResultados(res.d);
        msg.textContent = textoOk;
        msg.className = "eq-mensagem visivel ok";
        notificarEmail(payload, soMensagem); // notifica por e-mail mesmo com sucesso
        try{ localStorage.setItem("despertar_enquete_votada_v2", "1"); }catch(err){}
        if(!soMensagem){
          form.querySelectorAll('input[name="eq-voto"]').forEach(function(i){ i.disabled = true; });
        }
        document.getElementById("eq-comentario").value = "";
      }else{
        throw new Error(res.d && res.d.erro ? res.d.erro : "erro");
      }
    })
    .catch(function(err){
      // Fallback honesto: se o PHP falhou, envia por e-mail via FormSubmit
      notificarEmail(payload, soMensagem);
      msg.textContent = soMensagem ? "💛 Mensagem enviada (por e-mail)! Obrigado." : "💛 Obrigado! Seu voto foi enviado (por e-mail).";
      msg.className = "eq-mensagem visivel ok";
      try{ localStorage.setItem("despertar_enquete_votada_v2", "1"); }catch(err){}
    });
  }

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
