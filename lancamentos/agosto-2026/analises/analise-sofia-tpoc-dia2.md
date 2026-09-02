# Análise Sofia TPOC — Lançamento Agosto/2026 (Dia 2 · 13/08)

## Escopo

Esta análise usa duas fontes:

1. Tabela `n8n_chat_histories_tpoc_tests` (plural). Esta tabela é a viva. Ela tem 3.302 mensagens.
2. Prompt e tools na pasta `agente-tpoc/`.

A tabela `n8n_chat_histories_tpoc_test` (singular) ficou de fora. Ela mistura lançamentos e agentes antigos.

## Conclusões principais

1. A tool `verificarAlunaPorEmail` foi desconectada. Resolvido.
2. A tool `get_bonus` tem 4 erros antigos no banco. As linhas não têm data. O node atual está limpo. Monitorar.
3. A base de objeções não cobre "fiz o WTP, tenho desconto?". Esta dúvida é recorrente.
4. A tool `get_conhecimento` devolve 7,5KB por chamada. Desperdício de tokens.
5. Nenhuma lead ficou sem resposta.

## Dados

Os nomes das tabelas são confusos. Isto atrasou esta análise.

| Tabela | Linhas | Estado | Conteúdo |
|---|---|---|---|
| `n8n_chat_histories_tpoc_tests` (plural) | 3.302 | viva | Agosto/2026 |
| `n8n_chat_histories_tpoc_test` (singular) | 21.760 | parada | misto: maio, outros agentes |
| `n8n_chat_histories_tpoc_marco` | 792 | parada | fase antiga |
| `n8n_chat_histories_sofia` | 22.506 | desconhecido | legado |

A tabela singular mistura conteúdo de outros agentes. Por exemplo: análise de copy sobre "café" e "não consigo gravar vídeos".

Ação: usar um padrão de nome. Exemplo: `n8n_chat_histories_<lancamento>_<agente>`. Nunca reusar uma tabela "test".

Hoje adicionei a coluna `created_at`. Ela grava a data só das mensagens novas. As mensagens antigas seguem sem data.

## Falhas técnicas

### `get_bonus` — 4 erros antigos

Fato (verificado no banco): existem 4 respostas de tool com este erro:

```
Cannot assign to read only property 'name' of object
'Error: Node 'Code in JavaScript' hasn't been executed'
```

Cada erro vem depois de uma chamada `get_bonus` com `{"perfil":"publica_geral"}` ou `{"perfil":"aluna_wtp"}`. Os ids são 459 a 537. A tabela tem 3.327 linhas. Os erros estão no início da sequência.

Correção de uma suposição minha: eu afirmei que o código de `get_bonus` referenciava o node `Code in JavaScript`. Isto está errado. O código é auto-contido e limpo. O que restou de maio foi o schema de input da tool. O modelo via e passava `perfil`. A UI do n8n hoje mostra "No parameters are set up to be filled by AI". O schema também está limpo agora.

Limite: as 4 linhas de erro não têm `created_at`. Não dá para saber quando ocorreram. O id mostra a ordem, não o tempo. Portanto, não há prova de que `get_bonus` quebra hoje.

Monitoramento (baseline 13/08, 01h UTC): erros de tool com `created_at` = 0, em 36 mensagens novas. Amostra pequena. Repetir a consulta com mais volume.

```sql
SELECT count(*) FROM n8n_chat_histories_tpoc_tests
WHERE message->>'type'='tool'
  AND (message->>'content') ILIKE '%error%'
  AND created_at IS NOT NULL;
```

### `verificarAlunaPorEmail` — resolvido

Fato: a tool foi chamada 10 vezes. A última chamada está no id 656. Ela devolvia `{"encontrada":true}`.

O modelo chamou a tool com e-mails reais (andreiac13@, carolgalindo27@, cristianethurypsi@). Também chamou com uma pergunta de bônus. Isto mostra uma tool legada confundindo o modelo.

Estado atual: desconectada. Não há chamadas novas desde o id 656.

Ressalva: se a intenção for atender ex-alunas WTP, crie uma regra no prompt. Não reative a tool legada.

## Objeções

### Falta a objeção "fiz o WTP, tenho desconto?"

"WTP" aparece 201 vezes nas mensagens vivas. "desconto" aparece 11 vezes.

Exemplo real: "Oi, eu fiz o WTP em maio. Soube que tem um desconto especial pra quem fez o WTP".

A base `base-de-objecoes.md` tem 10 objeções. Nenhuma cobre este caso.

Ação: adicionar a objeção 11. Definir a resposta oficial. Adicionar a regra no prompt: quando a lead citar o WTP, confirmar o valor da vaga e seguir para o fechamento. Não prometer desconto.

### Boleto é a segunda dúvida

"boleto" aparece 47 vezes. As leads pedem boleto antes de 14/08 (o gate).

A base cobre o caso (objeção 3). Mas o volume sugere antecipar a resposta: "boleto libera dia 14. Você garante a vaga hoje no PIX ou cartão."

Ação: verificar se a Sofia antecipa esta resposta. Se não, reforçar no prompt.

### "desconto" pedido pela lead não tem rota

A blacklist proíbe "desconto" na saída da Sofia. Mas a lead pode pedir desconto. Não há resposta oficial para este pedido.

Ação: definir a resposta para "tem desconto?" fora do caso WTP. Reforçar o valor do método e o fechamento.

## Eficiência

### `get_conhecimento` devolve 7,5KB por chamada

Foram 66 chamadas hoje. A média é 7.512 caracteres. O máximo é 8.308. A tool devolve a base inteira em toda chamada.

Impacto: ~500KB de tokens por dia. A base inteira também infla o contexto da conversa.

Ação: usar recuperação por trechos (chunking). Ou encurtar a tool para responder só ao tópico. O mesmo vale para `get_objecoes`.

### Memória grava "Calling X with input" como mensagem

As mensagens de chamada de tool ("Calling get_links with input: {...}") ficam gravadas como `type: ai`. Ao recarregar o histórico, isto vira ruído.

Ação: filtrar estas mensagens da memória do AI Agent. Manter só human/ai finais.

### Instrução interna vaza no payload

`links.js` devolve `parcelamento_alternativo: "12x de R$249,78 (usar somente se o banco bloquear 18x)"`. O texto entre parênteses é instrução interna. Se o modelo ecoar, a lead lê o "manual".

Ação: separar o valor da instrução. Usar um campo próprio para a instrução.

### Formato deriva das regras

Na tabela viva, 1.657 mensagens são da Sofia. Destas: 60 passam de 300 caracteres (3,6%), 4 começam com "Perfeito", 6 usam emoji fora da lista.

São violações de regras duras do prompt. O volume é baixo.

Ação (opcional): validar o formato antes de enviar. Ou aceitar a taxa e monitorar.

## Pontos positivos

- Nenhuma lead ficou sem resposta. As 431 sessões terminam com mensagem da Sofia.
- `get_links` funciona. Devolve `status: aberto`, R$2.497 à vista, 18x de R$180,42. Boleto ausente antes de 14/08, como previsto.
- `get_conhecimento` saiu do estado quebrado. Na fase antiga eram 2.837 erros. Hoje são 0.

## Próximos passos

1. ~~Desconectar `verificarAlunaPorEmail`~~ — feito.
2. Monitorar `get_bonus` com a consulta acima. Se "erros com created_at" subir de 0, reabrir o caso.
3. Adicionar a objeção 11 (WTP/desconto) na base e no prompt.
4. Trocar `get_conhecimento`/`get_objecoes` por recuperação por trechos.
5. Padronizar os nomes das tabelas de chat.

> Nota: o n8n MCP desta sessão aponta para outra instância. Qualquer mudança de node é manual na UI do n8n da Beppler.
