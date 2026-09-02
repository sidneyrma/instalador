# Rastreio de origem no painel /stats (v5 — medição honesta)

**Para:** Missão com Deus · missaocomdeus.com.br

---

## 0. O que mudou da v4 para a v5 (leia antes)

A v4 tinha um erro grave, e o senhor apontou com razão: aparecia **266%**.
A causa: ela misturava dois números de bases diferentes e contava **requisições**
como se fossem **visitas**.

O que foi corrigido:

| Problema da v4 | Correção na v5 |
|---|---|
| «266% entraram pelo site antigo» (número maior que o total) | Cada bloco tem **base e período próprios**. Nenhum percentual mistura blocos. |
| Contava cada requisição como uma visita | Conta **visita (sessão)**: 30 min sem atividade = nova visita. Critério do Google Analytics. |
| Robô de varredura virava «visita» no site antigo (o 301 responde para tudo) | **Funil explícito**: robôs, ataques e IPs em modo varredura são descartados e o descarte é mostrado no painel. |
| `/stats` (o senhor abrindo o painel) contava como visita de irmão | Páginas internas da casa (`/stats`, `/palavra`, `/mural`) e endpoints `.php` **não entram** mais em visita/origem. Continuam no ranking de páginas vistas, porque isso é honesto. |
| Origem contada a cada requisição | A origem é a do **primeiro acesso da visita**. Uma visita, uma origem. Assim as linhas somam o total. |
| Dias ordenados como texto (errava na virada do mês) | Ordenação por data de verdade. |

**Por isso os números vão cair.** Caiu porque agora é visita de gente, e não pedido de arquivo.
O número antigo estava inflado, não o novo.

---

## 1. O que o painel responde

**Bloco «De onde vêm os nossos irmãos»** (site novo, base única):

| Pergunta | Onde |
|---|---|
| Quantos chegam pela busca do Google (SEO) | Card **SEO (busca)** + tabela **Origem da visita** |
| Quantos chegam com o endereço antigo declarado | Linha **Site antigo compraoseu.com** |
| Quantos vêm direto (digitou, app, favoritos) | Card **Direto** |
| Quantos vêm de Instagram, TikTok, YouTube, WhatsApp | Card **Redes** |
| Por qual página entram / qual o Google mais entrega | Tabelas **Por qual página eles entram** e **Páginas que o Google mais entrega** |
| Quem nos indica | Tabela **Quem nos indica (domínios)** |
| Dia a dia | Tabela **Últimos 7 dias (site novo, base única)** |

**Bloco separado «Medição do endereço antigo»** (compraoseu.com), com funil próprio:
requisições → robôs descartados → ataques descartados → varredura descartada →
requisições de gente → **visitas** → pessoas. E, dessas visitas, onde a pessoa estava antes.

---

## 2. Instalar (2 passos)

**Passo 1.** aaPanel → **Files** → `/home/deploy/` → **Upload** →
envie `consultoria-redes/gerar_estatisticas.py`. Pode sobrescrever o antigo.

**Passo 2.** aaPanel → **Terminal**:

```
python3 /home/deploy/gerar_estatisticas.py
```

**Passo 3.** Abra **https://missaocomdeus.com.br/stats.html**

O cron que já existe não precisa ser mexido. Nada muda no site.

---

## 3. Como ler com honestidade

- **Visita** = sessão de 30 minutos. Navegar do livro 04 para o livro 05 é a mesma visita.
- **Pessoas** = IPs distintos. É aproximação: IP de celular é compartilhado e muda.
- **Percentual** só vale dentro do mesmo bloco. Os dois blocos não se somam.
- **«Direto»** cresce porque WhatsApp, Instagram e TikTok abrem o link sem avisar
  de onde a pessoa veio. Não é gente que digitou o endereço, necessariamente.
  Para resolver isso de verdade: use os links marcados do `LINKS_COM_UTM.md`.
- **Site antigo (declarado)** = o navegador avisou que veio do compraoseu.com.
  Quando ele não avisa, a visita cai em «Direto». As duas linhas se completam.

---

## 4. Opcional: descontar os seus próprios acessos

Se o senhor quiser que os seus acessos não entrem na conta (o senhor abre o painel
várias vezes ao dia), descubra o seu IP (Google: «qual é o meu ip») e coloque na
linha do cron:

```
STATS_IPS_IGNORAR="189.10.20.30" python3 /home/deploy/gerar_estatisticas.py
```

O painel mostra quantos acessos foram descontados por isso.

---

## 5. Opcional: links marcados (UTM)

Arquivo **`LINKS_COM_UTM.md`**. Antes de usar, rode o **`APLICAR_CANONICAL.py`**
(passo 6 abaixo) para o Google não achar que são páginas repetidas.

---

## 6. Opcional: canonical

```
python3 /home/deploy/APLICAR_CANONICAL.py
```

Faz backup `.bak` de cada arquivo antes. Não toca no player da Palavra.

---

## 7. Se aparecer «Não achei o log do site antigo»

```
ls /www/wwwlogs/ | grep -i compraoseu
```

Se o nome for outro, passe na linha do cron:
`STATS_LOG_ANTIGO=/www/wwwlogs/nome-certo.log python3 /home/deploy/gerar_estatisticas.py`

Outras variáveis úteis: `STATS_LOG_EXTRA` (globs de logs rotacionados),
`STATS_SESSAO_MIN` (minutos da sessão, padrão 30).

---

## 8. Onde estão os arquivos no GitHub

Estão no branch da nossa sessão:
<https://github.com/sidneyrma/instalador/tree/arena/01a061ac-instalador/consultoria-redes>

Download direto do script:
<https://raw.githubusercontent.com/sidneyrma/instalador/arena/01a061ac-instalador/consultoria-redes/gerar_estatisticas.py>

> Observação da casa: o GitHub está **atrás** do servidor. O que vale no ar é o
> que está em `/www/wwwroot/missaocomdeus.com.br/`.

---

«Lâmpada para os meus pés é a tua palavra, e luz para o meu caminho.» (Salmo 119:105)
