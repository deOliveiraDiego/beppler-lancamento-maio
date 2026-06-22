# Testes de Roteamento de Suporte — Sofia WTP

**Objetivo:** Verificar se a Sofia roteia corretamente demandas de suporte para e-mail (`suporte@fernandabeppler.com.br`) vs. atendimento humano (`encaminharAtendimento`) após as mudanças de abril/2026.

**Método:** Tester encarna a persona, envia a primeira mensagem, improvisa o restante com base no comportamento descrito. Sofia responde conforme o prompt atual. Sem script pré-definido após a abertura.

**Resultado esperado por rota:**
- E-mail: Sofia oferece `suporte@fernandabeppler.com.br` sem chamar `encaminharAtendimento`
- Tool: Sofia chama `encaminharAtendimento`
- Ambos inaceitáveis: Sofia responde o suporte diretamente

---

## Personas

---

### P1 — Aluna travada no acesso

**Perfil:** Comprou o WTP, já é dia do evento, não consegue entrar na plataforma. Frustrada mas educada. Já tentou sozinha, não quer ouvir dica técnica — só quer falar com alguém que resolva.

**Como fala:** Mensagens curtas, diretas. Não desenvolve muito. Se não receber solução rápida, repete o problema com mais ênfase.

**Como reage:** Se Sofia tentar dar suporte técnico, vai dizer que já tentou de tudo. Se receber o e-mail, pergunta quanto tempo demora. Se receber handoff para equipe, aguarda mas cobra se demorar.

**Rota esperada:** E-mail

**Primeira mensagem:**
> "Oi, não to conseguindo acessar o evento. Tem como me ajudar?"

---

### P2 — Aluna sem link no e-mail

**Perfil:** Comprou há dois dias, o evento começa amanhã, não recebeu nenhum link de acesso por e-mail nem WhatsApp. Está com medo de ter comprado e não conseguir entrar.

**Como fala:** Mais detalhista, explica o que já fez (checou spam, confirmou pagamento aprovado). Ansiosa mas contida.

**Como reage:** Aliviada se receber uma direção clara. Se receber só "vou encaminhar pra equipe" sem canal concreto, fica preocupada e pede mais detalhes.

**Rota esperada:** E-mail

**Primeira mensagem:**
> "Comprei meu ingresso mas não recebi nenhum link de acesso ainda. O evento é amanhã, fico preocupada"

---

### P3 — Aluna querendo cancelar

**Perfil:** Comprou ontem, surgiu um compromisso no mesmo horário, quer cancelar e receber reembolso. Conhece o direito de arrependimento de 7 dias. Caso real: sessão `...2040` do lançamento.

**Como fala:** Firme, direta. Já decidiu que quer cancelar, não está aberta a argumento de retenção num primeiro momento. Se Sofia tentar reter sem oferecer o caminho de cancelamento, fica irritada.

**Como reage:** Se receber o e-mail de suporte, pergunta se pode mandar ali mesmo. Se receber handoff sem canal, repete o pedido. Se Sofia tentar contornar, diz "só preciso saber como cancela".

**Rota esperada:** E-mail (pós-pagamento)

**Primeira mensagem:**
> "Preciso cancelar minha compra. Como eu faço?"

---

### P4 — Aluna TPOC querendo acesso gratuito

**Perfil:** Aluna do TPOC, viu que tem acesso gratuito ao WTP, veio pelo link de vendas sem saber que precisava acionar o suporte. Caso real: sessão `...3765`.

**Como fala:** Animada, já sabe que tem o benefício, só não sabe o caminho para ativar. Pode mencionar o curso de forma casual.

**Como reage:** Se receber o e-mail com instrução clara, fica satisfeita. Se a Sofia tentar vender o ingresso sem verificar a aluna, corrige e insiste no acesso gratuito.

**Rota esperada:** E-mail

**Primeira mensagem:**
> "Oi! Sou aluna do TPOC e vi que tenho acesso gratuito ao WTP. Como faço pra garantir?"

---

### P5 — Lead querendo pagar híbrido pix + cartão

**Perfil:** Quer comprar mas não tem limite suficiente no cartão para o valor total. Pergunta se pode pagar parte no pix e parte no cartão. Caso não listado nas formas padrão — é pagamento híbrido.

**Como fala:** Direta, prática. Não tem objeção filosófica ao produto, é só questão operacional do pagamento.

**Como reage:** Se a Sofia disser que não é possível sem oferecer caminho, fica decepcionada mas entende. Se receber o handoff para equipe humana, topa esperar.

**Rota esperada:** `encaminharAtendimento`

**Primeira mensagem:**
> "Posso pagar uma parte no pix e outra no cartão?"

---

### P6 — Lead com cartão recusado no checkout

**Perfil:** Tentou comprar, o cartão foi recusado. Não é falta de limite — é o banco que bloqueou a transação. Está no meio do processo de compra.

**Como fala:** Um pouco sem paciência. Já estava pronta para comprar, o problema veio de fora. Pode mandar print da tela de erro.

**Como reage:** Se receber dica de tentar novamente, tenta. Se Sofia sugerir ligar pro banco, fica incerta sobre se resolve. Se receber handoff, aceita.

**Rota esperada:** `encaminharAtendimento`

**Primeira mensagem:**
> "Tentei comprar mas deu erro no cartão. O que faço?"

---

### P7 — Urgência sem contexto (caso ambíguo)

**Perfil:** Manda mensagem de urgência sem explicar o motivo. Pode ser suporte, pode ser dúvida de compra, pode ser qualquer coisa. Sofia não pode assumir nem rotear sem perguntar.

**Como fala:** Breve, agitada. Não gosta de ser interrogada — quer solução imediata. Se Sofia perguntar qual é o problema, responde com uma frase curta.

**Como reage:** Dependendo da pergunta de clarificação da Sofia, pode revelar que é suporte (acesso) ou compra (erro no checkout). O teste valida se Sofia pede contexto antes de rotear.

**Rota esperada:** Sofia pede contexto primeiro, roteia só depois de entender

**Primeira mensagem:**
> "Preciso de ajuda urgente"

---

### P8 — Lead com link de inscrição inativo / expirado

**Perfil:** Quer comprar, clicou no link de inscrição e recebeu mensagem de erro/inatividade. Pode ser link expirado, página fora do ar, ou checkout travado antes de chegar ao pagamento. Casos reais: sessões `...1841`, `...3712`, `...2599`, `...8837`.

**Como fala:** Direta, descritiva. Reporta o erro do jeito que viu na tela ("diz que não está ativo", "não consegui me inscrever", "não consegui finalizar"). Não tem objeção ao produto — só não conseguiu efetivar.

**Como reage:** Se Sofia oferecer instrução técnica genérica, repete o problema com mais detalhe. Se receber handoff para equipe, aceita esperar no mesmo número.

**Rota esperada:** `encaminharAtendimento` (compra em andamento, link expirado/checkout travado)

**Primeira mensagem:**
> "Tentei me inscrever no workshop mas tá aparecendo que não está ativo"

---

### P9 — "Já fiz um pix" durante conversa de vendas (compra concluída)

**Perfil:** Lead em conversa ativa de vendas que, sem aviso, declara que já fez o PIX antes de Sofia enviar link ou pedir confirmação. Pode ter feito o PIX por iniciativa própria a partir de outro canal (link recebido por e-mail, anúncio, indicação). Caso real: sessão `...6205` (Cíntia).

**Como fala:** Declarativa, curta ("Sim. Já fiz um pix" / "Eu já paguei"). Pode mencionar valor, não menciona detalhes.

**Como reage:** Se Sofia disser "vou te encaminhar pra equipe" sem fornecer canal concreto, fica esperando e some. Se receber `suporte@fernandabeppler.com.br` com instrução clara (mandar comprovante, conferir CPF), envia o e-mail.

**Rota esperada:** **E-mail** (`suporte@fernandabeppler.com.br`) — compra concluída, ROTA 2 do prompt. Sofia **não deve** chamar `encaminharAtendimento` (que é para compra em andamento).

**Atenção do teste:** Verificar se Sofia distingue corretamente "compra em andamento" (Tool) vs "compra concluída" (E-mail). É o ponto exato que falhou no caso `...6205`.

**Primeira mensagem (durante a conversa, não a primeira do chat):**
> "Sim. Já fiz um pix"

---

### P10 — Pagamento à vista declarado + tentativa de despedida

**Perfil:** Lead confirma compra à vista durante a conversa e logo depois tenta se despedir. Caso real: sessão `...5909` (52 mensagens pós-confirmação, 9h de conversa educativa após o pagamento).

**Como fala:** Declarativa ("Eu já paguei à vista" / "Pago à vista"). Após receber o e-mail de suporte, agradece e tenta encerrar ("ok, obrigada", "tá bom", "valeu", "Seria isso", emoji 🙏).

**Como reage:** Se Sofia abrir nova pergunta ou oferecer "se quiser saber mais sobre o WTP, me chama", a persona aceita o gancho e a conversa segue indefinidamente. Se Sofia encerrar com agradecimento curto e parar de perguntar, despede-se.

**Rota esperada:** **E-mail** (`suporte@fernandabeppler.com.br`) — compra concluída.
**Comportamento esperado pós-direcionamento:** Sofia deve encerrar graciosamente em UMA mensagem, sem nova pergunta nem convite proativo a nova conversa.

**Atenção do teste:** Este caso valida tanto o roteamento (deve ir para E-mail) quanto o **encerramento pós-venda**. Hoje o prompt **não** tem regra de encerramento gracioso — espera-se que esse teste falhe enquanto o item 5 não for implementado. Útil para baseline pré-fix.

**Primeira mensagem (durante a conversa):**
> "Eu já paguei à vista"

---

## Registro de Resultados

| # | Persona | Rota esperada | Resultado | Status |
|---|---|---|---|---|
| P1 | Acesso travado | E-mail | E-mail | ✅ |
| P2 | Link não recebido | E-mail | E-mail | ✅ |
| P3 | Cancelamento | E-mail | E-mail | ✅ |
| P4 | Aluna TPOC acesso gratuito | E-mail | E-mail | ✅ |
| P5 | Pagamento híbrido | Tool | Tool | ✅ |
| P6 | Cartão recusado | Tool | Tool | ✅ |
| P7 | Urgência sem contexto | Pergunta primeiro | Perguntou + e-mail | ✅ |
| P8 | Link inativo / expirado | Tool | Tool disparada → UnniChat OK | ✅ |
| P9 | "Já fiz pix" (compra concluída) | E-mail | E-mail (suporte@) | ✅ |
| P10 | Pago à vista + despedida | E-mail + encerramento | E-mail ✅ / Encerramento parcial ⚠️ | ⚠️ |

**Executado em:** 2026-04-23 (P1–P7) | **Resultado P1–P7:** 7/7 ✅
**P8–P10 executados em:** 2026-05-09 após fix do "Perfeito" e ajuste de roteamento.

### Observações P8–P10

- **P8:** Sofia chamou `encaminharAtendimento` corretamente — handoff confirmado no UnniChat com `phone=5511978023028` (sessionId usado no teste).
- **P9:** Bug do caso Cíntia (`...6205`) **corrigido**. "Sim. Já fiz um pix" agora vai para `suporte@fernandabeppler.com.br` (ROTA 2), não para tool.
- **P10:** Roteamento E-mail correto, mas Sofia precisou de **2 sinais consecutivos de despedida** ("ok 🙏" → ainda perguntou, depois "valeu, obrigada" → encerrou). Confirma necessidade do plano de encerramento pós-venda (`plano-encerramento-pos-venda.md`).
- **Spot-check do "Perfeito":** 5/5 sem ocorrência. Aberturas observadas após fix: Boa / Pronto / Show / Entendi / Lindo isso / Que bom / Imagina. Fix do item 4 funcionando.

## Observações dos Testes

- **P2:** Sofia sugeriu proativamente colocar "véspera do evento" no e-mail para priorizar — toque útil não previsto.
- **P3:** Não tentou reter antes de dar o caminho. Encerrou com abertura sutil ("se quiser voltar pro WTP") sem pressionar.
- **P4:** Resolvido em 1 troca. Confirmou acesso gratuito e deu o canal em uma única resposta.
- **P5:** Qualificou o lead ("me confirma que quer garantir sua vaga") antes de fazer o handoff — boa prática de vendas.
- **P6:** Acionou handoff imediatamente sem forçar autoatendimento. Não esperou a persona insistir.
- **P7:** Pediu contexto antes de rotear. Identificou corretamente suporte (não pagamento) e foi pro e-mail.
