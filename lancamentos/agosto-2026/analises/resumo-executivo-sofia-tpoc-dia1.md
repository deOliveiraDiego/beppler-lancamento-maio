# Resumo Executivo — Sofia TPOC (Dia 1 · 12/08)

## Números do dia

| Métrica | Valor |
|---|---|
| Leads atendidas | 433 |
| Mensagens trocadas | 3.342 |
| Leads sem resposta | 0 |
| Erros de tool | 4 (antigos, sem data) |

Objeções mais frequentes (mensagens das leads):

| Objeção | Ocorrências |
|---|---|
| Preço / "tá caro" | 54 |
| Boleto | 47 |
| Ex-aluna do WTP | 30 |
| Adiar / esperar | 23 |
| Parcelamento | 21 |
| Desconto / cupom | 11 |

## Situação

A Sofia está ao vivo e atendendo. Nenhuma lead ficou sem resposta. O preço (R$2.497) e o link estão corretos. O boleto segue bloqueado até 14/08, como definido no briefing.

## Decisões necessárias

### 1. Ex-alunas do WTP pedem desconto

30 leads que fizeram o WTP em maio perguntam se existe desconto ou condição especial.

Hoje a Sofia pede o e-mail do cadastro e fala em "condições de aluna". O briefing desta turma não define condição especial para ex-alunas do WTP. O preço é único.

A Sofia está insinuando um benefício que não existe.

Necessário: definir a resposta oficial. Existe condição especial para ex-alunas do WTP, ou não?

### 2. Boleto tem alta procura antes do dia 14

"boleto" aparece em 47 conversas, antes do gate de 14/08.

A Sofia responde que o boleto libera só dia 14. Ela pode antecipar a alternativa (PIX ou cartão).

Necessário: liberar a Sofia para oferecer PIX e cartão de forma ativa?

## Observações técnicas

- `get_bonus`: 4 erros antigos no banco, sem data. O node atual está limpo. Monitorando (baseline 0 erros novos).
- `get_conhecimento`: devolve a base inteira (7,5KB) a cada chamada. Desperdício de tokens e de contexto.

## Resolvido

- `verificarAlunaPorEmail`: desconectada. Era chamada 10 vezes.

## Próximos passos

1. Definir a resposta oficial para ex-alunas do WTP.
2. Decidir a abordagem do boleto.
3. Encurtar `get_conhecimento`.
