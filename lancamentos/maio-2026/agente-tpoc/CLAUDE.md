# TPOC — Agente Sofia (Vendas)

Conteúdo do agente Sofia para o lançamento do TPOC (Tarot na Prática do Ofício Completo).
Roda em **n8n** com integração WhatsApp. Há dois agentes paralelos: **produção** e **teste**.

## Mapeamento arquivo → node n8n

| Arquivo | Node n8n | Observação |
|---|---|---|
| `prompt.md` | System Message do AI Agent (prod) | Referencia `$('Code in JavaScript')` |
| `prompt-teste.md` | System Message do AI Agent (teste) | Referencia `$('Code')` |
| `links.js` | Code Tool `get_links` (prod) | Tool dinâmica chamada pelo Agent |
| `links-teste.js` | Code Tool `get_links` (teste) | |
| `bonus.js` | Code Tool `get_bonus` (prod) | Tool dinâmica chamada pelo Agent |
| `bonus-teste.js` | Code Tool `get_bonus` (teste) | |
| `alunas-wtp-telefones.js` | Code node inicial (whitelist por telefone) | Define `perfil = aluna_wtp` para números na lista |
| `alunas-wtp-emails.js` | Code Tool `verificarAlunaPorEmail` | Lookup por email |

Diferença entre prod e teste: nome do node JavaScript inicial. Em prod o node se chama
`Code in JavaScript`, no agente de teste se chama `Code`.

## Workflow para mudanças

1. Editar `prompt.md`, `links.js` ou `bonus.js` (versões prod).
2. Rodar `./make-teste.sh` na raiz da pasta — regenera os 3 arquivos `-teste`
   substituindo `Code in JavaScript` por `Code`.
3. Colar a versão prod no agente de prod e a versão teste no agente de teste.
4. Salvar + ativar o workflow no n8n.

## Gotchas conhecidos

### Variável de perfil no system message

O perfil da lead (`aluna_wtp` ou `publica_geral`) é resolvido pelo Code node inicial
(pelo telefone) e usado em condicionais do prompt.

**Convenção atual:** declarar o valor uma vez no topo do prompt em uma linha
`**PERFIL_LEAD desta conversa:** {{ $('Code in JavaScript').first().json.perfil }}` e
referenciar a string literal `PERFIL_LEAD` (caixa alta) em todos os branches:
`Se PERFIL_LEAD = "aluna_wtp": ...`

**Não fazer:**
- Inline da expressão `{{ ... }}` dentro de condicionais — quando o n8n renderiza,
  o valor substitui a expressão e gera tautologia ambígua tipo `Se aluna_wtp = "aluna_wtp"`,
  que confunde o LLM.
- Sintaxe `{{perfil}}` solta — o n8n não resolve isso, vira `[undefined]` em runtime.

### Sintaxe correta da expressão n8n

Apenas estas formas resolvem o perfil:
- Prod: `{{ $('Code in JavaScript').first().json.perfil }}`
- Teste: `{{ $('Code').first().json.perfil }}`

### Boleto

- Boleto é **exclusivo de aluna WTP** (regra de negócio confirmada pela Sara).
- `links.js` controla isso: campo `boleto` e `link_boleto` só vêm no payload se
  `now >= 25/05 && perfil === 'aluna_wtp'`.
- O link de boleto (`link_boleto`) é checkout SEPARADO (plataforma TMB),
  diferente do `link` do checkout principal (Sendflow, PIX/cartão).
- A Sofia nunca deve dizer "selecione boleto dentro do checkout" — quando boleto
  está disponível, ele tem link próprio.
- A regra de negócio "boleto só pra aluna WTP" vive **na tool**, não no prompt.
  Se a tool não retornar o campo, o prompt já redireciona pra PIX/cartão sem
  confirmar nem negar.

## Webhooks (referência rápida pra testes)

- **Teste:** `https://connect.fernandabeppler.com.br/webhook/tpoc-teste`
- **Produção:** URL com UUID — pedir ao usuário caso necessário.

Payload: `{"sessionId": "<telefone>", "chatInput": "<mensagem>"}`.
- `sessionId` precisa ser um telefone presente em `alunas-wtp-telefones.js`
  para o perfil cair em `aluna_wtp`. Qualquer outro número cai em `publica_geral`.

Cuidado: chamadas em prod **gravam memória de sessão** no banco — usar com parcimônia
e preferir telefones de teste quando possível.
