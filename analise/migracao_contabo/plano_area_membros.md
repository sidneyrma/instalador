# 🔐 PLANO: SISTEMA DE ACESSO AO PORTAL (login, cadastro, videoaulas e sorteio)

**Criado em:** 18/08/2026
**Contexto:** o autor quer que cada comprador tenha seu próprio acesso (sem
compartilhar o dele), com tela de login/cadastro no estilo Kiwify, acesso às
14 videoaulas (hospedadas no YouTube, acessadas por link conforme cronograma)
e possibilidade de sorteios. O domínio missaocomdeus.com.br ainda aguarda
liberação da HostGator ("Falha no registro").

---

## 1. 🚧 SITUAÇÃO DO DOMÍNIO missaocomdeus.com.br

**Sintoma:** no aaPanel, o site mostra "Falha no registro" e o botão
"Gerenciar" fica DESABILITADO.

**O que isso significa (honestidade total):**
- Domínios **.com.br** são controlados pelo **Registro.br** (não é como .com).
- O registro **não é automático**: exige que o titular tenha **CPF ou CNPJ
  válido** e a confirmação dos dados/documentos.
- "Falha no registro" = o registro no Registro.br **não foi concluído**.
  Pode ser: pendência de dados do titular (CPF/CNPJ), pendência de
  confirmação/documento, ou pagamento.

**O que o autor deve fazer:**
1. Entrar no painel da **HostGator** (onde comprou) e verificar o status do
   pedido/registro do domínio.
2. Conferir se informou **CPF/CNPJ válido do titular** (obrigatório para
   .com.br) e se confirmou o e-mail/documento pedido.
3. Se pedirem documento (ex.: comprovante), enviar.
4. Se necessário, abrir chamado/suporte da HostGator: "status do registro do
   domínio missaocomdeus.com.br".
5. O Registro.br pode levar de horas a alguns dias após a confirmação.

**Enquanto isso:** o site compraoseu.com continua no ar normalmente — nada é
perdido. O missaocomdeus é um passo futuro.

---

## 2. 🎓 O QUE A KIWIFY JÁ RESOLVE (importante!)

O autor quer "não precisar que usem o meu acesso". **A Kiwify JÁ resolve
isso desde o início:**

- **Cada comprador recebe seu próprio login** na área de membros da Kiwify
  (`dashboard.kiwify.com.br/courses`).
- As **videoaulas podem ser cadastradas na própria Kiwify** (ela suporta
  incorporar vídeos do YouTube por módulo/aula) — o aluno vê as 14 aulas lá,
  com o cronograma.
- O botão "🔓 Entrar no Portal" do nosso site já aponta para lá.

**Ou seja:** a estrutura de "login por comprador + videoaulas + cronograma"
**já existe pronta, paga e segura** na Kiwify. O que falta é cadastrar as 14
aulas lá (o autor tem os links do YouTube).

---

## 3. 🛠️ OPÇÕES DE SISTEMA DE ACESSO NO NOSSO SITE

Se o autor quiser uma área de membros COM A CARA do Portal (dentro do
missaocomdeus.com.br), existem 3 caminhos:

### Opção A — Usar a Kiwify (RECOMENDADA, custo zero de manutenção)
- Login dos alunos fica no dashboard da Kiwify (já pronto).
- Cadastrar as 14 videoaulas na Kiwify (módulos conforme cronograma).
- Nosso site continua como vitrine + botão "Entrar no Portal".
- **Prós:** seguro, sem manutenção, sem risco de expor dados, sem custo.
- **Contras:** a "cara" é da Kiwify, não do nosso site (dá para personalizar
  minimamente).

### Opção B — Login simples por CÓDIGO no nosso site (PHP + arquivo JSON)
- Criar uma página `portal.html` com tela de **login por código de acesso**.
- Cada comprador recebe um **código único** (o autor gera e envia).
- As 14 videoaulas (links do YouTube) ficam protegidas atrás do login.
- **Sem banco de dados:** usuários/códigos num arquivo JSON (simples).
- **Prós:** funciona, com a cara do Portal, sem MySQL.
- **Contras:** segurança limitada (arquivo JSON não escala; se muitos
  usuários, fica lento); senha/código simples pode ser compartilhado; exige
  que o autor gerencie os códigos manualmente (mas dá para automatizar).

### Opção C — Sistema completo (PHP + MySQL + webhook Kiwify) [PROJETO MAIOR]
- Instalar **MySQL** no servidor (ainda não tem).
- Tela de cadastro/login com e-mail + senha (hash seguro).
- **Webhook da Kiwify:** quando alguém compra, a Kiwify avisa o nosso site e o
  sistema libera o acesso automaticamente (cria a conta).
- Área de membros com as 14 aulas.
- **Prós:** escalável, automático, com a cara do Portal.
- **Contras:** leva dias para construir; exige manutenção e cuidados de
  segurança (criptografia de senha, proteção contra ataques); risco se não for
  bem feito.

---

## 4. 🎁 SORTEIOS (simples e honesto)

O sorteio pode ser feito sem sistema complexo:

- **Formulário de participação** (nome + e-mail + WhatsApp) — pode usar o
  FormSubmit (já configurado) para enviar as inscrições ao e-mail do autor.
- **Sorteio:** o autor pode usar uma ferramenta gratuita (ex.: sorteador
  online) ou um pequeno script que sorteia entre os e-mails recebidos.
- Regras claras e transparentes (data, prêmio, como participa).

---

## 5. 🎯 RECOMENDAÇÃO DO CONSULTOR (honestidade total)

**Para hoje (rápido e seguro):**
1. **Cadastrar as 14 videoaulas na Kiwify** (ela já é o sistema de login dos
   compradores). Isso resolve 90% do que o autor quer, sem programar nada.
2. **Criar o formulário de sorteio** no site (FormSubmit → e-mail do autor).

**Para amanhã (se quiser a cara do Portal):**
3. **Opção B (login por código + PHP + JSON)** como primeiro passo — é viável
   em um dia, dá a experiência de "portal próprio" e não exige MySQL.
4. Evoluir para a **Opção C (MySQL + webhook)** só quando houver muitos
   alunos e o autor quiser automatizar tudo.

**Importante:** criar login próprio **não é complicado de começar**, mas exige
**cuidado com segurança** (senhas com hash, proteção contra acesso direto aos
links). A Kiwify já cuida disso por nós. Por isso a recomendação é: usar a
Kiwify para o acesso pago AGORA, e construir o portal próprio em etapas.

---

## 6. 📌 PRÓXIMOS PASSOS (a decidir com o autor)

- [ ] Autor verifica o registro do domínio na HostGator (CPF/CNPJ + docs)
- [ ] Autor decide: Opção A (Kiwify) / B (código + JSON) / C (MySQL)
- [ ] Se Opção B: eu construo a tela de login por código + página das 14
      aulas protegida (PHP + JSON), pronta para subir
- [ ] Criar formulário de sorteio (FormSubmit)
- [ ] Cadastrar as 14 aulas na Kiwify (autor tem os links do YouTube)

*"Tudo tem o seu tempo determinado" (Eclesiastes 3:1). O acesso justo e
seguro é parte do crescimento da obra — e será construído com sabedoria,
etapa por etapa.*
