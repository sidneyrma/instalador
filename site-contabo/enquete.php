<?php
/**
 * enquete.php — Endpoint de votação da enquete do Portal O Despertar
 *
 * GET  -> retorna os resultados atuais (JSON com percentuais)
 * POST -> registra um voto (+ comentário opcional) e retorna os resultados
 *
 * Dados guardados em: enquete_dados.json (mesmo diretório)
 * Uso: https://compraoseu.com/enquete.php
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$ARQUIVO = __DIR__ . '/enquete_dados.json';
$ARQUIVO_IP = __DIR__ . '/enquete_ips.json';

$OPCOES = array(
    'amei'     => 'Amei, me ajuda muito a continuar a leitura',
    'gostei'   => 'Gostei, e muito prático',
    'util'     => 'Ainda estou descobrindo, mas parece util',
    'nao_usei' => 'Ainda nao usei a leitura online'
);

function dados_iniciais() {
    return array(
        'votos' => 0,
        'opcoes' => array('amei' => 0, 'gostei' => 0, 'util' => 0, 'nao_usei' => 0),
        'comentarios' => array()
    );
}

function criar_arquivo($arq) {
    $ok = @file_put_contents($arq, json_encode(dados_iniciais(), JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
    if ($ok !== false) {
        @chmod($arq, 0664);
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
        return dados_iniciais();
    }
    return $d;
}

function salvar_dados($arq, $dados) {
    $fp = @fopen($arq, 'c+');
    if (!$fp) {
        criar_arquivo($arq);
        $fp = @fopen($arq, 'c+');
    }
    if (!$fp) {
        return false;
    }
    flock($fp, LOCK_EX);
    $t = stream_get_contents($fp);
    $atual = json_decode($t, true);
    if (!is_array($atual) || !isset($atual['opcoes'])) {
        $atual = dados_iniciais();
    }
    // soma o novo voto
    foreach ($dados as $chave => $valor) {
        if (is_array($valor)) {
            if (!isset($atual[$chave]) || !is_array($atual[$chave])) {
                $atual[$chave] = array();
            }
            foreach ($valor as $k => $v) {
                $atual[$chave][$k] = (isset($atual[$chave][$k]) ? $atual[$chave][$k] : 0) + $v;
            }
        } else {
            $atual[$chave] = (isset($atual[$chave]) ? $atual[$chave] : 0) + $valor;
        }
    }
    ftruncate($fp, 0);
    rewind($fp);
    $ok = fwrite($fp, json_encode($atual, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT));
    flock($fp, LOCK_UN);
    fclose($fp);
    return $ok !== false ? $atual : false;
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
    foreach ($res['opcoes'] as $chave => $op) {
        $p = isset($res['percentuais'][$chave]) ? $res['percentuais'][$chave] : 0;
        $n = $op['votos'];
        $linhas .= '<div class="linha"><div class="rot">' . htmlspecialchars($op['rotulo'], ENT_QUOTES, 'UTF-8') . '</div>'
                 . '<div class="barra"><div class="fill" style="width:' . $p . '%"></div></div>'
                 . '<div class="pct">' . $p . '% (' . $n . ')</div></div>';
    }
    $com = '';
    if (!empty($res['comentarios'])) {
        $com = '<div class="com"><h3>Comentários dos leitores</h3>';
        foreach ($res['comentarios'] as $c) {
            $com .= '<div class="c"><span>💬 ' . htmlspecialchars($c['texto'], ENT_QUOTES, 'UTF-8') . '</span><em>' . $c['data'] . '</em></div>';
        }
        $com .= '</div>';
    }
    return '<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
         . '<meta name="viewport" content="width=device-width, initial-scale=1">'
         . '<meta name="robots" content="noindex, nofollow">'
         . '<title>Enquete — Portal O Despertar</title>'
         . '<style>body{margin:0;font-family:Georgia,serif;background:#0e1a2e;color:#e8ecf3;padding:32px 16px}'
         . '.wrap{max-width:620px;margin:0 auto;background:#16283f;border:1px solid rgba(201,162,75,.3);border-radius:16px;padding:28px}'
         . 'h1{color:#c9a24b;font-size:1.4rem;margin:0 0 6px}h2{color:#e3c877;font-size:1.05rem;font-weight:normal;margin:0 0 22px}'
         . '.linha{margin-bottom:16px}.rot{font-size:.92rem;margin-bottom:6px}.barra{height:14px;background:#0e1a2e;border-radius:8px;overflow:hidden}'
         . '.fill{height:100%;background:linear-gradient(90deg,#c9a24b,#e3c877);border-radius:8px;transition:width .5s}'
         . '.pct{font-size:.8rem;color:#9fb0c8;margin-top:4px;text-align:right}'
         . '.tot{text-align:center;color:#9fb0c8;font-size:.85rem;margin-top:22px}'
         . '.com{border-top:1px dashed rgba(201,162,75,.4);margin-top:22px;padding-top:16px}'
         . '.com h3{color:#c9a24b;font-size:.9rem;margin:0 0 10px}.c{font-size:.85rem;color:#c4cdda;padding:6px 0;border-bottom:1px dotted rgba(201,162,75,.2)}'
         . '.c em{color:#c9a24b;font-size:.75rem;margin-left:8px;font-style:normal}</style></head><body><div class="wrap">'
         . '<h1>📊 Enquete do Portal</h1><h2>O que você achou da leitura online com marcadores?</h2>'
         . $linhas
         . '<div class="tot">' . $tot . ($tot === 1 ? ' voto' : ' votos') . ' até agora</div>'
         . $com
         . '</div></body></html>';
}

$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo === 'GET') {
    $dados = ler_dados($ARQUIVO);
    $json = resultado_json($dados);
    // Se o acesso é de um navegador (não uma requisição fetch da Home),
    // mostra uma página bonita com barras e percentuais.
    $aceita = isset($_SERVER['HTTP_ACCEPT']) ? $_SERVER['HTTP_ACCEPT'] : '';
    if (strpos($aceita, 'text/html') !== false) {
        echo pagina_resultado($json);
        exit;
    }
    echo json_encode($json, JSON_UNESCAPED_UNICODE);
    exit;
}

if ($metodo === 'POST') {
    $corpo = file_get_contents('php://input');
    $req = json_decode($corpo, true);
    if (!is_array($req)) {
        http_response_code(400);
        echo json_encode(array('erro' => 'Dados invalidos'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    $voto = isset($req['voto']) ? $req['voto'] : '';
    if (!isset($OPCOES[$voto])) {
        http_response_code(400);
        echo json_encode(array('erro' => 'Opcao de voto invalida'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    // Proteção leve: no mínimo 30 segundos entre votos do mesmo IP
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
        echo json_encode(array('erro' => 'Aguarde alguns segundos antes de votar novamente'), JSON_UNESCAPED_UNICODE);
        exit;
    }
    $ips[$ip] = $agora;
    @file_put_contents($ARQUIVO_IP, json_encode($ips));

    $novo = array(
        'votos' => 1,
        'opcoes' => array($voto => 1)
    );

    // Comentário opcional (máx. 500 caracteres)
    $comentario = isset($req['comentario']) ? trim(strip_tags($req['comentario'])) : '';
    if ($comentario !== '') {
        if (function_exists('mb_substr')) {
            $comentario = mb_substr($comentario, 0, 500);
        } else {
            $comentario = substr($comentario, 0, 500);
        }
        $novo['comentarios'] = array(array(
            'texto' => $comentario,
            'data' => date('d/m/Y H:i')
        ));
    }

    $salvo = salvar_dados($ARQUIVO, $novo);
    if ($salvo === false) {
        http_response_code(500);
        echo json_encode(array('erro' => 'Nao foi possivel salvar o voto. Verifique a permissao de escrita do diretorio.'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    echo json_encode(resultado_json($salvo), JSON_UNESCAPED_UNICODE);
    exit;
}

http_response_code(405);
echo json_encode(array('erro' => 'Metodo nao permitido'), JSON_UNESCAPED_UNICODE);
