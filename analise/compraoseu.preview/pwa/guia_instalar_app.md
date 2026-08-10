# 📱 COMO SEU SITE VIRA UM "APP" NO CELULAR (PWA)

**Objetivo:** permitir que seus leitores instalem o compraoseu.com como um **aplicativo
com ícone na tela inicial** — abrindo direto o site, sem digitar endereço.

---

## ✅ ESCOLHIDO: Ícone da Opção A (livro aberto com luz dourada)

O ícone do app é um **livro aberto com luz**, no estilo da marca (navy + dourado).
Já gerado em todas as dimensões necessárias e publicado no GitHub Pages.

---

## 🎯 A SOLUÇÃO QUE FUNCIONA SEM SUBIR ARQUIVOS NA VENDD

> A Vendd (plataforma de landing pages) **não tem opção de upload de arquivos
> estáticos** (manifest.json / sw.js). Mas isso **não impede o PWA básico**!

A estratégia: **o `manifest.json` e os ícones ficam no GitHub Pages**
(que libera acesso cross-origin), e a Home só precisa de um bloco no `<head>`.

### Como fica:

| Recurso | Onde está | Como chega |
|---|---|---|
| `manifest.json` | GitHub Pages | link `rel="manifest"` na Home |
| Ícones (192/512/maskable/apple) | GitHub Pages | links no `<head>` da Home |
| Nome do app | no manifest | "Portal O Despertar" |
| Ícone do iPhone | `apple-touch-icon.png` | link no `<head>` |

### Passo único na Vendd:
1. Na página principal, abra o **código/HTML** (ou as Configurações da página);
2. Cole o conteúdo do arquivo `analise/compraoseu.preview/pwa/codigo_para_vendd.html`
   no `<head>` (antes do `</head>`);
3. Salve.

Pronto! O site agora tem manifest + ícones. Os visitantes fazem:

**No Android (Chrome):** abrir `compraoseu.com` → menu **⋮** → **"Adicionar à tela inicial"** →
o atalho aparece com o **ícone do livro dourado** e o nome **Portal O Despertar** 📲

**No iPhone (Safari):** abrir `compraoseu.com` → botão **Compartilhar** →
**"Adicionar à Tela de Início"** → o atalho usa o `apple-touch-icon` (livro dourado) 📲

---

## 🛠️ OPCIONAL: PWA COMPLETO (botão "Instalar" automático + offline)

Para o Chrome oferecer o **botão "Instalar"** automaticamente e o app funcionar
**offline**, é necessário o **service worker** (`sw.js`) no **mesmo domínio**
(`https://www.compraoseu.com/sw.js`). Isso exige upload de arquivo na Vendd.

**Como descobrir se a Vendd permite:**
1. Acesse o menu **Vendd GPT** (você tem no painel) e pergunte:
   *"Como faço upload de arquivos estáticos (manifest.json e sw.js) no meu domínio?"*
2. Ou fale com o **Suporte** da Vendd;
3. Ou procure em **Configurações** / **Domínios** se há "Arquivos", "Assets" ou "Código personalizado".

**Se a Vendd permitir upload:**
- Suba `manifest.json` e `sw.js` (pasta `pwa/`) para o domínio;
- Troque na Home o link do manifest para `https://www.compraoseu.com/manifest.json`;
- Volte a incluir o registro do service worker no `<head>`:
```html
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('https://www.compraoseu.com/sw.js');
    });
  }
</script>
```

**Se não permitir:** tudo bem! O **atalho na tela inicial com o ícone bonito**
(caminho acima) já cobre 90% do benefício — o visitante abre o site com 1 toque
no ícone do livro, sem digitar endereço. Apenas não terá o modo tela cheia
automático nem o botão "Instalar" nativo.

---

## ✅ CHECKLIST

- [ ] Ícones publicados no GitHub Pages (feito: `docs/icones/`)
- [ ] `manifest.json` publicado no GitHub Pages (feito: `docs/manifest.json`)
- [ ] Home com o bloco do `<head>` colado (feito no `paginas/home_preview.html`)
- [ ] Colar a Home atualizada na Vendd
- [ ] Testar no celular: adicionar à tela inicial → ícone do livro dourado
- [ ] (Opcional) Perguntar ao Vendd GPT/Suporte sobre upload de `sw.js`

---

*Ícone: Opção A (livro aberto com luz) · Portal O Despertar · Missão com Deus*
