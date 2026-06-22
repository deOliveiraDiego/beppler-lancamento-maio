# Design Spec: Sofia Analytics Dashboard

**Data:** 2026-04-29  
**Status:** Aprovado

---

## Objetivo

Criar um dashboard HTML estático hospedado no GitHub Pages que exiba as análises periódicas de performance da Sofia WTP. Elimina o roundtrip para claude.ai — o HTML é gerado/atualizado diretamente no Claude Code após cada novo relatório MD.

---

## Repositório

- **Repo:** `deoliveiratech/beppler-lancamento-maio`
- **Branch principal:** `main`
- **GitHub Pages:** servido do `main`, pasta raiz (`/`)
- **Init:** pasta `/lancamento-maio` existente vira a raiz do repo

---

## Estrutura de arquivos

```
lancamento-maio/
  index.html              ← shell: header, tab bar, container
  style.css               ← todos os estilos
  app.js                  ← lógica de tabs + fetch de fragmentos
  analyses/
    dia1-2.html           ← fragmento HTML (sem <html>/<head>/<body>)
    dia1-4.html
    dia5-10.html
  analise-sofia-wtp-*.md  ← fonte da verdade (mantidos no repo)
  wtp/
  handoff-*.md
  docs/
```

Os arquivos em `analyses/` são fragmentos puros — apenas o conteúdo da análise, sem wrapper de página. `index.html` é o shell completo.

---

## index.html — shell

Estrutura fixa:

```html
<header>
  <span class="eyebrow">deOliveiraTech · ANÁLISE DE PERFORMANCE</span>
  <h1>Sofia WTP — Lançamento Maio 2026</h1>
  <p class="date-range">[range do tab ativo]</p>
  <nav class="tabs">...</nav>
</header>
<main id="content">
  <!-- fragmento injetado via JS -->
</main>
<footer>
  deOliveiraTech · [stats do tab ativo]
</footer>
```

Sem menção a Dalton Lab em nenhum elemento — header, footer, meta tags, comentários.

---

## app.js — lógica de tabs

Array de configuração dos tabs:

```js
const TABS = [
  { id: "dia1-2",   label: "Dias 1–2",   file: "analyses/dia1-2.html"  },
  { id: "dia1-4",   label: "Dias 1–4",   file: "analyses/dia1-4.html"  },
  { id: "dia5-10",  label: "Dias 5–10",  file: "analyses/dia5-10.html" },
];
const DEFAULT_TAB = "dia5-10"; // mais recente sempre ativo por default
```

Comportamento:
- Na carga, ativa `DEFAULT_TAB` via fetch
- Clique em tab: fetch do fragmento → injeta em `#content` → atualiza classe `active` na nav
- Cache em memória: fragmentos já carregados não são re-fetchados
- URL hash sincronizada: `#dia5-10` — permite link direto para um tab

---

## style.css — sistema visual

Baseado no design do artifact (prints aprovados):

| Elemento | Estilo |
|---|---|
| Tipografia | System font stack, sem-serif |
| Background | `#ffffff` |
| Eyebrow / labels | Small caps, tracking expandido, cor cinza |
| Tab ativa | Background `#111`, texto branco |
| Tab inativa | Borda, background transparente |
| KPI cards | Grid 3×2, borda, número grande (~2.5rem), sublabel cinza |
| Alerta box | Borda esquerda destacada, fundo levemente tintado |
| Labels qualitativos | OK (verde), PROBLEMA (preto), ATENÇÃO (laranja), PENDENTE (vermelho) |
| Barras de funil | `div` com `width` proporcional inline, altura fixa |
| Código/citações | Fundo `#f5f5f5`, monospace, padding |
| Resolved items | `text-decoration: line-through`, opacidade reduzida |
| Footer | Cinza claro, texto pequeno, flex space-between |

---

## Fragmentos de análise (analyses/*.html)

Cada fragmento segue esta estrutura de seções na ordem:

1. **Alerta** — `<div class="alert">` — omitido se não houver pendências
2. **Métricas** — `<section class="metrics"><div class="kpi-grid">` — 6 cards
3. **Sessões por dia** — `<section><table>`
4. **Funil e profundidade** — `<section class="funnel">` — duas colunas
5. **Qualitativo** — `<section class="qualitative">` — itens com label lateral
6. **Recomendações** — `<section class="recommendations">` — itens com prioridade
7. **Conclusão** — `<div class="conclusion">` — síntese em negrito
8. **Metadados** — `<script type="application/json" id="tab-meta">` com `dateRange` e `stats` para o footer

O `app.js` lê os metadados do fragmento após inject para atualizar o date range no header e stats no footer.

---

## Workflow de atualização

Quando um novo relatório MD for gerado:

1. Claude lê o MD
2. Gera `analyses/diaX-Y.html` (fragmento estruturado)
3. Adiciona entrada em `TABS` no `app.js`
4. Atualiza `DEFAULT_TAB` para o novo tab
5. Push para `main` → GitHub Pages atualiza

Tempo estimado por atualização: uma sessão Claude Code, ~5 min.

---

## Branding

- **Header eyebrow:** "deOliveiraTech · ANÁLISE DE PERFORMANCE"
- **Footer:** "deOliveiraTech · [stats]"
- **Nenhuma** menção a Dalton Lab em qualquer arquivo (HTML, CSS, JS, comentários, meta tags)

---

## Fora do escopo

- Autenticação / proteção de acesso
- Backend / API
- Geração automática de HTML a partir de MD (sem build step)
- Suporte a `file://` local sem servidor
