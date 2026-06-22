const TABS = [
  { id: 'dia1-2',   label: 'Dias 1–2',   file: 'analyses/dia1-2.html'   },
  { id: 'dia1-4',   label: 'Dias 1–4',   file: 'analyses/dia1-4.html'   },
  { id: 'dia5-10',  label: 'Dias 5–10',  file: 'analyses/dia5-10.html'  },
  { id: 'dia11-15', label: 'Dias 11–15', file: 'analyses/dia11-15.html' },
];

const DEFAULT_TAB = 'dia11-15';

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
