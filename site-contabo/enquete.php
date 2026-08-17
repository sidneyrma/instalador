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

function ler_dados($arq) {
    if (!file_exists($arq)) {
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

$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo === 'GET') {
    echo json_encode(resultado_json(ler_dados($ARQUIVO)), JSON_UNESCAPED_UNICODE);
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
