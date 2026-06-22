# Plano — Encerramento Pós-Venda da Sofia

**Status:** Planejamento (não executar). Decisão pendente sobre prompt-only vs prompt+workflow.

---

## Diagnóstico

Após a Sofia confirmar pagamento e direcionar a lead para `suporte@fernandabeppler.com.br`, ela continua engajando em conversas educativas (Tarot, arcanos, ritual diário, etc.) que se estendem por horas — e em alguns casos, dias — sem critério de encerramento.

**Magnitude (banco de chat até 09/mai):**

| Sessão | Msgs AI pós-confirmação | Duração pós-conf | Observação |
|---|---|---|---|
| `...5548` | 66 | 7d 19h | Lead disse "Seria isso" (despedida); Sofia perguntou "Pode me dizer o que você quis confirmar exatamente?" |
| `...7258` | 42 | 4d 10h | — |
| `...5909` | 27 | 9h | Caso citado no relatório dia 11–15 |
| `...6158` | 15 | 20min | — |
| `...7814` | 15 | 19min | — |
| `...2618` | 14 | 31min | — |
| ...+5 sessões | 5–13 cada | minutos a horas | — |

**Total:** 11 sessões com 5+ mensagens AI desnecessárias pós-confirmação. ~226 mensagens AI gastas em loop pós-venda.

---

## Mecânica do bug (dois eixos)

1. **Falha de leitura de despedida.** Sinais como "Seria isso", "Ok 🙏", "valeu", "tá bom", "obrigada" não são reconhecidos como fim de turno. Sofia interpreta como gancho para nova pergunta.

2. **Convite proativo a nova conversa.** Frases como _"Se depois quiser aproveitar melhor o WTP, me chama por aqui, tá?"_ abrem deliberadamente porta para nova engajamento.

**Conflito com o prompt atual:** a regra explícita _"NUNCA termine uma mensagem com frase passiva sem direcionamento"_ + _"NUNCA reaja passivamente — sempre conduza"_ **incentivam** o comportamento atual. Para encerrar, é preciso uma **exceção** que sobreponha essas regras em contexto pós-venda.

---

## Por que está fora do padrão da Sofia

A Sofia é consultora de **vendas WTP**. Após a venda concluída + canal de suporte direcionado, o lead está formalmente fora do escopo de vendas:

- A informação operacional (acesso, materiais, confirmação) só pode vir de `suporte@fernandabeppler.com.br`
- A continuação da conversa não pode oferecer nada que mova a lead em direção à venda (já comprou) nem em direção ao suporte (não é o canal certo)
- O loop educativo é, no melhor caso, **gentil**; no pior caso, **competitivo com canais oficiais** (a aluna pode ficar com a expectativa de tirar dúvidas pelo WhatsApp em vez do e-mail).

---

## Opções

### Opção A — Prompt-only (regra de encerramento explícita)

Adicionar nova seção em `CONTEXTO ESPECÍFICO`:

```markdown
### ENCERRAMENTO PÓS-VENDA

**Quando aplicar:** Lead confirmou pagamento (PIX feito, "já paguei", "à vista") E você já direcionou para `suporte@fernandabeppler.com.br`.

**Ação:**
- Despedir-se em UMA mensagem curta com agradecimento e parar.
- NÃO fazer nova pergunta. NÃO oferecer "se quiser saber mais sobre o WTP".
- Reconhecer estes sinais de despedida e fechar imediatamente: "ok", "tá", "obrigada", "valeu", "show", "seria isso", emojis 🙏 / 👍.
- Esta regra **sobrepõe** "NUNCA reaja passivamente" e "NUNCA termine com frase passiva sem direcionamento".

**Exemplos:**
- Lead: "Ok 🙏" → Sofia: "Show. Boa imersão por lá." (FIM — não perguntar mais nada)
- Lead: "Seria isso" → Sofia: "Beleza. Qualquer coisa, me chama por aqui." (FIM)
```

**Prós:**
- Simples. Mantém a Sofia como único agente. Sem mudança de stack.
- Reversível em segundos (só editar o prompt).

**Contras:**
- Modelo já viola regras explícitas (ex: "Perfeito" persiste em 15,6% mesmo proibido). Não é certo que seguirá esta regra de forma confiável.
- Adiciona mais 1 regra de "exceção que sobrepõe outra regra" — complexidade cognitiva sobe.

### Opção B — Prompt + Workflow (guard rail no workflow)

Mesma regra do prompt + adicionar **node de detecção** no workflow n8n que:
1. Detecta confirmação de pagamento (regex + match com "Já paguei", "Sim. Já fiz um pix", "Pago à vista", etc.).
2. Após N mensagens AI subsequentes (ex: ≥ 2), **encerra a sessão** ou para de responder.

**Prós:**
- Garantia determinística — não depende do modelo seguir a regra.
- Possível registrar evento de "venda concluída" no banco.

**Contras:**
- Complexidade alta. Pode encerrar conversas legítimas (ex: aluna que pagou e tem dúvida real de produto, não de suporte).
- Requer instrumentação no workflow + testes.
- Confirmação de pagamento via texto é frágil — falsos positivos são prováveis.

### Opção C — Workflow-only (encerramento puro por tempo/turnos)

Sem mexer no prompt, adicionar regra no workflow: após X minutos de inatividade do lead pós-confirmação OU Y mensagens AI sem resposta humana com conteúdo, encerrar sessão.

**Prós:**
- Não mexe no prompt.
- Determinístico.

**Contras:**
- Encerra também conversas onde o lead pode voltar legitimamente.
- Não resolve o convite proativo da Sofia para nova conversa (o problema continua acontecendo dentro da janela ativa).

---

## Recomendação

**Começar pela Opção A (prompt-only).** Justificativa:

1. É a abordagem alinhada com a régua "o que está dentro do escopo da Sofia". Encerramento gracioso é comportamento de comunicação — pertence ao prompt.
2. Antes de instrumentar o workflow, é preciso saber se o modelo consegue obedecer a regra. Se não conseguir (medir após 1–2 semanas), aí sim escalar para Opção B.
3. A medição existente (sessões com pós-confirmação ≥ 5 msgs AI) já serve como métrica de sucesso.

**Caso de teste:** P10 do `testes-roteamento-suporte.md` (lead que paga à vista e tenta se despedir) — designado para capturar exatamente esse comportamento.

---

## Próximos passos (quando decidir executar)

1. Validar o fix do "Perfeito" primeiro — ver se o modelo absorve regra explícita com exemplos.
2. Se sim: aplicar Opção A no prompt da Sofia (n8n).
3. Rodar P10 do arquivo de testes.
4. Medir taxa de encerramento limpo (sem nova pergunta após confirmação) por 1 semana.
5. Se < 80% de aderência, escalar para Opção B (workflow guard rail).

---

## Métricas para acompanhar

- **% de sessões com confirmação que terminam em ≤ 1 msg AI pós-direcionamento** (alvo: ≥ 80%)
- **Mensagens AI desnecessárias pós-conf por sessão** (alvo: ≤ 2)
- **Taxa de despedidas reconhecidas** (lead manda "ok" / 🙏 → Sofia encerra) (alvo: 100%)
