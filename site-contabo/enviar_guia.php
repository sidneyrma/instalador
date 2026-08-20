<?php
/**
 * enviar_guia.php — Envia o Guia "Pais e Filhos: Conversas que Protegem"
 *
 * Recebe o e-mail do pai/mãe, envia:
 *   1) O guia COMPLETO (abertura, 7 perguntas, encerramento, versículos)
 *      + o link da página, para o pai/mãe (agradecimento)
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

    // ===== 1. Enviar o guia completo para o pai/mãe =====
    $assunto_pai = 'Guia Pais e Filhos: Conversas que Protegem';

    $corpo_pai = <<<TXT
Paz e graça, querido(a) irmão(ã)!

Obrigado por se importar com o diálogo em família. Segue o guia completo "Pais e Filhos: Conversas que Protegem", com as 7 perguntas para conversar com seu filho(a) com amor, respeito e a presença de Deus.

Para ver a versão ilustrada na página, acesse o link:
$LINK_GUIA

============================================
ABERTURA AMOROSA (leia para o seu filho(a))
============================================
"Filho(a), estas perguntas não são um teste e não têm resposta errada. São um convite para nos conhecermos melhor, com amor e respeito. Responda com o coração: o que você sentir, eu quero ouvir. E se não quiser responder alguma agora, tudo bem, isso também é uma resposta válida."

============================================
AS 7 PERGUNTAS
============================================

Pergunta 1: O que mais te impede de abrir o coração com a gente?
Opções de exemplo: Medo de bronca, Vergonha, Acho que não vão entender, Sinto que estão sempre ocupados.
Dica para os pais: abre a porta do diálogo sem julgar. O filho diz o que o trava, e vocês aprendem como chegar.

Pergunta 2: Entre seus amigos, isso é uma coisa comum? Alguém já te ofereceu vape, bebida ou outra coisa assim?
Opções de exemplo: Nunca vi isso rolar, É comum mas nunca me ofereceram, Já me ofereceram e fiquei na dúvida, Já aconteceu e não me senti bem.
Dica para os pais: aborda os temas sensíveis com curiosidade sobre o ambiente, não acusação direta. Isso reduz a defensividade e aumenta a honestidade.

Pergunta 3: O que você acha que os adultos não entendem sobre o que os jovens enfrentam hoje?
Resposta livre.
Dica para os pais: dá voz ao filho. Ele se sente ouvido, e vocês descobrem o mundo do jeito que ele vê.

Pergunta 4: Se você pudesse pedir uma coisa para se sentir mais amado e ouvido, o que seria?
Opções de exemplo: Mais tempo juntos, Mais conversa sem julgamento, Mais confiança, Mais liberdade com limites claros.
Dica para os pais: o filho diz o que precisa, e vocês recebem um presente de orientação.

Pergunta 5: Você percebe os esforços e sacrifícios que fazemos por você? O que mais você nota?
Resposta livre.
Dica para os pais: lembra o amor e a dedicação dos pais, sem só cobrar do filho. Ele reconhece o que recebe.

Pergunta 6: Quando algo dá errado, você se sente seguro(a) para contar para a gente?
Opções de exemplo: Sempre, Às vezes, Quase nunca, Tenho medo da reação.
Dica para os pais: mostra o nível de confiança real, e vocês entendem onde precisam melhorar, sem bronca. Se for difícil dizer em voz alta, vale escrever num papel.

Pergunta 7: Se você pudesse nos contar uma coisa sobre você que ainda não contou, o que seria?
Resposta livre (totalmente opcional).
Dica para os pais: o fechamento perfeito, um convite à intimidade. O filho escolhe o que quer compartilhar, no tempo dele.

============================================
ENCERRAMENTO AMOROSO
============================================
"Obrigado por confiar em nós. Não importa o que você respondeu: você é amado(a), você é importante, e nós estamos aqui para caminhar com você, sempre. Que Deus nos ajude a nos amarmos cada dia mais."

============================================
FUNDAMENTO BÍBLICO
============================================
"E vós, pais, não provoqueis vossos filhos à ira, mas criai-os na disciplina e admoestação do Senhor." (Efésios 6:4)
"Ensina a criança no caminho em que deve andar, e, ainda quando for velho, não se desviará dele." (Provérbios 22:6)
"E estas palavras que hoje te ordeno estarão no teu coração; e as ensinarás a teus filhos, falando delas assentado em tua casa." (Deuteronômio 6:6-7)

Com amor, em Cristo Jesus,
Equipe Missão com Deus
missaocomdeus.com.br
TXT;

    $cab_pai = "From: Missão com Deus <no-reply@missaocomdeus.com.br>\r\n";
    $cab_pai .= "Reply-To: " . $DESTINO . "\r\n";
    $cab_pai .= "Content-Type: text/plain; charset=utf-8\r\n";

    $ok_pai = @mail($email_pai, $assunto_pai, $corpo_pai, $cab_pai);

    // ===== 2. Notificar o autor =====
    $assunto_autor = 'Guia Pais e Filhos solicitado';
    $corpo_autor = "Um pai/mãe solicitou o Guia Pais e Filhos!\n\n";
    $corpo_autor .= "E-mail do pai/mãe: " . $email_pai . "\n";
    $corpo_autor .= "Data: " . date('d/m/Y H:i') . "\n\n";
    $corpo_autor .= "Missão com Deus · missaocomdeus.com.br\n";

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
