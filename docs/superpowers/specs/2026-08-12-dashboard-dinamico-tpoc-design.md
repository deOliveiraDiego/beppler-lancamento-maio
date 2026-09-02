# Design — Dashboard Dinâmico Sofia TPOC (v1)

Data: 12/08/2026 · Status: aprovado em brainstorming

## Objetivo

Transformar o dashboard estático do dia atual em um **dashboard dinâmico** com:

- números **gerais** (acumulado do lançamento);
- números do **dia corrente**;
- **trend** por dia (mensagens/leads/objeções);
- quebra de **objeções**.

Público: **interno (Diego) + cliente (EAM)** — precisa de URL acessível, mas **sem PII** exposta.

## Decisões tomadas

1. **Camada de dados 100% automática** (SQL vivo), sem IA na v1.
2. **Sem insight do analista na v1** (adiado; a função deixa costura para adicionar depois).
3. **Acesso via Supabase + view/function** (opção 2), não via n8n.
4. **`fetch` cru no PostgREST** no browser, sem SDK.
5. **RLS desligado nas tabelas cruas** (já é o estado atual) — o browser nunca lê telefone/conteúdo, só agregados.
6. Trend deriva de `created_at` (`GROUP BY date`); **sem snapshot diário** — histórico só existe daqui pra frente (coluna criada em 12/08).

## Arquitetura

```
Supabase Postgres
  └─ função get_tpoc_metrics()  (SECURITY DEFINER, agrega tudo)
        ↑ GRANT EXECUTE apenas ao role `anon`
Browser (HTML/JS estático)
  └─ fetch POST https://<projeto>.supabase.co/rest/v1/rpc/get_tpoc_metrics
        com header apikey + Authorization: Bearer <anon>
        → renderiza cards + trend + objeções
```

Uma chamada só. A credencial que fica no cliente é a **chave anon** (pública por design), que só consegue `EXECUTE` na função — nunca `SELECT` nas tabelas.

## Camada de dados

### Função `get_tpoc_metrics()`

Retorna um JSON único (valores abaixo são ilustrativos — snapshot de 12/08):

```jsonc
{
  "totais":  { "leads": 433, "mensagens": 3342, "mensagens_ai": 1671, "mensagens_human": 1117, "tool_calls": 554, "erros_tool": 4, "dias": 1 },
  "hoje":    { "leads": 0, "mensagens": 0, "erros_tool": 0, "objeções": 0 },
  "trend":   [ { "dia": "2026-08-12", "mensagens": 3342, "leads": 433, "human": 1117 } ],
  "objeções": [
    { "categoria": "preço",   "geral": 54, "hoje": 0 },
    { "categoria": "boleto",  "geral": 47, "hoje": 0 },
    { "categoria": "wtp",     "geral": 30, "hoje": 0 },
    { "categoria": "adiar",   "geral": 23, "hoje": 0 },
    { "categoria": "parcela", "geral": 21, "hoje": 0 },
    { "categoria": "desconto","geral": 11, "hoje": 0 }
  ]
}
```

### Definições das métricas (tabela `n8n_chat_histories_tpoc_tests`)

- `leads` = `COUNT(DISTINCT session_id)`
- `mensagens` = `COUNT(*)`
- `mensagens_ai` / `mensagens_human` / `tool_calls` = contagem por `message->>'type'` (`ai` / `human` / `tool`)
- `erros_tool` = contagem `type='tool' AND message->>'content' ILIKE '%error%'`
- `dias` = dias corridos desde a abertura do carrinho (12/08), em America/Sao_Paulo
- **hoje** = mesmo critério, filtrando `created_at` no dia corrente em America/Sao_Paulo; `hoje.objeções` = soma das menções de todas as categorias hoje
- **trend** = `GROUP BY (created_at AT TIME ZONE 'America/Sao_Paulo')::date`
- **objeções** = classificação por regex sobre `type='human'`:
  - preço → `caro|preço|valor`
  - boleto → `boleto`
  - wtp → `wtp`
  - adiar → `próxima turma|esperar|depois|outra edição`
  - parcela → `parcelar|parcela`
  - desconto → `desconto|cupom|promoção`

### Segurança

- Função `SECURITY DEFINER` (owner `postgres`) — lê as tabelas com privilégio do owner.
- `GRANT EXECUTE ON FUNCTION get_tpoc_metrics() TO anon;`
- Tabelas cruas: **RLS off + sem GRANT para `anon`** (estado atual, manter).
- Único dado sensível no cliente = chave anon (pública) + URL do projeto (pegar no painel do Supabase).

## Front-end (estático, espelha o de maio)

- `index.html` + `app.js` + `style.css`, sem build.
- No load, `fetch` para o RPC:

```js
fetch('https://<projeto>.supabase.co/rest/v1/rpc/get_tpoc_metrics', {
  method: 'POST',
  headers: {
    'apikey': '<anon>',
    'Authorization': 'Bearer <anon>',
    'Content-Type': 'application/json'
  },
  body: '{}'
})
```

- Layout (aprovado no mockup): **Hoje → Geral → Trend → Objeções**.

| Bloco | Conteúdo |
|---|---|
| Hoje | leads hoje, mensagens hoje, erros hoje, objeções hoje |
| Geral | leads únicas, mensagens, erros de tool, dias de lançamento |
| Trend | barras/linha de mensagens (e leads) por dia |
| Objeções | barras horizontais por categoria (geral + hoje) |

- Exibir timestamp de "atualizado em".

## Hospedagem

- Dashboard vive em `lancamentos/agosto-2026/analytics/` (espelhando maio).
- Publicação: **GitHub Pages / Netlify / Vercel servindo só a pasta `analytics/`** (não o repo inteiro). Decisão final fica no plano de implementação.

## Fora de escopo (v1)

- Insight do analista (Camada 2) — adiado.
- Histórico por dia anterior a 12/08 (não há `created_at`).
- Autenticação por senha (chave anon é o único gate; agregados não são sensíveis).
- Métricas de conversão (pagamento confirmado) — o DB de chat não registra conversão; exigiria cruzar com outra fonte.

## Riscos / pré-requisitos

- Pegar a **URL do projeto** e a **chave anon** no painel do Supabase.
- Confirmar que `anon` tem `USAGE` no schema `public` (padrão do Supabase).
- A classificação de objeções é heurística (regex) — pode sub/sobre-contar; aceitável para v1.
