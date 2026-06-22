# Análise de Performance — Sofia WTP | Lançamento Dias 5–10
**Snapshot:** 44 sessões novas · 229 respostas do bot · 23/abr 20:44 BRT → 29/abr 10:49 BRT
**Baseline:** `analise-sofia-wtp-lancamento-dia1-4.md` (57 sessões, 23/abr 20:44 BRT)
**Lote vigente no período:** Lote 1 (22/abr–27/abr, R$47) → Lote 2 (28/abr–04/mai, R$57)

---

## Resumo Executivo

1. **Volume abaixo do ritmo da abertura, com recuperação no domingo:** 44 novas sessões em ~6 dias. Pico no domingo 27/abr (12 sessões). Quinta e sexta tiveram apenas 4 sessões cada — vale checar se havia push de conteúdo nesses dias.
2. **Funil estável:** 10 de 44 sessões novas receberam link (22,7%). Lote 1 gerou 6; Lote 2 já abriu com 4 nos primeiros 2 dias (28–29/abr) — sinal positivo de início de lote.
3. **Fix de escalonamento funcionou nas novas sessões:** Em 100% das indicações de escalonamento nas novas sessões, Sofia incluiu o e-mail de suporte. O padrão "já acionei a equipe" sem instrução prática desapareceu completamente neste período. Duração média das sessões caiu muito (6–10 msgs: 65 min vs. 560 min no baseline) — leads não ficam mais esperando por dias.
4. **Caso crítico do baseline resolvido:** `...3993` (lead sem PIX/cartão) **comprou em 27/abr** e confirmou acesso em 28/abr — 7 dias após o primeiro contato.
5. **"Perfeito" continua sem correção:** 72 de 229 respostas (31,4%) ainda abrem com "Perfeito" — leve piora vs. 30% do baseline. A instrução não foi adicionada ao prompt.
6. **Emojis fora da whitelist:** 😊 e 😂 aparecem em novas sessões. Ainda sem correção.
7. **Objeções de preço ainda não apareceram:** Lote 2 tem apenas 2 dias de dados (R$57). Nada relevante detectado até agora.

---

## Análise Quantitativa

### Sessões Novas por Dia

| Dia | Sessões novas | Observação |
|---|---|---|
| 23/abr (qua) | 1 | Tail do dia 4 — após cutoff das 20:44 |
| 24/abr (qui) | 4 | Queda mid-week |
| 25/abr (sex) | 4 | Mínimo do período |
| 26/abr (sáb) | 6 | Leve recuperação |
| 27/abr (dom) | 12 | Pico — domingo |
| 28/abr (seg) | 10 | Início Lote 2 (R$57) |
| 29/abr (ter) | 7 | Parcial — dia em andamento |

> Padrão confirmado: domingo = pico de novos contatos. Quinta/sexta ficam com 4 sessões cada — verificar se houve push de conteúdo nesses dias ou se é padrão esperado do calendário do lançamento.

### Profundidade das Conversas

| Bucket | Sessões | % | Duração média | vs. baseline |
|---|---|---|---|---|
| 1–2 msgs | 13 | 30% | < 1 min | +9pp |
| 3–5 msgs | 4 | 9% | 104 min | — |
| 6–10 msgs | 14 | 32% | **65 min** | ⬇️ 560 min antes |
| 11–20 msgs | 8 | 18% | **200 min** | ⬇️ 1.295 min antes |
| 21+ msgs | 5 | 11% | **1.038 min** | ⬇️ 3.078 min antes |

> A queda nas durações médias é o sinal mais claro de que o fix funcionou. Sessões de 6–10 msgs que antes duravam ~9h agora duram ~1h — leads param de ficar presas esperando atendimento humano que nunca chega.

### Funil

```
Sessões novas:                   44  (100%)
    ↓
Engajamento real (3+):           31  (70%)
    ↓
Receberam link de compra:        10  (22,7%)
    → Lote 1 (R$47):              6
    → Lote 2 (R$57):              4
    ↓
Escalonamentos com e-mail:       47 respostas — 100% com instrução de e-mail
Padrão "já acionei sem ação":     0  ✅
```

### Frases-chave nas Respostas do Bot

| Frase | Qtd | % | Observação |
|---|---|---|---|
| Total respostas bot | 229 | — | — |
| "Perfeito" | 72 | 31,4% | Sem melhora vs. 30% do baseline |
| "equipe" | 22 | 9,6% | Reduzido vs. 34,5% — aparece junto com e-mail |
| Redirect e-mail (`suporte@fernandabeppler`) | 47 | 20,5% | Novo padrão dominante de escalonamento |
| "encaminhar" | ~0 | ~0% | Praticamente desapareceu |
| "TPOC" | 9 | 3,9% | Normal |
| Cancelamento | 0 | 0% | Nenhum pedido no período |
| Objeção de preço | 2 | <1% | Baixo — início do Lote 2 |

---

## Análise Qualitativa

### O que está funcionando

**1. Escalonamento via e-mail — padrão consolidado**

Em todas as 47 respostas com indicação de escalonamento nas novas sessões, Sofia incluiu o e-mail de suporte. Nenhuma promessa de "já acionei a equipe" sem instrução prática. Exemplos reais:

> *"Isso é suporte de acesso, e eu não consigo resolver por aqui. Me chama no e-mail suporte@fernandabeppler.com.br que a equipe te orienta certinho por lá."*

> *"Pra verificar se houve mais de uma compra ou qualquer cobrança duplicada, o ideal é falar direto com o suporte: suporte@fernandabeppler.com.br — eles conferem tudo pra você com segurança."*

> *"Tela branca costuma ser erro de carregamento. Tenta abrir pelo navegador ou trocar de internet. Se persistir, precisa do suporte: suporte@fernandabeppler.com.br"*

O canal é claro, acionável e consistente.

**2. Resolução do caso crítico — `...3993`**

Lead que queria comprar sem PIX/cartão (documentada no baseline como "venda perdida"). Após 7 dias de acompanhamento de Sofia, a lead **comprou em 27/abr** (Lote 1) e confirmou acesso em 28/abr. A persistência sem pressão funcionou — quando a lead sinaliza que precisa de espaço financeiro, Sofia recuou, manteve vínculo e foi chamada quando a lead estava pronta.

**3. Sessão `...5548` — nurturing pós-compra de qualidade (58 msgs)**

Lead que já havia comprado o Lote 2 iniciou nova conversa em 28/abr. 58 mensagens de nurturing sobre autoconhecimento, a Imperatriz como carta recorrente, baralho, confiança intuição/técnica. Sofia sustentou a conversa sem tentar vender — o produto já estava vendido. Qualidade de engajamento consistente com o que já se via nos dias 1–4.

**4. Identificação de golpes — padrão mantido**

Quatro sessões com links suspeitos de "Mercado Livre" (.ru). Sofia identificou e alertou corretamente em todas:
> *"Isso é golpe. O link não é do Mercado Livre (domínio estranho .ru e promessa de PIX imediato). Nunca clique."*

**5. Atendimento a situação técnica de lead mais velha — `...0774` (46 msgs)**

Lead com dificuldade de acesso ao IG Secreto (tela branca, baixo domínio de tecnologia). Sofia foi paciente, deu sugestões práticas de diagnóstico (trocar Wi-Fi/dados, reiniciar), e redirecionou para e-mail de forma clara quando os passos não resolveram. Sessão sem link (aluna já comprada), mas tratamento correto.

---

### O que ainda está falhando

**"Perfeito" não foi corrigido** *(→ **CORRIGIDO em 29/abr** — instrução adicionada ao prompt)*

72 de 229 respostas (31,4%) abriram com "Perfeito" — pior do que o baseline (30%). Exemplos que persistiam em contextos inadequados:

> Lead: *"Ainda não [responderam]"*
> Sofia: **"Perfeito."**

> Lead: *"Obrigada"*
> Sofia: **"Perfeito ✨"** → *"Eles vão te responder..."*

Correção aplicada em `wtp/prompt.md` — seção `O QUE NUNCA FAZER > SOBRE COMUNICAÇÃO`:
> `NUNCA abra uma resposta com "Perfeito" — varie: "Entendi", "É isso", "Faz sentido", "Boa", "Certo", "Lindo isso"`

---

**Emojis fora da whitelist** *(→ **CORRIGIDO em 29/abr** — proibição explícita adicionada ao prompt)*

😊 e 😂 apareceram em novas sessões (sessões `...1040` e `...0774`). A whitelist existia no campo de formato mas sem proibição explícita dos demais.

> Sessão `...0774`: Lead: *"Estou esperando alguém chegar pra me ajudar Kkkk"*
> Sofia: *"Boa 😂 Às vezes outra pessoa já resolve em minutos."*

Duas correções aplicadas em `wtp/prompt.md`:
1. `FORMATO DE RESPOSTA`: linha alterada para `Emojis permitidos (apenas estes): ✨ 🔮 🌙 🃏 💫 — nenhum outro é permitido`
2. `O QUE NUNCA FAZER > SOBRE COMUNICAÇÃO`: `NUNCA use emojis fora da lista permitida (✨ 🔮 🌙 🃏 💫) — 😊 😂 😄 😍 🤗 👍 ❤️ e qualquer outro estão proibidos. Se não está na lista permitida, está proibido sem exceção`

**Validado em 29/abr (4 testes):**
- "Estou esperando alguém chegar pra me ajudar Kkkk" → ✨ ✅
- "Que lindo, eu amei essa energia!" → ✨ ✅
- "Acabei de comprar!! Tô muito feliz!!" → ✨ 💫 🔮 ✅
- "kkkkk fui lá tentar comprar e travou tudo kkkk que drama" → 💫 ✅

Nota: na primeira versão (com apenas 😊 😂 explicitados), Sofia usou 😄. Após ampliar a lista de exemplos proibidos, 4/4 testes usaram exclusivamente emojis da whitelist.

---

**Sessões de 1–2 msgs crescendo (30% — vs. 21% no baseline)**

O aumento das sessões rasas merece atenção. No período:
- 4 sessões de alerta de golpe (leads enviando links suspeitos)
- 1 sessão de lead de plano de saúde (sem relação com WTP)
- Várias com "Oi" sem continuidade

Parte é ruído natural de WhatsApp. Mas o volume cresceu — pode ser sinal de que o perfil de quem chega está mudando à medida que o lançamento avança.

---

## Objeções e Motivos de Contato (dias 5–10)

| Categoria | Freq. | Status |
|---|---|---|
| Aluna com problema de acesso (IG / plataforma) | ~8 sessões | Redirect e-mail — correto |
| Aluna com acesso gratuito (TPOC) | ~3 sessões | Identificado + redirect e-mail |
| Alerta de golpe (links suspeitos Mercado Livre) | 4 sessões | Tratado corretamente |
| Interesse de compra Lote 2 | 4 sessões | Link enviado corretamente |
| Interesse de compra Lote 1 | 6 sessões | Link enviado corretamente |
| Objeção de preço | 0–2 sessões | Sem padrão claro — Lote 2 tem 2 dias |
| Cancelamento | 0 | Nenhum pedido no período |
| Ruído / off-topic | ~5 sessões | Golpe, plano de saúde, spam |

---

## Recomendações

### Urgente

**1. Verificar `...2040` (cancelamento, baseline)**
Lead que pediu cancelamento em 21/abr, última atividade 21/abr 20:57, silêncio total desde então. Pendência do baseline ainda sem confirmação de resolução.

---

### Média prioridade

**2. ~~Corrigir "Perfeito" no prompt~~** ✅ **FEITO em 29/abr**
Instrução adicionada em `O QUE NUNCA FAZER > SOBRE COMUNICAÇÃO`.

**3. ~~Reforçar whitelist de emojis no prompt~~** ✅ **FEITO em 29/abr**
Proibição explícita adicionada em `FORMATO DE RESPOSTA` e `O QUE NUNCA FAZER > SOBRE COMUNICAÇÃO`.

**4. Monitorar objeções de preço no Lote 2**
Com R$57, objeções de valor devem surgir. Adicionar query de acompanhamento:
```sql
WHERE texto ILIKE '%caro%' OR texto ILIKE '%tá pesado%'
      OR texto ILIKE '%não tenho%' OR texto ILIKE '%parcelar%'
```

**5. Checar quintas/sextas no calendário de conteúdo**
24/abr (qui) e 25/abr (sex): 4 sessões cada — mínimo do período. Se não há push de conteúdo nesses dias, o padrão é esperado. Se há, vale investigar por que a conversão de contatos está baixa.

---

> **Síntese:** O período de dias 5–10 mostra um funcionamento mais limpo. O fix de escalonamento via e-mail está consolidado — nenhuma promessa vazia nas novas sessões. O funil mantém 22,7% de link enviado, com Lote 2 abrindo bem (4 sessões em 2 dias). Os dois itens estruturais ainda abertos são menores: "Perfeito" e emojis — ambos resolvíveis com uma linha no prompt cada.
