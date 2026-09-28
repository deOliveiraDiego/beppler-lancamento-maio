// Code node n8n — carrega o System Message da Sofia do GitHub (setembro/2026)
//
// O AI Agent lê o prompt de: {{ $('Prompt GitHub Teste').first().json.data }}
//
// Proteções:
//   - Cache no static data do workflow: GitHub no máximo 1x a cada 5 min.
//   - Validação: só aceita texto que começa com "# SYSTEM PROMPT" e tem 20 mil+ chars.
//   - GitHub fora ou conteúdo quebrado → usa a última versão boa guardada.
//   - Depois de falha, espera 1 min antes de tentar o GitHub de novo.
// Static data só é gravado em execução do workflow ativo (não em "Test workflow").

const ARQUIVO = 'prompt-teste.md';
const CHAVE = 'promptTeste';
const URL = `https://raw.githubusercontent.com/deOliveiraDiego/beppler-lancamento-maio/main/lancamentos/setembro-2026/agente-tpoc/${ARQUIVO}`;
const TTL_MS = 5 * 60 * 1000;
const RETRY_MS = 60 * 1000;
const TIMEOUT_MS = 3000;

const store = $getWorkflowStaticData('global');
const valido = (t) => typeof t === 'string' && t.startsWith('# SYSTEM PROMPT') && t.length >= 20000;
const agora = Date.now();
const cache = store[CHAVE];
const temCache = cache && valido(cache.texto);

if (temCache && agora - cache.em < TTL_MS) {
  return [{ json: { data: cache.texto, origem: 'cache' } }];
}

let origem;
try {
  const texto = await this.helpers.httpRequest({ method: 'GET', url: `${URL}?t=${agora}`, timeout: TIMEOUT_MS, json: false });
  if (valido(texto)) {
    store[CHAVE] = { texto, em: agora };
    return [{ json: { data: texto, origem: 'github' } }];
  }
  origem = 'github-invalido';
} catch (e) {
  origem = 'github-erro';
}

if (temCache) {
  cache.em = agora - TTL_MS + RETRY_MS;
  return [{ json: { data: cache.texto, origem: `${origem}+cache` } }];
}
throw new Error(`Prompt indisponível (${origem}) e sem cópia guardada`);
