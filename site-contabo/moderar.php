<?php
session_start();
header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');
header('Referrer-Policy: no-referrer');

$CHAVE_SECRETA = ''; // Protegida fora do Git

$DIR = __DIR__ . '/dados';
$PUB = $DIR . '/avaliacoes.json';
$PEN = $DIR . '/avaliacoes-pendentes.json';

function ler($arq) {
    if (!is_file($arq)) return array('itens' => array());
    $fp = fopen($arq, 'r');
    if (!$fp) return array('itens' => array());
    flock($fp, LOCK_SH);
    $raw = stream_get_contents($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    $j = json_decode($raw, true);
    if (is_array($j) && isset($j[0])) return array('itens' => $j);
    if (!is_array($j) || !isset($j['itens'])) return array('itens' => array());
    return $j;
}

function gravar($arq, $dados) {
    if (!is_dir(dirname($arq))) @mkdir(dirname($arq), 0750, true);
    $tmp = $arq . '.tmp';
    $fp = fopen($tmp, 'c+');
    if (!$fp) return false;
    if (!flock($fp, LOCK_EX)) { fclose($fp); return false; }
    ftruncate($fp, 0);
    rewind($fp);
    $ok = fwrite($fp, json_encode($dados, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT)) !== false;
    fflush($fp);
    flock($fp, LOCK_UN);
    fclose($fp);
    return $ok ? rename($tmp, $arq) : false;
}

function h($s) {
    return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

if ($CHAVE_SECRETA === 'TROQUE-ESTA-PALAVRA-2026') {
    http_response_code(403);
    echo 'Troque a palavra secreta em moderar.php antes de usar esta tela.';
    exit;
}

$tentativas = isset($_SESSION['mod_tent']) ? (int)$_SESSION['mod_tent'] : 0;
if ($tentativas > 12) {
    http_response_code(429);
    echo 'Muitas tentativas. Feche o navegador e volte mais tarde.';
    exit;
}

$ok = !empty($_SESSION['mod_ok']) && $_SESSION['mod_ok'] === hash('sha256', $CHAVE_SECRETA);

if (!$ok) {
    $recebida = '';
    if (!empty($_POST['chave'])) $recebida = (string)$_POST['chave'];
    elseif (!empty($_GET['chave'])) $recebida = (string)$_GET['chave'];
    if ($recebida !== '' && hash_equals($CHAVE_SECRETA, $recebida)) {
        $_SESSION['mod_ok'] = hash('sha256', $CHAVE_SECRETA);
        $_SESSION['mod_tent'] = 0;
        header('Location: moderar.php');
        exit;
    }
    if ($recebida !== '') {
        $_SESSION['mod_tent'] = $tentativas + 1;
    }
    ?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Checagem de depoimentos</title>
<style>
  body{font-family:Georgia,serif;background:#0e1a2e;color:#f6f1e7;margin:0;padding:40px 18px}
  form{max-width:360px;margin:10vh auto;background:#16283f;padding:28px;border-radius:16px;border:1px solid rgba(201,162,75,.4)}
  label{display:block;margin-bottom:10px}
  input{width:100%;padding:10px;border-radius:8px;border:0;box-sizing:border-box}
  button{margin-top:14px;width:100%;padding:12px;border:0;border-radius:999px;background:#c9a24b;color:#0e1a2e;font-weight:800;cursor:pointer}
</style>
</head>
<body>
<form method="post" action="moderar.php">
  <label>Palavra secreta
    <input type="password" name="chave" required autocomplete="current-password">
  </label>
  <button type="submit">Entrar</button>
</form>
</body>
</html>
    <?php
    exit;
}

$aviso = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && !empty($_POST['acao']) && !empty($_POST['id'])) {
    $id = preg_replace('/[^a-f0-9]/', '', (string)$_POST['id']);
    $pend = ler($PEN);
    $novo = array();
    $achou = null;
    foreach ($pend['itens'] as $it) {
        if (isset($it['id']) && $it['id'] === $id) $achou = $it;
        else $novo[] = $it;
    }
    if ($achou) {
        if ($_POST['acao'] === 'aprovar') {
            $pub = ler($PUB);
            unset($achou['ip']);
            $pub['itens'][] = $achou;
            gravar($PUB, $pub);
            $aviso = 'Publicado.';
        } else {
            $aviso = 'Recusado. Não aparece na página.';
        }
        $pend['itens'] = $novo;
        gravar($PEN, $pend);
    }
}

$pend = ler($PEN);
$pub = ler($PUB);
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Checagem de depoimentos</title>
<style>
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#f6f1e7;color:#1c1a15;margin:0;padding:24px}
  h1{font-family:Georgia,serif;color:#0e1a2e}
  .card{background:#fff;border:1px solid rgba(201,162,75,.4);border-radius:14px;padding:16px 18px;margin:12px 0;max-width:720px}
  .estrelas{color:#c9a24b;letter-spacing:.08em}
  .meta{color:#5c5646;font-size:.86rem}
  form{display:inline}
  button{border:0;border-radius:999px;padding:8px 16px;font-weight:700;cursor:pointer;margin-right:8px}
  .ok{background:#c9a24b;color:#0e1a2e}
  .no{background:#eee;color:#5c5646}
  .aviso{color:#2e7d32;font-weight:700}
</style>
</head>
<body>
<h1>Checagem de depoimentos</h1>
<p class="meta">Só o que você aprovar aparece em /guardar. Leia com calma. Cada texto é de um irmão de verdade.</p>
<?php if ($aviso) echo '<p class="aviso">'.h($aviso).'</p>'; ?>
<p class="meta">Na fila: <?php echo count($pend['itens']); ?> · Publicados: <?php echo count($pub['itens']); ?></p>
<?php if (!$pend['itens']) { echo '<p>Nenhum depoimento esperando agora.</p>'; } ?>
<?php foreach (array_reverse($pend['itens']) as $it) { ?>
  <div class="card">
    <div><strong><?php echo h($it['nome']); ?></strong> · <span class="estrelas"><?php echo str_repeat('★', (int)$it['estrelas']); ?></span></div>
    <div class="meta"><?php echo h($it['data']); ?></div>
    <p><?php echo h($it['texto']); ?></p>
    <form method="post">
      <input type="hidden" name="id" value="<?php echo h($it['id']); ?>">
      <button class="ok" name="acao" value="aprovar" type="submit">Aprovar e publicar</button>
      <button class="no" name="acao" value="recusar" type="submit">Recusar</button>
    </form>
  </div>
<?php } ?>
</body>
</html>
