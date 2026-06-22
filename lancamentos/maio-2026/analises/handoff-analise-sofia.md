# Handoff: Análise de Performance da Sofia — WTP Lançamento Maio 2026

**Data:** 23/04/2026
**Status:** Em andamento — lançamento ativo até 22/05/2026 às 14h

---

## 1. Objetivo

Monitorar e analisar a performance da agente Sofia no canal WhatsApp durante o lançamento do WTP (Workshop Tarot na Prática), gerando relatórios quali/quant periódicos a partir dos dados brutos no Supabase. O objetivo é identificar falhas, padrões de objeção e oportunidades de melhoria no prompt/workflow enquanto o lançamento ainda está ativo.

---

## 2. Contexto essencial

### Infraestrutura
- **Agente:** Sofia — vendedora do WTP via WhatsApp
- **Stack em produção:** n8n (não o ADK Python — esse é ambiente de dev/testes)
- **DB:** Supabase (Postgres) em `aws-0-sa-east-1.pooler.supabase.com:5432`
- **Credencial:** `DATABASE_URL` em `/Users/deoliveiradiego/Projects/deoliveiratech/beppler/.env`
- **Tabela:** `n8n_chat_histories_wtp`
- **Schema da tabela:**
  ```
  id          integer (PK)
  session_id  varchar(255)  → MSISDN do WhatsApp (número de telefone)
  message     jsonb         → {type: "human"|"ai", content: string, tool_calls: [...]}
  created_at  timestamptz   → UTC
  ```
- **Parsing do `content`:** Respostas da IA às vezes têm `content` como JSON string com chave `output`. Sempre usar:
  ```sql
  CASE WHEN message->>'content' LIKE '%"output"%'
  THEN (message->>'content')::jsonb->>'output'
  ELSE message->>'content' END AS texto
  ```

### Fontes dos docs do agente (PRODUÇÃO = pasta `wtp/`)
| Arquivo | Caminho | Uso |
|---|---|---|
| Prompt | `lancamento-maio/wtp/prompt.md` | Instruções completas da Sofia |
| Base de conhecimento | `lancamento-maio/wtp/base-de-conhecimento.md` | `get_conhecimento` |
| Base de objeções | `lancamento-maio/wtp/base-de-objecoes.md` | `get_objecoes` |
| Links / lotes | `lancamento-maio/wtp/links.js` | `get_links` (Code node n8n) |
| Preview TPOC | `lancamento-maio/wtp/base-de-tpoc-preview.md` | `get_tpoc_preview` |

> ⚠️ Não usar `beppler-adk/sofia/tools.py` como referência de produção — é ambiente de dev. O `links.js` é a fonte correta.

### Lotes do WTP
| Lote | Período | Preço | Bônus |
|---|---|---|---|
| Zero | 01/04–21/04 | R$37 / 3x R$12,95 | E-book "50 Mitos sobre Tarot" |
| 1 | 22/04–27/04 | R$47 / 4x R$12,53 | null |
| 2 | 28/04–04/05 | R$57 / 5x R$12,35 | null |
| 3 | 05/05–11/05 | R$67 / 6x R$12,29 | null |
| 4 | 12/05–18/05 | R$77 / 8x R$10,91 | null |
| Último | 19/05–22/05 14h | R$79 / 12x R$7,90 | null |

---

## 3. O que já foi feito

### Relatórios gerados
1. **`analise-sofia-wtp-lancamento-dia1-2.md`** — Dias 1-2 (20/abr–21/abr), 406 msgs, 27 sessões. *(Análise inicial, substituída pela versão completa abaixo.)*
2. **`analise-sofia-wtp-lancamento-dia1-4.md`** — Dias 1-4 (20/abr–23/abr), 922 msgs, 57 sessões. *(Versão mais atual — usar essa como baseline.)*

Ambos em `/Users/deoliveiradiego/Projects/deoliveiratech/beppler/lancamento-maio/`.

### Bug identificado e resolvido
- **`encaminharAtendimento` nunca era chamada:** Em 159 mensagens Sofia dizia "vou encaminhar" sem chamar a ferramenta. Corrigido durante o lançamento (23/04 ou antes). Os relatórios já refletem esse fato como histórico.

### Casos críticos documentados (no relatório dia 1-4)
- `554388423993` — lead que queria comprar sem PIX/cartão, esperou 34h, ainda com interesse no final. *(Verificar resolução.)*
- `5521994928040` — lead que pediu cancelamento, tentou por 20h, desistiu. *(Verificar chargeback.)*

---

## 4. Estado atual

- Lançamento ativo, Lote 1 vigente (22/04–27/04, R$47)
- Bug de escalonamento resolvido
- Relatório de dias 1-4 é o baseline atual
- Próxima análise deverá cobrir do dia 20/04 até a data de execução (acumulado completo do lançamento)

---

## 5. Como fazer a próxima análise (passo a passo)

### Conexão ao banco
```bash
export PGPASSWORD='ZIINeHVRShgINDua'
DB="postgresql://postgres.ziljerhxhhudzufqsktp:ZIINeHVRShgINDua@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"
psql "$DB"
```

### Bloco de queries — rodar tudo junto

**1. Volume geral**
```sql
SELECT
  COUNT(*) AS total_msgs,
  COUNT(DISTINCT session_id) AS sessoes,
  SUM(CASE WHEN message->>'type'='human' THEN 1 ELSE 0 END) AS msgs_human,
  SUM(CASE WHEN message->>'type'='ai' THEN 1 ELSE 0 END) AS msgs_ai,
  ROUND(COUNT(*)::numeric / COUNT(DISTINCT session_id), 1) AS media_msg_sessao,
  MIN(created_at AT TIME ZONE 'America/Sao_Paulo') AS primeira,
  MAX(created_at AT TIME ZONE 'America/Sao_Paulo') AS ultima
FROM n8n_chat_histories_wtp;
```

**2. Sessões novas por dia**
```sql
WITH first_msg AS (
  SELECT session_id, MIN(created_at AT TIME ZONE 'America/Sao_Paulo') AS inicio
  FROM n8n_chat_histories_wtp GROUP BY session_id
)
SELECT DATE(inicio) AS dia, COUNT(*) AS sessoes_novas
FROM first_msg GROUP BY dia ORDER BY dia;
```

**3. Distribuição por hora (BRT)**
```sql
SELECT
  EXTRACT(HOUR FROM created_at AT TIME ZONE 'America/Sao_Paulo') AS hora_brt,
  COUNT(*) AS msgs
FROM n8n_chat_histories_wtp
GROUP BY hora_brt ORDER BY hora_brt;
```

**4. Histograma de profundidade**
```sql
WITH sess AS (
  SELECT session_id, COUNT(*) AS total,
    EXTRACT(EPOCH FROM (MAX(created_at)-MIN(created_at)))/60 AS duracao_min
  FROM n8n_chat_histories_wtp GROUP BY session_id
)
SELECT
  CASE WHEN total<=2 THEN '1-2' WHEN total<=5 THEN '3-5'
       WHEN total<=10 THEN '6-10' WHEN total<=20 THEN '11-20' ELSE '21+' END AS bucket,
  COUNT(*) AS sessoes,
  ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),0) AS pct,
  ROUND(AVG(duracao_min),0) AS duracao_media_min
FROM sess
GROUP BY bucket
ORDER BY ARRAY_POSITION(ARRAY['1-2','3-5','6-10','11-20','21+'],
  CASE WHEN total<=2 THEN '1-2' WHEN total<=5 THEN '3-5'
       WHEN total<=10 THEN '6-10' WHEN total<=20 THEN '11-20' ELSE '21+' END);
```

**5. Funil (links enviados por lote + escalonamentos)**
```sql
WITH ai_texts AS (
  SELECT session_id,
    CASE WHEN message->>'content' LIKE '%"output"%'
    THEN (message->>'content')::jsonb->>'output'
    ELSE message->>'content' END AS texto
  FROM n8n_chat_histories_wtp WHERE message->>'type'='ai'
)
SELECT
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-0-wtp%' THEN session_id END)   AS lote_zero,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-1wtp%' THEN session_id END)    AS lote_1,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-2wtp%' THEN session_id END)    AS lote_2,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-3wtp%' THEN session_id END)    AS lote_3,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-4wtp%' THEN session_id END)    AS lote_4,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%ultimolotewtp%' THEN session_id END) AS lote_ultimo,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%clkdmg.site/pay%' THEN session_id END) AS total_com_link,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%Vou te conectar com nossa equipe%' THEN session_id END) AS escalonamentos_reais
FROM ai_texts;
```

**6. Frases-chave nas respostas**
```sql
WITH ai_texts AS (
  SELECT session_id,
    CASE WHEN message->>'content' LIKE '%"output"%'
    THEN (message->>'content')::jsonb->>'output'
    ELSE message->>'content' END AS texto
  FROM n8n_chat_histories_wtp WHERE message->>'type'='ai'
)
SELECT
  COUNT(*)                                            AS total_respostas_bot,
  COUNT(*) FILTER (WHERE texto ILIKE '%Perfeito%')   AS usando_perfeito,
  COUNT(*) FILTER (WHERE texto ILIKE '%equipe%')     AS menciona_equipe,
  COUNT(*) FILTER (WHERE texto ILIKE '%encaminhar%') AS menciona_encaminhar,
  COUNT(*) FILTER (WHERE texto ILIKE '%cancelar%' OR texto ILIKE '%cancelamento%') AS cancelamento,
  COUNT(*) FILTER (WHERE texto ILIKE '%TPOC%')       AS menciona_tpoc,
  COUNT(*) FILTER (WHERE texto ILIKE '%acesso gratuito%') AS acesso_gratuito,
  COUNT(*) FILTER (WHERE texto ILIKE '%garantia%')   AS menciona_garantia,
  COUNT(*) FILTER (WHERE texto ILIKE '%e-book%' OR texto ILIKE '%50 Mitos%') AS menciona_ebook
FROM ai_texts;
```

**7. Visão de todas as sessões (drop-off, link, silêncio)**
```sql
WITH sess_stats AS (
  SELECT session_id, COUNT(*) AS total_msgs,
    EXTRACT(EPOCH FROM (MAX(created_at)-MIN(created_at)))/60 AS duracao_min,
    MAX(created_at AT TIME ZONE 'America/Sao_Paulo') AS ultima_ts
  FROM n8n_chat_histories_wtp GROUP BY session_id
),
last_msg AS (
  SELECT DISTINCT ON (session_id) session_id,
    message->>'type' AS last_role,
    CASE WHEN message->>'content' LIKE '%"output"%'
    THEN (message->>'content')::jsonb->>'output'
    ELSE message->>'content' END AS last_text
  FROM n8n_chat_histories_wtp ORDER BY session_id, created_at DESC
),
link_sessions AS (
  SELECT DISTINCT session_id FROM n8n_chat_histories_wtp
  WHERE message->>'type'='ai' AND (
    CASE WHEN message->>'content' LIKE '%"output"%'
    THEN (message->>'content')::jsonb->>'output'
    ELSE message->>'content' END
  ) ILIKE '%clkdmg.site/pay%'
),
equipe_sessions AS (
  SELECT DISTINCT session_id FROM n8n_chat_histories_wtp
  WHERE message->>'type'='ai' AND (
    CASE WHEN message->>'content' LIKE '%"output"%'
    THEN (message->>'content')::jsonb->>'output'
    ELSE message->>'content' END
  ) ILIKE '%equipe%'
)
SELECT
  s.session_id, s.total_msgs,
  ROUND(s.duracao_min) AS duracao_min,
  l.last_role,
  ROUND(EXTRACT(EPOCH FROM (NOW() AT TIME ZONE 'America/Sao_Paulo' - s.ultima_ts))/3600, 1) AS horas_silencio,
  CASE WHEN ls.session_id IS NOT NULL THEN 'sim' ELSE 'não' END AS recebeu_link,
  CASE WHEN es.session_id IS NOT NULL THEN 'sim' ELSE 'não' END AS mencionou_equipe,
  LEFT(l.last_text, 80) AS ultima_msg
FROM sess_stats s
JOIN last_msg l ON l.session_id = s.session_id
LEFT JOIN link_sessions ls ON ls.session_id = s.session_id
LEFT JOIN equipe_sessions es ON es.session_id = s.session_id
ORDER BY s.total_msgs DESC;
```

**8. Ler uma sessão específica completa**
```sql
SELECT id,
  message->>'type' AS role,
  CASE WHEN message->>'content' LIKE '%"output"%'
  THEN (message->>'content')::jsonb->>'output'
  ELSE message->>'content' END AS texto,
  to_char(created_at AT TIME ZONE 'America/Sao_Paulo', 'DD/MM HH24:MI') AS ts
FROM n8n_chat_histories_wtp
WHERE session_id = 'NUMERO_AQUI'
ORDER BY id;
```

---

## 6. O que NÃO foi atualizado / ainda falta

- **Análise de novas sessões pós-correção do bug de escalonamento** — o relatório atual cobre até 23/04, com o bug ainda ativo na maior parte do período. A próxima análise vai refletir o comportamento corrigido pela primeira vez.
- **Verificação dos dois casos críticos:** saber se `554388423993` foi atendida e comprou, e se `5521994928040` gerou chargeback.
- **Análise de lotes futuros:** Lote 1 (22/04–27/04) teve 9 sessões com link ao final do dia 23 — vale acompanhar conversão real.
- **Comparativo de performance antes/depois do fix do escalonamento** — dado mais valioso que virá com a próxima análise.
- **Objeções de preço** — não apareceram com destaque nos primeiros 4 dias (lote zero era R$37). Podem surgir com lotes maiores (Lote 2+, R$57+).

---

## 7. Como estruturar o próximo relatório

Usar o arquivo `analise-sofia-wtp-lancamento-dia1-4.md` como template — mesma estrutura de seções. Nomear o novo como:

```
analise-sofia-wtp-lancamento-diaX-Y.md
```

Onde X é o primeiro dia coberto (sempre 1 = 20/abr) e Y é o último dia da análise.

### O que comparar com o relatório anterior
- Volume (msgs, sessões, média/sessão) — tendência de crescimento
- Taxa de link por sessão — esperado aumentar com fix do escalonamento
- "equipe" e "encaminhar" nas respostas — esperado cair com fix
- "Perfeito" como abertura — verificar se foi corrigido no prompt
- Sessões novas por dia — ritmo do lançamento
- Lotes com link — quais lotes estão convertendo mais

### Sessões que valem ler integralmente (critérios)
1. Top 3 em volume de msgs (profundidade = engajamento ou loop)
2. Sessões com link enviado E menção à equipe (casos mistos: vendeu mas teve suporte)
3. Sessões com 11+ msgs E sem link (leads engajadas que não converteram — por quê?)
4. Sessões novas de apenas 1-2 msgs (fantasmas: auto-replies, números errados)
5. Qualquer sessão com horas_silencio > 24h E last_role = 'human' (lead mandou, bot sumiu — falha operacional)

---

## 8. Perguntas em aberto para a próxima sessão

1. O bug de escalonamento foi corrigido como? (prompt, workflow n8n, ou os dois?) — Isso muda o que monitorar.
2. `554388423993` — a lead finalmente comprou?
3. `5521994928040` — houve chargeback?
4. "Perfeito" como tique foi corrigido no prompt?
5. A partir do Lote 2 (R$57), surgirão objeções de preço — vale adicionar query para detectar palavras como "caro", "valor", "tá pesado", "não tenho".

---

## 9. Instruções para a próxima sessão

- **Tom:** direto e analítico. O usuário já conhece bem o projeto — não precisa de explicações básicas.
- **Sequência recomendada:** rodar todas as queries do bloco 5 de uma vez (paralelo), depois ler as sessões-chave, depois escrever o relatório.
- **Não recriar o que já existe:** ler o `analise-sofia-wtp-lancamento-dia1-4.md` antes de começar para não repetir achados já documentados. Focar no delta.
- **Salvar o novo relatório** em `/Users/deoliveiradiego/Projects/deoliveiratech/beppler/lancamento-maio/`.
- **Mascarar session_ids** no relatório final — mostrar apenas últimos 4 dígitos (ex.: `...3993`).
- O banco é read-only para análise — nunca rodar INSERT/UPDATE/DELETE.
