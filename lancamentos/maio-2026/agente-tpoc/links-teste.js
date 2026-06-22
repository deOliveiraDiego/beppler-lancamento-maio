// Code Tool n8n — get_links Sofia TPOC
//
// Retorna 1 de 3 status:
//   - "pre_abertura": carrinho ainda não abriu para esse perfil (inclui abertura_em)
//   - "aberto":       carrinho ativo (inclui preço, link, parcelamento, fechamento_em)
//   - "encerrado":    carrinho já fechou para todos (inclui fechamento_em)
//
// Resolução de perfil (cascata):
//   1. Se o Agent passou perfil="aluna_wtp" no query (ex: promoção via email), respeita.
//   2. Senão, lê o perfil original do Code (telefone normalizado).
//   3. Fallback final: publica_geral.
//
// Boleto: a info do boleto só existe nesta tool a partir de 25/05. Antes disso,
// formas_pagamento omite boleto completamente — se a Sofia não vê, ela não fala.
// Boleto é EXCLUSIVO de aluna_wtp (checkout TMB, plataforma separada do Sendflow).
// Para publica_geral, boleto NUNCA é ofertado.

const raw = typeof query === 'string' ? JSON.parse(query) : query;
const perfilAgent = raw?.perfil;
const perfilCodeNode = $('Code')?.first()?.json?.perfil;

const perfil = perfilAgent === 'aluna_wtp'
  ? 'aluna_wtp'
  : (perfilCodeNode || 'publica_geral');

const now = DateTime.now().setZone('America/Sao_Paulo');

const aberturaAluna = DateTime.fromISO('2026-05-23T00:00:00', { zone: 'America/Sao_Paulo' });
const aberturaGeral = DateTime.fromISO('2026-05-25T00:00:00', { zone: 'America/Sao_Paulo' });
const fechamento = DateTime.fromISO('2026-05-28T23:59:59', { zone: 'America/Sao_Paulo' });
const boletoDisponivel = DateTime.fromISO('2026-05-25T00:00:00', { zone: 'America/Sao_Paulo' });

const abertura = perfil === 'aluna_wtp' ? aberturaAluna : aberturaGeral;

// 1) Pré-abertura — carrinho ainda não abriu para esse perfil
if (now < abertura) {
  return JSON.stringify({
    status: 'pre_abertura',
    perfil,
    abertura_em: abertura.toFormat("dd/MM"),
    mensagem: perfil === 'aluna_wtp'
      ? `O carrinho TPOC para alunas WTP abre em ${abertura.toFormat("dd/MM")} à tarde, ao vivo no evento.`
      : `O carrinho TPOC para o público geral abre em ${abertura.toFormat("dd/MM")}.`,
  });
}

// 2) Encerrado — passou da data de fechamento
if (now > fechamento) {
  return JSON.stringify({
    status: 'encerrado',
    perfil,
    fechamento_em: fechamento.toFormat("dd/MM"),
    mensagem: `As inscrições do TPOC foram encerradas em ${fechamento.toFormat("dd/MM")}.`,
  });
}

// 3) Aberto — carrinho ativo
const precoVista = perfil === 'aluna_wtp' ? 'R$2.497,00' : 'R$3.000,00';
const parcelado = perfil === 'aluna_wtp' ? '18x de R$180,42' : '18x de R$216,77';
const link = perfil === 'aluna_wtp' ? 'https://i.sendflow.pro/l/wtp-sofia' : 'https://i.sendflow.pro/l/tpocsofia';

// Boleto só existe nesta tool a partir de 25/05 — antes disso, omitir completamente.
// Boleto é EXCLUSIVO de aluna_wtp (checkout TMB separado). Publica_geral nunca vê boleto.
const boletoLiberado = now >= boletoDisponivel && perfil === 'aluna_wtp';

const boletoDetalhe = 'Entrada de R$258,25 + 11x de R$258,25';
const linkBoleto = 'https://pay.tmb.com.br/EscoladeArte/P64158301YV';

const formas = boletoLiberado
  ? `PIX (à vista), cartão de crédito (18x) ou boleto bancário (${boletoDetalhe})`
  : 'PIX (à vista) ou cartão de crédito (18x)';

const payload = {
  status: 'aberto',
  perfil,
  preco_vista: precoVista,
  parcelado,
  parcelamento_alternativo: '12x no cartão (usar somente se o banco bloquear 18x)',
  formas_pagamento: formas,
  link,
  fechamento_em: fechamento.toFormat("dd/MM"),
  order_bump: 'Bruxa de Negócios — R$97,00 à vista ou 18x R$7,01',
};

if (boletoLiberado) {
  payload.boleto = boletoDetalhe;
  payload.link_boleto = linkBoleto;
}

return JSON.stringify(payload);
