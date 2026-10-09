<?php
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

$DIR = __DIR__ . '/dados';
$PUB = $DIR . '/avaliacoes.json';
$PEN = $DIR . '/avaliacoes-pendentes.json';
$MAX = 200;

function responder($cod, $dados) {
    http_response_code($cod);
    echo json_encode($dados, JSON_UNESCAPED_UNICODE);
    exit;
}

function garantir_pasta($dir) {
    if (!is_dir($dir)) {
        @mkdir($dir, 0750, true);
    }
}

function ler($arq) {
    if (!is_file($arq)) {
        return array('itens' => array());
    }
    $fp = fopen($arq, 'r');
    if (!$fp) return array('itens' => array());
    flock($fp, LOCK_SH);
    $raw = stream_get_contents($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    $j = json_decode($raw, true);
    if (is_array($j) && isset($j[0])) {
        return array('itens' => $j);
    }
    if (!is_array($j) || !isset($j['itens']) || !is_array($j['itens'])) {
        return array('itens' => array());
    }
    return $j;
}

function gravar($arq, $dados) {
    garantir_pasta(dirname($arq));
    $tmp = $arq . '.tmp';
    $fp = fopen($tmp, 'c+');
    if (!$fp) return false;
    if (!flock($fp, LOCK_EX)) {
        fclose($fp);
        return false;
    }
    ftruncate($fp, 0);
    rewind($fp);
    $ok = fwrite($fp, json_encode($dados, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT)) !== false;
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    if (!$ok) {
        @unlink($tmp);
        return false;
    }
    return rename($tmp, $arq);
}

function publico($item) {
    return array(
        'nome' => $item['nome'],
        'estrelas' => (int)$item['estrelas'],
        'texto' => $item['texto'],
        'data' => $item['data'],
    );
}

function limpar($s, $max) {
    $s = trim(strip_tags((string)$s));
    $s = preg_replace('/\s+/u', ' ', $s);
    if (function_exists('mb_substr')) {
        $s = mb_substr($s, 0, $max, 'UTF-8');
    } else {
        $s = substr($s, 0, $max);
    }
    return $s;
}

$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo === 'GET') {
    $dados = ler($PUB);
    $itens = array_map('publico', $dados['itens']);
    $itens = array_reverse($itens);
    $itens = array_slice($itens, 0, 40);
    $notas = array();
    foreach ($dados['itens'] as $it) {
        $notas[] = (int)$it['estrelas'];
    }
    $total = count($dados['itens']);
    $media = $total ? round(array_sum($notas) / $total, 1) : 0;
    responder(200, array(
        'itens' => $itens,
        'total' => $total,
        'media' => $media,
    ));
}

if ($metodo !== 'POST') {
    responder(405, array('erro' => 'Método não permitido.'));
}

$entrada = json_decode(file_get_contents('php://input'), true);
if (!is_array($entrada)) {
    $entrada = $_POST;
}

if (!empty($entrada['website']) || !empty($entrada['site_do_meio'])) {
    responder(200, array('ok' => true, 'mensagem' => 'Obrigado. Recebemos sua avaliação.'));
}

$nome = limpar(isset($entrada['nome']) ? $entrada['nome'] : '', 40);
$texto = limpar(isset($entrada['texto']) ? $entrada['texto'] : '', 400);
$estrelas = isset($entrada['estrelas']) ? (int)$entrada['estrelas'] : (isset($entrada['nota']) ? (int)$entrada['nota'] : 0);

if (strlen($nome) < 2) {
    responder(400, array('erro' => 'Escreva seu nome (pelo menos duas letras).'));
}
if ($estrelas < 1 || $estrelas > 5) {
    responder(400, array('erro' => 'Escolha de 1 a 5 estrelas.'));
}
$tam = function_exists('mb_strlen') ? mb_strlen($texto, 'UTF-8') : strlen($texto);
if ($tam < 10) {
    responder(400, array('erro' => 'Escreva um comentário com pelo menos 10 caracteres.'));
}

$ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
$hash = $ip ? hash('sha256', $ip . 'missao-depoimento') : '';
$agora = time();

$pend = ler($PEN);
$pub = ler($PUB);
foreach (array_merge($pend['itens'], $pub['itens']) as $it) {
    if ($hash && isset($it['ip']) && $it['ip'] === $hash && ($agora - (int)$it['ts']) < 86400) {
        responder(429, array('erro' => 'Você já enviou um depoimento hoje. Volte amanhã, se quiser escrever de novo.'));
    }
}

$item = array(
    'id' => bin2hex(random_bytes(8)),
    'nome' => $nome,
    'estrelas' => $estrelas,
    'texto' => $texto,
    'data' => date('d/m/Y'),
    'ts' => $agora,
    'ip' => $hash,
);

$pend['itens'][] = $item;
if (count($pend['itens']) > $MAX) {
    $pend['itens'] = array_slice($pend['itens'], -$MAX);
}

if (!gravar($PEN, $pend)) {
    responder(500, array('erro' => 'Não foi possível gravar agora. Tente de novo em instantes.'));
}

function avisar_email($nome, $estrelas, $texto) {
    $para = 'portalmissaocomdeus@gmail.com';
    $assunto = 'Nova avaliacao na fila da Missao com Deus';
    $corpo = "Chegou uma avaliacao esperando sua leitura.\n\nNome: ".$nome."\nEstrelas: ".$estrelas."\nData: ".date('d/m/Y H:i')."\n\n".$texto."\n\nAbra: https://missaocomdeus.com.br/moderar.php\nAprove ou recuse. So o que voce aprovar aparece em /guardar.\n";
    $log = array('quando' => date('c'), 'mail' => null, 'formsubmit' => null);

    // Gmail recusa carta que finge ser do proprio Gmail (From: @gmail.com) vinda do servidor.
    $cab  = "From: Missao com Deus <noreply@missaocomdeus.com.br>\r\n";
    $cab .= "Reply-To: ".$para."\r\n";
    $cab .= "MIME-Version: 1.0\r\n";
    $cab .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $ok_mail = @mail($para, '=?UTF-8?B?'.base64_encode($assunto).'?=', $corpo, $cab, '-f noreply@missaocomdeus.com.br');
    $log['mail'] = $ok_mail ? 'ok' : 'falhou';

    $campos = http_build_query(array(
        '_subject' => $assunto,
        '_captcha' => 'false',
        '_template' => 'box',
        'nome' => $nome,
        'estrelas' => (string)$estrelas,
        'avaliacao' => $texto,
        'link' => 'https://missaocomdeus.com.br/moderar.php',
    ));
    $fs = null;
    if (function_exists('curl_init')) {
        $ch = curl_init('https://formsubmit.co/ajax/'.$para);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/x-www-form-urlencoded',
            'Accept: application/json',
        ));
        curl_setopt($ch, CURLOPT_POSTFIELDS, $campos);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 8);
        curl_setopt($ch, CURLOPT_TIMEOUT, 20);
        curl_setopt($ch, CURLOPT_USERAGENT, 'MissaoComDeus/1.0');
        $fs = curl_exec($ch);
        $log['formsubmit'] = ($fs !== false && $fs !== '') ? substr($fs, 0, 180) : ('curl '.curl_error($ch));
        curl_close($ch);
    } else {
        $ctx = stream_context_create(array('http' => array(
            'method' => 'POST',
            'header' => "Content-Type: application/x-www-form-urlencoded\r\nAccept: application/json\r\n",
            'content' => $campos,
            'timeout' => 20,
        )));
        $fs = @file_get_contents('https://formsubmit.co/ajax/'.$para, false, $ctx);
        $log['formsubmit'] = $fs ? substr($fs, 0, 180) : 'file_get_contents falhou';
    }

    $pasta = __DIR__ . '/dados';
    if (!is_dir($pasta)) {
        @mkdir($pasta, 0750, true);
    }
    @file_put_contents($pasta . '/email-aviso.log', json_encode($log, JSON_UNESCAPED_UNICODE)."\n", FILE_APPEND | LOCK_EX);
}

avisar_email($nome, $estrelas, $texto);

responder(200, array(
    'ok' => true,
    'mensagem' => 'Obrigado. Recebemos sua avaliação.',
));
