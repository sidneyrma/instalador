<?php
header('Cache-Control: no-store');
$f = __DIR__ . '/geo_visitas.json';
if (isset($_GET['ping'])) { echo 'ok'; exit; }
if (isset($_GET['json'])) { header('Content-Type: application/json; charset=utf-8'); echo file_exists($f) ? file_get_contents($f) : '{}'; exit; }
$ua = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
if (preg_match('/bot|crawl|spider|python|curl|wget|headless|facebookexternalhit|whatsapp|telegram|scan|probe/i', $ua)) { echo 'nao'; exit; }
$d = json_decode(file_get_contents('php://input'), true);
if (!is_array($d)) { $d = array('pais'=>'','uf'=>'','cidade'=>''); }
if ((empty($d['uf']) && empty($d['cidade'])) && isset($_GET['auto'])) {
  $ip = isset($_SERVER['HTTP_CF_CONNECTING_IP']) ? $_SERVER['HTTP_CF_CONNECTING_IP'] : (isset($_SERVER['HTTP_X_FORWARDED_FOR']) ? $_SERVER['HTTP_X_FORWARDED_FOR'] : (isset($_SERVER['HTTP_X_REAL_IP']) ? $_SERVER['HTTP_X_REAL_IP'] : $_SERVER['REMOTE_ADDR']));
  $ip = trim(explode(',', $ip)[0]);
  if (filter_var($ip, FILTER_VALIDATE_IP)) {
    $ctx = stream_context_create(array('http'=>array('timeout'=>12),'ssl'=>array('verify_peer'=>false,'verify_peer_name'=>false)));
    $r = @file_get_contents('https://ipwho.is/' . $ip, false, $ctx);
    if (!$r && function_exists('curl_init')) {
      $ch = curl_init('https://ipwho.is/' . $ip);
      curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($ch, CURLOPT_TIMEOUT, 12);
      curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
      curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
      $r = curl_exec($ch);
      curl_close($ch);
    }
    $j = $r ? json_decode($r, true) : null;
    if (is_array($j) && !empty($j['success'])) {
      $d = array('pais'=>(isset($j['country_code'])?$j['country_code']:''), 'uf'=>(isset($j['region'])?$j['region']:''), 'cidade'=>(isset($j['city'])?$j['city']:''));
    } else {
      $r2 = @file_get_contents('http://ip-api.com/json/' . $ip . '?fields=status,countryCode,regionName,city&lang=pt-BR', false, stream_context_create(array('http'=>array('timeout'=>12))));
      $j2 = $r2 ? json_decode($r2, true) : null;
      if (is_array($j2) && isset($j2['status']) && $j2['status'] === 'success') {
        $d = array('pais'=>(isset($j2['countryCode'])?$j2['countryCode']:''), 'uf'=>(isset($j2['regionName'])?$j2['regionName']:''), 'cidade'=>(isset($j2['city'])?$j2['city']:''));
      }
    }
  }
}
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
