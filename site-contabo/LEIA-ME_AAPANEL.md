# Correção de cache dos áudios diários — execução pelo aaPanel

## Preferência: executar o script no servidor

O `corrigir_cache_audio_aapanel.py` faz uma alteração pontual **nos arquivos que já estão publicados**, em vez de substituir páginas completas. Ele cria uma cópia de segurança de `index.html`, `palavra.html` e `sw.js` antes de gravar e preserva o restante do conteúdo atual do servidor.

O script usa somente a biblioteca padrão do Python 3 e não acessa a internet. Por segurança, ele primeiro roda em modo de simulação. Se os trechos publicados não forem os esperados, ele aborta sem alterar os arquivos; não tente forçar a substituição.

### 1. Coloque o script fora da pasta pública

Baixe `corrigir_cache_audio_aapanel.py` desta pasta do Drive e envie pelo aaPanel para uma pasta fora da raiz pública do site — por exemplo, `/www/corrigir_cache_audio_aapanel.py`. **Não deixe o script dentro da pasta pública**, para que não possa ser baixado por visitantes.

Confirme no aaPanel a raiz real do site. O padrão no script é `/www/wwwroot/missaocomdeus.com.br`; se a raiz for outra, use o caminho correto no parâmetro `--root`.

### 2. Faça a simulação primeiro

No Terminal do aaPanel, rode (ajuste o caminho se necessário):

```bash
python3 /www/corrigir_cache_audio_aapanel.py --root /www/wwwroot/missaocomdeus.com.br
```

A simulação mostra os três arquivos e os trechos que pretende mudar. Ela **não grava nada** e ainda não cria backup. Se aparecer `ABORTADO`, pare: isso indica que o conteúdo publicado não corresponde aos trechos reconhecidos pelo script.

### 3. Aplique com backup

Se a simulação listar os três ajustes esperados, rode:

```bash
python3 /www/corrigir_cache_audio_aapanel.py --root /www/wwwroot/missaocomdeus.com.br --apply
```

O script vai mostrar a pasta de backup e pedir a confirmação digitada `APLICAR`. Sem essa confirmação, não grava. O backup é criado fora da pasta pública, na pasta pessoal do usuário do terminal (normalmente `/root/backup_audio_cache_DATA_HORA`), com os três originais e `MANIFEST.json`. O script verifica o backup, aplica as mudanças atomicamente e confere os arquivos gravados.

Se quiser escolher o destino do backup, acrescente um caminho que fique fora da raiz pública, por exemplo:

```bash
python3 /www/corrigir_cache_audio_aapanel.py --root /www/wwwroot/missaocomdeus.com.br --backup-dir /root/backup_audio_cache_manual --apply
```

### 4. Verifique o app

Com a correção aplicada, feche completamente o app instalado e abra-o novamente com internet. Teste reprodução na Home, download, compartilhamento e algumas faixas em `/palavra.html`. Não apague os dados do site/app como primeiro passo, pois isso pode apagar progresso salvo. O relatório do terminal informa o local do backup.

## O que o script muda

- Nas URLs diárias de reprodução, download e compartilhamento da Home, usa `?v=20261105`.
- Em `palavra.html`, usa o mesmo identificador de versão para o áudio diário.
- Em `sw.js`, muda a chave do cache de v10 para v11.
- Não altera os arquivos MP3, não limpa os dados do navegador, não toca em `/indicacoes.html` e não substitui o conteúdo completo das páginas.

Quando uma fala diária for substituída mantendo o mesmo nome `.mp3`, um token novo precisa ser usado nos dois HTMLs para evitar a reutilização de uma URL antiga em cache. O script desta entrega está fixado no token `20261105`.

## Arquivos HTML completos

O pacote também contém `index.html`, `palavra.html` e `sw.js` completos, derivados de `origin/main` (`c5f3a69469a2c630fbc9f1d46576d43a9681c4d2`). Eles são uma alternativa manual, mas **prefira o script**, pois ele preserva possíveis alterações feitas diretamente no servidor. Só substitua páginas completas depois de comparar a versão publicada e fazer backup.

Nenhuma alteração foi aplicada ao aaPanel por esta entrega.
