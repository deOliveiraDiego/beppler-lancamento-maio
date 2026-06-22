# Beppler — Agentes & Lançamentos

Acervo de trabalho dos agentes de IA da **Fernanda Beppler** (cliente de Oliveiras Tech).
O **agente vivo roda no n8n** — este repo é a fonte de verdade dos prompts, tools e
materiais de cada lançamento, organizados pra reaproveitar info de um lançamento pro outro.

> Nota: a pasta ainda se chama `lancamento-maio` por histórico; o escopo já é multi-lançamento.

## Organização

Tudo é organizado **por lançamento**, em `lancamentos/<mês-ano>/`. Cada lançamento é
auto-contido:

```
lancamentos/<lançamento>/
├── briefing/      → briefing original do cliente (fonte de verdade da oferta/datas)
├── agente-tpoc/   → prompt.md, links.js, bonus.js + versões -teste, bases, tooling
├── agente-wtp/    → (quando houver) agente de suporte/pós-venda
├── analytics/     → dashboard de performance (HTML/JS)
└── analises/      → relatórios e handoffs do lançamento
```

## Lançamentos

| Lançamento | Status | Funil | Carrinho |
|---|---|---|---|
| [maio-2026](lancamentos/maio-2026/) | ✅ encerrado | Evento WTP → TPOC | 23–28/05/2026 |
| [agosto-2026](lancamentos/agosto-2026/) | 🟡 em preparação | Série gratuita Beabá do Tarot → TPOC | 12–20/08/2026 |

## Como um novo lançamento começa

1. `cp -r` do `agente-tpoc/` do lançamento anterior pro novo (ponto de partida).
2. **Não** copiar os arquivos PII de aluna (`alunas-wtp-*.js`) se o novo lançamento não tiver WTP.
3. Editar `prompt.md` / `links.js` / `bonus.js` conforme o novo briefing.
4. Detalhes de mecânica e do mapeamento arquivo → node n8n: ver `agente-tpoc/CLAUDE.md`.

Convenções gerais do repo: ver [`CLAUDE.md`](CLAUDE.md).
