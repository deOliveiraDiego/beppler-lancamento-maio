# Configuração do Code Tool — perfil inferido pelo Agent

**Importante:** `$fromAI()` **não funciona dentro do JavaScript do Code Tool** (`@n8n/n8n-nodes-langchain.toolCode`). É uma expression do editor visual, exclusiva de tools como HTTP Request Tool. Pro Code Tool, o equivalente funcional é o **input schema** nativo do node.

Fonte: docs oficiais e [thread da comunidade](https://community.n8n.io/t/how-to-use-fromai-command-in-inside-code-tool-or-output-value-from-previous-tool/102292).

---

## Como funciona

1. Habilitamos `Specify Input Schema` no Code Tool.
2. Declaramos o campo `perfil` no schema com uma descrição clara — isso vira a "instrução" pro Agent inferir o valor.
3. O Agent (Sofia) lê o contexto da conversa, infere o perfil efetivo e passa estruturado.
4. Dentro do JS do Code Tool, lemos via `query.perfil`.

---

## 1. Node `get_bonus` — configuração no n8n

**Aba "Specify Input Schema":** ON

**Schema Type:** `From JSON Example`

**JSON Example:**

```json
{
  "perfil": "aluna_wtp"
}
```

OU **Schema Type:** `Define below` (manual) com JSON Schema completo (mais expressivo):

```json
{
  "type": "object",
  "properties": {
    "perfil": {
      "type": "string",
      "enum": ["aluna_wtp", "publica_geral"],
      "description": "Perfil efetivo da lead nesta conversa. Retornar 'aluna_wtp' se a lead foi confirmada como aluna do WTP por qualquer caminho: (a) o Code in JavaScript inicial já a classificou como aluna_wtp pelo telefone, OU (b) verificarAlunaPorEmail retornou encontrada:true em alguma mensagem anterior desta conversa. Retornar 'publica_geral' caso contrário."
    }
  },
  "required": ["perfil"]
}
```

**JavaScript do node** (substituir o `bonus.js` atual):

```javascript
// Code Tool — get_bonus
// Input: { perfil: "aluna_wtp" | "publica_geral" } via schema do tool (inferido pelo Agent)

const input = typeof query === 'string' ? JSON.parse(query) : query;
const perfil = input?.perfil || 'publica_geral';

const now = DateTime.now().setZone('America/Sao_Paulo');

const bonusPorData = [
  // ... mesma estrutura de antes ...
];

const bonusAtivo = bonusPorData.find(b => {
  const perfilValido = b.perfil === 'todas' || b.perfil === perfil;
  return perfilValido && now >= b.data && now <= b.fim;
});

if (!bonusAtivo) {
  return JSON.stringify({
    tem_bonus: false,
    bonus_ativos: [],
    descricao: 'Não há bônus disponível no momento.',
  });
}

return JSON.stringify({
  tem_bonus: true,
  bonus_ativos: bonusAtivo.itens,
  label: bonusAtivo.label,
  descricao: bonusAtivo.itens.join('. '),
});
```

A única diferença vs `bonus.js` atual: lê de `query.perfil` em vez de `$input.first().json.perfil`.

---

## 2. Node `get_links` — configuração no n8n

Mesma estrutura. Schema:

```json
{
  "perfil": "aluna_wtp"
}
```

(Ou versão manual idêntica ao schema do `get_bonus` acima)

**JavaScript:** aplicar a mesma mudança — ler `perfil` de `query.perfil` em vez de input.

---

## 3. Como colar no n8n

1. Abrir workflow Sofia (`vqNWUQUjr4g9d839`).
2. Clicar no node `get_bonus`.
3. Ativar **"Specify Input Schema"** (toggle).
4. Selecionar **"From JSON Example"** e colar o JSON example do passo 1.
5. Substituir o conteúdo do **JavaScript** pelo código acima.
6. Salvar.
7. Repetir pro node `get_links` (mesmo schema, JS análogo).
8. Reativar workflow.

---

## Validação esperada

Mesmos 4 cenários da iteração anterior:

| Cenário | sessionId | Esperado |
|---|---|---|
| Aluna WTP via telefone (com 9) | número da lista | get_bonus retorna bônus de hoje |
| Aluna WTP via fix do "9" | número da lista sem o 9 | get_bonus retorna bônus de hoje |
| **Aluna promovida via email** | sessionId fake + email válido | **get_bonus retorna bônus de hoje após promoção** ← o que estava quebrado |
| Pública geral (não promovida) | sessionId fake | get_bonus retorna vazio (24/05 só tem bônus aluna_wtp) |
