# Missão com Deus

## Escopo e arquitetura do projeto

**Atualizado em 05/11/2026**
Site público: <https://missaocomdeus.com.br>
Repositório: <https://github.com/sidneyrma/instalador>

### 1. Finalidade

O site é um portal cristão de conteúdo e estudo. Reúne páginas institucionais, leituras digitais, áudio, materiais de estudo, experiências interativas para famílias e um caminho externo para conhecer o acesso completo. A fé cristã é central. Recomendações de livros, serviços e conteúdo externo exigem discernimento editorial, não apenas avaliação técnica.

### 2. Ambiente de produção

- O site é hospedado em servidor Linux administrado pelo aaPanel.
- A estrutura usa páginas HTML/CSS/JavaScript, arquivos estáticos, endpoints PHP e tarefas administrativas em Python.
- O caminho de publicação documentado no projeto é `/www/wwwroot/missaocomdeus.com.br/`. Confirmar a raiz e as regras atuais no aaPanel antes de qualquer operação.
- Nginx atende as páginas e rotas do domínio. O fluxo de pagamento sai do site para um checkout externo; o site não deve receber dados de cartão.
- O servidor é a fonte de verdade do que está publicado. O GitHub registra o projeto, mas não comprova sozinho o estado do aaPanel. Para a versão mais atual do repositório, consultar `main`; o checkout local pode estar desatualizado.

### 3. Mapa funcional do site

- **Entrada e navegação:** `/` (Home), `/indicacoes.html` (indicações de leitura) e páginas institucionais como `/nossa-missao.html` e `/privacidade.html`.
- **Acesso e pós-compra:** `/guardar` apresenta o acesso completo e encaminha ao checkout externo; `/obrigado.html` é uma página de retorno após a compra.
- **Biblioteca e leitores:** páginas `livroNN.html` para as obras publicadas, com `leitor.html` como componente de leitura compartilhado quando aplicável. Os arquivos e rotas atuais devem ser conferidos em `site-contabo/` e no servidor.
- **Conteúdo e estudo:** `/palavra.html`, `/biblica.html`, `/salmos.html`, `/trilogia-da-alma.html` e `/anestesia-mental.html`.
- **Pais e Filhos:** `/conhecer-guia-pais-filhos.html`, `/guia-pais-filhos.html`, `/guia-pais-filhos-espelho.html` e o leitor da obra correspondente.
- **Administração e acompanhamento:** `/stats.html` e rotas `q-*` são componentes operacionais/de medição, não páginas de navegação pública.

As URLs podem ser reescritas pelo Nginx e nem sempre exibem a extensão `.html`. Antes de alterar uma rota, conferir o arquivo, a configuração do servidor e os links que a utilizam.

### 4. Estrutura do repositório

- `site-contabo/`: cópia versionada das páginas do site, recursos estáticos, alguns endpoints e utilitários de operação. Não enviar a pasta inteira ao servidor como substituição automática.
- `site-contabo/audio/`, `fotos/`, `icones/` e `livros/`: recursos associados às páginas. Alterar apenas o recurso solicitado e verificar suas referências.
- `site-contabo/*.php` e arquivos de rota `q-*`: endpoints e marcadores usados por formulários, interações e acompanhamento. Conferir dependências e regras de acesso antes de mexer.
- `site-contabo/gerar_estatisticas.py`: ferramenta de geração do painel a partir de registros do servidor. Não é executada a cada visita ao site.
- `analise/`: scripts auxiliares, testes, simulações, prévias e documentação técnica. Não é diretório público para upload.
- `livro/` e `edicoes/`: recursos editoriais e materiais de preparação das obras.

### 5. Como uma atualização chega à produção

**Substituição por arquivo**

1. Confirmar a versão-alvo no GitHub `main` e conferir o arquivo servido no aaPanel.
2. Preparar apenas o arquivo solicitado, mantendo nome, rota, recursos relacionados e funcionamento existente.
3. A pessoa responsável faz backup do arquivo remoto e envia manualmente o HTML/PHP/recurso aprovado pelo aaPanel.
4. Verificar a página publicada, os links, os formulários e a versão servida. Não declarar publicação concluída sem confirmação no servidor.

**Atualização por script Python**

1. Ler o script e confirmar exatamente quais arquivos e dados ele altera.
2. Usar a versão correspondente às fontes atuais do servidor; preparar simulação, backup e caminho de reversão.
3. Executar somente com autorização explícita, pelo comando e caminho confirmados no aaPanel. Não rodar scripts de atualização por suposição.
4. Conferir o resultado no servidor. Se o script mexer em Nginx, validar com `nginx -t` antes de recarregar o serviço.

Scripts de manutenção e arquivos de configuração não substituem a inspeção do servidor. Uma prévia ou arquivo preparado não significa que houve publicação.

### 6. Dados, integrações e limites

- Logs, arquivos de visitantes, IPs, respostas de formulários, tokens, senhas e configurações privadas não devem ser publicados nem incluídos em commits.
- O código-fonte do chatbox AtendeChat/Conectaí permanece no Google Drive e é um projeto separado do site; não presumir que esteja integrado à Laura do portal nem alterar sua instalação sem autorização própria.
- As redes oficiais confirmadas são Instagram `@portal.missaocomdeus`, TikTok `@portalmissaocomdeus` e Facebook `portalmissaocomdeus`. Não substituir esses destinos por endereços históricos ou não confirmados.

### 7. Regras de continuidade

- Não fazer alterações de produção sem pedido específico. A autorização atual é preparar arquivos para upload manual; não solicitar credenciais nem publicar diretamente.
- Manter a Home e `/indicacoes.html` sem alterações até novo pedido explícito.
- Atualizadores e alterações de estatísticas permanecem pausados. Não executar `gerar_estatisticas.py` nem outros atualizadores de estatísticas sem retomada explícita do responsável.
- Em commits, incluir somente os arquivos diretamente solicitados e revisar o diff antes de enviar.
