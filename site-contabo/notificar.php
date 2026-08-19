<?php
/**
 * notificar.php — Envio de e-mail 100% próprio (sem FormSubmit)
 *
 * Recebe um POST em JSON com os dados do voto/comentário e envia o e-mail
 * direto pelo PHP (mail()), ficando tudo sob o nosso controle.
 *
 * Uso: https://missaocomdeus.com.br/notificar.php
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$DESTINO = 'compraoseu.com@gmail.com';
$ARQUIVO_IP = __DIR__ . '/enquete_ips.json';

$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo === 'POST') {
    $corpo = file_get_contents('php://input');
    $req = json_decode($corpo, true);
    if (!is_array($req)) {
        http_response_code(400);
        echo json_encode(array('erro' => 'Dados invalidos'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    $voto = isset($req['voto']) ? $req['voto'] : '';
    $mensagem = isset($req['mensagem']) ? trim(strip_tags($req['mensagem'])) : '';
    $email_leitor = isset($req['email']) ? trim($req['email']) : '';
    $so_mensagem = isset($req['so_mensagem']) ? (bool)$req['so_mensagem'] : false;

    // Validação leve do e-mail do leitor (se informado)
    if ($email_leitor !== '' && !filter_var($email_leitor, FILTER_VALIDATE_EMAIL)) {
        $email_leitor = '';
    }

    // Proteção: no mínimo 5 segundos entre envios do mesmo IP
    $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : 'desconhecido';
    $ips = array();
    if (file_exists($ARQUIVO_IP)) {
        $t = @file_get_contents($ARQUIVO_IP);
        $ips = json_decode($t, true);
        if (!is_array($ips)) { $ips = array(); }
    }
    $agora = time();
    if (isset($ips[$ip]) && ($agora - $ips[$ip]) < 5) {
        http_response_code(429);
        echo json_encode(array('erro' => 'Aguarde alguns segundos antes de enviar novamente'), JSON_UNESCAPED_UNICODE);
        exit;
    }
    $ips[$ip] = $agora;
    @file_put_contents($ARQUIVO_IP, json_encode($ips));

    // Monta o e-mail
    $assunto = $so_mensagem ? '💬 Mensagem do Portal (Missão com Deus)' : '📊 Voto na enquete do Portal';
    $corpo_email = "Nova participação no Portal Missão com Deus\n\n";
    $corpo_email .= "Data: " . date('d/m/Y H:i') . "\n";
    if (!$so_mensagem && $voto !== '') {
        $corpo_email .= "Voto: " . $voto . "\n";
    }
    if ($mensagem !== '') {
        $corpo_email .= "Mensagem: " . $mensagem . "\n";
    }
    if ($email_leitor !== '') {
        $corpo_email .= "E-mail do leitor (para responder): " . $email_leitor . "\n";
    }
    $corpo_email .= "\n— Missão com Deus · missaocomdeus.com.br\n";

    $cabecalhos = "From: Missão com Deus <no-reply@missaocomdeus.com.br>\r\n";
    $cabecalhos .= "Reply-To: " . ($email_leitor !== '' ? $email_leitor : $DESTINO) . "\r\n";
    $cabecalhos .= "Content-Type: text/plain; charset=utf-8\r\n";

    $enviado = @mail($DESTINO, $assunto, $corpo_email, $cabecalhos);

    if ($enviado) {
        echo json_encode(array('ok' => true, 'msg' => 'E-mail enviado com sucesso'), JSON_UNESCAPED_UNICODE);
    } else {
        http_response_code(500);
        echo json_encode(array('erro' => 'Nao foi possivel enviar o e-mail. Verifique o mail() do servidor.'), JSON_UNESCAPED_UNICODE);
    }
    exit;
}

http_response_code(405);
echo json_encode(array('erro' => 'Metodo nao permitido'), JSON_UNESCAPED_UNICODE);
