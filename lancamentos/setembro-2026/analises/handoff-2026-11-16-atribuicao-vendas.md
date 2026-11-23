# Handoff: atribuição de vendas da Sofia na Black (16/11/2026)

> Escrito em 16/11/2026 para retomar quando a Sara (EAM) mandar o export de vendas.
> Não há segredos aqui. A senha do banco fica em `~/.claude/secrets/deoliveiratech.env`.
> O repo é **público**: a saída do script (telefone, e-mail, valores) nunca entra no git.
> O contexto comercial (por que isso importa, proposta, abordagem) está fora do git, em `docs/conta/`. Leia `docs/conta/HANDOFF.md` primeiro, se existir na sua máquina.

---

## 1. Em uma frase

O script que cruza vendas com conversas da Sofia está pronto, testado e já conectado ao banco de conversas. Falta só o **export de vendas do Guru e da TMB**, pedido à Sara no grupo "✨ IA | EAM ✨" em 16/11, para gerar o primeiro número de vendas atribuídas à Sofia.

## 2. Estado em 16/11

| Item | Estado |
|---|---|
| Script `lancamentos/setembro-2026/analytics/atribuicao/atribuicao.py` | Pronto. Só biblioteca padrão do Python + `psql` |
| Testes `test_atribuicao.py` (dados fictícios) | 3 de 3 passando |
| Conexão com o banco de conversas | Ok. Variável `BEPPLER_DATABASE_URL` no arquivo de segredos (atualizada em 16/11, depois do restore de 08/11) |
| Conversas na tabela `n8n_chat_histories_tpoc_setembro` | 3.101 linhas, 382 contatos com telefone, 334 com data, 53 receberam link |
| Export de vendas | **Aguardando a Sara.** Pedido: Guru e TMB de 21/09 a 19/11, com colunas de UTM |

## 3. Como rodar quando o export chegar

1. Salve os arquivos do export em `docs/conta/atribuicao/` (fora do git).
2. Rode na raiz do repo:

```bash
set -a; . ~/.claude/secrets/deoliveiratech.env; set +a
python3 -I lancamentos/setembro-2026/analytics/atribuicao/atribuicao.py \
  --vendas docs/conta/atribuicao/guru.csv docs/conta/atribuicao/tmb.csv \
  --desde 2026-09-21 --ate 2026-11-19
```

3. Leia o resumo no terminal. O detalhe sai em `docs/conta/atribuicao/resumo.json` e `vendas-classificadas.csv`.
4. Se o script avisar coluna não encontrada, indique o nome exato: `--col-telefone "Telefone"`, `--col-valor "Valor"`, `--col-status ...`, `--col-data ...`, `--col-utm-medium ...` etc.

## 4. Como o script classifica cada venda aprovada

Na ordem, a primeira regra que bate:

| Classe | Regra | Conta como |
|---|---|---|
| `utm` | UTM da venda tem `utm_medium=ia`, `ia-vendas` ou "sofia" | Atribuída |
| `link` | Telefone ou e-mail bate com uma sessão que recebeu link da Sofia até 30 dias antes da compra (`--janela-dias`) | Atribuída |
| `conversa` | Bate com sessão que conversou antes da compra, sem link | Influenciada |
| `pos_compra` | A primeira conversa foi depois da compra | Suporte, não venda |
| `sem_contato` | Nenhuma sessão bate | — |

Detalhes do casamento:
- **Telefone:** chave = DDD + últimos 8 dígitos. Tolera DDI 55 e o nono dígito faltando (o Unnichat cortava o 9 em maio).
- **E-mail:** extraído das mensagens da pessoa (`type=human`) na conversa.
- **Link:** resposta da Sofia (`type=ai`) contendo `sndflw.com`, `sendflow.pro`, `clkdmg.site`, `pay.tmb.com.br` ou a página do combo-black.
- **Status:** entra só venda aprovada ou paga. Reembolso, cancelamento, chargeback, boleto pendente e expirado ficam fora.
- **Fuso:** datas do banco vêm em UTC e são convertidas para Brasília. Datas do export são lidas como horário de Brasília.
- Sessões que não são telefone (testes `claude-…`) ficam fora.

## 5. Limites conhecidos

- **As primeiras mensagens não têm data.** 484 linhas sem `created_at`; as conversas com data começam em 23/09 16h34 UTC, e o carrinho abriu em 21/09. Essas pessoas entram no cruzamento por telefone, mas sem checar a ordem conversa → compra.
- **"Atribuída por link" tem teto de 53 pessoas** (as que receberam link). Acima disso, só pela UTM.
- **Os cabeçalhos reais do Guru e da TMB não foram vistos ainda.** A detecção de colunas cobre os nomes mais comuns em português e inglês; confira os avisos na primeira rodada.
- **Não usar as "17 conversões" das análises de maio:** eram sessões com link, não vendas.

## 6. Próximos passos

1. **Até 21/11:** se a Sara não responder, lembrete no privado dela, oferecendo também um acesso só de leitura ao Guru.
2. Rodar o script, conferir uma amostra de 5 a 10 vendas classificadas como `link` à mão (abrir a conversa e ver se faz sentido).
3. Levar o número para o relatório de resultado da Sofia em 2026 (contexto em `docs/conta/`).
4. Depois: a API do Cademí guarda as transações dos checkouts (`GET /sales/transactions`) e permitiria automatizar isso sem export manual. Notas em `docs/conta/cademi-api.md` (local).
