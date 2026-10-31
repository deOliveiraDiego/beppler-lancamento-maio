// Code Tool n8n — get_links Sofia Black Vitalícia (setembro/2026)
//
// Link principal: página de vendas (dois preços na mesma tela), para PIX e
// cartão. Sofia NÃO envia checkout Guru.
//
// Carlos, 28/09: boleto é TMB 18x (entrada + 17x), com link próprio por
// perfil (aluna / não aluna). Boleto TMB só quando a lead pede boleto.
//
// Retorna 1 de 3 status: "pre_abertura" | "aberto" | "pre_reabertura".
//
// Sara/Carlos, 31/10: depois do fechamento de 09/10 a Sofia NUNCA diz que a
// Black encerrou. Reabertura relâmpago em 09/11 (Tarot da Semana), fechamento
// 19/11. Preço e hora da reabertura ainda não vieram: até lá, status
// "pre_reabertura" (sem preço, sem link). Quando vierem, abrir a janela
// reabertura → fechamentoReabertura com o payload "aberto".
//
// Gates:
//   - Preço só existe a partir da live/abertura (21/09 10h01).
//   - Boleto só entra no payload a partir de 23/09 (links TMB de aluna e
//     de não aluna).

// Relógio de teste: 31/10 19h00 (relógio de teste).
const now = DateTime.fromISO('2026-10-31T19:00:00', { zone: 'America/Sao_Paulo' });

const abertura = DateTime.fromISO('2026-09-21T10:01:00', { zone: 'America/Sao_Paulo' });
const fechamento = DateTime.fromISO('2026-10-09T23:59:59', { zone: 'America/Sao_Paulo' });
const boletoDisponivel = DateTime.fromISO('2026-09-23T00:00:00', { zone: 'America/Sao_Paulo' });

const paginaVendas = 'https://sndflw.com/l/black-sofia';
const linkBoletoAluna = 'https://pay.tmb.com.br/EscoladeArte/9K929006127';
const linkBoletoNaoAluna = 'https://pay.tmb.com.br/EscoladeArte/VBV285809LQ';

if (now < abertura) {
  return JSON.stringify({
    status: 'pre_abertura',
    abertura_em: abertura.toFormat('dd/MM HH:mm'),
    mensagem: 'O carrinho da Black Vitalícia abre na live de 21/09.',
  });
}

if (now > fechamento) {
  return JSON.stringify({
    status: 'pre_reabertura',
    reabertura_em: '09/11, na live Tarot da Semana',
    mensagem: 'A Black Vitalícia das Bruxas volta numa reabertura relâmpago no dia 09/11, na live Tarot da Semana, com todas as formas de pagamento liberadas.',
    instrucao_agente:
      'NUNCA diga que a Black está encerrada, indisponível ou fechada. Diga que ela volta numa reabertura relâmpago dia 09/11, na live Tarot da Semana, e que a pessoa precisa ficar no grupo VIP para não perder. NÃO envie preço, link de página nem link de grupo. NÃO invente horário.',
  });
}

const boletoLiberado = now >= boletoDisponivel;

const formas = boletoLiberado
  ? 'PIX (à vista) e cartão de crédito (até 18x) na página de vendas. Boleto (18x, entrada + 17) por link próprio de aluna ou de não aluna.'
  : 'PIX (à vista) ou cartão de crédito (até 18x). Boleto ainda não está liberado.';

const payload = {
  status: 'aberto',
  link: paginaVendas,
  preco_aluna_vista: 'R$3.997,00',
  preco_aluna_parcelado: '18x de R$288,81',
  preco_lead_vista: 'R$4.997,00',
  preco_lead_parcelado: '18x de R$361,06',
  cartao: 'até 18x',
  boleto_parcelas: boletoLiberado ? '18x' : null,
  formas_pagamento: formas,
  fechamento_em: fechamento.toFormat('dd/MM'),
  instrucao_agente:
    'Para PIX e cartão, envie o campo link (página de vendas). Boleto: só quando a pessoa pedir boleto; se ela ainda não disse se é aluna da Fernanda, pergunte antes e envie só o link de boleto do perfil dela (link_boleto_aluna ou link_boleto_nao_aluna). NUNCA envie os dois links de boleto juntos. NÃO envie checkout GURU. NÃO cite preço Golden (R$2.997). Se a pessoa se declarar Golden, encaminharAtendimento.',
};

if (boletoLiberado) {
  payload.link_boleto_aluna = linkBoletoAluna;
  payload.link_boleto_nao_aluna = linkBoletoNaoAluna;
}

return JSON.stringify(payload);
