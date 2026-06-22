# Handoff: Análise de Performance Sofia — WTP Lançamento Maio 2026

**Data:** 29/04/2026
**Status:** Em andamento — lançamento ativo até 22/05/2026 às 14h

---

## 1. Objetivo

Monitorar e analisar a performance da agente Sofia no WhatsApp durante o lançamento do WTP, gerando relatórios quali/quant periódicos a partir dos dados brutos no Supabase. O objetivo é identificar falhas, padrões de objeção e oportunidades de melhoria no prompt/workflow enquanto o lançamento ainda está ativo.

---

## 2. Contexto essencial

### Infraestrutura
- **Agente:** Sofia — vendedora do WTP via WhatsApp
- **Stack:** n8n em produção (não o ADK Python — esse é dev/testes)
- **DB:** Supabase (Postgres) em `aws-0-sa-east-1.pooler.supabase.com:5432`
- **Credencial:** `DATABASE_URL` em `/Users/deoliveiradiego/Projects/deoliveiratech/beppler/.env`
- **Tabela principal:** `n8n_chat_histories_wtp`
- **Schema:**
  ```
  id          integer (PK)
  session_id  varchar(255)  → número de telefone
  message     jsonb         → {type: "human"|"ai", content: string, tool_calls: [...]}
  created_at  timestamptz   → UTC
  ```
- **Parsing do `content`:**
  ```sql
  CASE WHEN message->>'content' LIKE '%"output"%'
  THEN (message->>'content')::jsonb->>'output'
  ELSE message->>'content' END AS texto
  ```

### Importante: tool_calls no banco
O campo `tool_calls` nas mensagens AI está **sempre vazio `[]`**. Isso é esperado — o n8n armazena apenas as mensagens finais de conversa, não os passos internos do agente. **Não é possível verificar chamadas de ferramenta (ex: `encaminharAtendimento`) por essa tabela.** Para isso, seria necessário acessar os logs de execução do n8n.

### Fix de escalonamento
O bug anterior ("Sofia dizia 'já encaminhei pra equipe' sem acionar ferramenta") foi corrigido via mudança de comportamento textual: Sofia agora redireciona para `suporte@fernandabeppler.com.br` em vez de prometer escalonamento via WhatsApp. Quando a equipe é acionada pela ferramenta (e funciona), a conversa simplesmente para — isso é comportamento esperado, não sinal de falha.

### Lotes do WTP
| Lote | Período | Preço |
|---|---|---|
| Zero | 01/04–21/04 | R$37 |
| 1 | 22/04–27/04 | R$47 |
| 2 | 28/04–04/05 | R$57 |
| 3 | 05/05–11/05 | R$67 |
| 4 | 12/05–18/05 | R$77 |
| Último | 19/05–22/05 14h | R$79 |

### Fontes dos docs (PRODUÇÃO = pasta `wtp/`)
| Arquivo | Caminho |
|---|---|
| Prompt | `lancamento-maio/wtp/prompt.md` |
| Base de conhecimento | `lancamento-maio/wtp/base-de-conhecimento.md` |
| Base de objeções | `lancamento-maio/wtp/base-de-objecoes.md` |
| Links / lotes | `lancamento-maio/wtp/links.js` |
| Preview TPOC | `lancamento-maio/wtp/base-de-tpoc-preview.md` |

---

## 3. O que já foi feito

1. **`analise-sofia-wtp-lancamento-dia1-2.md`** — Dias 1–2 (20/abr–21/abr), 406 msgs, 27 sessões. *(análise inicial)*
2. **`analise-sofia-wtp-lancamento-dia1-4.md`** — Dias 1–4 (20/abr–23/abr 20:44 BRT), 922 msgs, 57 sessões. *(baseline atual)*
3. **`analise-sofia-wtp-lancamento-dia5-10.md`** — Dias 5–10 (23/abr 20:44 BRT → 29/abr 10:49 BRT), **44 sessões novas**, 229 respostas do bot. *(gerado nesta sessão)*

### O que ficou para trás nesta sessão
- Foi gerado um relatório incorreto `analise-sofia-wtp-lancamento-dia1-10.md` (acumulado desde o dia 1) — **já foi deletado**. O correto é sempre gerar o delta a partir do cutoff do último relatório.
- O relatório dia5-10 tinha conclusão errada sobre `encaminharAtendimento` (afirmava "0 chamadas" com base no chat log, mas o banco não persiste tool calls internos do n8n) — **já corrigido no relatório final**.

---

## 4. Estado atual

### Snapshot em 29/abr 10:49 BRT
- **Total acumulado:** 1.474 msgs · 101 sessões · 10 dias
- **Período novo (dia5-10):** 44 sessões novas
  - 10 com link (22,7%): Lote 1 = 6, Lote 2 = 4
  - Duração média de sessões 6–10 msgs: 65 min (era 560 min no baseline — fix funcionou)
  - Escalonamento: 100% das 47 indicações incluem e-mail de suporte
  - "Perfeito": 72/229 = 31,4% (piora leve vs. 30% do baseline — não corrigido no prompt)
  - Emojis fora da whitelist: 😊, 😂 detectados (não corrigido no prompt)

### Casos críticos
| Sessão | Situação | Status |
|---|---|---|
| `...3993` | Lead sem PIX/cartão, 7 dias de acompanhamento | ✅ **Comprou em 27/abr**, confirmou acesso 28/abr |
| `...2040` | Lead pedindo cancelamento desde 21/abr | ⚠️ Última atividade 21/abr 20:57, 181h silêncio — pendente |

### Lote atual
Lote 2 ativo (28/abr–04/mai, R$57). Primeiros 2 dias: 4 sessões com link. Sem objeções de preço relevantes ainda.

---

## 5. Próximos passos

1. **Verificar caso `5521994928040`** — Lead que pediu cancelamento em 21/abr, nunca atendida. Checar se houve chargeback ou disputa.

2. **Corrigir "Perfeito" no prompt** — Adicionar ao `wtp/prompt.md`:
   > Nunca abra uma resposta com "Perfeito". Varie: "Entendi", "É isso", "Faz sentido", "Boa", "Certo", "Lindo isso".

3. **Reforçar whitelist de emojis no prompt** — Adicionar ao `wtp/prompt.md`:
   > Apenas estes emojis são permitidos: ✨ 🔮 🌙 🃏 💫. Nenhum outro.

4. **Gerar próximo relatório delta** quando acumular ~5–7 dias novos (por volta de 04/mai–06/mai). Usar o cutoff `2026-04-29 13:49:32+00` (UTC) como início.

5. **Monitorar objeções de preço no Lote 2 e Lote 3** — Adicionar à query de frases-chave:
   ```sql
   COUNT(*) FILTER (WHERE texto ILIKE '%caro%' OR texto ILIKE '%tá pesado%'
     OR texto ILIKE '%não tenho%' OR texto ILIKE '%parcelar%') AS objec_preco
   ```

6. **Checar padrão quinta/sexta** — 24/abr e 25/abr tiveram apenas 4 sessões cada. Verificar se havia push de conteúdo nesses dias ou se é padrão esperado.

---

## 6. Perguntas em aberto

1. `5521994928040` — Houve chargeback ou disputa após 21/abr?
2. O "Perfeito" foi ou vai ser corrigido no prompt?
3. Os emojis (😊, 😂) foram ou vão ser corrigidos?
4. Quinta/sexta (24–25/abr) sem push de conteúdo — é padrão esperado do calendário?
5. A partir do Lote 3 (R$67), objeções de preço devem aparecer — há intenção de adicionar argumentação de preço no prompt?

---

## 7. Artefatos relevantes

### Conexão ao banco
```bash
export PGPASSWORD='ZIINeHVRShgINDua'
DB="postgresql://postgres.ziljerhxhhudzufqsktp:ZIINeHVRShgINDua@aws-0-sa-east-1.pooler.supabase.com:5432/postgres"
psql "$DB"
```

### Cutoff para o próximo relatório
```
2026-04-29 13:49:32+00   (UTC)
= 29/abr 10:49 BRT
```

### Bloco de queries para o próximo relatório (substituir `$CUTOFF` pelo valor acima)

```sql
-- 1. Volume geral das sessões novas
WITH new_sessions AS (
  SELECT session_id FROM n8n_chat_histories_wtp
  GROUP BY session_id HAVING MIN(created_at) > '$CUTOFF'
)
SELECT COUNT(*) AS sessoes_novas,
  (SELECT COUNT(*) FROM n8n_chat_histories_wtp h JOIN new_sessions ns ON h.session_id=ns.session_id) AS total_msgs
FROM new_sessions;

-- 2. Sessões novas por dia
WITH first_msg AS (
  SELECT session_id, MIN(created_at) AS inicio FROM n8n_chat_histories_wtp GROUP BY session_id
)
SELECT DATE(inicio AT TIME ZONE 'America/Sao_Paulo') AS dia, COUNT(*) AS sessoes_novas
FROM first_msg WHERE inicio > '$CUTOFF' GROUP BY dia ORDER BY dia;

-- 3. Histograma de profundidade (sessões novas)
WITH new_sessions AS (
  SELECT session_id FROM n8n_chat_histories_wtp
  GROUP BY session_id HAVING MIN(created_at) > '$CUTOFF'
),
sess AS (
  SELECT h.session_id, COUNT(*) AS total,
    EXTRACT(EPOCH FROM (MAX(h.created_at)-MIN(h.created_at)))/60 AS duracao_min
  FROM n8n_chat_histories_wtp h JOIN new_sessions ns ON h.session_id=ns.session_id
  GROUP BY h.session_id
)
SELECT
  CASE WHEN total<=2 THEN '1-2' WHEN total<=5 THEN '3-5'
       WHEN total<=10 THEN '6-10' WHEN total<=20 THEN '11-20' ELSE '21+' END AS bucket,
  COUNT(*) AS sessoes,
  ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),0) AS pct,
  ROUND(AVG(duracao_min),0) AS duracao_media_min
FROM sess GROUP BY bucket
ORDER BY ARRAY_POSITION(ARRAY['1-2','3-5','6-10','11-20','21+'],
  CASE WHEN total<=2 THEN '1-2' WHEN total<=5 THEN '3-5'
       WHEN total<=10 THEN '6-10' WHEN total<=20 THEN '11-20' ELSE '21+' END);

-- 4. Funil e frases-chave (sessões novas)
WITH new_sessions AS (
  SELECT session_id FROM n8n_chat_histories_wtp
  GROUP BY session_id HAVING MIN(created_at) > '$CUTOFF'
),
ai_texts AS (
  SELECT h.session_id,
    CASE WHEN h.message->>'content' LIKE '%"output"%'
    THEN (h.message->>'content')::jsonb->>'output'
    ELSE h.message->>'content' END AS texto
  FROM n8n_chat_histories_wtp h JOIN new_sessions ns ON h.session_id=ns.session_id
  WHERE h.message->>'type'='ai'
)
SELECT
  (SELECT COUNT(*) FROM new_sessions) AS sessoes_novas,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-1wtp%' THEN session_id END)     AS lote_1,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-2wtp%' THEN session_id END)     AS lote_2,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-3wtp%' THEN session_id END)     AS lote_3,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%lote-4wtp%' THEN session_id END)     AS lote_4,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%ultimolotewtp%' THEN session_id END) AS lote_ultimo,
  COUNT(DISTINCT CASE WHEN texto ILIKE '%clkdmg.site/pay%' THEN session_id END) AS total_com_link,
  COUNT(*) AS total_respostas_bot,
  COUNT(*) FILTER (WHERE texto ILIKE '%Perfeito%')   AS usando_perfeito,
  COUNT(*) FILTER (WHERE texto ILIKE '%equipe%')     AS menciona_equipe,
  COUNT(*) FILTER (WHERE texto ILIKE '%suporte@fernandabeppler%') AS redirect_email,
  COUNT(*) FILTER (WHERE texto ILIKE '%cancelar%' OR texto ILIKE '%cancelamento%') AS cancelamento,
  COUNT(*) FILTER (WHERE texto ILIKE '%TPOC%')       AS menciona_tpoc,
  COUNT(*) FILTER (WHERE texto ILIKE '%caro%' OR texto ILIKE '%tá pesado%'
    OR texto ILIKE '%não tenho%' OR texto ILIKE '%parcelar%') AS objec_preco
FROM ai_texts;

-- 5. Visão de todas as sessões novas
WITH new_sessions AS (
  SELECT session_id FROM n8n_chat_histories_wtp
  GROUP BY session_id HAVING MIN(created_at) > '$CUTOFF'
),
sess_stats AS (
  SELECT h.session_id, COUNT(*) AS total_msgs,
    EXTRACT(EPOCH FROM (MAX(h.created_at)-MIN(h.created_at)))/60 AS duracao_min,
    MAX(h.created_at AT TIME ZONE 'America/Sao_Paulo') AS ultima_ts
  FROM n8n_chat_histories_wtp h JOIN new_sessions ns ON h.session_id=ns.session_id
  GROUP BY h.session_id
),
last_msg AS (
  SELECT DISTINCT ON (h.session_id) h.session_id,
    h.message->>'type' AS last_role,
    CASE WHEN h.message->>'content' LIKE '%"output"%'
    THEN (h.message->>'content')::jsonb->>'output'
    ELSE h.message->>'content' END AS last_text
  FROM n8n_chat_histories_wtp h JOIN new_sessions ns ON h.session_id=ns.session_id
  ORDER BY h.session_id, h.created_at DESC
),
link_sessions AS (
  SELECT DISTINCT h.session_id FROM n8n_chat_histories_wtp h
  JOIN new_sessions ns ON h.session_id=ns.session_id
  WHERE h.message->>'type'='ai'
    AND (CASE WHEN h.message->>'content' LIKE '%"output"%'
         THEN (h.message->>'content')::jsonb->>'output'
         ELSE h.message->>'content' END) ILIKE '%clkdmg.site/pay%'
),
escalou AS (
  SELECT DISTINCT h.session_id FROM n8n_chat_histories_wtp h
  JOIN new_sessions ns ON h.session_id=ns.session_id
  WHERE h.message->>'type'='ai'
    AND (CASE WHEN h.message->>'content' LIKE '%"output"%'
         THEN (h.message->>'content')::jsonb->>'output'
         ELSE h.message->>'content' END) ILIKE '%suporte@fernandabeppler%'
)
SELECT s.session_id, s.total_msgs,
  ROUND(s.duracao_min) AS dur_min,
  ROUND(EXTRACT(EPOCH FROM (NOW() AT TIME ZONE 'America/Sao_Paulo' - s.ultima_ts))/3600, 1) AS h_silencio,
  CASE WHEN ls.session_id IS NOT NULL THEN 'sim' ELSE 'não' END AS link,
  CASE WHEN es.session_id IS NOT NULL THEN 'sim' ELSE 'não' END AS escalou_email,
  LEFT(l.last_text, 90) AS ultima_msg
FROM sess_stats s
JOIN last_msg l ON l.session_id=s.session_id
LEFT JOIN link_sessions ls ON ls.session_id=s.session_id
LEFT JOIN escalou es ON es.session_id=s.session_id
ORDER BY s.total_msgs DESC;

-- 6. Ler uma sessão específica completa
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

### Relatórios existentes
```
lancamento-maio/analise-sofia-wtp-lancamento-dia1-2.md   (baseline inicial)
lancamento-maio/analise-sofia-wtp-lancamento-dia1-4.md   (baseline principal)
lancamento-maio/analise-sofia-wtp-lancamento-dia5-10.md  (gerado nesta sessão — mais recente)
lancamento-maio/handoff-analise-sofia.md                 (handoff da sessão anterior)
lancamento-maio/handoff-analise-sofia-dia5-10.md         (este arquivo)
```

---

## 8. Instruções para a próxima sessão

- **Tom:** direto e analítico. Sem explicações básicas — o usuário conhece bem o projeto.
- **Escopo do relatório:** sempre delta a partir do cutoff do último relatório. Nunca acumular do dia 1. Usar o cutoff `2026-04-29 13:49:32+00` como início do próximo relatório.
- **Nomenclatura:** `analise-sofia-wtp-lancamento-diaX-Y.md` onde X e Y são os dias do lançamento (dia 1 = 20/abr). Próximo será dia 11 em diante.
- **Sequência recomendada:** rodar todas as queries de uma vez, ler as sessões-chave (top 3 por volume, sessões 11+ msgs sem link, sessões com h_silencio > 48h), escrever o relatório.
- **Sessões-chave a ler:** top 3 por `total_msgs`, sessões com `link=não` e `total_msgs > 10`, sessões com `h_silencio > 48` e `last_role = human` (bot sumiu — falha operacional).
- **Mascarar session_ids:** mostrar apenas últimos 4 dígitos (ex: `...3993`) no relatório final.
- **Banco é read-only** para análise — nunca rodar INSERT/UPDATE/DELETE.
- **Armadilha:** não afirmar que `encaminharAtendimento` "nunca foi chamada" com base no chat log — o banco não persiste tool calls internos do n8n. Usar evidência comportamental (equipe aparece ou não nas conversas, durações das sessões).
- **Foco no delta:** o que mudou em relação ao relatório anterior. Não repetir achados já documentados. Comparar taxas com o baseline quando relevante.
