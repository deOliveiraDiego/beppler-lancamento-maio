# Black Vitalícia — Agente Sofia (Vendas) · Setembro/2026

Conteúdo da Sofia para o Combo Black Vitalícia. Roda em **n8n** + WhatsApp.
Dois agentes: **produção** e **teste**. Prompt construído com a skill `prompt-guide` (7 seções).

> **Vs. agosto:** não é TPOC avulso. Dois preços (aluna / lead) na **mesma página**;
> Sofia não identifica perfil no cartão/PIX. Golden é trilho à parte e **não entra**
> na tool até o Carlos cravar checkout vs grupo. Boleto é TMB 18x (entrada + 17x), a partir
> de 23/09, com **link próprio por perfil** (Carlos, 28/09): quando a lead pede boleto, a Sofia
> pergunta se ela é aluna antes e envia só o link do perfil dela.

## Mapeamento arquivo → node n8n

| Arquivo | Node n8n |
|---|---|
| `prompt.md` | System Message (prod) |
| `prompt-teste.md` | System Message (teste) — lido do GitHub (`main`) pelo node `Prompt GitHub Teste` |
| `prompt-loader.js` | Code node `Prompt GitHub Teste`: cache 5 min + validação + última versão boa se o GitHub falhar |
| `links.js` | Code Tool `get_links` (prod) |
| `links-teste.js` | Code Tool `get_links` (teste) |
| `bonus.js` | Code Tool `get_bonus` (prod) |
| `bonus-teste.js` | Code Tool `get_bonus` (teste) |

Não há `alunas-wtp-*.js` versionado. Lista Golden chegou (16/09); lookup espera o Carlos. Se entrar, arquivo gitignored e cola direto no n8n.

## Workflow para mudanças

1. Editar `prompt.md`, `links.js` ou `bonus.js`.
2. Rodar `./make-teste.sh`.
3. Colar prod no agente de prod e teste no de teste.
4. Salvar + ativar no n8n.

## Contrato das tools

### `get_links`
JSON com `status`: `"pre_abertura"` | `"aberto"` | `"encerrado"`.
- `aberto`: `link` (página de vendas com as duas inscrições — link de PIX e cartão), `preco_aluna_vista`,
  `preco_aluna_parcelado`, `preco_lead_vista`, `preco_lead_parcelado`, `cartao`, `boleto_parcelas`
  (`null` antes de 23/09, `'18x'` a partir de 23/09), `formas_pagamento`, `fechamento_em`,
  `instrucao_agente`. A partir de 23/09 também `link_boleto_aluna` e `link_boleto_nao_aluna`
  (checkouts TMB, entrada + 17x).
- Boleto (Carlos, 28/09): só quando a lead pede boleto; Sofia pergunta se é aluna e envia só
  o link do perfil dela, nunca os dois. Sem `link_aluna` / `link_lead`; checkout Guru não é enviado.
- Sem campo Golden. Sem `order_bump`.

### `get_bonus`
`{ tem_bonus, bonus_ativos, label, descricao }`. Janelas em minutos desde 21/09 10h01.
Repescagem após 30 min: bônus de 15 e 30 min voltam até 24h.

## Regras que vivem NA TOOL

- Preço só a partir de **21/09 10h01**.
- Boleto só a partir de **23/09** (`boleto_parcelas: null` e sem `link_boleto_*` antes).
- Fechamento: **09/10 23:59** (Carlos disse que pode estender).

## Webhooks

- **Teste:** `https://connect.fernandabeppler.com.br/webhook/3550ea5b-86f4-4f8d-aff9-13db4d251cf4/chat`
- **Prod WhatsApp:** ainda não criado neste lançamento (não reusar `webhook/sofia` de agosto).

## Pendências

- Golden: lista Cademí chegou (16/09). Lookup e 2.997 esperam o Carlos (checkout vs grupo).

## Não copiar de agosto

- Webhook `d29fee58-...` e `webhook/sofia` são do TPOC agosto.
- Regra de "Golden = acesso grátis ao TPOC" — **errada** nesta oferta (Golden é preço pago).
