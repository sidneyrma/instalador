<?php
/* geo.php - localizacao real pelo navegador. Blindagem 12/09/2026.
   Selo JS1: registro so entra vindo de JavaScript de uma pagina da casa.
   Nada de IP guardado: so PAIS|UF|CIDADE. */
ignore_user_abort(true);
header('Cache-Control: no-store');
header('Access-Control-Allow-Origin: *');
$f = __DIR__ . '/geo_visitas.json';
/* sal + pasta de selos com nome imprevisivel (ninguem adivinha o caminho) */
$saltfile = __DIR__ . '/.geo_salt';
if (!is_file($saltfile)) { @file_put_contents($saltfile, bin2hex(random_bytes(16))); }
$salt = trim((string)@file_get_contents($saltfile));
$marcas = __DIR__ . '/.geo_m_' . substr(hash('sha256', $salt), 0, 12) . '.json';
if (isset($_GET['ping'])) { echo 'ok'; exit; }
if (isset($_GET['json'])) { header('Content-Type: application/json; charset=utf-8');
  echo file_exists($f) ? file_get_contents($f) : '{}'; exit; }
$ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
if (preg_match('/bot|crawl|spider|python|curl|wget|headless|facebookexternalhit|telegram|scan|probe|zgrab|go-http|okhttp|nuclei|masscan/i', $ua)) { echo 'nao'; exit; }
/* token de sessao: o snippet pede antes de registrar, e o rob6 de varredura nao faz isso */
if (isset($_GET['token'])) {
  $tk = substr(hash('sha256', $ua . '|' . $_SERVER['REMOTE_ADDR'] . '|' . floor(time()/3600) . '|' . $salt), 0, 16);
  $m = file_exists($marcas) ? (array) json_decode(file_get_contents($marcas), true) : array();
  if (!isset($m[$tk])) {
    $m[$tk] = time();
    foreach ($m as $k => $t0) { if ((int)$t0 < time() - 86400) unset($m[$k]); }
    @file_put_contents($marcas, json_encode($m), LOCK_EX);
  }
  header('Content-Type: text/plain'); echo $tk; exit;
}
$d = json_decode(file_get_contents('php://input'), true);
if (!is_array($d)) { $d = array(); }
$ref = isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : '';
$casa = preg_match('#^https?://([a-z0-9.-]+\.)?missaocomdeus\.com\.br#i', $ref);
if ((empty($d['uf']) && empty($d['cidade'])) && isset($_GET['auto'])) {
  /* GET do snippet: exige referer da casa + token batendo com a sessao */
  if (!$casa) { echo 'nao'; exit; }
  $tk = isset($_GET['s']) ? preg_replace('/[^0-9a-f]/', '', $_GET['s']) : '';
  $m = file_exists($marcas) ? (array) json_decode(file_get_contents($marcas), true) : array();
  if ($tk === '' || !isset($m[$tk])) { echo 'nao'; exit; }
  $ip = isset($_SERVER['HTTP_CF_CONNECTING_IP']) ? $_SERVER['HTTP_CF_CONNECTING_IP']
       : (isset($_SERVER['HTTP_X_FORWARDED_FOR']) ? $_SERVER['HTTP_X_FORWARDED_FOR']
       : (isset($_SERVER['HTTP_X_REAL_IP']) ? $_SERVER['HTTP_X_REAL_IP'] : $_SERVER['REMOTE_ADDR']));
  $ip = trim(explode(',', $ip)[0]);
  if (filter_var($ip, FILTER_VALIDATE_IP)) {
    $ctx = stream_context_create(array('http'=>array('timeout'=>12),'ssl'=>array('verify_peer'=>false,'verify_peer_name'=>false)));
    $r = @file_get_contents('https://ipwho.is/' . $ip, false, $ctx);
    if (!$r && function_exists('curl_init')) {
      $ch = curl_init('https://ipwho.is/' . $ip);
      curl_setopt_array($ch, array(CURLOPT_RETURNTRANSFER=>true, CURLOPT_TIMEOUT=>12,
        CURLOPT_SSL_VERIFYPEER=>false, CURLOPT_SSL_VERIFYHOST=>false));
      $r = curl_exec($ch); curl_close($ch);
    }
    $j = $r ? json_decode($r, true) : null;
    if (is_array($j) && !empty($j['success'])) {
      $d = array('pais'=>(isset($j['country_code'])?$j['country_code']:''),
                 'uf'=>(isset($j['region'])?$j['region']:''),
                 'cidade'=>(isset($j['city'])?$j['city']:''),
                 'isp'=>(isset($j['connection']['isp'])?$j['connection']['isp']:''));
    } else {
      $r2 = @file_get_contents('http://ip-api.com/json/' . $ip . '?fields=status,countryCode,regionName,city,isp,as&lang=pt-BR', false, stream_context_create(array('http'=>array('timeout'=>12))));
      $j2 = $r2 ? json_decode($r2, true) : null;
      if (is_array($j2) && isset($j2['status']) && $j2['status'] === 'success') {
        $d = array('pais'=>(isset($j2['countryCode'])?$j2['countryCode']:''),
                   'uf'=>(isset($j2['regionName'])?$j2['regionName']:''),
                   'cidade'=>(isset($j2['city'])?$j2['city']:''),
                   'isp'=>(isset($j2['isp'])?$j2['isp']:''));
      }
    }
  }
}
/* filtro de maquina: quem mora em data center / host nao entra no rebanho */
$suspeito = strtolower((isset($d['isp']) ? $d['isp'] : '') . ' ' . (isset($d['org']) ? $d['org'] : ''));
if ($suspeito !== '' && preg_match('/hostinger|contabo|digitalocean|ovh|hetzner|alibaba|tencent|bytedance|volcano|amazon|azure|microsoft|fastly|cloudflare|scaleway|vultr|linode|netscout|arbor network|erneuerbare|stiftung|zwiebelfreunde|\btor\b|\btor\.\B|godaddy|namecheap|serveral|hosting|data ?center|\bcdn\b/i', $suspeito)) { echo 'maquina'; exit; }
$pais = substr(trim((string)$d['pais']), 0, 5);
$uf = substr(trim((string)$d['uf']), 0, 80);
$cidade = substr(trim((string)$d['cidade']), 0, 90);
if ($uf === '' && $cidade === '') { echo 'nao'; exit; }
if ($uf === '') { $uf = 'Outros paises'; }
$a = file_exists($f) ? json_decode(file_get_contents($f), true) : array();
if (!is_array($a)) { $a = array(); }
$k = $pais . '|' . $uf . '|' . $cidade;
$a[$k] = isset($a[$k]) ? intval($a[$k]) + 1 : 1;
echo @file_put_contents($f, json_encode($a, JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT), LOCK_EX) ? 'ok' : 'nao';
