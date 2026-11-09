# Black Vitalícia das Bruxas — briefing (20/09/2026)

Status do agente Sofia no n8n: workflow **Black Friday - 2026** (`i4lJmLV5ORNG6Wjt`) ativo.
Estes arquivos locais reconstruíram o contrato. O dump do n8n falhou (MCP desligado no workflow).

Este documento separa fato e regra fechada.

**Termos (um termo = um significado):**
- `página de vendas`: https://sndflw.com/l/black-sofia
- `trilho`: Golden, aluna ou lead. A página escreve `Não Aluna` no lugar de lead.
- `carrinho`: período de compra, 21/09 10h01 até 09/10
- `boleto`: opção na página de vendas a partir de 23/09. A Sofia não envia URL TMB.

**Fontes:**
- Grupo EAM, 02/09 (Carlos, pacote)
- Grupo EAM, 09/09 e 10/09 (Sara, valores e links)
- Grupo EAM, 15/09 e 16/09 (Carlos fecha a operação da Sofia)
- Página de vendas combo-black
- n8n: workflow criado 15/09

---

## 1. Fatos confirmados

O nome da oferta é Black Vitalícia das Bruxas.
A oferta inclui acesso permanente a todos os cursos atuais.
A oferta inclui acesso permanente a todos os cursos futuros.
A oferta inclui atualizações (Carlos, 15/09).

A live ocorre em 21/09 às 10h01.
O carrinho de lead e de aluna abre na live, 21/09.
O carrinho fecha em 09/10. A hora do fechamento está ausente. Este briefing usa 23h59.
O boleto libera em 23/09 para todas as ofertas, na página de vendas.

Sofia só atende a partir da abertura do carrinho.

| Trilho | À vista | Cartão | A Sofia envia |
|---|---|---|---|
| Lead | R$ 4.997,00 | 18x de R$ 361,06 | página de vendas |
| Aluna | R$ 3.997,00 | 18x de R$ 288,81 | página de vendas |
| Golden | R$ 2.997,00 | 18x de R$ 216,55 | nenhum. Encaminha para humano |

Cartão: até 18x.
Boleto: 12x, a partir de 23/09, na página.
PIX: na página.

Página de vendas da Sofia: https://sndflw.com/l/black-sofia

Checkouts GURU existem (lote especial). A Sofia **não** os envia.
TMB aluna: https://pay.tmb.com.br/EscoladeArte/MPJ127271CU
TMB lead: https://pay.tmb.com.br/EscoladeArte/8R111368294
A Sofia **não** envia TMB. Os dois entram na página no dia 23.

---

## 2. Regras fechadas (Carlos, 15–16/09)

1. A Sofia não identifica aluna versus lead.
2. A Sofia envia só a página de vendas. Os dois preços ficam na mesma tela, sem login.
3. A pessoa escolhe o botão Aluna ou Não Aluna.
4. A Sofia não envia checkout separado.
5. A Sofia não atende Golden. Declaração de Golden → humano (Marcelly). Diego dispara aviso no grupo EAM no WhatsApp dele.
6. Cursos atuais estão liberados. A Sofia não informa data de entrega de curso novo.
7. A barra de 75% da página de obrigado saiu.

Conflito antigo (Golden abre antes de 21/09): a Sofia **não** opera o trilho Golden. A campanha Golden 15–20/09 fica fora deste agente.

---

## 3. Bônus de agilidade

A página de vendas coloca três itens nas primeiras 24 h:
- ingresso do Retiro das Bruxas de Beppler (2026), R$ 5.000
- Kit Mandinguinha da Virada com frete grátis
- Passaporte Dourado

O texto do Carlos (15 min, 30 min, 1 h, 3 h) não entrou na tool `get_bonus`.
A tool segue a página.

---

## 4. Agente no repo

Pasta: `lancamentos/setembro-2026/agente-tpoc/`

| Arquivo | Função |
|---|---|
| `prompt.md` | system message |
| `links.js` | status do carrinho + único `link` |
| `bonus.js` | janela de 24 h |
| `base-de-conhecimento.md` | produto |
| `base-de-objecoes.md` | objeções |

Lista Golden: não versionar (`alunas-golden-*.js` no gitignore).

---

## 5. Ainda aberto

1. Conferir o canvas n8n contra estes arquivos. MCP está desligado nesse workflow.
2. Confirmar o webhook de produção do WhatsApp (se já não for o Chat Trigger de teste).
3. Hora exata do fechamento em 09/10.
4. Ligar o acesso MCP no card do workflow, se quiser dump fiel na próxima sessão.
