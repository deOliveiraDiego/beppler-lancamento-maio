// Code Tool n8n — get_links Sofia Black Vitalícia (setembro/2026)
//
// Carlos, 16/09: Sofia NÃO identifica aluna vs lead e NÃO envia checkout
// separado. O único link é a página de vendas (dois preços na mesma tela).
//
// Retorna 1 de 3 status: "pre_abertura" | "aberto" | "encerrado".
//
// Gates:
//   - Preço só existe a partir da live/abertura (21/09 10h01).
//   - Boleto só entra no payload a partir de 23/09. Continua o MESMO link
//     (página de vendas). Não há URL TMB neste payload.

// Relógio de teste: 23/09 10h00 (aberto + boleto liberado).
const now = DateTime.fromISO('2026-09-23T10:00:00', { zone: 'America/Sao_Paulo' });

const abertura = DateTime.fromISO('2026-09-21T10:01:00', { zone: 'America/Sao_Paulo' });
const fechamento = DateTime.fromISO('2026-10-09T23:59:59', { zone: 'America/Sao_Paulo' });
const boletoDisponivel = DateTime.fromISO('2026-09-23T00:00:00', { zone: 'America/Sao_Paulo' });

const paginaVendas = 'https://sndflw.com/l/black-sofia';

if (now < abertura) {
  return JSON.stringify({
    status: 'pre_abertura',
    abertura_em: abertura.toFormat('dd/MM HH:mm'),
    mensagem: 'O carrinho da Black Vitalícia abre na live de 21/09.',
  });
}

if (now > fechamento) {
  return JSON.stringify({
    status: 'encerrado',
    fechamento_em: fechamento.toFormat('dd/MM'),
    mensagem: 'As inscrições da Black Vitalícia foram encerradas.',
  });
}

const boletoLiberado = now >= boletoDisponivel;

const formas = boletoLiberado
  ? 'PIX (à vista), cartão de crédito (até 18x) ou boleto (12x). Cartão e PIX e boleto ficam na página de vendas.'
  : 'PIX (à vista) ou cartão de crédito (até 18x). Boleto ainda não está liberado.';

const payload = {
  status: 'aberto',
  link: paginaVendas,
  preco_aluna_vista: 'R$3.997,00',
  preco_aluna_parcelado: '18x de R$288,81',
  preco_lead_vista: 'R$4.997,00',
  preco_lead_parcelado: '18x de R$361,06',
  cartao: 'até 18x',
  boleto_parcelas: boletoLiberado ? '12x' : null,
  formas_pagamento: formas,
  fechamento_em: fechamento.toFormat('dd/MM'),
  instrucao_agente:
    'Envie SOMENTE o campo link (página de vendas). NÃO envie checkout GURU nem TMB. A pessoa escolhe Aluna ou Não Aluna na página. NÃO cite preço Golden (R$2.997). Se a pessoa se declarar Golden, encaminharAtendimento.',
};

if (boletoLiberado) {
  payload.boleto_na_pagina = true;
}

return JSON.stringify(payload);
