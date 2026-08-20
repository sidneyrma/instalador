<?php
/**
 * enviar_guia.php — Envia o Guia "Pais e Filhos: Conversas que Protegem"
 *
 * Recebe o e-mail do pai/mãe, envia:
 *   1) O guia (link + conteúdo) para o pai/mãe (agradecimento)
 *   2) Notificação para o autor (compraoseu.com@gmail.com)
 *
 * Uso: https://missaocomdeus.com.br/enviar_guia.php (POST JSON)
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$DESTINO = 'compraoseu.com@gmail.com';
$LINK_GUIA = 'https://missaocomdeus.com.br/guia-pais-filhos.html';

$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo === 'POST') {
    $corpo = file_get_contents('php://input');
    $req = json_decode($corpo, true);
    if (!is_array($req)) {
        http_response_code(400);
        echo json_encode(array('erro' => 'Dados invalidos'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    $email_pai = isset($req['email']) ? trim($req['email']) : '';
    if ($email_pai === '' || !filter_var($email_pai, FILTER_VALIDATE_EMAIL)) {
        http_response_code(400);
        echo json_encode(array('erro' => 'Informe um e-mail valido'), JSON_UNESCAPED_UNICODE);
        exit;
    }

    // Proteção: 5s entre envios do mesmo IP
    $ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : 'desconhecido';
    $ips = array();
    if (file_exists(__DIR__ . '/enquete_ips.json')) {
        $t = @file_get_contents(__DIR__ . '/enquete_ips.json');
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
    @file_put_contents(__DIR__ . '/enquete_ips.json', json_encode($ips));

    // ===== 1. Enviar o guia para o pai/mãe =====
    $assunto_pai = '👨‍👩‍👧 Guia Pais e Filhos: Conversas que Protegem';
    $corpo_pai = "Paz e graça, querido(a) irmão(ã)!\n\n";
    $corpo_pai .= "Obrigado por se importar com o diálogo em família. Segue o guia\n";
    $corpo_pai .= "\"Pais e Filhos: Conversas que Protegem\":\n\n";
    $corpo_pai .= "👉 " . $LINK_GUIA . "\n\n";
    $corpo_pai .= "Nele você encontra as 7 perguntas para conversar com seu filho(a)\n";
    $corpo_pai .= "com amor e respeito, além do fundamento bíblico.\n\n";
    $corpo_pai .= "\"Ensina a criança no caminho em que deve andar, e, ainda quando\n";
    $corpo_pai .= "for velho, não se desviará dele.\" (Provérbios 22:6)\n\n";
    $corpo_pai .= "Com amor, em Cristo Jesus,\n";
    $corpo_pai .= "Equipe Missão com Deus\n";
    $corpo_pai .= "— missaocomdeus.com.br\n";

    $cab_pai = "From: Missão com Deus <no-reply@missaocomdeus.com.br>\r\n";
    $cab_pai .= "Reply-To: " . $DESTINO . "\r\n";
    $cab_pai .= "Content-Type: text/plain; charset=utf-8\r\n";

    $ok_pai = @mail($email_pai, $assunto_pai, $corpo_pai, $cab_pai);

    // ===== 2. Notificar o autor =====
    $assunto_autor = '📨 Guia Pais e Filhos solicitado';
    $corpo_autor = "Um pai/mãe solicitou o Guia Pais e Filhos!\n\n";
    $corpo_autor .= "E-mail do pai/mãe: " . $email_pai . "\n";
    $corpo_autor .= "Data: " . date('d/m/Y H:i') . "\n\n";
    $corpo_autor .= "— Missão com Deus · missaocomdeus.com.br\n";

    $cab_autor = "From: Missão com Deus <no-reply@missaocomdeus.com.br>\r\n";
    $cab_autor .= "Content-Type: text/plain; charset=utf-8\r\n";

    @mail($DESTINO, $assunto_autor, $corpo_autor, $cab_autor);

    if ($ok_pai) {
        echo json_encode(array('ok' => true, 'msg' => 'Guia enviado para o seu e-mail!'), JSON_UNESCAPED_UNICODE);
    } else {
        http_response_code(500);
        echo json_encode(array('erro' => 'Nao foi possivel enviar o guia agora. Tente novamente em instantes.'), JSON_UNESCAPED_UNICODE);
    }
    exit;
}

http_response_code(405);
echo json_encode(array('erro' => 'Metodo nao permitido'), JSON_UNESCAPED_UNICODE);
