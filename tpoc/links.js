// Code node n8n — get_links Sofia TPOC
// Recebe perfil via input: { perfil: "aluna_wtp" | "publica_geral" }
// Retorna 1 de 3 status:
//   - "pre_abertura": carrinho ainda não abriu para esse perfil (inclui abertura_em)
//   - "aberto":       carrinho ativo (inclui preço, link, parcelamento, fechamento_em)
//   - "encerrado":    carrinho já fechou para todos (inclui fechamento_em)

const input = $input.first().json;
const perfil = input.perfil || 'publica_geral';

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

const boletoDetalhe = perfil === 'aluna_wtp'
  ? 'Entrada de R$258,25 + 11x de R$258,25'
  : 'Entrada de R$310,27 + 11x de R$310,27';

const formas = now >= boletoDisponivel
  ? `PIX (à vista), cartão de crédito (18x) ou boleto bancário (${boletoDetalhe})`
  : perfil === 'aluna_wtp'
    ? 'PIX (à vista) ou cartão de crédito (18x). Boleto disponível a partir de 25/05.'
    : 'PIX (à vista) ou cartão de crédito (18x).';

return JSON.stringify({
  status: 'aberto',
  perfil,
  preco_vista: precoVista,
  parcelado,
  formas_pagamento: formas,
  link,
  fechamento_em: fechamento.toFormat("dd/MM"),
  order_bump: 'Bruxa de Negócios — R$97,00 à vista ou 18x R$7,01',
});
