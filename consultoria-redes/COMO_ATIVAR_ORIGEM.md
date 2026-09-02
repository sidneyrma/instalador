# Rastreio de origem no painel /stats (v4)

**Para:** Missão com Deus · missaocomdeus.com.br
**O que é:** o painel de estatísticas passa a responder *de onde os nossos irmãos estão chegando*.

---

## 1. O que o painel passa a responder

| Pergunta | Onde aparece |
|---|---|
| Quantos chegam pela busca do Google (SEO) | Card **SEO (busca)** + tabela **Origem** |
| Quantos chegam pelo endereço antigo compraoseu.com (301) | Card **Site antigo** + tabela própria logo abaixo |
| Quantos vêm direto (digitou, favoritos, grupos) | Card **Direto** |
| Quantos vêm de Instagram, TikTok, YouTube, WhatsApp | Card **Redes** |
| Por qual página eles entram | Tabela **Por qual página eles entram** |
| Qual página o Google mais entrega | Tabela **Páginas que o Google mais entrega** |
| Quem nos indica (outros sites) | Tabela **Quem nos indica (domínios)** |
| Dia a dia: SEO × direto × redes × site antigo | Tabela **Últimos 7 dias por origem** |

Não usa cookie, não usa Google Analytics, não instala script de ninguém.
É só o **log do servidor** (o mesmo que já gerava o painel). O site não muda nada.

---

## 2. Instalar (2 passos)

**Passo 1.** aaPanel → **Files** → pasta `/home/deploy/` → **Upload** →
envie o arquivo `gerar_estatisticas.py` desta pasta.
Pode sobrescrever o antigo sem medo: a v4 faz tudo que a v3 já fazia e acrescenta a origem.

**Passo 2.** aaPanel → **Terminal** → cole esta linha e dê Enter:

```
python3 /home/deploy/gerar_estatisticas.py
```

**Passo 3.** Abra **https://missaocomdeus.com.br/stats.html**

> Se o painel já rodava no cron (de hora em hora), **não precisa mexer no cron**:
> ele continua no ar e agora gera a v4 sozinho.

---

## 3. Se aparecer «Não achei o log do site antigo»

O script procura o log do compraoseu.com em três lugares. Se ele não achar,
descubra o nome certo em **2 linhas** no Terminal:

```
ls /www/wwwlogs/ | grep -i compraoseu
```

Se aparecer um nome diferente (exemplo: `compraoseu.com.log_2026-09-01`),
acrescente o caminho na linha do cron, assim:

```
STATS_LOG_ANTIGO=/www/wwwlogs/compraoseu.com.log_2026-09-01 python3 /home/deploy/gerar_estatisticas.py
```

Se não aparecer **nenhum** arquivo, o compraoseu.com não está mais registrando log
nisse servidor. Ainda assim o painel funciona: ele mostra as chegadas pelo site novo
(SEO, direto, redes) e a linha do site antigo fica marcada como «não lido».

---

## 4. Como ler o painel sem se enganar

**Chegada** = o primeiro acesso da visita, quando quem indicou é de fora da casa.
Navegar do livro 04 para o livro 05 **não conta** (é a mesma visita).

**Regra de ouro: não somar os dois blocos.**
Quem vem do compraoseu.com atravessa o redirecionamento e chega no site novo,
e o navegador guarda a origem de *antes* (o Google, por exemplo).
Ou seja: aquela visita **já está contada** dentro do número de SEO.

- O bloco de cima responde: *«de todo mundo que chegou, quanto é busca, quanto é direto?»*
- O bloco do site antigo responde: *«do pessoal que ainda vem pelo endereço antigo,
  quanto é busca e quanto é gente que digitou o endereço?»*

Robôs, varredores e ferramentas de SEO de empresa (SEMrush, Ahrefs) continuam descartados.

---

## 5. Opicional: marcar os links que o senhor compartilha

WhatsApp e Instagram não avisam de onde a pessoa veio, então ela aparece como **Direto**.
Para enxergar de verdade, use os links prontos do arquivo **`LINKS_COM_UTM.md`**.
O painel já lê essas marcações automaticamente.

Se for usar links marcados, vale rodar antes o **`APLICAR_CANONICAL.py`** (passo 6)
para o Google não achar que são páginas repetidas.

---

## 6. Opcional: proteger o SEO ao usar links marcados (canonical)

Script **`APLICAR_CANONICAL.py`** (nesta pasta). Ele só acrescenta uma linha no
`<head>` das páginas dizendo ao Google qual é o endereço oficial de cada uma.
Faz backup de cada arquivo antes de mexer.

aaPanel → **Terminal** → 2 linhas:

```
cp APLICAR_CANONICAL.py /home/deploy/ 2>/dev/null; cd /home/deploy
python3 /home/deploy/APLICAR_CANONICAL.py
```

(Se o arquivo foi enviado direto para `/home/deploy/`, só a segunda linha basta.)

> Não mexe em `index.html` por inteiro, não troca o player da Palavra, não apaga nada.
> Só insere uma linha e guarda uma cópia `.bak` do arquivo anterior.

---

## 7. Marcar o redirecionamento do site antigo (só se quiser o detalhe)

**Atenção: isto NÃO é obrigatório.** O bloco do site antigo já funciona sem mexer em nada.
Só faça este passo se o senhor quiser ver, página por página, quem chegou pelo 301.

No Nginx do compraoseu.com, onde hoje está o redirect, trocar por:

```
location / {
    if ($is_args) {
        return 301 https://missaocomdeus.com.br$request_uri&utm_source=compraoseu&utm_medium=redirect;
    }
    return 301 https://missaocomdeus.com.br$request_uri?utm_source=compraoseu&utm_medium=redirect;
}
```

Antes de recarregar, **sempre**:

```
nginx -t
```

Se o teste falhar, **não recarregue** e desfaça a alteração (volte o bloco anterior).
O 301 está saudável e aprovado no Google Search Console. Se está funcionando, melhor não mexer.

---

## 8. O que NÃO muda

- `index.html` e os 12 livros continuam intocados.
- Nenhuma mudança no Nginx (a não ser que o senhor escolha os passos opcionais).
- `stats.html` é sobrescrito a cada rodada, não acumula arquivos.
- `leituras.json` continua sendo gerado para a biblioteca.
- O painel continua `noindex` (não aparece no Google).

«Lâmpada para os meus pés é a tua palavra, e luz para o meu caminho.» (Salmo 119:105)
