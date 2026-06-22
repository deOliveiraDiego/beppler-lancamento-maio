# Lançamento Agosto/2026 — Beabá do Tarot → TPOC

> Briefing organizado a partir do Google Doc da equipe da Fernanda Beppler
> ([doc original](https://docs.google.com/document/d/1UUl0yg46xLV6FKGL1kVJPLnRuWtgoc6LpJWV26ZL1og/edit)),
> cruzado com o que o agente Sofia tem implementado hoje (lançamento de maio).
>
> Status: **contextualização**. Nada foi alterado no agente ainda.

---

## 1. O que é o lançamento

**Beabá do Tarot** — série de **3 aulas gratuitas ao vivo** (CPL) que celebra e abre uma
nova turma do **TPOC | Tarot Por Onde Começar®**. 100% online e gratuito; porta de
entrada pro produto principal. **Não há WTP neste lançamento.**

### Funil
Série gratuita Beabá do Tarot (3 aulas) → abertura de carrinho do TPOC.

### Jornada completa da aluna
- **13/07** — início da captação (orgânico + tráfego pago)
- **13/07 a 10/08** — aquecimento via *Tarot da Semana* (toda segunda às 10h01)
- **27/07 a 07/08** — 10 áudios no WhatsApp às 10h (reforçando "você consegue aprender Tarot")
- **10/08 (seg)** — CPL1 às 10h01 | tira-dúvidas 19h | tema: *Qual o melhor Tarot para começar*
- **11/08 (ter)** — CPL2 às 10h01 | tira-dúvidas 19h | tema: *Como eliminar o branco na hora da leitura*
- **12/08 (qua)** — CPL3 às 10h01 | tira-dúvidas 19h | tema: *Como interpretar as cartas* + **sorteio**
- **12/08** — **abertura do carrinho TPOC**
- **15/08 (sáb)** — Imersão Degustação TPOC AO VIVO (10h01 às 18h, 8h, aberto ao público no YouTube)
- **19/08 (qua)** — Aula Magna TPOC (aberta a não alunas)
- **20/08 (qui)** — **fechamento do carrinho** à meia-noite (deixa aberto até 9h do dia 21)
- **21/08 (sex)** — Downsell / nova oportunidade (PPNT)

---

## 2. Oferta e pagamento

### Preço — Oferta TPOC25 (preço ÚNICO, sem trilho de perfil)
De ~~R$3.000,00~~ por:
- TPOC + **TCA (Tarot e as Chaves da Alma) incluído**
- **18x de R$180,42** ou **R$2.497,00 à vista**
- (também citado: 12x de R$249,78)

### Formas de pagamento
- Cartão de crédito (até 18x)
- PIX (à vista)
- **Boleto bancário — liberado a partir de 14/08** (sexta, durante a Imersão)

### Produtos adicionais
- **Order Bump** (no ato da compra): *Bruxa de Negócios* — R$97,00 à vista
- **Cross Sell**: *Imersão das Ervas* — R$497,00
- **Downsell** (pós-fechamento, 21/08): *PPNT* — 12x de R$99,70 ou R$997,00 à vista

### Garantia
7 dias (direito de arrependimento, CDC).

### Gates de divulgação (REGRA DURA)
- **NÃO divulgar o preço do TPOC antes da abertura do carrinho (12/08).**
- **NÃO divulgar a abertura de boleto antes de 14/08.**

---

## 3. Bônus (acumulativos por dia de carrinho aberto)

**Todas as inscritas recebem:** método completo TPOC (Despertar da Taróloga, Arcanos
Maiores, Métodos de Leituras, Arcanos Menores), acompanhamento diário, Salas de
Treinamento, Relicário, Coletânea Tarot da Semana, e-book do método, Série completa
Beabá do Tarot, Tarot Astrológico, Como Unir os Significados das Cartas.

**Bônus de agilidade:**
- **12/08 (Dia 1, qua):**
  - primeiras 3h → sorteio da *Caixa Mágica da Fê* (itens físicos + ingresso pro Retiro)
  - 100 primeiras → deck de Tarot
  - primeiras 24h → Curso *TCA | Tarot e as Chaves da Alma*
- **13/08 (Dia 2, qui):** *Combo Tarot+* (aulas integrando Tarot com outras ferramentas mágicas)
- **14/08 (Dia 3, sex):** sem novos bônus — chamada massiva pra Imersão
- **15/08 (Imersão):** reabertura do bônus TCA + *Planilha de Organização Financeira* do Carlos + aula de aplicação

**Bônus do gratuito:** sorteio no CPL3 (12/08) de 1 *Tarot 1909 clássico RWS* (anunciado dia 09/08).

---

## 4. Replay e disponibilidade
- Replay das aulas do Beabá disponível **até domingo pós-fechamento do carrinho**.
- Resposta padrão sobre prazo: *"Pode sair do ar a qualquer momento. Assista ainda hoje."*
- Mensagem-chave: quando as vagas do TPOC encerrarem, o Beabá vira conteúdo do curso e sai do ar no gratuito.

---

## 5. Links

| Link | Status |
|---|---|
| Inscrição no Beabá do Tarot (CPL) | **A chegar** — usar placeholder genérico nos testes |
| Checkout TPOC | `https://i.sendflow.pro/l/tpocsofia` |
| Checkout de boleto (plataforma separada?) | **A confirmar** se existe link próprio, como em maio (TMB) |

> Observação operacional do doc: em caso de recusa no checkout (ex: banco bloqueando
> 18x), orientar a aluna a (1) liberar com o banco ou (2) comprar em 12x; persistindo,
> encaminhar pra atendimento humano.

---

## 6. O que MUDA vs. o agente atual (lançamento de maio)

| Tema | Maio (implementado hoje) | Agosto (este lançamento) |
|---|---|---|
| Origem da lead | Evento WTP ao vivo | Série gratuita Beabá do Tarot (CPL) |
| **Perfil da lead** | Split `aluna_wtp` vs `publica_geral` (preço/link/boleto distintos) | **SEM split** — não há WTP. Perfil único. |
| Preço | 2 trilhos: WTP R$2.497 / novas R$3.000, **links diferentes** | **Preço único R$2.497**, um só checkout |
| Boleto | Exclusivo aluna WTP, a partir de 25/05 | **Pra todas, a partir de 14/08** (não é mais regra de perfil) |
| Calendário | 23–28/05 | 12–20/08 |
| Bônus | Cascata 23–28/05 com trilho WTP | Cascata 12–15/08, sem trilho |
| Order bump / cross / downsell | Não existiam | Novos: Bruxa de Negócios, Imersão das Ervas, PPNT |
| Gates de divulgação | Preço / boleto | Preço (antes 12/08) + boleto (antes 14/08) |

**Impacto técnico principal:** o split de perfil que hoje rege `links.js`, `bonus.js` e
condicionais do `prompt.md` **perde a função comercial** — preço, link e boleto passam a
ser iguais pra todo mundo. O trilho `aluna_wtp` provavelmente sai (ou é neutralizado).

---

## 7. ⚠️ DÚVIDAS PRA CONFIRMAR COM A EQUIPE

Pontos que precisam de decisão da equipe antes de a gente construir/ajustar o agente:

1. **A Sofia atende durante a série gratuita (fase pré-carrinho, ~13/07 a 11/08)?**
   - Se **sim**: o que ela responde nessa fase? (tira-dúvidas do CPL, suporte de
     inscrição, reforço de presença ao vivo, aquecimento — mas **sem falar preço**, que
     é gate até 12/08.)
   - Se **não**: ela só passa a atender a partir da **abertura do carrinho (12/08)**?

2. **A Sofia deve mencionar Order Bump, Cross Sell e Downsell nas conversas?**
   - Ou essas ofertas ficam **só na página/checkout**, e a Sofia não as cita
     proativamente?
   - (Se cita: em que momento e com que abordagem — só se a aluna perguntar, ou ativo?)

3. **Links pendentes:**
   - Link(s) de inscrição do Beabá do Tarot.
   - Existe checkout de boleto separado (como o TMB de maio) ou o boleto é uma opção
     dentro do checkout principal?

### Pontos já definidos (não precisam confirmação)
- ✅ Sem diferenciação de perfil — não há WTP neste lançamento.
- ✅ Link de inscrição chega depois; nos testes usamos placeholder genérico.
