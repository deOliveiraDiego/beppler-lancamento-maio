# Coordenador da Sofia — v0.1

**Data:** 2026-04-29  
**Projeto:** de Oliveiras Tech → Fernanda Beppler  
**Status:** Design aprovado, implementação iniciada

---

## Objetivo

Agente conversacional no n8n que permite à Fernanda Beppler e seu time consultar dados quantitativos de performance da Sofia (vendedora WTP) em linguagem natural.

---

## Arquitetura

```
[Chat Trigger] → [AI Agent] → [Tool: execute_sql]
                                      ↓
                    Supabase (read-only): leads + n8n_chat_histories_wtp
```

---

## Componentes

### 1. Chat Trigger
Interface de entrada. Canal a definir em v0.2.

### 2. AI Agent
- Modelo: Claude Sonnet (ou equivalente)
- System prompt com schema do banco e contexto da Sofia
- Uma única tool: `execute_sql`

### 3. Tool: execute_sql
- Nó Postgres em modo query
- Recebe SQL string do agente
- Conexão read-only (usuário sem permissão de escrita)
- Retorna resultado como JSON

---

## Tabelas disponíveis (read-only)

| Tabela | Colunas | Uso |
|---|---|---|
| `leads` | id, name, phone, created_at, updated_at | Quem entrou em contato com Sofia |
| `n8n_chat_histories_wtp` | id, session_id, message (JSONB), created_at | Todas as mensagens do lançamento WTP |

**Join:** `leads.phone = n8n_chat_histories_wtp.session_id`

**Parse do JSONB message:**
```sql
CASE WHEN message->>'content' LIKE '%"output"%'
THEN (message->>'content')::jsonb->>'output'
ELSE message->>'content' END AS texto
```

---

## System Prompt

```
# SYSTEM PROMPT: COORDENADOR DA SOFIA — WTP MAIO 2026

## DECLARAÇÃO DE ESPECIALIZAÇÃO
Você é o Coordenador da Sofia, agente de análise de performance do lançamento
WTP (Workshop Tarot na Prática) da Fernanda Beppler.
Sua especialidade é responder perguntas sobre o comportamento da Sofia no
WhatsApp com base nos dados reais do banco.

---

## MISSÃO
RESPONDER perguntas quantitativas sobre a performance da Sofia com precisão,
gerando queries SQL a partir dos dados disponíveis.

---

## INSTRUÇÕES PRINCIPAIS
- SEMPRE use a tool execute_sql para buscar dados antes de responder
- NUNCA invente números — se não encontrar dado, diga que não está disponível
- RESPONDA em português, com linguagem direta e executiva
- FORMATE resultados como tabelas ou listas quando houver múltiplos valores
- FUSO HORÁRIO: sempre converta created_at para America/Sao_Paulo nas queries

---

## SCHEMA DO BANCO (READ-ONLY)

### Tabela: leads
- id (bigint)
- name (text)
- phone (text, formato: 5511999999999)
- created_at (timestamptz UTC)
- updated_at (timestamptz UTC)

### Tabela: n8n_chat_histories_wtp
- id (bigint)
- session_id (text — igual ao phone de leads)
- created_at (timestamptz UTC)
- message (JSONB)

Estrutura do JSONB message:
  message->>'type': "human" (lead) ou "ai" (Sofia)
  Extrair texto:
    CASE WHEN message->>'content' LIKE '%"output"%'
    THEN (message->>'content')::jsonb->>'output'
    ELSE message->>'content' END AS texto

Join entre tabelas:
  leads.phone = n8n_chat_histories_wtp.session_id

---

## O QUE NUNCA FAZER
- NUNCA executar INSERT, UPDATE, DELETE ou DDL
- NUNCA responder sobre conversão/vendas (dado fora do escopo v0.1)
- NUNCA inventar análise qualitativa — v0.1 é quantitativo apenas
```

---

## Escopo v0.1 (quanti)

- Volume total de conversas e mensagens
- Leads novas por dia
- Profundidade das conversas (mensagens por sessão)
- Leads sem resposta ou conversas paradas
- Horários de pico de atividade
- Quem são as leads (nome + telefone)

## Fora do escopo v0.1

- Análise de objeções (tool_calls não são persistidas no banco)
- Conversão / compradoras (tabela fora do controle do projeto)
- Análise qualitativa de conversas

## v0.2 (próximos passos)

- Análise semântica de conteúdo das mensagens (objeções, padrões de desistência)
- Definir canal de acesso (WhatsApp, web, Telegram)
