# Black Vitalícia — Agente Sofia (Vendas) · Setembro/2026

Conteúdo da Sofia para o Combo Black Vitalícia. Roda em **n8n** + WhatsApp.
Dois agentes: **produção** e **teste**. Prompt construído com a skill `prompt-guide` (7 seções).

> **Vs. agosto:** não é TPOC avulso. Dois preços (aluna / lead) na **mesma página**;
> Sofia não identifica perfil. Golden é trilho à parte e **não entra** na tool
> até existir lista de telefones. Boleto é TMB, a partir de 23/09.

## Mapeamento arquivo → node n8n

| Arquivo | Node n8n |
|---|---|
| `prompt.md` | System Message (prod) |
| `prompt-teste.md` | System Message (teste) |
| `links.js` | Code Tool `get_links` (prod) |
| `links-teste.js` | Code Tool `get_links` (teste) |
| `bonus.js` | Code Tool `get_bonus` (prod) |
| `bonus-teste.js` | Code Tool `get_bonus` (teste) |

Não há `alunas-wtp-*.js` neste lançamento. Lista Golden, quando chegar, é gitignored (`**/alunas-wtp-*.js` ou arquivo local equivalente) e cola direto no n8n.

## Workflow para mudanças

1. Editar `prompt.md`, `links.js` ou `bonus.js`.
2. Rodar `./make-teste.sh`.
3. Colar prod no agente de prod e teste no de teste.
4. Salvar + ativar no n8n.

## Contrato das tools

### `get_links`
JSON com `status`: `"pre_abertura"` | `"aberto"` | `"encerrado"`.
- `aberto`: `preco_aluna_vista`, `parcelado_aluna`, `preco_lead_vista`, `parcelado_lead`,
  `formas_pagamento`, `link` (página com as duas inscrições), `link_aluna`, `link_lead`,
  `fechamento_em`. A partir de 23/09: `boleto_aluna`, `boleto_lead`, `link_boleto_aluna`,
  `link_boleto_lead`.
- Sem campo Golden. Sem `order_bump`.

### `get_bonus`
`{ tem_bonus, bonus_ativos, label, descricao }`. Janelas em minutos desde 21/09 10h01.
Repescagem após 30 min: bônus de 15 e 30 min voltam até 24h.

## Regras que vivem NA TOOL

- Preço só a partir de **21/09 10h01**.
- Boleto só a partir de **23/09** (campos omitidos antes).
- Fechamento: **09/10 23:59** (Carlos disse que pode estender).

## Pendências

- URLs TMB (`PLACEHOLDER-tmb-aluna` / `PLACEHOLDER-tmb-lead`).
- Lista Golden.
- Confirm do honor system (pergunta no grupo, 15/09).
- Webhook de teste/prod deste lançamento — ainda não criado no n8n.

## Não copiar de agosto

- Webhook `d29fee58-...` e `webhook/sofia` são do TPOC agosto.
- Regra de "Golden = acesso grátis ao TPOC" — **errada** nesta oferta (Golden é preço pago).
