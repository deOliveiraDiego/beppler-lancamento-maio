# TPOC — Agente Sofia (Vendas) · Lançamento AGOSTO/2026 (Beabá do Tarot)

Conteúdo do agente Sofia para o lançamento do TPOC (Tarot Por Onde Começar®).
Roda em **n8n** com integração WhatsApp. Há dois agentes paralelos: **produção** e **teste**.

> **Diferença-chave vs. maio:** este lançamento **NÃO tem WTP** e **NÃO tem split de
> perfil**. Preço, link e boleto são iguais pra todas (trilho único). Toda a mecânica de
> `aluna_wtp` / `publica_geral` (whitelist por telefone, lookup por email, condicionais
> de perfil no prompt) **foi removida**. Veja `briefing/` pra contexto comercial completo.

## Mapeamento arquivo → node n8n

| Arquivo | Node n8n | Observação |
|---|---|---|
| `prompt.md` | System Message do AI Agent (prod) | |
| `prompt-teste.md` | System Message do AI Agent (teste) | |
| `links.js` | Code Tool `get_links` (prod) | Tool dinâmica chamada pelo Agent |
| `links-teste.js` | Code Tool `get_links` (teste) | |
| `bonus.js` | Code Tool `get_bonus` (prod) | Tool dinâmica chamada pelo Agent |
| `bonus-teste.js` | Code Tool `get_bonus` (teste) | |

Não há mais arquivos `alunas-wtp-*.js` nem tool `verificarAlunaPorEmail` neste lançamento.

A distinção prod/teste era o nome do node JavaScript inicial (`Code in JavaScript` em prod,
`Code` no teste). Como nenhum arquivo referencia mais esse node (o perfil saiu), os arquivos
`-teste` hoje saem **byte-a-byte iguais** aos de prod — `make-teste.sh` virou efetivamente
um no-op, mas continue rodando por convenção (caso volte a haver expressões dependentes do node).

## Workflow para mudanças

1. Editar `prompt.md`, `links.js` ou `bonus.js` (versões prod).
2. Rodar `./make-teste.sh` na raiz da pasta — regenera os 3 arquivos `-teste`.
3. Colar a versão prod no agente de prod e a versão teste no agente de teste.
4. Salvar + ativar o workflow no n8n.

## Contrato das tools (o prompt depende disso)

### `get_links`
Retorna JSON com `status`: `"pre_abertura"` | `"aberto"` | `"encerrado"`.
- `aberto`: `preco_vista`, `parcelado`, `parcelamento_alternativo`, `formas_pagamento`,
  `link`, `fechamento_em`, e `link_boleto` (só a partir de 14/08).
- **Não há** campo `perfil` nem `order_bump`.

### `get_bonus`
Retorna `{ tem_bonus, bonus_ativos: [], label, descricao }`. No ramo sem bônus, `label`
não é emitido. Sem campo `perfil`.

## Regras de negócio que vivem NA TOOL (não no prompt)

### Gates de divulgação (regra dura do briefing)
- **Preço** só "existe" a partir da abertura do carrinho (**12/08**) — antes disso
  `get_links` retorna `pre_abertura` e a Sofia não tem preço pra falar.
- **Boleto** só entra no payload a partir de **14/08** (campo `link_boleto`). Se a tool
  não retorna o campo, a Sofia não menciona boleto e segue com PIX/cartão.
- Boleto é pra **todas** (não é mais regra de perfil, como era em maio).

### Calendário
Carrinho abre **12/08**, fecha **20/08 à meia-noite** (fica aberto até **9h de 21/08**).
Imersão Degustação 15/08; Aula Magna 19/08.

## ⚠️ Pendências (placeholders no código até a equipe confirmar)

- **Horário exato de abertura do carrinho** em 12/08 (após CPL3 das 10h01). Hoje `links.js`
  usa `12/08 00:00` (o gate de preço cobre a manhã do dia).
- **Checkout de boleto**: existe link próprio (plataforma separada, como o TMB de maio) ou
  o boleto é uma opção dentro do checkout principal? `link_boleto` em `links.js` é
  **PLACEHOLDER** — trocar quando confirmado.
- **Link de inscrição do Beabá do Tarot**: ainda não chegou (usar placeholder nos testes).

## Webhooks (referência pra testes)

> ⚠️ As URLs abaixo são do workflow de **maio** — **confirmar/atualizar** para o workflow
> de agosto antes de testar em prod.

- **Teste (maio):** `https://connect.fernandabeppler.com.br/webhook/tpoc-teste`
- **Produção:** URL com UUID — pedir ao usuário.

Payload: `{"sessionId": "<telefone>", "chatInput": "<mensagem>"}`.
Como não há mais whitelist por telefone, **qualquer `sessionId`** cai no fluxo único.

Cuidado: chamadas em prod **gravam memória de sessão** no banco — usar com parcimônia.
