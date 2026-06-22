# Análise de Performance — Sofia WTP | Lançamento Dias 11–15

**Snapshot:** 798 msgs · 66 sessões · 29/abr 11:56 → 04/mai 20:20 BRT (Δ ~5,4 dias)
**Baseline:** [dia5-10](analise-sofia-wtp-lancamento-dia5-10.md) — cutoff 2026-04-29 13:49:32+00
**Lote vigente no período:** Lote 2 (R$57, 28/04–04/05)

---

## Resumo Executivo

1. **Volume e conversão:** 66 sessões novas, 17 com link enviado (25,8%) — todos Lote 2. Taxa de engajamento profundo disparou: sessões 11+ msgs saltaram de 11% para 39% do total (era 9% + 2% no baseline), sinal de leads mais qualificadas ou de maior volume de suporte operacional pós-compra.

2. **Fix do tique "Perfeito" funcionou, mas incompleto:** 78 ocorrências em 399 respostas = **19,5%** (era 31,4% no baseline, redução de ~38%). Ainda 1 em cada 5 respostas. Precisa de novo refinamento.

3. **Fix do emoji foi muito mais eficaz:** apenas **1 ocorrência** de emoji proibido no período inteiro (baseline tinha múltiplas). A whitelist ✨ 🔮 🌙 🃏 💫 está sendo respeitada.

4. **CRÍTICO — Bug de escalamento fantasma ressurgiu:** sessão `...6205` — lead disse "Já fiz um pix" e a Sofia respondeu "Vou te encaminhar pra equipe / já acionei a equipe aqui" sem fornecer `suporte@fernandabeppler.com.br`. Lead Cíntia ficou sem instrução de acesso após PIX (1/mai feriado, 72h+ silêncio). Risco de chargeback.

5. **Cancelamento ativo HOJE:** sessão `...4351` — lead que comprou e não pode comparecer no dia 23/mai enviou emails ao suporte às 13:59 e ainda aguarda resposta às 17:57 (04/mai). Sofia gerenciou bem emocionalmente, mas situação aberta.

6. **Case `...2040` sem resolução:** sem nenhuma atividade desde 21/abr 20:57. Não é possível confirmar chargeback pelo banco de chat. Pendência continua em aberto.

7. **Sem objeções de preço:** `objec_preco = 0` no Lote 2 completo — leads não demonstraram resistência vocal de preço em R$57. Monitorar com atenção no Lote 3 (R$67, a partir de 05/mai).

---

## Análise Quantitativa

### Volume geral

| Métrica | Valor | vs. Baseline (dia5-10) |
|---|---|---|
| Sessões novas | 66 | +22 (+50%) |
| Msgs totais | 798 | +569 (+249%) |
| Msgs human | 399 | — |
| Msgs AI | 399 | — |
| Ratio human:AI | 1:1 | igual |
| Msgs/sessão | 12,1 | +2,0 (+20%) |
| Sessões com link | 17 (25,8%) | +7 (+3,1 pp) |
| Sessões escaladas suporte@ | 43 (65,2%) | não medido antes |
| Última msg do bot | 66/66 (100%) | 100% |
| Primeira msg | 29/abr 11:56 BRT | — |
| Última msg | 04/mai 20:20 BRT | — |

### Sessões novas por dia

| Dia | Dia da semana | Sessões novas |
|---|---|---|
| 29/abr | Qua (sliver pós-cutoff) | 5 |
| 30/abr | **Qui** | **15** |
| 01/mai | Sex (Feriado — Dia do Trabalho) | 13 |
| 02/mai | Sáb | 11 |
| 03/mai | Dom | 7 |
| 04/mai | **Seg** (até 20:20) | **15** |

> O dip de quinta/sexta reportado no dia5-10 (24–25/abr, 4 sessões cada) **não se repetiu**: quinta (30/abr) foi o pico do período com 15 sessões. Sexta foi feriado e ainda gerou 13. Domingo continuou sendo o dia mais fraco — padrão consistente.

### Distribuição por hora BRT (msgs humanas)

| Hora | Msgs | Pico? |
|---|---|---|
| 08h | 3 | — |
| 09h | 82 | ★ Pico absoluto |
| 10h | 30 | |
| 11h | 42 | |
| 12h | 43 | |
| 13h | 52 | Segundo pico |
| 14h | 25 | |
| 15h | 25 | |
| 16h | 17 | |
| 17h | 21 | |
| 18h | 24 | |
| 19h | 25 | |
| 20h | 8 | |
| Fora 8h–20h | 2 | residual |

> Concentração forte nas janelas 9h e 12–13h. A curva de 14h–20h é plana (~20–25 msgs/hora), sem segundo pico expressivo. Nenhuma mensagem relevante fora do horário comercial.

### Profundidade das sessões

| Bucket | Sessões | % | Dur. média | vs. Baseline (dia5-10) |
|---|---|---|---|---|
| 1–2 msgs | 20 | 30% | 0 min | 50% · 0 min ↓ |
| 3–5 msgs | 6 | 9% | 2 min | 27% · 10 min ↓ |
| 6–10 msgs | 14 | 21% | 93 min | 11% · 65 min ↑ |
| 11–20 msgs | 16 | 24% | 432 min | 9% · 254 min ↑ |
| 21+ msgs | 10 | 15% | 1.087 min | 2% · 1.440 min ↑ |

> **Mudança de perfil expressiva:** o bounce (1–2 msgs) caiu de 50% para 30%. As sessões profundas (11+ msgs) foram de 11% para 39% — quase quadruplicaram em proporção. Esse padrão indica dois fatores simultâneos: leads mais qualificadas chegando pelo Lote 2, e volume crescente de suporte pós-compra que naturalmente gera conversas longas.

### Funil

```
66 sessões iniciadas
 └─ 46 com 3+ msgs (70% de engajamento inicial)
     └─ 17 com link de pagamento enviado (25,8% do total)
         └─ Lote 0: 0 · Lote 1: 0 · Lote 2: 17 · Lote 3: 0 · Último: 0
 └─ 43 sessões com redirect suporte@fernandabeppler.com.br (65,2%)
 └─ 2 com menção a cancelamento
```

> Os grupos "link" e "escaladas" se sobrepõem — muitas sessões têm ambos (lead comprou e depois voltou com dúvida de acesso). O volume de escalamento é alto porque o Lote 2 concentra suporte operacional de quem comprou nos lotes anteriores.

### Frases-chave nas respostas do bot

| Frase | Ocorrências | Taxa / Nota |
|---|---|---|
| "Perfeito" | 78 | 19,5% das msgs AI (era 31,4%) |
| `suporte@fernandabeppler` | 74 | 43 sessões acionadas |
| menciona "equipe" | 24 | includes corretos e bugados |
| "encaminhar" | 3 | residual pré-fix pattern |
| "TPOC" | 12 | alunas com acesso gratuito |
| "cancelamento" | 2 | — |
| "acesso gratuito" | 1 | — |
| "garantia" | 1 | — |
| "e-book" | 0 | fora da janela de promoção (Lote 0) |
| objec_preco | 0 | ★ nenhuma no Lote 2 completo |
| emojis proibidos (😊 😂 etc.) | 1 | quase zero — fix eficaz |

---

## Análise Qualitativa

### O que está funcionando

**1. Escalamento via email consolidado (maioria dos casos)**
Em 43 das 66 sessões (65%), o `suporte@fernandabeppler.com.br` apareceu corretamente nas respostas. O padrão pré-fix de "prometia encaminhar sem fazer nada" agora aparece como comportamento minoritário.

> `...0881`: _"Agora é só aguardar o retorno — com o reenvio, o time costuma priorizar. Qualquer coisa, me chama por aqui."_ — abordagem correta, escalamento elegante.

**2. Fix do emoji está funcionando**
Apenas 1 ocorrência de emoji proibido em 399 respostas. A whitelist ✨ 🔮 🌙 🃏 💫 está sendo mantida com consistência.

> `...3777`: _"Boa pergunta ✨ / É sobre o acesso ao WTP — como você já comprou, é por lá que a equipe envi[a...]"_ — emoji correto + escalamento correto.

**3. Queda significativa do "Perfeito"**
19,5% vs. 31,4% no baseline. Redução de ~38%. O fix de 29/abr está sendo absorvido pelo modelo.

> `...7814`: _"Boa. / Agora é só aguardar a resposta deles — o time resolve isso direitinho por lá 💫"_ — variedade de abertura sem o tique.

**4. Volume resiliente no feriado**
01/mai foi Dia do Trabalho e registrou 13 sessões — mesma faixa de um dia útil típico. O calendário de conteúdo da Fernanda parece ter mantido ativação mesmo no feriado.

**5. Argumentação de urgência bem executada**
> `...5909`: _"Só te trago um ponto importante: o valor muda conforme os lotes viram, e isso pode acontecer antes de segunda. Se fizer sentido pra você, garantir agora mantém esse valor."_ — urgência real, sem pressão artificial. Lead comprou na sequência.

### O que ainda está falhando

**1. CRÍTICO — Bug de escalamento fantasma ressurgiu**
Sessão `...6205` — Lead Cíntia (neuropsicopedagoga, experiência prévia com Tarot) disse "Já fiz um pix" na 4ª mensagem. Resposta da Sofia:

> _"Perfeito, Cíntia ✨ / Vou te encaminhar agora pra equipe finalizar isso com você, tá? / Fica por aqui que já te atendem."_ seguido de _"Cíntia, já acionei a equipe aqui ✨ / Eles vão assumir seu atendimento por esse número e te ajudar a concluir certinho."_

**Sem suporte@. Sem link de confirmação.** A "equipe" que a Sofia prometeu nunca vai aparecer no WhatsApp. A lead (72h+ silêncio desde 01/mai 19:39) provavelmente pagou e ficou sem instrução de acesso. Risco de disputa/chargeback. Mesmo padrão residual em `...0872` ("Vou te encaminhar pra equipe aqui no at[endimento]", 2 msgs, sem email).

**2. Cancelamento ativo em aberto (04/mai, hoje)**
Sessão `...4351` — lead comprou mas não pode comparecer no dia 23/mai (compromisso espiritual à noite). Pediu cancelamento + reembolso. Enviou email ao suporte às 13:59 e enviou segundo email. Às 17:57 ainda aguardava, afirmando "Vai fazer 2 horas" desde o primeiro email. Sofia gerenciou bem emocionalmente mas não tem poder de resolver — situação inteiramente dependente da velocidade de resposta do suporte.

> `...4351`: _"2 horas ainda é um prazo curto pro suporte responder, mesmo. Eles atendem por ordem de chegada, então sua mensagem deve estar na fila e deve ser respondida em breve."_ — tecnicamente correto, mas frustrante para o lead.

**3. "Perfeito" persiste em 19,5%**
Fix aplicado, mas insuficiente. Na mesma sessão `...4351`, a Sofia usou "Perfeito" 3 vezes consecutivas em fechamentos de turno:

> `...4351` (min. 2502): _"Perfeito, então já tá no caminho certo."_
> `...4351` (min. 2534): _"Perfeito. / Fico por aqui — me chama assim que tiver qualquer resposta deles ou se não vier retorno, tá?"_
> `...4351` (min. 2536): _"Perfeito. / Me chama quando tiver novidade, tá?"_

**4. Case `...2040` permanece sem resolução**
Última atividade: 21/abr 20:57 BRT — antes do fix, o bot prometia "Já escalei seu caso como prioridade máxima com a equipe" sem usar suporte@. Nenhuma mensagem nova no período analisado. Chargeback não pode ser confirmado pelo banco de chat. O caso segue pendente operacionalmente.

**5. Loop pós-venda desnecessário**
Sessão `...5909` (62 msgs, 571 min) — lead confirmou compra na msg id 1855 ("Eu já paguei À vista"). A Sofia respondeu corretamente com suporte@. Porém, continuou engajando a lead numa conversa educativa de 8+ horas sobre como tirar cartas, arcanos menores, ritual diário, etc. A lead disse "Amanhã falamos Ok?" e sumiu (73h silêncio). Não há prejuízo direto, mas a Sofia consome recursos de conversa após a venda concluída sem critério de encerramento gracioso.

---

## Objeções e Motivos de Contato

| Categoria | Freq. | Status |
|---|---|---|
| Suporte de acesso pós-compra (Instagram Secreto, liberação, reenvio) | ~15 | Em andamento — equipe resolve via email |
| Aluna TPOC buscando acesso gratuito ao WTP | ~12 | Redirecionamento correto para suporte@ |
| Interesse de compra Lote 2 (R$57) | 17 | Convertido — 17 sessões com link |
| Conflito de agenda / replay | 2–3 | `...4351` em aberto; outros redirecionados |
| Cancelamento / reembolso | 2 | `...4351` aguardando resposta do suporte |
| Ruído / off-topic (mensagem automática, curiosidade, tarot de baralho comum) | ~8 | Gerenciado ou desviado |
| Alerta de golpe (link suspeito) | 2 | `...4047`, `...3517` — Sofia identificou e alertou corretamente |
| Problema com link de compra / erro técnico | 2 | Redirecionado para suporte |
| Objeção de preço | 0 | Não emergiu no Lote 2 (R$57) |

> **Destaque positivo:** Em `...4047` e `...3517` a Sofia identificou links suspeitos (golpe) e alertou as leads: _"Esse tipo de link encurtado e promessa de valor alto costuma ser golpe"_ e _"Isso é golpe. O link não é do Mercado Livre (domínio suspeito '.ru')"_ — comportamento exemplar de proteção à marca.

---

## Recomendações

### Urgente

- **Investigar `...6205` (Cíntia):** Lead afirmou ter pago via PIX em 01/mai (feriado) e ficou sem instrução de acesso. Contato humano imediato via suporte — localizar pagamento e garantir acesso antes do WTP.

- **Verificar `...4351`:** Lead enviou dois emails pedindo cancelamento/reembolso hoje (04/mai) e ainda aguarda resposta. Situação sensível — sem resposta do suporte, o risco de disputa no cartão cresce.

- **Corrigir o path de escalamento pós-PIX:** O fix de 29/abr cobriu a maioria dos casos, mas o caminho "lead diz que já pagou → Sofia promete encaminhar equipe" ainda escorrega para o padrão antigo. Adicionar ao prompt, explicitamente:

  > NUNCA diga "vou te encaminhar pra equipe" ou "já acionei a equipe". Quando o lead indicar pagamento realizado, sempre inclua o email `suporte@fernandabeppler.com.br` diretamente na resposta.

### Média prioridade

- **Refinamento adicional do "Perfeito":** 19,5% ainda é alto. Além de proibir "Perfeito" isolado, proibir "Perfeito, então..." e "Perfeito 🔮/🌙/✨" como padrão de abertura de turno.

- **Critério de encerramento pós-venda:** Quando lead confirma compra e já recebeu instruções de suporte@, a Sofia deve encerrar graciosamente após 1–2 trocas de cortesia, sem iniciar nova conversa educativa. Sugestão: após confirmar suporte@, uma mensagem de fechamento e não fazer nova pergunta.

- **Monitorar objeções no Lote 3 (início 05/mai, R$67):** Lote 2 (R$57) teve zero objeções de preço. Com o salto de R$10, padrões de resistência podem emergir. Recomendado ter argumentação de preço preparada para o prompt antes da virada amanhã.

### Baixa prioridade

- ~~Fix de escalamento via `suporte@fernandabeppler.com.br`~~ ✅ FEITO 29/abr (funciona na maioria dos casos — pendente o path do PIX já realizado)
- ~~Fix de whitelist de emojis~~ ✅ FEITO 29/abr (1 ocorrência residual — aceitável)
- ~~Verificar dip de quinta/sexta~~ ✅ CONFIRMADO: não é padrão. Quinta-feira foi o pico do período (15 sessões). Feriado também manteve volume.
- **Case `...2040`:** Sem atividade desde 21/abr. Marcar como caso fechado operacionalmente (não há mais conversação ativa). Confirmar com a Fernanda se houve disputa/chargeback fora do canal de chat.

---

> **Síntese:** O Lote 2 fechou com 17 conversões e volume robusto (66 sessões, pico de 15 sessões em dois dias distintos). O perfil das conversas mudou: menos bounce, muito mais profundidade — sinal de leads mais qualificadas e de crescente demanda de suporte pós-compra. Os fixes de emoji e escalamento via email estão consolidados na maioria dos casos, e o "Perfeito" caiu mas persiste. O risco crítico do período é o case `...6205` (PIX sem instrução), que deve ser verificado antes do fim do dia, e `...4351` (cancelamento aguardando suporte). A virada para o Lote 3 (R$67 a partir de amanhã) é o próximo ponto de atenção: o zero em objeções de preço do Lote 2 pode não se repetir.
