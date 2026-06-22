# CLAUDE.md — Repo Beppler (Agentes & Lançamentos)

## O que é este repo

Fonte de verdade dos agentes de IA da Fernanda Beppler. O **agente roda no n8n**;
aqui ficam os prompts/tools/materiais versionados, organizados **por lançamento**.

## Estrutura (por lançamento)

Trabalho fica em `lancamentos/<mês-ano>/`. Cada lançamento é auto-contido:

| Pasta | Conteúdo |
|---|---|
| `briefing/` | Briefing original do cliente (oferta, datas, bônus) — fonte de verdade |
| `agente-tpoc/` | Agente de vendas TPOC: `prompt.md`, `links.js`, `bonus.js`, versões `-teste`, bases, `make-teste.sh` |
| `agente-wtp/` | Agente de suporte/pós-venda WTP (quando o lançamento tiver WTP) |
| `analytics/` | Dashboard de performance (HTML/JS estático) |
| `analises/` | Relatórios e handoffs |

**Lançamento atual em preparação:** `lancamentos/agosto-2026/` (Beabá do Tarot → TPOC).
**Mecânica do agente TPOC** (mapeamento arquivo → node n8n, gotchas de perfil/boleto,
webhooks): ver `agente-tpoc/CLAUDE.md` dentro de cada lançamento.

## Regras

- **PII de alunas** (`alunas-wtp-*.js`): NUNCA versionar (gitignored via `**/alunas-wtp-*.js`).
  Ficam só local; colar conteúdo direto nos Code nodes do n8n.
- **Não renomear a pasta raiz** (`lancamento-maio`) — quebra paths/git. O escopo é multi-lançamento.
- Novo lançamento começa copiando o `agente-tpoc/` do anterior; não copiar PII se não houver WTP.
