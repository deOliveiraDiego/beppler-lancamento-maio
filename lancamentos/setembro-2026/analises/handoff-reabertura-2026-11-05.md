# Handoff — Sofia na Reabertura Relâmpago (09/11 → 19/11)

Escrito em 05/11/2026. Fatos do cliente em `briefing/reabertura-relampago.md`.

## Onde paramos

1. 04/11: enviadas ao Carlos (privado) 6 perguntas sobre a reabertura. Ele respondeu tudo no mesmo dia (ver briefing).
2. Decidido focar em deixar a Sofia pronta para o dia 09 **antes** de planejar o pós-fechamento e o downsell.
3. Pergunta do boleto (links TMB) fica para **depois** de ajustar o que já temos.

## Decisão: como ligar a Sofia na hora da abertura

**Problema:** a Fê abre ao vivo, sem horário fixo. Quem sabe a hora é a equipe da EAM. Pedir para abrirem o
Unnichat, acharem o workflow e ativarem é lento demais.

**Solução: um link de um toque**, fixado no grupo `✨ IA | EAM ✨`.

- Unnichat **não tem API pública conhecida** para ligar/desligar agente (busca em 04/11 não achou). Por isso o
  liga/desliga fica no n8n.
- Diego confirmou: com o Unnichat ligado e o workflow do n8n **desligado**, nada acontece e o fluxo do grupo VIP
  não é afetado.

**Desenho:**

1. Workflow novo **"Ligar Sofia"**: Webhook GET com token secreto →
   nó n8n "Activate workflow" (alvo: `Vendas - Sofia`, id `_wikb5rfhy_A9I5katNq7`) →
   grava hora da abertura no Redis (ex.: `sofia:setembro:reabertura:aberto_em`) →
   avisa no grupo da IA ("Sofia ligada às HH:MM") →
   responde na tela "Sofia ligada às HH:MM ✅".
2. `bonus.js` e `links.js` leem `aberto_em` do Redis (via node antes do agente, como o fluxo do prompt de teste).
3. **Antes do dia 09, nesta ordem:** desligar `Vendas - Sofia` no n8n → religar a Sofia no Unnichat.
   Ordem invertida = Sofia responde antes da hora.
4. Testar o link apontando para o workflow de teste antes de usar em produção.

Estimativa: ~1h30.

**Bloqueios para começar:**
- [ ] Chave da API do n8n (Settings › n8n API) ou credencial "n8n API" existente.
- [ ] Ok do Diego para mexer em produção (passo 3).

> Descartado: painel com seletor de estado (complexo demais); cliente religar no Unnichat (lento);
> modo silencioso com workflow ativo (desnecessário, já que workflow desligado não atrapalha).

## Checklist "Sofia redonda" para o dia 09

1. [ ] **`bonus.js`**: só 2 bônus — 30 min Kit Mandinguinha + frete; 1h leitura de Ano Novo. Janela a partir de `aberto_em`. Remover Passaporte, Caixa Mágica, Retiro e repescagem.
2. [ ] **`links.js`**: status `aberto` na reabertura (gate por `aberto_em`), preços de cartão iguais, boleto 18x com valores novos (aluna 302,79 + 17x; não aluna 378,54 + 17x). Fechamento interno 19/11 23:59. Links TMB: manter os de setembro até o Carlos confirmar.
3. [ ] **`base-de-conhecimento.md`**: cursos e bônus de 31/10 (Rituais vira "já existe"; Caixa Rápido vira bônus; Retiro e bônus de setembro fora).
4. [ ] **`prompt.md`**: urgência sem data ("pode fechar a qualquer momento"); "Quero participar…" após a abertura = venda com link; seção BOLETO com valores da tool.
   - **Bug achado:** linhas ~58 e ~202 mandam enviar `link_aluna` / `link_lead`, campos que a tool não devolve desde setembro. Corrigir.
   - `agente-tpoc/CLAUDE.md` ainda cita status `"encerrado"`; o atual é `"pre_reabertura"`. Atualizar.
5. [ ] **Testes**: bateria no agente de teste → `./make-teste.sh` → colar em prod.

## Pendências com o cliente (perguntar depois dos ajustes)

- [ ] Links de boleto TMB (aluna/não aluna, desde 28/09) continuam valendo com os valores novos?
- [ ] Semana pós-fechamento: página e valores continuam os mesmos quando a Sofia liberar o link?
- [ ] Informações do downsell.
- [ ] Combinar com a equipe: quem toca no link "Ligar Sofia" na hora da abertura.

## Depois do dia 19 (não planejado ainda)

- Semana pós-fechamento: "vou verificar com a gerência" + link depois. Ideia do Diego: automação que envia o
  link após alguns minutos (n8n Wait). Alternativa discutida: avisar no grupo e liberar se ninguém bloquear.
  A Sofia não consegue esperar entre mensagens sozinha.
- Depois da primeira semana: tudo para atendimento humano.
- Downsell.
