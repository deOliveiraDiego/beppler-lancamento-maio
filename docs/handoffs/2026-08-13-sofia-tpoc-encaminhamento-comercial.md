# Handoff — Sofia TPOC (agosto/2026): encaminhamento pro time comercial

**Date:** 2026-08-13
**Branch:** `main`
**Scope:** `lancamentos/agosto-2026/agente-tpoc/`

## Goal of next session

Diagnosticar e corrigir por que a Sofia **fala que vai direcionar pro time comercial, mas a conversa não é de fato direcionada** (feedback da Marcela, 13/08). Fechar a resposta pro time EAM (unnichat vs. IA) e aplicar a correção no n8n da Beppler.

## Estado agora

- **n8n-beppler MCP adicionado** em `~/.config/opencode/opencode.jsonc` (chave `n8n-beppler`, url `https://connect.fernandabeppler.com.br/mcp-server/http`). Token de auth JÁ está no config (não duplicar em docs). **Requer reiniciar o opencode** para as tools `n8n-beppler_*` carregarem — sem hot-reload.
- Nesta sessão a investigação foi feita via curl/Python JSON-RPC direto no endpoint MCP, porque as tools nativas do `n8n-beppler` ainda não estavam carregadas. Na próxima sessão (pós-restart) usar as tools MCP nativas.

## O que já foi descoberto (verificado no n8n da Beppler)

### Workflows da instância (search_workflows)

| id | nome | active | availableInMCP |
|---|---|---|---|
| `_wikb5rfhy_A9I5katNq7` | Vendas - Sofia | true | **false** |
| `ygsnACL52oStaPqx5lJ0y` | TPOC - AI Agent | true | **false** |
| `Zdx6MenSoTFgNaHx` | TPOC - AI Agent Test | true | **true** |
| `h52eT8UbkpJUfrPgxB4ry` | [Testes] [Sofia] [TPOC] | true | false |
| `nwpnSauy2WbkWJMb` | [Testes] [Sofia] [WTP] | true | false |
| `xaQJTlzXlHjPAbZW` | [Testes] [Tita] | true | false |
| `k5w3VWlCvkFtotrC` | [NexIA] [Social Seller] [Tita] | false | false |
| `zoqTlyOvEICXWtap` | [NexIA] [Vendas] [Sofia] [TPOC] | false | false |

Só `TPOC - AI Agent Test` (`Zdx6MenSoTFgNaHx`) tem `availableInMCP: true` — é o workflow que o Diego apontou pra usar. Webhook de teste = `d29fee58-.../chat` (bate com `CLAUDE.md`). Prod ("Vendas - Sofia" e "TPOC - AI Agent") está **bloqueado pra MCP** — `get_workflow_details` / `get_execution` retornam "not available in MCP".

### Nós do `TPOC - AI Agent Test` (12 nodes)

AI Agent · OpenRouter Chat Model (×2) · get_conhecimento/get_objecoes (httpRequestTool v4.4) · get_links/get_bonus (toolCode v1.3) · **encaminharAtendimento (httpRequestTool v4.2)** · Code in JavaScript (code v2, **órfão**) · verificarAlunaPorEmail (disabled) · Postgres memory (tabela `n8n_chat_histories_tpoc_tests`) · When chat message received.

### Fato central: a tool `encaminharAtendimento` EXISTE e está ligada

Diferente da hipótese inicial (tool não implementada), a tool existe e está conectada ao AI Agent (`ai_tool`). Config do node:

```json
{
  "toolDescription": "Use esta tool para encaminhar o atendimento para a equipe",
  "method": "POST",
  "url": "https://unnichat.com.br/a/start/H5sqImpfgVBVnYjU83Ha",
  "sendBody": true,
  "bodyParameters": { "phone": "={{ $('When chat message received').first().json.sessionId }}" },
  "options": {}
}
```

**Sem campo `credentials`** — o POST vai **sem header de auth**. Existe uma credential `Unnichat` (`httpHeaderAuth`, id `Uz8sCT92p4zc9BKs`) na conta que **não está referenciada** pelo node.

### Credentials da instância

Redis · Supabase · OpenAi · Postgres · **Unnichat (httpHeaderAuth)** · OpenRouter · CohereApi · Manychat.

## Hipóteses a verificar (próximo passo)

1. **Prod tem a tool?** `Vendas - Sofia` e `TPOC - AI Agent` estão `availableInMCP: false`. Confirmar (na UI do n8n) se o prod tem `encaminharAtendimento` ligado com a MESMA url/hash. Se prod for um workflow mais velho sem a tool, isso explica tudo.
2. **Auth ausente:** o node não manda header auth pra unnichat. Se o `/a/start/<hash>` exigir o header (`Unnichat` httpHeaderAuth), o POST falha → sem transferência. Testar anexando a credential `Unnichat` ao node.
3. **Formato do `phone`:** em prod `sessionId` = telefone do webhook. Confirmar se o `/a/start` aceita o formato exato que chega (com/sem `+55`, com/sem `9`).
4. **Semântica do endpoint:** `/a/start` pode só ABRIR um atendimento na unnichat (ticket pro time) sem TRANSFERIR a conversa do WhatsApp — ou seja, a Sofia continua no chat e o time nunca assume. Confirmar com a EAM o que o endpoint faz de verdade.

## Restrições

- **Não publicar nada** (pedido explícito do Diego). Mudanças no n8n só após alinhar.
- Não disparar o endpoint unnichat com telefone real em teste (efeito colateral: abre atendimento real).
- `docs/handoffs/2026-08-11-sofia-tpoc-boleto-webhooks.md` ainda tem pendência aberta: `linkBoleto` placeholder em `links.js` (gate 14/08) — não se sobrepõe a este caso, mas fica de fundo.

## Context refs (não duplicar)

- Mecânica do agente: `lancamentos/agosto-2026/agente-tpoc/CLAUDE.md`
- Prompt (contém regras do encaminhamento): `agente-tpoc/prompt.md` (§ ROTEAMENTO DE SUPORTE, linhas ~259–284; `encaminharAtendimento` nas linhas 50/82/154/263)
- Análises Dia 1/Dia 2: `lancamentos/agosto-2026/analises/`
- Base de conhecimento servida por GitHub raw (`deOliveiraDiego/beppler-lancamento-maio/main/...`) — mudar local sem push não reflete no agente.

## Suggested skills

- `read-whatsapp-db` — puxar mensagem da Marcela / follow-up no grupo `✨ IA | EAM ✨`
- `diego-whatsapp-style` — rascunhar resposta pro time EAM
- `n8n-code-javascript` / `n8n-node-configuration` — se mexer no node httpRequestTool
- `i-have-adhd` — formato de resposta (sempre on neste user)
- `handoff` — fechar sessão seguinte
