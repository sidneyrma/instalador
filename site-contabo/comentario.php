<?php
if (!function_exists('mb_strlen')) {
    function mb_strlen($s) { return strlen($s); }
    function mb_substr($s, $inicio, $max) { return substr($s, $inicio, $max); }
}

$DESTINO      = 'portalmissaocomdeus@gmail.com';
$ARQUIVO      = __DIR__ . '/comentarios_dados.php';

function registrar_erro($msg) {
    @file_put_contents(__DIR__ . '/comentarios_erro.log', '[' . date('d/m/Y H:i:s') . '] ' . $msg . "\n", FILE_APPEND);
}

function campo($chave, $padrao = '') {
    if (isset($_POST[$chave]) && is_string($_POST[$chave])) return trim($_POST[$chave]);
    $raw = file_get_contents('php://input');
    if ($raw) {
        $dados = @json_decode($raw, true);
        if (is_array($dados) && isset($dados[$chave]) && is_string($dados[$chave])) return trim($dados[$chave]);
    }
    return $padrao;
}

function resp($data, $status = 200) {
    http_response_code($status);
    echo json_encode($data, JSON_UNESCAPED_UNICODE);
    exit;
}

function limpar($texto, $max) {
    $texto = preg_replace('/[\r\n\t]+/', ' ', $texto);
    $texto = strip_tags($texto);
    $texto = trim($texto);
    return mb_substr($texto, 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    resp(array('ok' => false, 'salvo' => false, 'email_enviado' => false, 'erro' => 'Método não permitido. Use POST.'), 405);
}

$curso      = limpar(campo('curso'), 60);
$nome       = limpar(campo('nome'), 80);
$comentario = limpar(campo('comentario'), 2000);
$pagina     = limpar(campo('pagina'), 120);
$email      = trim(campo('email'));

if (mb_strlen($comentario) < 3) {
    resp(array('ok' => false, 'salvo' => false, 'email_enviado' => false, 'erro' => 'Comentário muito curto.'), 422);
}

if ($nome === '') { $nome = 'Aluno(a)'; }
if ($curso === '') { $curso = 'Curso de videoaulas'; }

$registros = array();
if (file_exists($ARQUIVO)) {
    $incluido = @include $ARQUIVO;
    if (is_array($incluido)) $registros = $incluido;
}

$registros[] = array(
    'id' => uniqid('c_', true),
    'data' => date('Y-m-d H:i:s'),
    'curso' => $curso,
    'nome' => $nome,
    'comentario' => $comentario,
    'pagina' => $pagina,
    'email' => $email,
);

$salvo = false;
$conteudo = "<?php\nreturn " . var_export($registros, true) . ";\n";
$tmp = $ARQUIVO . '.tmp';
if (@file_put_contents($tmp, $conteudo) !== false) {
    if (@rename($tmp, $ARQUIVO)) { @chmod($ARQUIVO, 0644); $salvo = true; }
    else { registrar_erro('Falha ao renomear tmp'); }
} else {
    registrar_erro('Falha ao gravar ' . $ARQUIVO);
}

$emailEnviado = false;
$assunto = '💬 ' . $curso . ' — Comentário de aluno';
$corpo  = "Nova mensagem da área do aluno!\n\n";
$corpo .= "Curso: " . $curso . "\n";
$corpo .= "Nome: " . $nome . "\n";
$corpo .= "Página: " . $pagina . "\n";
$corpo .= "Data: " . date('d/m/Y H:i:s') . "\n\n";
$corpo .= "Mensagem:\n" . $comentario . "\n\n";

$headers = "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
$headers .= "From: Portal Missão com Deus <no-reply@missaocomdeus.com.br>\r\n";
$headers .= "Reply-To: " . ($email !== '' ? $email : $DESTINO) . "\r\n";

@ini_set('sendmail_from', 'no-reply@missaocomdeus.com.br');
$enviou = @mail($DESTINO, $assunto, $corpo, $headers);
if ($enviou) {
    $emailEnviado = true;
} else {
    registrar_erro('mail() retornou falso para ' . $DESTINO);
}

resp(array(
    'ok' => $salvo || $emailEnviado,
    'salvo' => $salvo,
    'email_enviado' => $emailEnviado,
    'erro' => (!$salvo && !$emailEnviado) ? 'Mensagem não pôde ser registrada.' : null,
));