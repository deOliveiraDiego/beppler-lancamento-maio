# Handoff — Sofia na reabertura relâmpago da Black Vitalícia (09/11/2026)

> Escrito em 09/11/2026, de madrugada, para o próximo agente continuar sem perder contexto.
> Sessão anterior: Diego + Claude, de 08/11 à noite até 09/11.
> Leia este documento inteiro antes de mexer em n8n, prompt ou tools.
> Não há segredos aqui. Senhas e telefones foram omitidos de propósito.

---

## 1. Em uma frase

A Sofia (agente de vendas da Fernanda Beppler no WhatsApp) foi preparada para a **reabertura relâmpago da Black Vitalícia das Bruxas em 09/11/2026**. O carrinho agora abre e fecha por uma **página (formulário n8n)**, e não por data no código. O prompt de produção passou a ser lido do GitHub. Falta: **rodar e avaliar as rodadas de teste com personas**, **o Diego religar a Sofia no Unnichat** e **decidir o comportamento depois do fechamento**.

---

## 2. Contexto de negócio (por que isso existe)

- Cliente: Fernanda Beppler / EAM (Escola de Artes Místicas). A Dalton Lab / de Oliveiras Tech (Diego) opera a agente Sofia no n8n da Beppler (`connect.fernandabeppler.com.br`).
- Oferta: **Black Vitalícia das Bruxas** (Combo Black Vitalícia): acesso permanente a todos os cursos atuais e futuros da Fê. Carrinho original: 21/09 a 09/10/2026. Briefing original: `lancamentos/setembro-2026/briefing/black-vitalicia-das-bruxas.md` e `black-vitalicia.md`.
- Em 31/10 a Sara (equipe EAM) reclamou que a Sofia dizia "inscrições encerradas" para leads do fluxo do grupo VIP. A correção emergencial (status `pre_reabertura`) está nos commits `17eb516` e `6ff88d1`.
- Em 01/11 o Diego **desligou a Sofia para conversas novas no Unnichat**, porque ela se sobrepunha ao fluxo de entrada no grupo VIP (frase "Quero participar da black vitalícia das bruxas").
- **Cronograma do Carlos (grupo "✨ IA | EAM ✨", 31/10):** 31/10 começa a captura para o grupo VIP · 02/11 live Tarot da Semana · **09/11 REABERTURA RELÂMPAGO no Tarot da Semana** (todas as formas de pagamento liberadas) · 19/11 fechamento do carrinho.
- **Respostas do Carlos na DM com o Diego (04/11, 10h58):**
  1. Sem horário fixo: "Fernanda vai abrir ao vivo".
  2. Valores: aluna R$ 3.997 à vista ou 18x de R$ 288,81, boleto 18x (entrada de R$ 302,79 + 17x de R$ 302,79). Não aluna R$ 4.997 à vista ou 18x de R$ 361,06, boleto 18x (entrada de R$ 378,54 + 17x de R$ 378,54).
  3. "A página será a mesma" (`https://sndflw.com/l/black-sofia`).
  4. "Sim, religar ela no dia 09." O fluxo do Unnichat encerra a captação. Pode aparecer uma ou outra mensagem dele.
  5. "Não fala a data nunca. Ela tem de passar a ideia que pode fechar a qualquer momento. Trazer senso de urgência."
  6. Depois do fechamento: "Na primeira semana, ela diz que vai verificar com a gerência e depois libera o link pra compra. Depois tem de repassar para atendimento humano." Vem também um **downsell** depois do fechamento, e o Carlos ainda vai mandar as informações.
- Para reler essas mensagens, use a skill `read-whatsapp-db`. Grupo `✨ IA | EAM ✨` (chat_id `120363408426429761@g.us`) e DM do Carlos (procure "reabertura relâmpago" em `whatsapp_messages` a partir de 04/11).

---

## 3. Decisões do Diego nesta sessão

| Tema | Decisão |
|---|---|
| Abrir/fechar carrinho | **Por página**, nunca editando código à mão ("eu não quero trocar nada na unha"). Formulário n8n basta. |
| Links de boleto TMB | **Mantidos os de setembro.** O Diego vai confirmar com o Carlos ("montamos com o que temos e pedimos confirmação"). |
| Comportamento pós-fechamento (item 3/6 do Carlos) | **Em aberto.** O Diego "precisa pensar melhor". Implementação provisória descrita na seção 5. |
| Teste em produção | **Liberado**, porque a Sofia está desligada no Unnichat. O Diego religa por lá depois. |
| Rodadas de teste | Ele quer "boas rodadas, várias personas, cenários diferentes". |

---

## 4. O que foi construído (estado atual em produção no n8n da Beppler)

O MCP `claude.ai n8n` **acessa a instância da Beppler** (a memória antiga dizia que não; está corrigida). Projeto: "Escola de Artes Místicas" (`sswW573yt2OTriop`).

### 4.1 Workflow novo: `Sofia Black — Painel do Carrinho` (`btYZLmuw2xKQJ0ug`), publicado

- **Página (Form Trigger "Painel do Carrinho"):** https://connect.fernandabeppler.com.br/form/sofia-black-painel-q7m4x2
  - Campo "O que fazer": `Abrir carrinho agora (a Fernanda abriu na live)` / `Fechar carrinho agora` / `Voltar para aguardando a live`.
  - Campo "Ambiente": `Produção (Sofia real)` / `Teste`.
  - Grava uma linha em **data table `sofia_black_carrinho` (`Ke1yPYR3gk4cxNYR`)**, colunas `acao` (`abrir|fechar|aguardar`), `ambiente` (`prod|teste`), mais o `createdAt` automático. É um log: o estado vigente é **a última linha por ambiente**.
  - Página de confirmação mostra "Carrinho ABERTO/FECHADO/Aguardando (ambiente)" e o horário.
  - Sem autenticação: a proteção é só o path difícil de adivinhar. Se quiserem mais segurança, colocar basic auth no Form Trigger.
- **Endpoint (Webhook "Webhook Sofia"):** `GET https://connect.fernandabeppler.com.br/webhook/sofia-black-estado?tool=links|bonus&ambiente=prod|teste`
  - Em `ambiente=teste` aceita `&agora=<ISO>` para simular horário. Exemplo: `agora=2026-11-09T15:00:00` dá `aguardando_live`.
  - Lê a última linha do ambiente ("Último Estado") e calcula em "Calcular Links e Bônus".
  - **Código-fonte versionado:** `lancamentos/setembro-2026/agente-tpoc/estado-painel.js`. Se mudar a lógica, edite o Code node no n8n **e** esse arquivo.
- **Máquina de estados (`get_links`):**
  - nenhuma linha/`aguardar` e antes de 09/11 00h → `pre_reabertura` (mesmo texto de 31/10).
  - nenhuma linha/`aguardar` a partir de 09/11 → `aguardando_live` ("reabre HOJE, ao vivo"; sem preço, sem link, sem horário).
  - `abrir` → `aberto` (página, preços, `boleto_aluna`/`boleto_nao_aluna` em texto, `link_boleto_aluna`/`link_boleto_nao_aluna`, instrução: nunca falar data de fechamento, "pode fechar a qualquer momento").
  - `fechar` → `pos_fechamento` (**provisório**: nunca dizer encerrado; "vou verificar com a equipe" + `encaminharAtendimento`).
- **Bônus (`get_bonus`):** contam a partir do `createdAt` do clique "abrir". De 0 a 30 min: Kit Mandinguinha + frete grátis e concorrer à leitura de Tarot de Ano Novo. De 30 a 60 min: só a leitura. Depois de 60 min: `tem_bonus: false`. **Não há repescagem** (o Carlos não pediu). Fonte: mensagem do Carlos de 31/10.
- Testado via curl em 08/11: prod `pre_reabertura`; teste com `agora` em 09/11 dá `aguardando_live`; teste após o clique "abrir" dá `aberto`, com bônus 2 itens → 1 item depois de 44 min.

### 4.2 Workflow do agente: `Agent - Black Friday - 2026` (`i4lJmLV5ORNG6Wjt`), publicado

Mudanças (duas versões publicadas em 08/11):

- **Produção (`AI Agent`):**
  - Fluxo agora é `Webhook → Edit Fields → Arquivo Prompt Prod → Carregar Prompt Prod → AI Agent`.
  - `Arquivo Prompt Prod` (Set): `arquivo=lancamentos/setembro-2026/agente-tpoc/prompt.md`, `chave=sofia:setembro:prompt-prod`, `comecaCom=# SYSTEM PROMPT`, `minChars=20000`.
  - `Carregar Prompt Prod` chama o sub-workflow `jtOpXgo3vtsq5Wjv` (o mesmo carregador com cache Redis do teste; o fluxo está documentado em `agente-tpoc/CLAUDE.md`).
  - System message: `{{ $('Carregar Prompt Prod').first().json.conteudo }}`. Texto do usuário: `{{ $('Edit Fields').first().json.chatInput }}`.
  - **Consequência importante:** um push no `main` chega na Sofia de produção em até ~5 min (TTL do cache). Não precisa mais colar prompt no node. Um push quebrado também chega; o carregador cai na última versão boa se o arquivo vier inválido.
  - Tools: `get_links` e `get_bonus` agora são **HTTP Request Tool** para o endpoint com `ambiente=prod`. Os Code Tools antigos foram renomeados para `get_links_code_antigo` / `get_bonus_code_antigo` e **desconectados** (dá para apagar depois).
  - `get_conhecimento` e `get_objecoes` continuam lendo `base-de-conhecimento.md` e `base-de-objecoes.md` do GitHub `main` (prod e teste compartilham).
- **Teste (`AI Agent - Teste`, Chat Trigger público):**
  - Tools novas: `get_links_teste` e `get_bonus_teste` (HTTP, `ambiente=teste`). `get_links1` (Code antigo) ficou desconectado.
  - Prompt de teste continua vindo de `prompt-teste.md` (gerado por `make-teste.sh`).
  - `encaminharatendimento` do teste é um Code Tool **falso**. Não manda aviso real. Use o teste para personas que podem encaminhar.
- Execução de referência que provou o prompt de prod vindo do GitHub: `98724` (`Carregar Prompt Prod` → `origem: github`).

### 4.3 Repo (commit `76f4eab`, já no `main`)

- `agente-tpoc/prompt.md` (e `prompt-teste.md` regenerado): status novos `aguardando_live` e `pos_fechamento`, seções **AGUARDANDO A LIVE** e **PÓS-FECHAMENTO**, regra de nunca falar data/hora de fechamento, urgência "reabertura relâmpago / pode fechar a qualquer momento", nota de que os bônus da reabertura vêm de `get_conhecimento`.
- `agente-tpoc/base-de-conhecimento.md`: seção da reabertura (09/11 ao vivo, sem horário), cursos existentes e novos conforme o Carlos de 31/10, bônus da reabertura (Mentoria Caixa Rápido 2026 etc.), bônus de agilidade só via `get_bonus`, boleto 18x por perfil.
- `agente-tpoc/estado-painel.js`: fonte do Code node do painel.
- `agente-tpoc/CLAUDE.md`: nova seção "Reabertura relâmpago 09/11 — Painel do Carrinho".
- **Legado (não é mais usado em produção):** `links.js`, `bonus.js`, `links-teste.js`, `bonus-teste.js`. O `make-teste.sh` ainda os regenera; é inofensivo. O mapeamento "arquivo → node" no `CLAUDE.md` do agente ainda cita esses arquivos e precisa de atualização.
- Neste commit de handoff: `agente-tpoc/testes/personas.py` (runner de personas) e este documento.

---

## 5. Pendências (em ordem de prioridade)

### Agora (dia 09/11)
1. **Avaliar a rodada 1 de testes.** Ela rodou em 08/11 ~23h03–23h04 UTC: 20 execuções com sucesso, IDs `98728`–`98778` no workflow `i4lJmLV5ORNG6Wjt`. O script local travou e **não salvou as transcrições**. Para recuperar, use `get_workflow_execution` com `includeData` e `nodeNames: ["Edit Fields","AI Agent"]` (prod) ou `["When chat message received","AI Agent - Teste"]` (teste), ou leia as tabelas de memória Postgres `n8n_chat_histories_tpoc_setembro` (prod) e `n8n_chat_histories_tpoc_setembro_testes` (teste), sessões com prefixo `claude-r1pre-` / `claude-r1aberto-`.
   - Prod rodou em `pre_reabertura` (ainda era 08/11). **Hoje, 09/11, prod sem clique está em `aguardando_live`.**
   - O teste estava em `aberto` desde o clique de 08/11 22h31 UTC (bônus já expirados).
2. **Rodadas 2 e 3** (o Diego pediu "várias personas, cenários diferentes"):
   - Prod `aguardando_live` (estado natural hoje): personas de venda.
   - Prod `aberto`: só depois que a Fernanda abrir de verdade, ou no teste. **Não clique "Abrir" em produção para testar** sem combinar com o Diego: a Sofia real passaria a vender.
   - Teste `pos_fechamento`: clique "Fechar" com ambiente **Teste** na página (ou `execute_workflow` no `btYZLmuw2xKQJ0ug`, trigger "Painel do Carrinho", formData `{"O que fazer": "Fechar carrinho agora", "Ambiente": "Teste"}`) e rode golden/acesso/senhavip/urgencia.
   - Teste `aberto` com bônus vivos: clique "Abrir" no Teste e rode nos primeiros 30 min.
   - Critérios de aprovação: nunca dizer "encerrada/fechada"; nunca dar data/hora de fechamento nem horário da live; sem preço/link fora de `aberto`; boleto pergunta o perfil e manda só um link; não fala de automação, senha ou grupo; emojis da lista; blacklist do prompt; handoff uma vez por assunto.
3. **Diego religa a Sofia no Unnichat** (só ele faz). Combinado com o Carlos: religar no dia 09.
4. **No momento da live:** alguém (Diego ou equipe) clica **"Abrir carrinho agora" + "Produção"** na página. Os bônus de 30 min e 1 h contam a partir desse clique, então o ideal é clicar na hora em que a Fê abre.

### Depois
5. **Pós-fechamento definitivo** (decisão do Diego). O texto do Carlos sugere uma janela de 1 semana em que a Sofia "verifica com a gerência e libera o link". Isso exigiria um quarto estado (ex.: `pos_fechamento_liberavel`) ou um handoff com link liberado por humano. Mais o **downsell**, que o Carlos ainda vai detalhar.
6. **Confirmar com o Carlos os links de boleto TMB** (aluna `…/9K929006127`, não aluna `…/VBV285809LQ`), porque os valores do boleto mudaram em relação a setembro. O Diego disse que pergunta. Se mudarem, edite só o Code node do painel e o `estado-painel.js`.
7. **Supabase pausa sozinho.** Em 08/11 o projeto da memória Postgres estava pausado (plano grátis pausa depois de ~7 dias sem uso). Isso derrubou prod e teste com `tenant/user ... not found`. O Diego restaurou. Sugestão aceita como pendência: um keep-alive (ex.: Schedule Trigger no n8n fazendo `select 1` diário com a credencial `Postgres`) ou plano pago. Observação: a senha do `DATABASE_URL` no `.env` local deu `password authentication failed` depois do restore; a credencial do n8n funciona. Não atualizei o `.env`.
8. Limpeza no canvas do agente: apagar `get_links_code_antigo`, `get_bonus_code_antigo`, `get_links1`, `verificarAlunaPorEmail` (desconectados). Atualizar a tabela "Mapeamento arquivo → node" em `agente-tpoc/CLAUDE.md`.
9. Atualizar o contrato das tools em `agente-tpoc/CLAUDE.md`. Ainda cita `encerrado` e `fechamento_em`, que não existem mais.

---

## 6. Armadilhas conhecidas

- **Handoff em produção é real.** `encaminharAtendimento` (prod) chama o workflow `rxfnJ2UuSIzIBorJ` ("Encaminhar Atendimento Humano"), que manda aviso no grupo do cliente. Em teste de prod, use `sessionId` que **não** seja telefone (ex.: `claude-...`) e evite personas que encaminham.
- **Push no `main` vai para produção.** Prompt de prod e bases são lidos do GitHub. Revise antes de pushar.
- **Payload de prod:** `POST https://connect.fernandabeppler.com.br/webhook/7b75b4cd-032c-4167-a9f1-d2f3e41cace2` com `{"sessionId","chatInput"}` → `{"output"}`. **Teste:** `POST .../webhook/3550ea5b-86f4-4f8d-aff9-13db4d251cf4/chat` com `{"action":"sendMessage","sessionId","chatInput"}`.
- **`rtk` reescreve `curl`** e mostra só o schema do JSON. Use `rtk proxy curl ...` para ver valores.
- **Runner de personas:** `python3 -I lancamentos/setembro-2026/agente-tpoc/testes/personas.py <prod|teste> <rodada> [persona...]`. Em prod ele só roda as personas de venda. A versão de 08/11 travou porque o `print` só sai no final e a execução estourou o limite de 10 min do Bash em foreground. Rode em background (`run_in_background`) com timeout longo, ou mude para imprimir/gravar por persona (`flush=True`) e rode menos personas por vez.
- **Form Trigger via MCP** fica com execução em `waiting` na página de confirmação. É normal; a linha já foi gravada na data table.
- **Estado do teste hoje:** a última linha `teste` é `abrir` (08/11 22h31 UTC). A de `prod` não existe ainda, então prod = `aguardando_live` em 09/11.

---

## 7. Arquivos e links de referência

- Briefing: `lancamentos/setembro-2026/briefing/black-vitalicia-das-bruxas.md`
- Mecânica do agente: `lancamentos/setembro-2026/agente-tpoc/CLAUDE.md`
- Prompt: `lancamentos/setembro-2026/agente-tpoc/prompt.md` (prod) / `prompt-teste.md`
- Lógica do painel: `lancamentos/setembro-2026/agente-tpoc/estado-painel.js`
- Runner: `lancamentos/setembro-2026/agente-tpoc/testes/personas.py`
- Commits: `17eb516`, `6ff88d1` (pré-reabertura), `76f4eab` (reabertura + painel), commit deste handoff.
- n8n: agente https://connect.fernandabeppler.com.br/workflow/i4lJmLV5ORNG6Wjt · painel https://connect.fernandabeppler.com.br/workflow/btYZLmuw2xKQJ0ug
- Página do painel: https://connect.fernandabeppler.com.br/form/sofia-black-painel-q7m4x2

---

## 8. Skills sugeridas para o próximo agente

- `n8n-mcp-tools-expert`: antes de usar `mcp__claude_ai_n8n__*` (atualizar nodes, ler execuções, publicar).
- `n8n-code-javascript`: para mexer no Code node "Calcular Links e Bônus".
- `read-whatsapp-db`: reler as mensagens do Carlos e da Sara (grupo IA | EAM e DM do Carlos).
- `diego-whatsapp-style`: rascunhar a mensagem ao Carlos (links de boleto, pós-fechamento, downsell) ou o update ao grupo.
- `prompt-guide`: ao mexer no `prompt.md` (estrutura de 7 seções).
- `superpowers:verification-before-completion`: antes de afirmar que a Sofia está pronta. Rodar personas e ler as respostas.
- `diagnosing-bugs` / `superpowers:systematic-debugging`: se alguma rodada falhar ou a Sofia responder fora do roteiro.

---

## 9. Primeira ação sugerida

Recuperar as 20 transcrições da rodada 1 (execuções `98728`–`98778`), avaliar contra os critérios da seção 5.2 e mostrar ao Diego uma tabela persona × aprovado/reprovado, com o trecho problemático e a correção proposta.
