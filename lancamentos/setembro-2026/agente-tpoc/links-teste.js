// Code Tool n8n — get_links Sofia Black Vitalícia (setembro/2026)
//
// Retorna 1 de 3 status:
//   - "pre_abertura": carrinho ainda não abriu
//   - "aberto":       carrinho ativo
//   - "encerrado":    carrinho já fechou
//
// Sofia NÃO identifica aluna vs lead. `link` é a página com as duas inscrições.
// `link_aluna` / `link_lead` só entram se a pessoa já se declarou no Zap.
// Golden NÃO entra neste payload (sem lista → Sofia não fala 2.997).
//
// GATES:
//   - Preço só existe a partir da abertura (21/09 10h01, live).
//   - Boleto só entra no payload a partir de 23/09. Antes, omitir.
//     Boleto é TMB (checkout separado), não opção no Guru.

const now = DateTime.now().setZone('America/Sao_Paulo');

// Live 21/09 10h01 — placeholder de horário até a equipe confirmar o minuto.
const abertura = DateTime.fromISO('2026-09-21T10:01:00', { zone: 'America/Sao_Paulo' });
const fechamento = DateTime.fromISO('2026-10-09T23:59:59', { zone: 'America/Sao_Paulo' });
const boletoDisponivel = DateTime.fromISO('2026-09-23T00:00:00', { zone: 'America/Sao_Paulo' });

if (now < abertura) {
  return JSON.stringify({
    status: 'pre_abertura',
    abertura_em: abertura.toFormat('dd/MM'),
    mensagem: `O carrinho da Vitalícia abre em ${abertura.toFormat('dd/MM')}.`,
  });
}

if (now > fechamento) {
  return JSON.stringify({
    status: 'encerrado',
    fechamento_em: fechamento.toFormat('dd/MM'),
    mensagem: `As inscrições da Vitalícia foram encerradas em ${fechamento.toFormat('dd/MM')}.`,
  });
}

const link = 'https://sndflw.com/l/black-sofia';
const linkAluna = 'https://sndflw.com/l/alunablacksofia';
const linkLead = 'https://sndflw.com/l/sofianaoalunablack';

const boletoLiberado = now >= boletoDisponivel;
// PENDENTE: Sara / Carlos — URLs TMB de aluna e lead.
const linkBoletoAluna = 'https://PLACEHOLDER-tmb-aluna';
const linkBoletoLead = 'https://PLACEHOLDER-tmb-lead';

const formas = boletoLiberado
  ? 'PIX (à vista), cartão de crédito (até 18x) ou boleto bancário (TMB, link próprio)'
  : 'PIX (à vista) ou cartão de crédito (até 18x)';

const payload = {
  status: 'aberto',
  preco_aluna_vista: 'R$3.997,00',
  parcelado_aluna: '18x de R$288,81',
  preco_lead_vista: 'R$4.997,00',
  parcelado_lead: '18x de R$361,06',
  formas_pagamento: formas,
  link,
  link_aluna: linkAluna,
  link_lead: linkLead,
  fechamento_em: fechamento.toFormat('dd/MM'),
};

if (boletoLiberado) {
  payload.boleto_aluna = 'Entrada de R$413,38 + 11 boletos';
  payload.boleto_lead = 'Entrada de R$516,81 + 11 boletos';
  payload.link_boleto_aluna = linkBoletoAluna;
  payload.link_boleto_lead = linkBoletoLead;
}

return JSON.stringify(payload);
