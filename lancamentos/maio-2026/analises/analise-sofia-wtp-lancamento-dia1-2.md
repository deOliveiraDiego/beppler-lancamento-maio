# Análise de Performance — Sofia WTP | Lançamento Dia 1–2
**Snapshot:** 406 mensagens · 27 sessões · 20/abr 09:58 BRT → 21/abr 23:24 BRT (~36h)

---

## Resumo Executivo

1. **Volume sólido pra primeira janela:** 27 sessões em 36h, média 15 msgs/sessão, 100% das conversas respondidas. Sofia não deixou nenhuma lead sem resposta.
2. **Funil estreito:** Só 5 sessões (18,5%) chegaram a receber link de compra. A maioria das sessões profundas (21+ msgs) foi de alunas existentes com problemas de acesso, não leads novas.
3. **FALHA CRÍTICA — `encaminharAtendimento` nunca foi chamada:** Em 77 mensagens Sofia diz "vou encaminhar pra equipe" mas a ferramenta jamais foi disparada. Nenhum escalonamento real aconteceu. As leads ficam esperando atendimento que nunca chega.
4. **Caso urgente ativo:** Sessão `...2040` — lead tentando cancelar compra por 20h, Sofia "acionou a equipe" 9 vezes sem efeito. Requer ação humana imediata.
5. **Tom e qualificação muito bons:** Onde o escalonamento não atrapalhou, o funil de qualificação foi fluente, linguagem do nicho precisa, modo FRIA funcional.
6. **"Perfeito" como tique verbal:** 58 de 203 respostas (28,6%) abrem com "Perfeito" — repetitivo, soa robótico.

---

## Análise Quantitativa

### Volume

| Métrica | Valor |
|---|---|
| Total de mensagens | 406 |
| Sessões únicas | 27 |
| Msgs humanas / bot | 203 / 203 (1:1 exato) |
| Média msgs/sessão | 15,0 |
| Sessões com link de compra enviado | 5 (18,5%) |
| Escalonamentos via ferramenta | **0 (ZERO)** ⚠️ |
| Sessões onde última msg é do bot | 27 / 27 (100%) |

### Distribuição por Hora (BRT)

| Período | Msgs | % do total | Observação |
|---|---|---|---|
| 09h–12h | 136 | 33,5% | Maior pico — abertura do dia |
| 15h–18h | 88 | 21,7% | Pico da tarde |
| 22h–23h | 96 | 23,6% | Pico noturno |
| 00h–08h | 34 | 8,4% | Volume baixo |
| 13h–14h | 6 | 1,5% | Quase morto |

### Profundidade das Conversas

| Bucket | Sessões | % |
|---|---|---|
| 1–2 msgs | 7 | 26% |
| 3–5 msgs | 5 | 19% |
| 6–10 msgs | 3 | 11% |
| 11–20 msgs | 5 | 19% |
| 21+ msgs | 7 | **26%** |

26% das sessões são rasas (1-2 msgs: abertura sem continuidade) e 26% são profundas (21+). Das 7 sessões com 21+, pelo menos 4 são alunas existentes com suporte, não conversão nova.

### Funil

```
Sessões iniciadas:        27  (100%)
    ↓
Engajamento real (3+):    20  (74%)
    ↓
Qualificadas → link:       5  (18,5%)
    ↓
Escalonamentos reais:      0  ⚠️  (ferramenta não chamada)
```

---

## Análise Qualitativa

### O que está funcionando

**1. Qualificação e conexão genuína**

O fluxo de vendas quando a lead é nova e engajada é excelente. Exemplo real (sessão `...8067`, 64 msgs em 36 min):

Lead chegou via conteúdo de "38 dias de Tarot" → Sofia qualificou sem empurrar produto → identificou que queria usar o Tarot com a família → enviou link na mensagem 5 da lead. Quando descobriu que a lead já havia comprado, fez post-purchase nurturing de qualidade: trabalhou o medo de "ver espíritos", recomendou baralho RWS, sugeriu exercício de 1 carta/dia e tiragem de 3 cartas. Lead de Londres, 3h30 da manhã — saiu satisfeita.

**2. Modo fria funcional**

Mensagens monossilábicas (Oi, Ok, Sim) foram tratadas sem CTA/link, com 1 pergunta direta — correto conforme o prompt.

**3. Identificação de aluna TPOC**

Sessão `...3765`: Lead informou ser TPOC. Sofia identificou acesso gratuito imediatamente:
> *"Como você já é aluna do TPOC, você tem acesso gratuito ao WTP"*

A intenção foi certa — só a ferramenta de escalonamento que falhou na sequência.

**4. Contenção de objeção de horário**

Sessão `...4877`: Lead queria cancelar por conflito com pós-grad. Sofia respondeu:
> *"Você não precisa assistir tudo perfeito. Mesmo parcial já traz insights. E se não fizer sentido, tem 7 dias de garantia."*

A lead se reinscreveu.

**5. Tom e linguagem do nicho**

Whitelist bem aplicada: "✨", "buscadora", "chamado", "despertar do dom", "ressoou". Blacklist respeitada — não detectei "desconto", "lançamento", "amiga", "tudo no seu tempo" em nenhuma das 203 respostas.

---

### O que está falhando

**CRÍTICO: A ferramenta de escalonamento não funciona**

77 mensagens mencionam "equipe" mas `encaminharAtendimento` foi chamada **zero vezes**. Toda promessa de "já encaminhei para a equipe" é falsa — nenhum ticket criado, nenhum humano notificado.

Prova real — sessão `...2040` (cancelamento, 52 msgs, 20h):

> Lead: *"Esqueci que tenho aula da pós. Tem como cancelar a compra?"*
> Sofia (msg 224): *"Vou te encaminhar agora pra equipe, tá?"*
> *(Lead volta 8 vezes ao longo de 20h: "Ainda não", "Não", "NÂO", "oio"...)*
> Sofia (msg 288): *"Já escalei seu caso como prioridade máxima agora com a equipe."*
> *(Equipe nunca aparece.)*

**Escalonamentos falsos repetidos**

Padrão recorrente em pelo menos 6 sessões. Sofia usa frases como:
- *"Já acionei a equipe novamente agora"*
- *"Vou reforçar agora com urgência"*
- *"Deixei seu caso como prioridade máxima"*

Tudo sem acionar a ferramenta.

**"Perfeito" como resposta automática**

58 de 203 respostas (28,6%) abrem com "Perfeito" — inclusive em contextos inadequados:
> Lead: *"Ainda não [fui atendida]"*
> Sofia: **"Perfeito"** 🌙

**Encerramento passivo**

Várias sessões terminam com frases passivas, contrariando a instrução do prompt ("NUNCA termine com frase passiva"):
- *"Seguimos por aqui ✨"*
- *"Se surgir algo, me chama por aqui, combinado?"*
- *"Qualquer coisa é só me chamar por aqui, tá?"*

**Sofia respondeu uma corretora de imóveis**

Sessão `...2426`: chegou um auto-reply de corretora (lista numerada 1️⃣2️⃣3️⃣, assinatura "Carla, corretora"). Sofia respondeu como se fosse lead legítima. Não é erro grave, mas mostra ausência de filtro pré-agente.

---

## Objeções e Motivos de Contato

| Categoria | Ocorrências | Exemplo real |
|---|---|---|
| Aluna com problema de acesso (ebook/IG secreto/plataforma) | ~4 sessões | *"Tentei acessar, mas ainda não recebi"* |
| Cancelamento de compra | 1 sessão (urgente) | Lead aguardando resolução há 20h+ |
| Conflito de horário | 2 sessões | *"Tenho aula da pós"* |
| Pergunta sobre replay/gravação | 1-2 sessões | Informado corretamente (sem replay; só no TPOC) |
| Aluna com acesso gratuito (TPOC) | 1-2 sessões | Identificado corretamente pela Sofia |
| Curiosidade sobre dom / medo (espíritos) | 1-2 sessões | Tratado muito bem |

---

## Recomendações

### Urgente (resolver hoje)

**1. Atender a sessão do cancelamento agora**
Número: `5521994928040`. Lead aguardando cancelamento de compra há 20h+. Risco de chargeback ou reclamação pública.

**2. Diagnosticar por que `encaminharAtendimento` não é chamada**
Verificar:
- O nó da ferramenta no workflow n8n está ativo e conectado?
- A ferramenta está sendo corretamente registrada no agente?
- Há logs de tool calls no n8n para essa ferramenta?

Se o agente está reconhecendo quando escalonar mas não chama a ferramenta, o fix é no prompt — adicionar reforço:

> **OBRIGATÓRIO:** quando identificar caso de suporte/cancelamento/acesso gratuito, você DEVE chamar `encaminharAtendimento` antes de qualquer resposta. Não apenas diga que vai encaminhar — chame a ferramenta imediatamente. Dizer "vou encaminhar" sem chamar a ferramenta não faz nada.

---

### Média prioridade (próximos dias)

**3. Variar abertura de resposta**
Adicionar instrução no prompt:
> Não abra respostas com "Perfeito" — varie entre: "Entendi", "É isso", "Faz sentido", "Boa", "Lindo isso".

**4. Fortalecer fechamento ativo após escalonamento**
Quando Sofia encaminha aluna com acesso gratuito, há oportunidade de nurturing para o TPOC antes de passar para o humano. Adicionar instrução específica + exemplo no prompt.

**5. Revisar frases de encerramento passivo**
Acrescentar ao prompt exemplos de encerramento ativo para situações pós-escalonamento: em vez de "se precisar me chama", usar uma pergunta direta ou argumento de conexão antes de encerrar.

---

### Baixa prioridade

**6. Filtro pré-agente no n8n**
Adicionar nó de filtro no workflow para detectar padrões de auto-reply (lista numerada 1️⃣2️⃣3️⃣, assinatura de bot/corretora) e descartar antes de chegar na Sofia.

**7. Identificação prévia de leads que já compraram**
Muitas sessões longas foram alunas com problemas de acesso. Um nó de lookup no n8n (checar histórico de compra pelo telefone) reduziria o volume de sessões desperdiçadas com suporte e redirecionaria essas alunas diretamente para o humano.

---

> **Estado geral:** Sofia performa muito bem quando o funil é de venda pura. O problema estrutural é o escalonamento — é onde mais sessões estão presas e onde a experiência quebra. Resolve isso e a qualidade do atendimento muda completamente.
