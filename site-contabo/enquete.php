<?php
/**
 * enquete.php — Endpoint de votação da enquete do Portal O Despertar
 *
 * GET  -> página bonita de resultado (navegador) ou JSON (fetch/API)
 * POST -> registra um voto (+ comentário opcional) e retorna resultados
 *
 * Dados:  enquete_dados.json (mesmo diretório) — criado automaticamente
 * Erros:  enquete_erro.log   (ajuda a diagnosticar permissões)
 * Uso:    https://compraoseu.com/enquete.php
 *         https://compraoseu.com/enquete.php?json=1  (JSON puro)
 */

header('Cache-Control: no-store');

// O Content-Type é definido por resposta (JSON ou HTML), não aqui no topo,
// para que a página bonita (text/html) renderize corretamente no navegador.

$ARQUIVO = __DIR__ . '/enquete_dados.json';
$ARQUIVO_IP = __DIR__ . '/enquete_ips.json';
$ARQUIVO_ERRO = __DIR__ . '/enquete_erro.log';

$OPCOES = array(
    'ansiedade' => 'Ansiedade e preocupacao',
    'magoas'    => 'Magoas e lembrancas do passado',
    'medo'      => 'Medo do futuro',
    'paz'       => 'Falta de paz e proposito'
);

function dados_iniciais() {
    return array(
        'votos' => 0,
        'opcoes' => array('ansiedade' => 0, 'magoas' => 0, 'medo' => 0, 'paz' => 0),
        'comentarios' => array()
    );
}

function registrar_erro($msg) {
    @file_put_contents(
        $GLOBALS['ARQUIVO_ERRO'],
        '[' . date('d/m/Y H:i:s') . '] ' . $msg . "\n",
        FILE_APPEND
    );
}

function criar_arquivo($arq) {
    $ok = @file_put_contents($arq, json_encode(dados_iniciais(), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
    if ($ok !== false) {
        @chmod($arq, 0664);
    } else {
        registrar_erro('Nao consegui criar ' . basename($arq) . ' em ' . __DIR__);
    }
    return $ok !== false;
}

function ler_dados($arq) {
    if (!file_exists($arq)) {
        criar_arquivo($arq);
        return dados_iniciais();
    }
    $t = @file_get_contents($arq);
    $d = json_decode($t, true);
    if (!is_array($d) || !isset($d['opcoes'])) {
        registrar_erro('Arquivo ' . basename($arq) . ' invalido ou vazio; recriando');
        criar_arquivo($arq);
        return dados_iniciais();
    }
    return $d;
}

function salvar_dados($arq, $dados) {
    // Gravação atômica: arquivo temporário + rename (evita corromper o arquivo)
    $atual = ler_dados($arq);
    $atual['votos'] = (isset($atual['votos']) ? $atual['votos'] : 0) + $dados['votos'];
    foreach ($dados['opcoes'] as $k => $v) {
        if (!isset($atual['opcoes'][$k])) { $atual['opcoes'][$k] = 0; }
        $atual['opcoes'][$k] += $v;
    }
    if (isset($dados['comentarios'])) {
        if (!isset($atual['comentarios']) || !is_array($atual['comentarios'])) {
            $atual['comentarios'] = array();
        }
        $atual['comentarios'] = array_merge($atual['comentarios'], $dados['comentarios']);
    }

    $tmp = $arq . '.tmp';
    $ok = @file_put_contents($tmp, json_encode($atual, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
    if ($ok === false) {
        registrar_erro('Falha ao escrever temporario ' . basename($tmp));
        return false;
    }
    @chmod($tmp, 0664);
    if (!@rename($tmp, $arq)) {
        // fallback: copia
        if (!@copy($tmp, $arq)) {
            registrar_erro('Falha ao renomear/copiar para ' . basename($arq));
            @unlink($tmp);
            return false;
        }
        @unlink($tmp);
    }
    return $atual;
}

function resultado_json($dados) {
    $tot = isset($dados['votos']) ? $dados['votos'] : 0;
    $res = array(
        'votos' => $tot,
        'opcoes' => array(),
        'percentuais' => array()
    );
    foreach ($GLOBALS['OPCOES'] as $chave => $rotulo) {
        $n = isset($dados['opcoes'][$chave]) ? $dados['opcoes'][$chave] : 0;
        $res['opcoes'][$chave] = array('rotulo' => $rotulo, 'votos' => $n);
        $res['percentuais'][$chave] = $tot > 0 ? round($n / $tot * 100) : 0;
    }
    $res['comentarios'] = isset($dados['comentarios']) ? array_slice(array_reverse($dados['comentarios']), 0, 20) : array();
    return $res;
}

function pagina_resultado($res) {
    $tot = $res['votos'];
    $linhas = '';
    $emoji = array('ansiedade' => '😰', 'magoas' => '😔', 'medo' => '😨', 'paz' => '🕊️');
    foreach ($res['opcoes'] as $chave => $op) {
        $p = isset($res['percentuais'][$chave]) ? $res['percentuais'][$chave] : 0;
        $n = $op['votos'];
        $e = isset($emoji[$chave]) ? $emoji[$chave] : '💬';
        $linhas .= '<div class="linha"><div class="rot">' . $e . ' ' . htmlspecialchars($op['rotulo'], ENT_QUOTES, 'UTF-8') . '</div>'
                 . '<div class="barra"><div class="fill" style="width:' . $p . '%"></div></div>'
                 . '<div class="pct">' . $p . '% (' . $n . ' ' . ($n === 1 ? 'voto' : 'votos') . ')</div></div>';
    }
    $com = '';
    if (!empty($res['comentarios'])) {
        $com = '<div class="com"><h3>💬 Comentários dos leitores</h3>';
        foreach ($res['comentarios'] as $c) {
            $com .= '<div class="c"><span>' . htmlspecialchars($c['texto'], ENT_QUOTES, 'UTF-8') . '</span><em>' . $c['data'] . '</em></div>';
        }
        $com .= '</div>';
    }
    return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
         . '<meta name="viewport" content="width=device-width, initial-scale=1">'
         . '<meta name="robots" content="noindex, nofollow">'
         . '<title>📊 Enquete — Portal O Despertar</title>'
         . '<style>'
         . 'body{margin:0;font-family:Georgia,serif;background:#0e1a2e;color:#e8ecf3;padding:28px 16px}'
         . '.wrap{max-width:640px;margin:0 auto}'
         . '.topo{text-align:center;padding:26px 18px;background:radial-gradient(600px 300px at 70% -20%,rgba(201,162,75,.18),transparent 60%),linear-gradient(170deg,#0e1a2e,#120b18);border:1px solid rgba(201,162,75,.25);border-radius:16px 16px 0 0}'
         . '.topo .selo{font-size:.72rem;letter-spacing:.35em;text-transform:uppercase;color:#e3c877;margin-bottom:12px}'
         . '.topo h1{color:#c9a24b;font-size:1.35rem;margin:0 0 6px}'
         . '.topo p{color:#c4cdda;font-size:.92rem;margin:0}'
         . '.card{background:#16283f;border:1px solid rgba(201,162,75,.25);border-top:none;padding:22px 20px}'
         . '.linha{margin-bottom:16px}.rot{font-size:.92rem;margin-bottom:6px;color:#e8ecf3}'
         . '.barra{height:14px;background:#0e1a2e;border-radius:8px;overflow:hidden}'
         . '.fill{height:100%;background:linear-gradient(90deg,#c9a24b,#e3c877);border-radius:8px;transition:width .6s}'
         . '.pct{font-size:.8rem;color:#9fb0c8;margin-top:4px;text-align:right}'
         . '.tot{text-align:center;color:#e3c877;font-size:.9rem;margin-top:20px;padding-top:14px;border-top:1px dashed rgba(201,162,75,.35)}'
         . '.tot b{font-size:1.3rem}'
         . '.com{border-top:1px dashed rgba(201,162,75,.4);margin-top:18px;padding-top:14px}'
         . '.com h3{color:#c9a24b;font-size:.9rem;margin:0 0 10px}'
         . '.c{font-size:.85rem;color:#c4cdda;padding:7px 0;border-bottom:1px dotted rgba(201,162,75,.2)}'
         . '.c em{color:#c9a24b;font-size:.75rem;margin-left:8px;font-style:normal}'
         . '.voltar{display:block;text-align:center;margin-top:20px;padding:13px;background:linear-gradient(180deg,#d4a83f,#b8860b);color:#fff;text-decoration:none;border-radius:10px;font-weight:700;font-size:.95rem}'
         . '.voltar:hover{opacity:.92}'
         . '.rodape{text-align:center;color:#7f8ca1;font-size:.75rem;margin-top:16px}'
         . '</style></head><body><div class="wrap">'
         . '<div class="topo"><div class="selo">Portal O Despertar</div><h1>📊 Enquete de participação</h1><p>Qual é a maior batalha da sua mente hoje?</p></div>'
         . '<div class="card">'
         . $linhas
         . '<div class="tot"><b>' . $tot . '</b> ' . ($tot === 1 ? 'voto' : 'votos') . ' até agora</div>'
         . $com
         . '</div>'
         . '<a class="voltar" href="https://compraoseu.com/#enquete">← Voltar para o site</a>'
         . '<div class="rodape">CompraOSeu · Missão com Deus · compraoseu.com</div>'
         . '</div></body></html>';
}

$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo === 'GET') {
    $dados = ler_dados($ARQUIVO);
    $json = resultado_json($dados);
    // JSON puro se pedido explicitamente (?json=1) ou via fetch (Accept sem text/html)
    $aceita = isset($_SERVER['HTTP_ACCEPT']) ? $_SERVER['HTTP_ACCEPT'] : '';
    $quer_json = isset($_GET['json']);
    if ($quer_json || strpos($aceita, 'text/html') === false) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode($json, JSON_UNESCAPED_UNICODE);
        exit;
    }
    header('Content-Type: text/html; charset=utf-8');
    echo pagina_resultado($json);
    exit;
}

if ($metodo === 'POST') {
    header('Content-Type: application/json; charset=utf-8');
    $corpo = file_get_contents('php://input');
    $req = json_decode($corpo, true);
    if (!is_array($req)) {
        http_response_code(400);
        echo json_encode(array('erro' => 'Dados invalidos'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    $voto = isset($req['voto']) ? $req['voto'] : '';
    $comentario = isset($req['comentario']) ? trim(strip_tags($req['comentario'])) : '';
    $email = isset($req['email']) ? trim(strip_tags($req['email'])) : '';
    if ($email !== '' && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $email = ''; // e-mail inválido: ignora, mas não bloqueia
    }
    if ($comentario !== '') {
        if (function_exists('mb_substr')) {
            $comentario = mb_substr($comentario, 0, 500);
        } else {
            $comentario = substr($comentario, 0, 500);
        }
    }

    // MODO MENSAGEM: quem já votou (ou não escolheu opção) pode enviar apenas
    // um comentário/mensagem, SEM contabilizar voto. O voto é opcional.
    $eh_voto = isset($OPCOES[$voto]);
    if (!$eh_voto && $comentario === '') {
        http_response_code(400);
        echo json_encode(array('erro' => 'Envie uma opcao de voto ou uma mensagem.'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    // Proteção leve: no mínimo 30 segundos entre ações do mesmo IP
    $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : 'desconhecido';
    $ips = array();
    if (file_exists($ARQUIVO_IP)) {
        $t = @file_get_contents($ARQUIVO_IP);
        $ips = json_decode($t, true);
        if (!is_array($ips)) { $ips = array(); }
    }
    $agora = time();
    if (isset($ips[$ip]) && ($agora - $ips[$ip]) < 30) {
        http_response_code(429);
        echo json_encode(array('erro' => 'Aguarde alguns segundos antes de enviar novamente'), JSON_UNESCAPED_UNICODE);
        exit;
    }
    $ips[$ip] = $agora;
    @file_put_contents($ARQUIVO_IP, json_encode($ips));

    // Monta a alteração: voto (se houver) e/ou comentário
    $novo = array('votos' => 0, 'opcoes' => array());
    if ($eh_voto) {
        $novo['votos'] = 1;
        $novo['opcoes'][$voto] = 1;
    }
    if ($comentario !== '') {
        $novo['comentarios'] = array(array(
            'texto' => $comentario,
            'data' => date('d/m/Y H:i'),
            'email' => $email  // privado: usado apenas para responder
        ));
    }

    $salvo = salvar_dados($ARQUIVO, $novo);
    if ($salvo === false) {
        http_response_code(500);
        echo json_encode(array('erro' => 'Nao foi possivel salvar. Verifique a permissao de escrita do diretorio.'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    $resposta = resultado_json($salvo);
    $resposta['so_mensagem'] = !$eh_voto;
    echo json_encode($resposta, JSON_UNESCAPED_UNICODE);
    exit;
}

http_response_code(405);
header('Content-Type: application/json; charset=utf-8');
echo json_encode(array('erro' => 'Metodo nao permitido'), JSON_UNESCAPED_UNICODE);
