# Sofia Analytics Dashboard — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Static HTML dashboard hospedado no GitHub Pages com tabs por período de análise, design editorial, branding deOliveiraTech.

**Architecture:** `index.html` (shell) + `style.css` + `app.js` (fetch de fragmentos + tab logic) + `analyses/*.html` (fragmentos por período). Sem build step, sem dependências externas.

**Tech Stack:** HTML5, CSS3 (custom properties, grid, flexbox), vanilla JS (fetch, hash routing), GitHub Pages.

---

## File Map

| Arquivo | Responsabilidade |
|---|---|
| `index.html` | Shell: header, tab nav, `#content` container, footer |
| `style.css` | Sistema visual completo: tipografia, tabs, cards, tabelas, qualitativo, recomendações |
| `app.js` | Config de tabs, fetch de fragmentos, injeção no DOM, cache, hash routing |
| `analyses/dia5-10.html` | Fragmento: período dias 5–10 (mais recente) |
| `analyses/dia1-4.html` | Fragmento: período dias 1–4 (baseline) |
| `analyses/dia1-2.html` | Fragmento: período dias 1–2 (análise inicial) |
| `.gitignore` | Ignora .DS_Store e afins |
| `README.md` | Uma linha descrevendo o projeto |

---

## Task 1: Git repo + GitHub

**Files:**
- Create: `.gitignore`
- Create: `README.md`

- [ ] **Step 1: Init git repo**

```bash
cd /Users/deoliveiradiego/Projects/deoliveiratech/beppler/lancamento-maio
git init
```

Expected: `Initialized empty Git repository in .../lancamento-maio/.git/`

- [ ] **Step 2: Criar .gitignore**

```
.DS_Store
*.swp
.env
node_modules/
```

- [ ] **Step 3: Criar README.md**

```markdown
# Sofia WTP — Analytics Dashboard

Dashboard de performance da agente Sofia durante o lançamento WTP Maio 2026.
```

- [ ] **Step 4: Criar repo no GitHub**

```bash
gh repo create deoliveiratech/beppler-lancamento-maio \
  --public \
  --description "Dashboard de análise de performance — Sofia WTP Lançamento Maio 2026" \
  --source . \
  --remote origin
```

Expected: URL do repo retornada pelo gh.

- [ ] **Step 5: Commit inicial**

```bash
git add .gitignore README.md
git commit -m "chore: init repo"
git push -u origin main
```

---

## Task 2: style.css

**Files:**
- Create: `style.css`

- [ ] **Step 1: Criar style.css completo**

```css
/* ─── Reset & Variables ─────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --text:          #111111;
  --text-muted:    #666666;
  --text-light:    #999999;
  --border:        #e0e0e0;
  --border-subtle: #f0f0f0;
  --bg:            #ffffff;
  --bg-subtle:     #f5f5f5;
  --ok:            #276527;
  --problema:      #111111;
  --atencao:       #b84a00;
  --pendente:      #b30000;
  --tab-active:    #111111;
  --max-width:     960px;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  font-size: 15px;
  color: var(--text);
  background: var(--bg);
  line-height: 1.55;
}

/* ─── Page Header ────────────────────────────────────── */
.page-header {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 48px 24px 0;
}

.eyebrow {
  display: block;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--text-muted);
  margin-bottom: 10px;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 6px;
}

.date-range {
  font-size: 0.88rem;
  color: var(--text-muted);
  margin-bottom: 32px;
}

/* ─── Tab Navigation ─────────────────────────────────── */
.tab-nav {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  gap: 8px;
  margin-bottom: 48px;
}

.tab-btn {
  padding: 6px 16px;
  border: 1px solid var(--border);
  background: transparent;
  cursor: pointer;
  font-size: 0.88rem;
  font-family: inherit;
  color: var(--text);
  transition: border-color 0.1s;
}

.tab-btn:hover:not(.active) {
  border-color: #aaa;
}

.tab-btn.active {
  background: var(--tab-active);
  color: #fff;
  border-color: var(--tab-active);
}

/* ─── Content Container ──────────────────────────────── */
#content {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 24px;
}

/* ─── Section Headers ────────────────────────────────── */
.section { margin-bottom: 56px; }

.section-label {
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--text-muted);
  font-weight: 500;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}

/* ─── Alert Box ──────────────────────────────────────── */
.alert {
  border: 1px solid var(--text);
  padding: 18px 22px;
  margin-bottom: 48px;
  font-size: 0.9rem;
}

.alert-title {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
  margin-bottom: 6px;
}

.alert p { color: var(--text); }

/* ─── KPI Grid ───────────────────────────────────────── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border-top: 1px solid var(--border);
  border-left: 1px solid var(--border);
}

.kpi-card {
  padding: 20px 22px;
  border-right: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.kpi-label {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.kpi-value {
  font-size: 2.2rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
}

.kpi-sub {
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* ─── Tables ─────────────────────────────────────────── */
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  text-align: left;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  font-weight: 500;
  padding: 0 0 10px;
  border-bottom: 1px solid var(--border);
}

.data-table td {
  padding: 10px 0;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 0.9rem;
}

.data-table td:first-child { font-weight: 500; }

.row-highlight td { background: var(--bg-subtle); }

/* ─── Funnel ─────────────────────────────────────────── */
.funnel-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px;
  align-items: start;
}

.funnel-stat-row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding: 9px 0;
  border-bottom: 1px solid var(--border-subtle);
  font-size: 0.9rem;
}

.funnel-stat-label { color: var(--text); }

.funnel-stat-value {
  font-weight: 700;
  white-space: nowrap;
}

.funnel-stat-note {
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-left: 6px;
  font-weight: 400;
}

.bar-row {
  margin-bottom: 12px;
}

.bar-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.bar-label { color: var(--text); font-weight: 500; }

.bar-track {
  height: 3px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--text);
  border-radius: 2px;
}

/* ─── Qualitative Items ──────────────────────────────── */
.qual-item {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 24px;
  padding: 20px 0;
  border-bottom: 1px solid var(--border);
}

.qual-label {
  font-size: 0.66rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
  padding-top: 2px;
  color: var(--text-muted);
}

.qual-label.ok       { color: var(--ok); }
.qual-label.problema { color: var(--problema); }
.qual-label.atencao  { color: var(--atencao); }

.qual-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 6px;
}

.qual-body { font-size: 0.88rem; color: var(--text); }

/* ─── Recommendation Items ───────────────────────────── */
.rec-item {
  display: grid;
  grid-template-columns: 88px 1fr;
  gap: 24px;
  padding: 20px 0;
  border-bottom: 1px solid var(--border);
}

.rec-item.resolved {
  opacity: 0.45;
}

.rec-label {
  font-size: 0.66rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-weight: 700;
  padding-top: 2px;
  color: var(--text-muted);
}

.rec-label.pendente { color: var(--pendente); }
.rec-label.medio    { color: var(--text); }
.rec-label.baixo    { color: var(--text-light); }

.rec-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 6px;
}

.rec-item.resolved .rec-title { text-decoration: line-through; }

.rec-body { font-size: 0.88rem; }

/* ─── Evidence / Blockquote ──────────────────────────── */
.evidence {
  background: var(--bg-subtle);
  padding: 12px 16px;
  margin: 10px 0;
  font-size: 0.85rem;
  line-height: 1.5;
}

.evidence cite {
  display: block;
  font-style: normal;
  margin-bottom: 2px;
  color: var(--text-muted);
  font-size: 0.78rem;
}

/* ─── Code blocks ────────────────────────────────────── */
pre {
  background: var(--bg-subtle);
  padding: 12px 16px;
  font-size: 0.8rem;
  font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
  overflow-x: auto;
  margin: 10px 0;
  line-height: 1.5;
}

/* ─── Conclusion Box ─────────────────────────────────── */
.conclusion {
  border: 1px solid var(--border);
  padding: 22px 26px;
  margin-top: 40px;
  font-size: 0.9rem;
  line-height: 1.6;
}

/* ─── Footer ─────────────────────────────────────────── */
.page-footer {
  max-width: var(--max-width);
  margin: 56px auto 0;
  padding: 20px 24px 40px;
  border-top: 1px solid var(--border);
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* ─── Loading state ──────────────────────────────────── */
.loading {
  padding: 48px 0;
  color: var(--text-muted);
  font-size: 0.88rem;
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "feat: add complete stylesheet"
```

---

## Task 3: index.html shell

**Files:**
- Create: `index.html`

- [ ] **Step 1: Criar index.html**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sofia WTP — Analytics · deOliveiraTech</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

  <header>
    <div class="page-header">
      <span class="eyebrow">deOliveiraTech · Análise de Performance</span>
      <h1 class="page-title">Sofia WTP — Lançamento Maio 2026</h1>
      <p class="date-range" id="date-range">Carregando...</p>
    </div>
    <nav class="tab-nav" id="tab-nav" role="tablist" aria-label="Períodos de análise"></nav>
  </header>

  <main id="content" role="main">
    <p class="loading">Carregando análise...</p>
  </main>

  <footer class="page-footer">
    <span>deOliveiraTech</span>
    <span id="footer-stats"></span>
  </footer>

  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Verificar abre sem erros**

```bash
python3 -m http.server 8080 &
open http://localhost:8080
```

Expected: página carrega, mostra "Carregando análise..." no main, sem erros no console.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add page shell"
```

---

## Task 4: app.js

**Files:**
- Create: `app.js`

- [ ] **Step 1: Criar app.js**

```js
const TABS = [
  { id: 'dia1-2',  label: 'Dias 1–2',  file: 'analyses/dia1-2.html'  },
  { id: 'dia1-4',  label: 'Dias 1–4',  file: 'analyses/dia1-4.html'  },
  { id: 'dia5-10', label: 'Dias 5–10', file: 'analyses/dia5-10.html' },
];

const DEFAULT_TAB = 'dia5-10';

const cache = {};

async function loadTab(tab) {
  const content = document.getElementById('content');
  content.innerHTML = '<p class="loading">Carregando...</p>';

  if (!cache[tab.id]) {
    const res = await fetch(tab.file);
    if (!res.ok) throw new Error(`Erro ao carregar ${tab.file}: ${res.status}`);
    cache[tab.id] = await res.text();
  }

  content.innerHTML = cache[tab.id];

  const metaEl = document.getElementById('tab-meta');
  if (metaEl) {
    try {
      const meta = JSON.parse(metaEl.textContent);
      document.getElementById('date-range').textContent = meta.dateRange || '';
      document.getElementById('footer-stats').textContent = meta.stats || '';
    } catch (_) {}
  }
}

function activateTab(tabId) {
  const tab = TABS.find(t => t.id === tabId) || TABS.find(t => t.id === DEFAULT_TAB);

  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tab.id);
    btn.setAttribute('aria-selected', btn.dataset.tab === tab.id);
  });

  history.replaceState(null, '', `#${tab.id}`);
  loadTab(tab).catch(err => {
    document.getElementById('content').innerHTML =
      `<p class="loading">Erro ao carregar análise: ${err.message}</p>`;
  });
}

function buildNav() {
  const nav = document.getElementById('tab-nav');
  TABS.forEach(tab => {
    const btn = document.createElement('button');
    btn.className = 'tab-btn';
    btn.dataset.tab = tab.id;
    btn.textContent = tab.label;
    btn.setAttribute('role', 'tab');
    btn.setAttribute('aria-selected', 'false');
    btn.addEventListener('click', () => activateTab(tab.id));
    nav.appendChild(btn);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  buildNav();
  const hash = location.hash.replace('#', '');
  const initialTab = TABS.find(t => t.id === hash) ? hash : DEFAULT_TAB;
  activateTab(initialTab);
});
```

- [ ] **Step 2: Verificar tabs renderizam (servidor deve estar rodando do task 3)**

Abrir `http://localhost:8080` — espera ver os 3 botões de tab no header. Os fragmentos ainda não existem, então o conteúdo mostrará erro de fetch — isso é esperado.

- [ ] **Step 3: Commit**

```bash
git add app.js
git commit -m "feat: add tab routing and fetch logic"
```

---

## Task 5: analyses/dia5-10.html (mais recente)

**Files:**
- Create: `analyses/dia5-10.html`

- [ ] **Step 1: Criar diretório**

```bash
mkdir -p analyses
```

- [ ] **Step 2: Criar analyses/dia5-10.html**

```html
<script type="application/json" id="tab-meta">
{"dateRange": "23/abr 20:44 → 29/abr 10:49 BRT · 6 dias", "stats": "44 sessões novas · 229 respostas bot"}
</script>

<div class="alert">
  <p class="alert-title">⚠ Pendente — Sessão ...2040 (cancelamento, desde dia 1)</p>
  <p>Lead pediu cancelamento em 21/abr, desistiu em 20:57 do mesmo dia. <strong>Sem confirmação de resolução.</strong> Verificar se houve chargeback ou disputa.</p>
</div>

<section class="section">
  <h2 class="section-label">Métricas — Dias 5–10</h2>
  <div class="kpi-grid">
    <div class="kpi-card">
      <span class="kpi-label">Respostas do bot</span>
      <span class="kpi-value">229</span>
      <span class="kpi-sub">44 sessões novas</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Links enviados</span>
      <span class="kpi-value">10</span>
      <span class="kpi-sub">22,7% das sessões</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Escalonamentos c/ e-mail</span>
      <span class="kpi-value">47</span>
      <span class="kpi-sub">100% com instrução ativa</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Promessas vazias</span>
      <span class="kpi-value">0</span>
      <span class="kpi-sub">Padrão "já acionei" — eliminado</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Tique "Perfeito"</span>
      <span class="kpi-value">31,4%</span>
      <span class="kpi-sub">72 de 229 · corrigido em 29/abr</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Lote vigente</span>
      <span class="kpi-value">L1→L2</span>
      <span class="kpi-sub">R$47 → R$57 a partir de 28/abr</span>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Sessões por dia</h2>
  <table class="data-table">
    <thead>
      <tr><th>Data</th><th>Sessões novas</th><th>Observação</th></tr>
    </thead>
    <tbody>
      <tr><td>23/abr (qua)</td><td>1</td><td>Tail do dia 4 — após cutoff 20:44</td></tr>
      <tr><td>24/abr (qui)</td><td>4</td><td>Queda mid-week</td></tr>
      <tr><td>25/abr (sex)</td><td>4</td><td>Mínimo do período</td></tr>
      <tr><td>26/abr (sáb)</td><td>6</td><td>Leve recuperação</td></tr>
      <tr class="row-highlight"><td>27/abr (dom)</td><td>12</td><td>Pico — domingo</td></tr>
      <tr class="row-highlight"><td>28/abr (seg)</td><td>10</td><td>Abertura Lote 2 (R$57)</td></tr>
      <tr><td>29/abr (ter)</td><td>7</td><td>Parcial — dia em andamento</td></tr>
    </tbody>
  </table>
</section>

<section class="section">
  <h2 class="section-label">Funil e Profundidade</h2>
  <div class="funnel-grid">
    <div class="funnel-stats">
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Sessões novas</span>
        <span class="funnel-stat-value">44 <span class="funnel-stat-note">100%</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Engajamento real (3+ msgs)</span>
        <span class="funnel-stat-value">31 <span class="funnel-stat-note">70%</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Receberam link</span>
        <span class="funnel-stat-value">10 <span class="funnel-stat-note">22,7% · 6 L1 · 4 L2</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Escalonamentos com e-mail</span>
        <span class="funnel-stat-value">47 <span class="funnel-stat-note">100% ✓</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Promessas sem ação</span>
        <span class="funnel-stat-value">0 <span class="funnel-stat-note">eliminado</span></span>
      </div>
    </div>
    <div class="funnel-bars">
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">1–2 msgs</span><span>13 &nbsp;30% &nbsp;↑ era 21%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:30%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">3–5 msgs</span><span>4 &nbsp;9%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:9%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">6–10 msgs</span><span>14 &nbsp;32% &nbsp;65 min vs. 560 min ⬇</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:32%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">11–20 msgs</span><span>8 &nbsp;18% &nbsp;200 min vs. 1.295 min ⬇</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:18%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">21+ msgs</span><span>5 &nbsp;11% &nbsp;1.038 min vs. 3.078 min ⬇</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:11%"></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Qualitativo — Dias 5–10</h2>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Escalonamento via e-mail — padrão consolidado</p>
      <p class="qual-body">100% das indicações de suporte incluem o e-mail (suporte@fernandabeppler.com.br). Nenhuma promessa vazia detectada nas novas sessões.</p>
      <div class="evidence">"Isso é suporte de acesso, e eu não consigo resolver por aqui. Me chama no e-mail suporte@fernandabeppler.com.br que a equipe te orienta certinho por lá."</div>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Caso crítico resolvido — ...3993 comprou</p>
      <p class="qual-body">Lead sem PIX/cartão que ficou 34h+ em loop no baseline. Após 7 dias de acompanhamento sem pressão, <strong>comprou em 27/abr (Lote 1) e confirmou acesso em 28/abr.</strong></p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Identificação de golpes — padrão mantido</p>
      <p class="qual-body">4 sessões com links suspeitos de "Mercado Livre" (.ru). Sofia identificou e alertou corretamente em todas.</p>
      <div class="evidence">"Isso é golpe. O link não é do Mercado Livre (domínio estranho .ru e promessa de PIX imediato). Nunca clique."</div>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Nurturing pós-compra de qualidade — sessão ...5548</p>
      <p class="qual-body">58 msgs com lead que já havia comprado o Lote 2. Sofia sustentou conversa sobre autoconhecimento, a Imperatriz como carta recorrente, intuição vs. técnica — sem tentar revender. Engajamento consistente.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label problema">Problema</span>
    <div>
      <p class="qual-title">"Perfeito" — resolvido ✅</p>
      <p class="qual-body">72 de 229 respostas (31,4%) abriam com "Perfeito" — leve piora vs. 30% do baseline.</p>
      <div class="evidence">
        Lead: "Ainda não [responderam]" → Sofia: <strong>Perfeito.</strong><br>
        Lead: "Obrigada" → Sofia: <strong>Perfeito ✨</strong> "Eles vão te responder..."
      </div>
      <p class="qual-body" style="margin-top:8px">Instrução adicionada em O QUE NUNCA FAZER &gt; SOBRE COMUNICAÇÃO. Validado em 29/abr.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label problema">Problema</span>
    <div>
      <p class="qual-title">Emojis fora da whitelist — resolvido ✅</p>
      <p class="qual-body">😊 e 😂 apareceram em novas sessões. A whitelist existia no formato mas sem proibição explícita dos demais.</p>
      <div class="evidence">
        Lead: "Estou esperando alguém chegar pra me ajudar Kkkk"<br>
        Sofia: "Boa 😂 Às vezes outra pessoa já resolve em minutos."
      </div>
      <p class="qual-body" style="margin-top:8px">Proibição explícita adicionada ao prompt. Após correção, 4/4 testes usaram exclusivamente emojis da whitelist.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label atencao">Atenção</span>
    <div>
      <p class="qual-title">Sessões rasas crescendo (30% vs. 21%)</p>
      <p class="qual-body">4 sessões de alerta de golpe, 1 de plano de saúde, várias com "Oi" sem continuidade. Parte é ruído natural. O aumento pode indicar mudança no perfil de quem chega à medida que o lançamento avança.</p>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Recomendações — Dias 5–10</h2>

  <div class="rec-item">
    <span class="rec-label pendente">Pendente</span>
    <div>
      <p class="rec-title">Verificar sessão ...2040 (cancelamento)</p>
      <p class="rec-body">Última atividade: 21/abr 20:57. Sem confirmação de resolução. Verificar se houve chargeback ou disputa.</p>
    </div>
  </div>

  <div class="rec-item resolved">
    <span class="rec-label medio">Médio</span>
    <div>
      <p class="rec-title">Eliminar "Perfeito" ✅ Resolvido</p>
      <p class="rec-body">Instrução adicionada em O QUE NUNCA FAZER &gt; SOBRE COMUNICAÇÃO.</p>
    </div>
  </div>

  <div class="rec-item resolved">
    <span class="rec-label medio">Médio</span>
    <div>
      <p class="rec-title">Reforçar whitelist de emojis ✅ Resolvido</p>
      <p class="rec-body">Proibição explícita em FORMATO DE RESPOSTA e O QUE NUNCA FAZER. Validado com 4 testes.</p>
    </div>
  </div>

  <div class="rec-item">
    <span class="rec-label medio">Médio</span>
    <div>
      <p class="rec-title">Monitorar objeções de preço no Lote 2</p>
      <p class="rec-body">R$57 tem apenas 2 dias de dados. Adicionar query de acompanhamento para Lote 3 (R$67).</p>
    </div>
  </div>

  <div class="rec-item">
    <span class="rec-label baixo">Baixo</span>
    <div>
      <p class="rec-title">Checar calendário de conteúdo nas quintas/sextas</p>
      <p class="rec-body">24 e 25/abr tiveram apenas 4 sessões cada (mínimo do período). Se não havia push de conteúdo nesses dias, o padrão é esperado. Se havia, vale investigar.</p>
    </div>
  </div>

  <div class="rec-item">
    <span class="rec-label baixo">Baixo</span>
    <div>
      <p class="rec-title">Filtro pré-agente no n8n</p>
      <p class="rec-body">Detectar e descartar auto-replies (listas numeradas, assinaturas de bots) antes de chegar na Sofia.</p>
    </div>
  </div>
</section>

<div class="conclusion">
  O período de dias 5–10 mostra um funcionamento mais limpo. O fix de escalonamento via e-mail está consolidado — nenhuma promessa vazia nas novas sessões. O funil mantém 22,7% de link enviado, com Lote 2 abrindo bem (4 sessões em 2 dias). <strong>Os dois itens estruturais abertos ("Perfeito" e emojis) foram corrigidos e validados em 29/abr — o próximo ciclo dirá se os ajustes seguraram.</strong>
</div>
```

- [ ] **Step 3: Verificar tab dia5-10 carrega corretamente**

Com servidor rodando em `http://localhost:8080`, recarregar a página. O tab "Dias 5–10" deve estar ativo, o alert deve aparecer, métricas em grid 3×2.

- [ ] **Step 4: Commit**

```bash
git add analyses/dia5-10.html
git commit -m "feat: add dia5-10 analysis fragment"
```

---

## Task 6: analyses/dia1-4.html (baseline)

**Files:**
- Create: `analyses/dia1-4.html`

- [ ] **Step 1: Criar analyses/dia1-4.html**

```html
<script type="application/json" id="tab-meta">
{"dateRange": "20/abr 09:58 → 23/abr 20:44 BRT · 4 dias", "stats": "922 msgs · 57 sessões · baseline principal"}
</script>

<section class="section">
  <h2 class="section-label">Métricas — Dias 1–4</h2>
  <div class="kpi-grid">
    <div class="kpi-card">
      <span class="kpi-label">Total de mensagens</span>
      <span class="kpi-value">922</span>
      <span class="kpi-sub">57 sessões únicas</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Sessões com link</span>
      <span class="kpi-value">12</span>
      <span class="kpi-sub">21% · Lote Zero: 5 · Lote 1: 9</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Escalonamentos reais</span>
      <span class="kpi-value">0</span>
      <span class="kpi-sub">⚠ ferramenta nunca chamada</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Tique "Perfeito"</span>
      <span class="kpi-value">30%</span>
      <span class="kpi-sub">138 de 461 respostas</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Média msgs/sessão</span>
      <span class="kpi-value">16,2</span>
      <span class="kpi-sub">proporção human/AI 1:1 exato</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Lote vigente</span>
      <span class="kpi-value">L0→L1</span>
      <span class="kpi-sub">R$37 → R$47 a partir de 22/abr</span>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Sessões por dia</h2>
  <table class="data-table">
    <thead>
      <tr><th>Data</th><th>Sessões novas</th><th>Observação</th></tr>
    </thead>
    <tbody>
      <tr class="row-highlight"><td>20/abr (dom)</td><td>18</td><td>Abertura do lançamento</td></tr>
      <tr><td>21/abr (seg)</td><td>9</td><td>Queda — dia útil pós-domingo</td></tr>
      <tr><td>22/abr (ter)</td><td>16</td><td>Recuperação — virada p/ Lote 1</td></tr>
      <tr><td>23/abr (qua)</td><td>14</td><td>Parcial — dia ainda em andamento</td></tr>
    </tbody>
  </table>
</section>

<section class="section">
  <h2 class="section-label">Funil e Profundidade</h2>
  <div class="funnel-grid">
    <div class="funnel-stats">
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Sessões iniciadas</span>
        <span class="funnel-stat-value">57 <span class="funnel-stat-note">100%</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Engajamento real (3+ msgs)</span>
        <span class="funnel-stat-value">45 <span class="funnel-stat-note">79%</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Receberam link</span>
        <span class="funnel-stat-value">12 <span class="funnel-stat-note">21%</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Escalonamentos reais</span>
        <span class="funnel-stat-value">0 <span class="funnel-stat-note">⚠ nenhum</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Sessões em loop de suporte</span>
        <span class="funnel-stat-value">~12 <span class="funnel-stat-note">21%</span></span>
      </div>
    </div>
    <div class="funnel-bars">
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">1–2 msgs</span><span>12 &nbsp;21%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:21%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">3–5 msgs</span><span>8 &nbsp;14%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:14%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">6–10 msgs</span><span>14 &nbsp;25% &nbsp;464 min (~8h)</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:25%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">11–20 msgs</span><span>8 &nbsp;14% &nbsp;1.181 min (~20h)</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:14%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">21+ msgs</span><span>15 &nbsp;26% &nbsp;1.184 min (~20h)</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:26%"></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Qualitativo — Dias 1–4</h2>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Qualificação e conexão nos fluxos de venda pura</p>
      <p class="qual-body">Sessão ...1042953 (66 msgs, comprou): lead masculino com 10 anos de contato esporádico com Tarot. Sofia identificou o perfil, qualificou sem forçar, enviou link no momento certo. Pós-compra com nurturing genuíno sobre escolha de baralho e técnica.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Modo fria funcional e consistente</p>
      <p class="qual-body">Mensagens de 1–3 palavras sem contexto tratadas sem CTA/link/emojis em todas as sessões analisadas.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Virada de lote correta</p>
      <p class="qual-body">Link do Lote 1 enviado corretamente a partir de 22/abr. A consulta a get_links funcionou como esperado na virada de lote.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label problema">Problema</span>
    <div>
      <p class="qual-title">CRÍTICO — encaminharAtendimento nunca chamada ✅ Resolvido</p>
      <p class="qual-body">0 chamadas reais em 4 dias. 159 mensagens mencionando "equipe", 50 com "encaminhar" — todas promessas vazias. Bug identificado e corrigido durante o lançamento.</p>
      <div class="evidence">
        Lead: "KD essa equipe? Eu preciso ir ao mercado."<br>
        Lead (dia seguinte): "Até agora nada. Nadinha."<br>
        Sofia: "Você não deveria estar passando por isso 💫 Acionei diretamente a equipe responsável agora."
      </div>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label problema">Problema</span>
    <div>
      <p class="qual-title">Lead querendo comprar esperou 34h — venda perdida por falha operacional</p>
      <p class="qual-body">Sessão ...3993: lead sem PIX/cartão ficou em loop por 34h aguardando equipe que nunca apareceu. Intenção de compra ativa até o final ("Até quando posso me inscrever?").</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label problema">Problema</span>
    <div>
      <p class="qual-title">Lead querendo cancelar esperou 49h — risco de chargeback</p>
      <p class="qual-body">Sessão ...2040 (52 msgs): pediu cancelamento em 21/abr, Sofia "acionou a equipe" 9 vezes. Nenhuma resposta real em 49 horas.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label atencao">Atenção</span>
    <div>
      <p class="qual-title">Tique "Perfeito" em contextos inadequados</p>
      <p class="qual-body">138 ocorrências (30% das respostas).</p>
      <div class="evidence">
        Lead: "Ainda não [fui atendida]" → Sofia: <strong>Perfeito</strong> 🌙<br>
        Lead: "Não" → Sofia: <strong>Perfeito</strong> 💫
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Recomendações — Dias 1–4</h2>

  <div class="rec-item resolved">
    <span class="rec-label pendente">Urgente</span>
    <div>
      <p class="rec-title">Bug de escalonamento — encaminharAtendimento nunca chamada ✅ Resolvido</p>
      <p class="rec-body">Em 159 mensagens Sofia dizia "vou encaminhar" sem nunca chamar a ferramenta. Corrigido durante o lançamento via mudança de comportamento textual: Sofia agora redireciona para suporte@fernandabeppler.com.br.</p>
    </div>
  </div>

  <div class="rec-item">
    <span class="rec-label pendente">Pendente</span>
    <div>
      <p class="rec-title">Verificar sessão ...2040 (cancelamento)</p>
      <p class="rec-body">Lead pediu cancelamento em 21/abr, sem atendimento confirmado. Verificar se houve chargeback ou disputa.</p>
    </div>
  </div>

  <div class="rec-item resolved">
    <span class="rec-label medio">Médio</span>
    <div>
      <p class="rec-title">Eliminar "Perfeito" ✅ Resolvido em 29/abr</p>
      <p class="rec-body">Instrução adicionada ao prompt em 29/abr. Validado em testes.</p>
    </div>
  </div>

  <div class="rec-item resolved">
    <span class="rec-label medio">Médio</span>
    <div>
      <p class="rec-title">Corrigir whitelist de emojis ✅ Resolvido em 29/abr</p>
      <p class="rec-body">Proibição explícita adicionada. Validado com 4 testes.</p>
    </div>
  </div>

  <div class="rec-item">
    <span class="rec-label baixo">Baixo</span>
    <div>
      <p class="rec-title">Filtro pré-agente no n8n</p>
      <p class="rec-body">Detectar e descartar auto-replies de bots (listas numeradas, assinaturas de corretoras) antes de chegar na Sofia.</p>
    </div>
  </div>
</section>

<div class="conclusion">
  A Sofia vende bem quando o caminho é limpo. O problema estrutural dos dias 1–4 foi o escalonamento — aproximadamente 40–50% das sessões ativas eram alunas com suporte não resolvido acumulando promessas vazias. <strong>O bug foi corrigido durante o lançamento. O impacto medido: pelo menos 2 casos com perda financeira potencial e ~12 sessões em loop.</strong>
</div>
```

- [ ] **Step 2: Verificar tab dia1-4 carrega**

Clicar em "Dias 1–4" — conteúdo deve trocar sem reload. Verificar que itens resolved aparecem com strikethrough e opacidade reduzida.

- [ ] **Step 3: Commit**

```bash
git add analyses/dia1-4.html
git commit -m "feat: add dia1-4 analysis fragment"
```

---

## Task 7: analyses/dia1-2.html (análise inicial)

**Files:**
- Create: `analyses/dia1-2.html`

- [ ] **Step 1: Criar analyses/dia1-2.html**

```html
<script type="application/json" id="tab-meta">
{"dateRange": "20/abr 09:58 → 21/abr 23:24 BRT · ~36h", "stats": "406 msgs · 27 sessões · análise inicial"}
</script>

<section class="section">
  <h2 class="section-label">Métricas — Dias 1–2</h2>
  <div class="kpi-grid">
    <div class="kpi-card">
      <span class="kpi-label">Total de mensagens</span>
      <span class="kpi-value">406</span>
      <span class="kpi-sub">27 sessões únicas</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Sessões com link</span>
      <span class="kpi-value">5</span>
      <span class="kpi-sub">18,5% das sessões</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Escalonamentos reais</span>
      <span class="kpi-value">0</span>
      <span class="kpi-sub">⚠ ferramenta nunca chamada</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Tique "Perfeito"</span>
      <span class="kpi-value">28,6%</span>
      <span class="kpi-sub">58 de 203 respostas</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Média msgs/sessão</span>
      <span class="kpi-value">15,0</span>
      <span class="kpi-sub">proporção human/AI 1:1 exato</span>
    </div>
    <div class="kpi-card">
      <span class="kpi-label">Lote vigente</span>
      <span class="kpi-value">L0</span>
      <span class="kpi-sub">R$37 — abertura do lançamento</span>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Distribuição por Hora (BRT)</h2>
  <table class="data-table">
    <thead>
      <tr><th>Período</th><th>Msgs</th><th>%</th><th>Observação</th></tr>
    </thead>
    <tbody>
      <tr class="row-highlight"><td>09h–12h</td><td>136</td><td>33,5%</td><td>Maior pico — abertura do dia</td></tr>
      <tr><td>15h–18h</td><td>88</td><td>21,7%</td><td>Pico da tarde</td></tr>
      <tr class="row-highlight"><td>22h–23h</td><td>96</td><td>23,6%</td><td>Pico noturno</td></tr>
      <tr><td>00h–08h</td><td>34</td><td>8,4%</td><td>Volume baixo</td></tr>
      <tr><td>13h–14h</td><td>6</td><td>1,5%</td><td>Quase morto</td></tr>
    </tbody>
  </table>
</section>

<section class="section">
  <h2 class="section-label">Funil e Profundidade</h2>
  <div class="funnel-grid">
    <div class="funnel-stats">
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Sessões iniciadas</span>
        <span class="funnel-stat-value">27 <span class="funnel-stat-note">100%</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Engajamento real (3+ msgs)</span>
        <span class="funnel-stat-value">20 <span class="funnel-stat-note">74%</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Receberam link</span>
        <span class="funnel-stat-value">5 <span class="funnel-stat-note">18,5%</span></span>
      </div>
      <div class="funnel-stat-row">
        <span class="funnel-stat-label">Escalonamentos reais</span>
        <span class="funnel-stat-value">0 <span class="funnel-stat-note">⚠ nenhum</span></span>
      </div>
    </div>
    <div class="funnel-bars">
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">1–2 msgs</span><span>7 &nbsp;26%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:26%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">3–5 msgs</span><span>5 &nbsp;19%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:19%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">6–10 msgs</span><span>3 &nbsp;11%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:11%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">11–20 msgs</span><span>5 &nbsp;19%</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:19%"></div></div>
      </div>
      <div class="bar-row">
        <div class="bar-meta"><span class="bar-label">21+ msgs</span><span>7 &nbsp;26% &nbsp;4 de 7 são suporte</span></div>
        <div class="bar-track"><div class="bar-fill" style="width:26%"></div></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Qualitativo — Dias 1–2</h2>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Qualificação e conexão genuína</p>
      <p class="qual-body">Sessão ...8067 (64 msgs, 36 min): lead chegou via conteúdo de "38 dias de Tarot". Sofia qualificou sem empurrar produto, identificou contexto familiar, enviou link na msg 5. Quando descobriu que a lead já havia comprado, fez post-purchase nurturing: trabalhou medo de "ver espíritos", recomendou baralho RWS, sugeriu exercício diário. Lead de Londres, 3h30 da manhã — saiu satisfeita.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Identificação de aluna TPOC</p>
      <p class="qual-body">Sessão ...3765: lead informou ser TPOC. Sofia identificou acesso gratuito imediatamente.</p>
      <div class="evidence">"Como você já é aluna do TPOC, você tem acesso gratuito ao WTP"</div>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label ok">OK</span>
    <div>
      <p class="qual-title">Contenção de objeção de horário</p>
      <p class="qual-body">Sessão ...4877: lead queria cancelar por conflito com pós-grad.</p>
      <div class="evidence">"Você não precisa assistir tudo perfeito. Mesmo parcial já traz insights. E se não fizer sentido, tem 7 dias de garantia."</div>
      <p class="qual-body" style="margin-top:6px">A lead se reinscreveu.</p>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label problema">Problema</span>
    <div>
      <p class="qual-title">CRÍTICO — encaminharAtendimento nunca chamada ✅ Resolvido</p>
      <p class="qual-body">77 mensagens com "vou encaminhar pra equipe" e 0 chamadas reais à ferramenta. Todas as promessas de atendimento foram falsas.</p>
      <div class="evidence">
        Lead ...2040 (20h de espera):<br>
        Sofia (msg 224): "Vou te encaminhar agora pra equipe, tá?"<br>
        Lead (8 retornos): "Ainda não", "Não", "NÃO", "oio"...<br>
        Sofia (msg 288): "Já escalei seu caso como prioridade máxima agora com a equipe."<br>
        <em>Equipe nunca aparece.</em>
      </div>
    </div>
  </div>

  <div class="qual-item">
    <span class="qual-label atencao">Atenção</span>
    <div>
      <p class="qual-title">Sofia respondeu auto-reply de corretora de imóveis</p>
      <p class="qual-body">Sessão ...2426: chegou lista numerada 1️⃣2️⃣3️⃣ com assinatura "Carla, corretora". Sofia respondeu como se fosse lead legítima. Não é erro grave, mas indica ausência de filtro pré-agente.</p>
    </div>
  </div>
</section>

<section class="section">
  <h2 class="section-label">Recomendações — Dias 1–2</h2>

  <div class="rec-item resolved">
    <span class="rec-label pendente">Urgente</span>
    <div>
      <p class="rec-title">Bug de escalonamento — encaminharAtendimento ✅ Resolvido</p>
      <p class="rec-body">Corrigido durante o lançamento. Sofia agora redireciona para suporte@fernandabeppler.com.br em vez de prometer escalonamento via WhatsApp.</p>
    </div>
  </div>

  <div class="rec-item">
    <span class="rec-label pendente">Pendente</span>
    <div>
      <p class="rec-title">Verificar sessão ...2040 (cancelamento)</p>
      <p class="rec-body">Lead pediu cancelamento, ficou 20h em loop. Verificar se houve chargeback ou disputa.</p>
    </div>
  </div>

  <div class="rec-item resolved">
    <span class="rec-label medio">Médio</span>
    <div>
      <p class="rec-title">Eliminar "Perfeito" ✅ Resolvido em 29/abr</p>
      <p class="rec-body">Instrução adicionada ao prompt. Validado em testes.</p>
    </div>
  </div>

  <div class="rec-item">
    <span class="rec-label baixo">Baixo</span>
    <div>
      <p class="rec-title">Filtro pré-agente no n8n</p>
      <p class="rec-body">Detectar e descartar auto-replies de bots antes de chegar na Sofia.</p>
    </div>
  </div>
</section>

<div class="conclusion">
  Volume sólido para a primeira janela: 27 sessões em 36h, 100% respondidas. A falha estrutural identificada no dia 1 foi o escalonamento — toda promessa de atendimento era falsa. <strong>O bug foi corrigido durante o lançamento. Onde o fluxo era de venda pura, a Sofia performou muito bem.</strong>
</div>
```

- [ ] **Step 2: Verificar tab dia1-2 carrega**

Clicar em "Dias 1–2" e confirmar que o conteúdo troca corretamente.

- [ ] **Step 3: Commit**

```bash
git add analyses/dia1-2.html
git commit -m "feat: add dia1-2 analysis fragment"
```

---

## Task 8: Deploy para GitHub Pages

**Files:** nenhum novo

- [ ] **Step 1: Confirmar todos os arquivos estão commitados**

```bash
git status
```

Expected: `nothing to commit, working tree clean`

- [ ] **Step 2: Push para main**

```bash
git push origin main
```

- [ ] **Step 3: Habilitar GitHub Pages**

```bash
gh api repos/deoliveiratech/beppler-lancamento-maio \
  --method PATCH \
  --field has_pages=true \
  -f "source[branch]=main" \
  -f "source[path]=/"
```

Se o comando acima falhar (API v3 de pages precisa ser feita depois do primeiro push), usar:

```bash
gh repo view deoliveiratech/beppler-lancamento-maio --web
```

E habilitar manualmente em Settings → Pages → Source: `main` / `/(root)`.

- [ ] **Step 4: Aguardar deploy e verificar URL**

GitHub Pages leva ~1 min para publicar. A URL será:
`https://deoliveiratech.github.io/beppler-lancamento-maio/`

```bash
sleep 60 && curl -s -o /dev/null -w "%{http_code}" \
  https://deoliveiratech.github.io/beppler-lancamento-maio/
```

Expected: `200`

- [ ] **Step 5: Verificar os 3 tabs no browser**

```bash
open https://deoliveiratech.github.io/beppler-lancamento-maio/
```

Checar:
- Tab "Dias 5–10" ativo por default
- Navegação entre tabs sem reload
- Hash na URL atualiza ao trocar tab (ex: `#dia1-2`)
- Footer mostra "deOliveiraTech" (sem Dalton Lab)
- Design editorial consistente com os prints aprovados

- [ ] **Step 6: Commit final**

```bash
git tag v1.0.0
git push origin v1.0.0
```

---

## Self-Review

**Cobertura do spec:**
- ✅ Repo `deoliveiratech/beppler-lancamento-maio`
- ✅ `index.html` shell com header, tabs, footer
- ✅ `style.css` separado
- ✅ `app.js` separado com fetch + cache + hash routing
- ✅ `analyses/*.html` fragmentos com tab-meta JSON
- ✅ Branding deOliveiraTech (zero Dalton Lab)
- ✅ Tab mais recente ativo por default
- ✅ GitHub Pages

**Sem placeholders:** confirmado — todo código é completo e executável.

**Consistência de tipos:** `tab-meta` lido via `document.getElementById('tab-meta')` após inject, consistente entre tasks 4 e 5–7. `TABS[].id` usado como `dataset.tab` e no hash, consistente em tasks 4 e 8.
