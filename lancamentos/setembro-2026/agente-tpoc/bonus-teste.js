// Code Tool n8n — get_bonus Sofia Black Vitalícia (setembro/2026)
// Bônus de agilidade a partir da abertura do carrinho (21/09 10h01).
// Não conta inscrições; janelas são tempo decorrido.
//
// Cascata (Carlos, 15/09):
//   15 min — Passaporte Dourado
//   30 min — Kit Mandinguinha + frete
//   1h     — sorteio Caixa Mágica da Fê
//   3h     — leitura de Tarot de Ano Novo com a Fê (vídeo)
//   24h    — ingresso Retiro das Bruxas (vale 5k)
// Repescagem: após 30 min, os bônus de 15 e 30 min voltam até completar 24h.

const now = DateTime.now().setZone('America/Sao_Paulo');
const abertura = DateTime.fromISO('2026-09-21T10:01:00', { zone: 'America/Sao_Paulo' });
const fim24h = abertura.plus({ hours: 24 });

if (now < abertura || now > fim24h) {
  return JSON.stringify({
    tem_bonus: false,
    bonus_ativos: [],
    descricao: 'Não há bônus de agilidade ativo neste momento.',
    instrucao_agente: 'Resposta definitiva: não há bônus de agilidade agora. NÃO chame get_bonus de novo nesta conversa e NÃO mencione bônus de agilidade. Conduza com urgência de fechamento e valor da Vitalícia.',
  });
}

const minutos = now.diff(abertura, 'minutes').minutes;

const passaporte = 'Primeiros 15 min: concorrer ao Passaporte Dourado (transporte + hospedagem do Retiro, encontro com a Fê, Tarot Golden Art Nouveau + toalha)';
const kit = 'Primeiros 30 min: Kit Mandinguinha da Virada + frete grátis para todo o Brasil';
const caixa = 'Primeira 1h: sorteio da Caixa Mágica da Fê (kit bule + xícara Marlete)';
const leitura = 'Primeiras 3h: concorre a uma leitura de Tarot de Ano Novo com a Fê (vídeo chamada)';
const retiro = 'Primeiras 24h: ingresso do Retiro das Bruxas de Beppler (valor de R$5.000)';

const itens = [];

if (minutos < 15) {
  itens.push(passaporte, kit, caixa, leitura, retiro);
} else if (minutos < 30) {
  itens.push(kit, caixa, leitura, retiro);
} else if (minutos < 60) {
  // Repescagem: 15 e 30 min voltam; 1h ainda vale.
  itens.push(passaporte, kit, caixa, leitura, retiro);
} else if (minutos < 180) {
  itens.push(passaporte, kit, leitura, retiro);
} else {
  itens.push(passaporte, kit, retiro);
}

return JSON.stringify({
  tem_bonus: true,
  bonus_ativos: itens,
  label: 'BÔNUS DE AGILIDADE',
  descricao: itens.join('. '),
});
