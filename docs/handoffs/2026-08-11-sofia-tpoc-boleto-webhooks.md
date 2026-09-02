# Handoff — Sofia TPOC (agosto/2026): boleto + webhooks + sync

**Date:** 2026-08-11  
**Branch:** `main`  
**Scope:** `lancamentos/agosto-2026/agente-tpoc/`

## Goal of next session

Plug the real boleto checkout URL into `links.js` when Sara replies in WhatsApp, then republish the Code Tool in n8n (prod + teste).

## State now

- **Override de teste removido** no repo: `links.js` / `bonus.js` (e `-teste`) usam `DateTime.now().setZone('America/Sao_Paulo')`. Diego confirmou override removido e publicado no n8n.
- **Webhooks agosto** documentados em `agente-tpoc/CLAUDE.md`:
  - Teste (Chat Trigger UI): `https://connect.fernandabeppler.com.br/webhook/d29fee58-868c-402a-814f-7866767c2694/chat`
  - Prod (WhatsApp): `https://connect.fernandabeppler.com.br/webhook/sofia`
- **Pedido do boleto enviado** (2026-08-11) no grupo WhatsApp `✨ IA | EAM ✨` (`120363408426429761@g.us`). Mensagem pediu URL do checkout de boleto à Sara.
- **Grupo errado a evitar:** `[PAUSADO] EAM` / antigo “DALTON LAB + EAM” (`120363422106480400@g.us`). Skill uazapi ainda lista o JID antigo — não usar.

## Blocker (único de produto)

- `linkBoleto` em `links.js` ainda é placeholder: `https://PLACEHOLDER-confirmar-checkout-boleto`
- Gate: boleto só entra no payload a partir de **14/08** (`boletoDisponivel`). Sem URL real, a Sofia não consegue enviar boleto quando o gate abrir.

## Uncommitted local (não commitado nesta sessão)

```
M  lancamentos/agosto-2026/agente-tpoc/CLAUDE.md   # webhooks agosto + remoção aviso override
M  lancamentos/agosto-2026/agente-tpoc/links.js
M  lancamentos/agosto-2026/agente-tpoc/links-teste.js
?? lancamentos/agosto-2026/agente-tpoc/chat-trigger-teste.json
```

Commit only if Diego asks.

## Workflow when Sara sends the URL

1. Replace `linkBoleto` in `links.js` (keep the 14/08 gate).
2. Run `./make-teste.sh` in `agente-tpoc/`.
3. Paste prod tools into n8n prod, teste into teste; save + activate.
4. Update pendência de boleto em `CLAUDE.md` (marcar URL recebida).
5. Optional smoke: Chat Trigger teste first; prod webhook sparingly (writes session memory).

Payload prod WhatsApp: `{"sessionId": "<telefone>", "chatInput": "<mensagem>"}`.

## Soft pendências (não bloqueiam hoje)

- Horário exato de abertura do carrinho em 12/08 (hoje `abertura` = `12/08 00:00`; gate cobre a manhã).
- Smoke test real após abertura do carrinho (12/08).

## Context refs (não duplicar)

- Mecânica do agente: `lancamentos/agosto-2026/agente-tpoc/CLAUDE.md`
- Repo root: `CLAUDE.md`
- Mensagem estilo cliente: skill `diego-whatsapp-style`
- Envio WhatsApp: skill `uazapi` (grupo certo: `✨ IA | EAM ✨`)

## Suggested skills

- `diego-whatsapp-style` — qualquer follow-up no grupo EAM
- `uazapi` — enviar/ler grupo; JID correto `120363408426429761@g.us`
- `i-have-adhd` — formato de resposta (sempre on neste user)
- `eighty-twenty` — se pedir enxugar status/decisão
- `n8n-code-javascript` — se editar Code Tools além do placeholder
- `handoff` — fechar sessão seguinte
