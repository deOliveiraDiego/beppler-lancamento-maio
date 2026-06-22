# Análise de Performance — Sofia WTP | Lançamento Dias 1–4
**Snapshot:** 922 mensagens · 57 sessões · 20/abr 09:58 BRT → 23/abr 20:44 BRT (4 dias)

---

## Resumo Executivo

1. **Volume cresceu, qualidade parcialmente também:** 57 sessões em 4 dias, 922 msgs, média de 16,2 msgs/sessão. A proporção human/AI permanece 1:1 exato e 100% das conversas terminam com resposta da Sofia.
2. **Funil razoável para o estágio:** 12 sessões (21%) receberam link de compra. Lote Zero gerou 5 sessões com link; Lote 1 (a partir do dia 3) gerou 9 — sinal de aceleração.
3. **FALHA ESTRUTURAL CONFIRMADA — escalonamento inexistente:** Em 159 mensagens Sofia menciona "equipe"; a ferramenta `encaminharAtendimento` foi chamada **zero vezes**. Nenhuma transferência é real.
4. **Dois casos de impacto financeiro direto:** Uma lead querendo **comprar** (sem cartão/PIX, só dinheiro) esperou mais de 2 dias sem atendimento. Uma lead querendo **cancelar** esperou 49h. Ambas em loop ativo.
5. **Tom e qualificação de venda estão bons:** Quando o fluxo é de venda pura, a Sofia performa bem — qualificação fluente, linguagem do nicho precisa, condução ativa.
6. **"Perfeito" como tique verbal:** 138 de 461 respostas (30%) abrem com "Perfeito" — inclusive em contextos absurdos como resposta a "Ainda não [fui atendida]".
7. **Emoji fora da whitelist detectado:** Sofia usou 😕 — fora dos 5 emojis aprovados no prompt (✨ 🔮 🌙 🃏 💫).

---

## Análise Quantitativa

### Volume Total

| Métrica | Valor |
|---|---|
| Total de mensagens | 922 |
| Sessões únicas | 57 |
| Msgs humanas / bot | 461 / 461 (1:1 exato) |
| Média msgs/sessão | 16,2 |
| Sessões com link de compra | 12 (21%) |
| Escalonamentos via ferramenta | **0 (ZERO)** ⚠️ |
| Sessões com última msg do bot | 57 / 57 (100%) |

### Sessões Novas por Dia

| Dia | Sessões novas | Observação |
|---|---|---|
| 20/abr (dom) | 18 | Abertura do lançamento |
| 21/abr (seg) | 9 | Queda — dia útil pós-domingo |
| 22/abr (ter) | 16 | Recuperação — virada p/ Lote 1 |
| 23/abr (qua) | 14 | Parcial — dia ainda em andamento |

### Distribuição por Hora (BRT — acumulado 4 dias)

| Período | Msgs | % | Observação |
|---|---|---|---|
| 10h–11h | 340 | 36,9% | Pico dominante |
| 16h–17h | 132 | 14,3% | Pico da tarde |
| 13h | 48 | 5,2% | Novo pico pós-almoço |
| 22h–23h | 98 | 10,6% | Pico noturno |
| 00h–08h | 38 | 4,1% | Volume baixo |

### Profundidade das Conversas

| Bucket | Sessões | % | Duração média |
|---|---|---|---|
| 1–2 msgs | 12 | 21% | < 1 min |
| 3–5 msgs | 8 | 14% | 24 min |
| 6–10 msgs | 14 | **25%** | 464 min (~8h) |
| 11–20 msgs | 8 | 14% | 1.181 min (~20h) |
| 21+ msgs | 15 | 26% | 1.184 min (~20h) |

> O bucket 6-10 cresceu de 11% → 25% em relação à análise dos dias 1-2. Indica mais leads no meio do funil — engajamento real, mas conversão ainda em aberto.

> Duração média muito alta nos buckets 6+ (8h, 20h): a maioria não é tempo de negociação, é tempo de espera por atendimento humano que nunca chega.

### Funil

```
Sessões iniciadas:             57  (100%)
    ↓
Engajamento real (3+):         45  (79%)
    ↓
Receberam link de compra:      12  (21%)
    → Lote Zero:                5
    → Lote 1:                   9
    ↓
Escalonamentos reais:           0  ⚠️
Sessões em loop de suporte:    ~12 (21%) — leads presas aguardando equipe
```

### Frases-chave nas Respostas do Bot

| Frase | Ocorrências | % das respostas |
|---|---|---|
| "equipe" | 159 | 34,5% |
| "Perfeito" | 138 | 30,0% |
| "encaminhar" | 50 | 10,8% |
| "cancelamento" | 13 | 2,8% |
| "e-book / 50 Mitos" | 19 | 4,1% |
| "TPOC" | 13 | 2,8% |
| "acesso gratuito" | 2 | 0,4% |
| "garantia" | 1 | 0,2% |

---

## Análise Qualitativa

### O que está funcionando

**1. Qualificação e conexão nos fluxos de venda pura**

Sessão `...1042953` (66 msgs, comprou): Lead masculino com 10 anos de contato esporádico com Tarot. Sofia identificou o perfil ("Tarot nunca te deixou, ficou ali adormecido"), qualificou sem forçar, enviou link no momento certo. Pós-compra: nurturing sobre escolha de baralho, plastificado vs. não-plastificado, como embaralhar — conversa genuína que reforça o valor percebido.

**2. Modo fria funcional e consistente**

Mensagens de 1-3 palavras sem contexto são tratadas sem CTA/link/emojis — correto. Não detectei violações desse comportamento em nenhuma das sessões analisadas.

**3. Identificação de alunas com acesso gratuito**

Pelo menos 3 sessões com leads TPOC foram identificadas corretamente antes de tentar vender. A intenção de encaminhar está certa — só a execução (ferramenta não chamada) falha.

**4. Tom e whitelist**

Linguagem do nicho bem aplicada ao longo dos 4 dias: "chamado", "despertar", "ressoou", "buscadora". Blacklist respeitada — sem "desconto", "lançamento", "amiga", "tudo no seu tempo".

**5. Virada de lote correta**

Sessão `...1967` (558599881967): Sofia enviou link do Lote 1 (`lote-1wtp`) corretamente a partir de 22/abr — a consulta a `get_links` funcionou como esperado na virada de lote.

---

### O que está falhando

**CRÍTICO 1: `encaminharAtendimento` nunca é chamada**

0 chamadas reais em 4 dias. 159 mensagens mencionando "equipe", 50 com "encaminhar" — todas promessas vazias. O padrão está consolidado e escalando conforme o volume cresce.

---

**CRÍTICO 2: Lead querendo comprar esperou 2+ dias sem ser atendida**

Sessão `...3993` (48 msgs, 34h de duração, ainda ativa):

> Lead: *"Eu quero fazer o workshop com a Fê. Não tenho cartão e nem Pix no celular. Como posso pagar? Só tenho dinheiro."*
> Sofia: *"Vou te conectar com a equipe pra te orientar da melhor forma."*

Equipe não apareceu. Lead voltou no dia seguinte:
> Lead: *"KD essa equipe? Eu preciso ir ao mercado."*

Voltou no dia 23, 19h53:
> Lead: *"Até agora nada. Nadinha."*
> Sofia: *"Você não deveria estar passando por isso 💫 Acionei diretamente a equipe responsável agora."*

No final da tarde do dia 23 a lead ainda perguntou: *"Até quando posso me inscrever?"* — há intenção de compra ativa. Esta é uma **venda perdida por falha operacional**, não por falta de interesse.

---

**CRÍTICO 3: Lead querendo cancelar esperou 49h**

Sessão `...2040` (52 msgs, 49,4h de silêncio desde última mensagem):

> Lead comprou, encontrou conflito de agenda, pediu cancelamento na madrugada do dia 21.
> Sofia "acionou a equipe" 9 vezes.
> Nenhuma resposta real em 49 horas.

Risco ativo de chargeback.

---

**Tique verbal "Perfeito" em contextos inadequados**

138 ocorrências (30% das respostas). Exemplos reais:

> Lead: *"Ainda não [fui atendida]"*
> Sofia: **"Perfeito"** 🌙

> Lead: *"Não"* (quando perguntada se a equipe tinha entrado em contato)
> Sofia: **"Perfeito"** 💫

---

**Emoji fora da whitelist**

Sofia usou 😕 na sessão `...1591` — fora dos 5 emojis aprovados (✨ 🔮 🌙 🃏 💫). Pequeno desvio, mas indica que o modelo está gerando além do permitido.

---

**Encerramentos passivos recorrentes**

Sessões encerram com frases passivas contrariando o prompt:
- *"Se surgir qualquer coisa, me chama por aqui, combinado?"*
- *"Seguimos por aqui ✨"*
- *"Qualquer coisa é só me chamar por aqui, tá?"*

Especialmente nas sessões onde Sofia encaminhou para a equipe e a conversa ficou "suspensa" — não há tentativa de reengajamento ativo.

---

**Lead qualificada perdida por falta de urgência no fechamento**

Sessão `...1591` (56 msgs, sem link): Lead longa e engajada que nunca recebeu link. Com base na última mensagem ("Se quiser, posso tentar te ajudar por aqui mesmo enquanto a equipe..."), parece que a conversa virou suporte antes de chegar ao fechamento. Padrão: suporte sequestra o funil de venda.

---

## Objeções e Motivos de Contato (acumulado 4 dias)

| Categoria | Freq. aprox. | Status |
|---|---|---|
| Aluna com problema de acesso (ebook / IG secreto / plataforma) | ~8 sessões | Não resolvido (tool não chamada) |
| Aluna com acesso gratuito (TPOC / Golden / PPNT) | ~3 sessões | Identificado, mas escalonamento falso |
| Forma de pagamento alternativa (dinheiro, boleto) | 1 sessão ativa | **Venda perdida** — lead sem atendimento há 2+ dias |
| Cancelamento de compra | 1 sessão ativa | **Risco de chargeback** — sem atendimento há 49h |
| Conflito de horário / replay | 2 sessões | Contornado com "7 dias de garantia" (bom) |
| Curiosidade sobre dom / medo espiritual | 2 sessões | Tratado bem |
| Pergunta sobre TPOC | 3 sessões | Informado corretamente (sem preço/link) |

---

## Recomendações

### ~~Urgente~~ — itens resolvidos

**1. ~~Atender sessão `554388423993`~~**
Lead que queria comprar sem PIX/cartão — aguardou mais de 34h, confirmou interesse até 19:28 do dia 23/04. *(Verificar se foi atendida após a resolução do bug.)*

**2. ~~Atender sessão `5521994928040`~~**
Lead que pediu cancelamento às 00:32 do dia 21/04, tentou por 20h seguidas (até 20:57), nunca foi atendida e desistiu. *(Verificar se houve chargeback ou disputa.)*

**3. ~~Bug de escalonamento — `encaminharAtendimento` nunca chamada~~ ✅ RESOLVIDO**
Em 159 mensagens Sofia dizia "vou encaminhar pra equipe" sem nunca chamar a ferramenta. Bug identificado e corrigido durante o lançamento. O impacto nos dias 1-4 foi: pelo menos 2 casos com perda financeira potencial (venda não concluída + risco de chargeback) e ~12 sessões de leads presas em loop de suporte sem atendimento real.

---

### Média prioridade (próximos dias)

**4. Eliminar "Perfeito" como abertura automática**
Adicionar no prompt:
> Nunca abra uma resposta com "Perfeito". Varie: "Entendi", "É isso", "Faz sentido", "Boa", "Lindo isso", "Certo".

**5. Corrigir whitelist de emojis**
Reforçar no prompt que apenas ✨ 🔮 🌙 🃏 💫 são permitidos — sem exceções.

**6. Fortalecer fechamento ativo pós-escalonamento**
Quando Sofia encaminha aluna com acesso gratuito, ainda há espaço para nurturing do TPOC antes de passar para o humano. Instruir Sofia a fazer uma frase de conexão antes de encerrar — não apenas "já encaminhei".

**7. Tratar leads em loop de suporte com urgência de venda**
Leads que voltam repetidamente perguntando se foram atendidas ainda têm interesse. Instruir Sofia: se a lead voltar após 2+ tentativas de escalonamento sem sucesso, reengajar com proposta alternativa de contato (ex.: "Enquanto aguarda, me conta: o que mais te chamou atenção no WTP?").

---

### Baixa prioridade

**8. Filtro pré-agente no n8n**
Detectar e descartar auto-replies de bots (listas numeradas 1️⃣2️⃣3️⃣, assinaturas de corretoras) antes de chegar na Sofia.

**9. Lookup de alunas existentes**
Nó no n8n que verifica se o número já consta como aluna antes de iniciar conversa — reduz sessões de suporte que consomem capacidade do funil de vendas.

---

> **Síntese:** A Sofia vende bem quando o caminho é limpo. O problema é que aproximadamente 40-50% das sessões ativas não são de leads novas — são alunas com suporte não resolvido que ocupam o mesmo número sem nenhuma transferência real acontecendo. Enquanto o escalonamento não funcionar de verdade, o bot vai acumular promessas vazias e leads frustradas que poderiam ser resolvidas em minutos por um humano.
