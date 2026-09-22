<?php
/**
 * enviar_guia_espelho.php - Envia o quiz "Filhos e Pais: O Espelho"
 *
 * Recebe o e-mail de quem concluiu o quiz e envia:
 *   1) A pagina completa do Espelho (abertura, 7 perguntas, encerramento,
 *      versiculos e frase para guardar) para a pessoa que pediu.
 *   2) Notificacao para o autor (portalmissaocomdeus@gmail.com).
 *
 * Uso: https://missaocomdeus.com.br/enviar_guia_espelho.php (POST JSON)
 */

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

$DESTINO = 'portalmissaocomdeus@gmail.com';
$LINK_GUIA = 'https://missaocomdeus.com.br/guia-pais-filhos-espelho';

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

    // Protecao: 5s entre envios do mesmo IP
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

    // ===== 1. Enviar a pagina completa do Espelho =====
    $assunto_pai = 'Filhos e Pais: O Espelho, da Missão com Deus';

    $corpo_pai = <<<TXT
Paz e graça, querido(a) irmão(ã)!

Obrigado por fazer o quiz "Filhos e Pais: O Espelho". Segue a página completa, com as 7 perguntas para você fazer aos seus pais e conhecer a história, os silêncios e os conselhos de quem te criou.

Para ver a versão ilustrada na página, acesse o link:
$LINK_GUIA

============================================
ABERTURA CARINHOSA
============================================
"Pai, mãe, eu não quero que isto seja uma entrevista. Quero só conhecer você um pouco melhor. E quero que você saiba: aqui também é espaço seu para falar, para sentir e para desabafar no seu tempo. Se alguma pergunta doer, a gente pode pular, respirar e voltar quando for bom para nós. Vou começar com algo simples."

============================================
AS 7 PERGUNTAS
============================================

Pergunta 1: Se você pudesse me pedir uma coisa que me aproximasse mais de você, o que seria?
Opções de exemplo: Mais tempo de qualidade, Mais paciência para conversar, Mais presença e cuidado, Mais respeito com seus limites, ou dizer com as próprias palavras.
Por quê: abre a conversa com um pedido que pode ser atendido. Mostra que aproximação não é só frase bonita.

Pergunta 2: Quando você tinha a minha idade, como era um dia comum na sua casa? E onde guardava seus medos e alegrias?
Opções de exemplo: Eu era bem livre e brincava muito, Eu era mais estudioso(a), Eu já ajudava em casa ou no trabalho, Eu cresci perto da igreja, ou contar à própria maneira.
Por quê: resgata a pessoa que o pai e a mãe foram antes de virar pai ou mãe.

Pergunta 3: Na sua época, como era o assunto bebida, cigarro e droga? O que você aprendeu, e o que me aconselharia hoje?
Opções de exemplo: Era tabu, quase não se falava, Vi de perto alguém sofrer com o vício, Hoje eu entendo como isso prejudica, Agradeça e não aceite. A recusa também é força, ou contar como foi na época.
Por quê: o pai ou a mãe aconselha de verdade, com honestidade e sem hipocrisia.

Pergunta 4: O que foi mais difícil e o que foi mais bonito em me criar até aqui?
Resposta livre.
Por quê: são duas condições opostas (o difícil e o bonito) e cada uma merece espaço próprio.

Pergunta 5: Tem algo que você guarda e que gostaria de desabafar comigo ou já tentou e não conseguiu se abrir?
Opções de exemplo: Fico em silêncio para não preocupar, Carrego coisas que nunca falei, Aprendi que fraqueza não era permitida, Oro, mas gostaria que alguém ouvisse, ou abrir o coração.
Por quê: o pai e a mãe também são autorizados a sentir, a carregar e a pedir abrigo.

Pergunta 6: O que você acha que a minha geração não entende sobre o que você já enfrentou? O que gostaria que eu soubesse?
Opções de exemplo: O silêncio era falta de espaço, O peso do trabalho e das responsabilidades, As dores que carreguei sem poder mostrar, Como a fé me sustentou, ou contar algo mais.
Por quê: o filho abre espaço para a história do pai e da mãe, e descobre que o que parece distância às vezes foi proteção.

Pergunta 7: Se você pudesse me contar uma coisa da sua vida que ainda não contou, ou me dizer o que gostaria de ter ouvido quando era jovem, o que seria?
Opções de exemplo: Algo da sua infância, Um sonho que ficou guardado, Uma dor que nunca disse em voz alta, Algo que gostaria que eu soubesse, ou preferir guardar ainda hoje.
Por quê: é o fechamento com espaço de cura. Confiança não se força, se constrói.

============================================
ENCERRAMENTO
============================================
"Obrigado por abrir a porta um pouco mais. Nenhum pai e nenhuma mãe termina de aprender. E nenhum filho termina de entender. Mas quem escolhe se aproximar, mesmo com medo, já está construindo uma casa mais firme. Que Deus ajude cada um de nós a ouvir com o coração, e a deixar de carregar tudo sozinho."

============================================
FUNDAMENTO BÍBLICO
============================================
"Honra teu pai e tua mãe, para que os teus dias se prolonguem na terra que o Senhor teu Deus te dá." (Êxodo 20:12)
"Assim como um pai se compadece de seus filhos, assim o Senhor se compadece daqueles que o temem." (Salmo 103:13)
"E estas palavras que hoje te ordeno estarão no teu coração; e as ensinarás a teus filhos." (Deuteronômio 6:6-7)

============================================
FRASE PARA GUARDAR
============================================
"Ser pai e mãe vai além de ser melhor amigo. Ser pai e mãe é plantar, segurar, soltar e confiar. E nenhum pai ainda terminou de aprender."

Com amor, em Cristo Jesus,
Equipe Missão com Deus
missaocomdeus.com.br
TXT;

    $cab_pai = "From: Missão com Deus <no-reply@missaocomdeus.com.br>\r\n";
    $cab_pai .= "Reply-To: " . $DESTINO . "\r\n";
    $cab_pai .= "Content-Type: text/plain; charset=utf-8\r\n";

    $ok_pai = @mail($email_pai, $assunto_pai, $corpo_pai, $cab_pai);

    // ===== 2. Notificar o autor =====
    $assunto_autor = 'Filhos e Pais: O Espelho solicitado';
    $corpo_autor = "Alguém concluiu o quiz e solicitou o Espelho!\n\n";
    $corpo_autor .= "E-mail: " . $email_pai . "\n";
    $corpo_autor .= "Data: " . date('d/m/Y H:i') . "\n\n";
    $corpo_autor .= "Missão com Deus · missaocomdeus.com.br\n";

    $cab_autor = "From: Missão com Deus <no-reply@missaocomdeus.com.br>\r\n";
    $cab_autor .= "Content-Type: text/plain; charset=utf-8\r\n";

    @mail($DESTINO, $assunto_autor, $corpo_autor, $cab_autor);

    if ($ok_pai) {
        echo json_encode(array('ok' => true, 'msg' => 'Página do Espelho enviada para o seu e-mail!'), JSON_UNESCAPED_UNICODE);
    } else {
        http_response_code(500);
        echo json_encode(array('erro' => 'Nao foi possivel enviar o Espelho agora. Tente novamente em instantes.'), JSON_UNESCAPED_UNICODE);
    }
    exit;
}

http_response_code(405);
echo json_encode(array('erro' => 'Metodo nao permitido'), JSON_UNESCAPED_UNICODE);
