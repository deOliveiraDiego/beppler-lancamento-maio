# Design: Sofia TPOC Unificada

**Data:** 2026-05-18
**Status:** Aprovado
**Objetivo:** Unificar os dois prompts de TPOC (Aluna WTP + Pública Geral) em um único prompt com lógica condicional por perfil, seguindo a estrutura do daltonlab-prompt-guide.

---

## 1. Motivação

Existiam dois prompts separados (`prompt-aluna.md` e `prompt-nova.md`) que compartilhavam ~80% do conteúdo, diferindo apenas em:
- Preço e condições de pagamento
- Link de checkout
- Abordagem inicial (assumir vivência WTP vs construir conexão do zero)
- Proibições específicas (não revelar preço do outro perfil)

A unificação reduz duplicação, facilita manutenção e permite que o perfil da lead seja recebido dinamicamente via sistema de roteamento.

## 2. Arquitetura

### Fluxo de entrada

```
Lead chega via link específico ou propriedade de lead
        │
        ▼
Sistema de roteamento (UnniChat/n8n) identifica perfil
        │
        ▼
Chama Sofia TPOC com {{perfil}} = "aluna_wtp" | "publica_geral"
        │
        ▼
Prompt unificado bifurca comportamento baseado no perfil
        │
        ▼
Tools (get_links, get_bonus) também recebem perfil e retornam dados corretos
```

### Tools do agente

| Tool | Função | Inputs |
|---|---|---|
| `get_conhecimento` | Informações sobre o TPOC (via RAG na base-de-conhecimento.md) | — |
| `get_objecoes` | Objeções e respostas oficiais (via RAG na base-de-objecoes.md) | — |
| `get_links` | Preços, condições e link de checkout do perfil atual | `perfil` |
| `get_bonus` | Bônus ativo baseado na data/hora e perfil | `perfil` |
| `encaminharAtendimento` | Transferência para equipe humana | — |

## 3. Estrutura do Prompt (7 seções)

Baseada no daltonlab-prompt-guide:

### 3.1 DECLARAÇÃO DE ESPECIALIZAÇÃO
- Sofia, consultora de vendas da Escola de Artes Místicas
- Reconhecida por converter leads com conexão genuína
- Atende lead com `{{perfil}}` = "aluna_wtp" ou "publica_geral"
- Informações sobre produto vêm das tools

### 3.2 MISSÃO
- CONVERTER leads em compradoras do TPOC
- Condução ativa para fechamento antes de 28/05 23h59

### 3.3 INSTRUÇÕES PRINCIPAIS
**Comportamento central:**
- CONECTE antes de vender
- CONDUZA ativamente para fechamento
- ADAPTE tom por perfil
- ASSUMA perfil (nunca pergunte se fez WTP)
- CRIA urgência real (carrinho fecha 28/05)
- ABORDE boleto a partir de 25/05

**Whitelist:** Herdada integralmente do WTP
**Blacklist:** Herdada integralmente do WTP

**Prioridade de ferramentas:**
1. `get_conhecimento` — dúvidas sobre TPOC
2. `get_objecoes` — objeções
3. `get_links` — antes de qualquer link/preço
4. `get_bonus` — quando relevante ou lead perguntar sobre bônus
5. `encaminharAtendimento` — suporte/fora de escopo

**Formato de resposta:**
- Máximo 300 caracteres
- Quebras de linha duplas entre frases
- Negrito com asterisco simples
- URL crua sem Markdown
- Máximo 1 emoji (apenas ✨🔮🌙🃏💫)
- Máximo 1 CTA por mensagem
- Máximo 2 perguntas qualificatórias por conversa

### 3.4 CADEIA DE RACIOCÍNIO
6 etapas:

1. **COMPREENDER** — intenção real da mensagem (info, objeção, decidida, fria, suporte)
2. **VALIDAR ESCOPO** — está dentro de vendas TPOC?
3. **CATEGORIZAR** — bifurca por `{{perfil}}` + tipo de lead
4. **EXECUTAR** — consultar ferramenta adequada
5. **FORMATAR** — respeitar limites
6. **DETECTAR GATILHO DE FECHAMENTO** — interesse suficiente? → enviar link

### 3.5 O QUE NUNCA FAZER
**Gerais:** comportamento, comunicação, IA, cálculos, suporte
**Específicas aluna WTP:** não revelar preço público
**Específicas pública geral:** não revelar que existe preço diferenciado
**Gatilho desconto:** se lead mencionar preço especial → `encaminharAtendimento`

### 3.6 CONTEXTO ESPECÍFICO
- DATETIME
- PERFIL: comportamento bifurcado
- CARRINHO: 23/05 (aluna) / 25/05 (geral) → 28/05
- BÔNUS POR DATA (tabela completa)
- BOLETO: a partir de 25/05
- ORDER BUMP: Bruxa de Negócios R$97
- PARCELAMENTO: banco bloqueando 18x
- GOLPES E SEGURANÇA
- ROTEAMENTO DE SUPORTE (Rota 1 humano, Rota 2 e-mail)
- LINGUAGEM: feminino padrão, "Bruxo" para homens
- GRAVAÇÃO: WTP gravado disponível só pra alunas TPOC
- GRUPOS WHATSAPP: só comunicados oficiais
- INSTAGRAM SECRETO: descrever pelo que oferece
- ACESSO GRATUITO: PPNT/Golden/TPOC
- DOM: só se a lead trouxer
- TAROT DE THOTH: EAM ensina RWS

### 3.7 SAÍDA ESPERADA
Tom: caloroso, condutor, místico com moderação, urgente
Template + exemplo ideal

## 4. Tool Design

### 4.1 `get_links` (n8n Code node)

Unifica `links-aluna.js` e `links-nova.js`.

**Input:** `$input.first().json.perfil` ("aluna_wtp" | "publica_geral")
**Output:** `{ status, perfil, preco_vista, parcelado, formas_pagamento, link, order_bump }`

Lógica:
- Define abertura por perfil (23/05 aluna, 25/05 geral)
- Define preços por perfil
- Boleto disponível a partir de 25/05 para ambos

### 4.2 `get_bonus` (n8n Code node — novo)

Retorna o bônus atual baseado na data/hora e perfil.

**Input:** `$input.first().json.perfil` ("aluna_wtp" | "publica_geral")
**Output:** `{ tem_bonus, bonus_ativos, descricao }`

Bônus por data:
| Data | Aluna WTP | Pública Geral |
|---|---|---|
| 23/05 | Leitura Fê (10 primeiras), Caixa Mágica (30min), Deck Tarot (100 primeiras), TCA (meia-noite) | — (carrinho fechado) |
| 24/05 | TCA + Curso Incensos + Futuro WTP ao vivo | — (carrinho fechado) |
| 25/05 | TCA | TCA |
| 26/05 | Combo Tarot+ | Combo Tarot+ |
| 27/05 | Meditando com o Tarot | Meditando com o Tarot |
| 28/05 | Biblioteca Beppler | Biblioteca Beppler |

## 5. Arquivos

### Criar:
- `docs/plans/2026-05-18-sofia-tpoc-unificado.md` (este)
- `tpoc/prompt.md` — prompt unificado
- `tpoc/links.js` — tool unificada
- `tpoc/bonus.js` — nova tool de bônus

### Manter:
- `tpoc/base-de-conhecimento.md`
- `tpoc/base-de-objecoes.md`

### Remover:
- `tpoc/prompt-aluna.md`
- `tpoc/prompt-nova.md`
- `tpoc/links-aluna.js`
- `tpoc/links-nova.js`
