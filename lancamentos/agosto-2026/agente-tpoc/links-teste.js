// Code Tool n8n — get_links Sofia TPOC (lançamento AGOSTO/2026 — Beabá do Tarot)
//
// Retorna 1 de 3 status:
//   - "pre_abertura": carrinho ainda não abriu (inclui abertura_em)
//   - "aberto":       carrinho ativo (inclui preço, link, parcelamento, fechamento_em)
//   - "encerrado":    carrinho já fechou (inclui fechamento_em)
//
// MUDANÇA vs. maio: NÃO há split de perfil neste lançamento (sem WTP).
//   Preço, link e boleto são iguais para todas. A tool não lê mais perfil
//   do Code node nem do query — trilho único.
//
// GATES de divulgação (regra dura do briefing):
//   - Preço só "existe" a partir da abertura do carrinho (12/08). Antes disso,
//     status pre_abertura — a Sofia não tem preço pra falar.
//   - Boleto só entra no payload a partir de 14/08. Antes disso é omitido
//     completamente — se a Sofia não vê, ela não fala.
//
// PENDÊNCIAS (confirmar com a equipe — ver briefing §5/§7):
//   - HORÁRIO exato de abertura do carrinho em 12/08 (após CPL3 das 10h01). Placeholder abaixo.
//   - Existe checkout de BOLETO separado (como o TMB de maio) ou o boleto é uma
//     opção dentro do checkout principal? `linkBoleto` abaixo é PLACEHOLDER.

const now = DateTime.now().setZone('America/Sao_Paulo');

// TODO confirmar horário exato — usando 00:00 do dia 12/08 (gate de preço cobre a manhã do dia 12).
const abertura = DateTime.fromISO('2026-08-12T00:00:00', { zone: 'America/Sao_Paulo' });
// Fechamento à meia-noite do dia 20, mas "deixa aberto até 9h do dia 21" (briefing §1).
const fechamento = DateTime.fromISO('2026-08-21T09:00:00', { zone: 'America/Sao_Paulo' });
// Boleto liberado pra TODAS a partir de 14/08 (não é mais regra de perfil).
const boletoDisponivel = DateTime.fromISO('2026-08-14T00:00:00', { zone: 'America/Sao_Paulo' });

// 1) Pré-abertura — carrinho ainda não abriu
if (now < abertura) {
  return JSON.stringify({
    status: 'pre_abertura',
    abertura_em: abertura.toFormat("dd/MM"),
    mensagem: `O carrinho do TPOC abre em ${abertura.toFormat("dd/MM")}.`,
  });
}

// 2) Encerrado — passou da data de fechamento
if (now > fechamento) {
  return JSON.stringify({
    status: 'encerrado',
    fechamento_em: fechamento.toFormat("dd/MM"),
    mensagem: `As inscrições do TPOC foram encerradas em ${fechamento.toFormat("dd/MM")}.`,
  });
}

// 3) Aberto — carrinho ativo (preço único Oferta TPOC25)
const link = 'https://i.sendflow.pro/l/tpocsofia';

// Boleto: só existe nesta tool a partir de 14/08 — antes disso, omitir completamente.
// TODO confirmar com a equipe: link próprio (plataforma separada) vs. opção dentro do checkout.
const boletoLiberado = now >= boletoDisponivel;
const linkBoleto = 'https://PLACEHOLDER-confirmar-checkout-boleto'; // TODO substituir quando a equipe confirmar

const formas = boletoLiberado
  ? 'PIX (à vista), cartão de crédito (até 18x) ou boleto bancário'
  : 'PIX (à vista) ou cartão de crédito (até 18x)';

const payload = {
  status: 'aberto',
  preco_vista: 'R$2.497,00',
  parcelado: '18x de R$180,42',
  parcelamento_alternativo: '12x de R$249,78 (usar somente se o banco bloquear 18x)',
  formas_pagamento: formas,
  link,
  fechamento_em: fechamento.toFormat("dd/MM"),
};

if (boletoLiberado) {
  payload.link_boleto = linkBoleto;
}

return JSON.stringify(payload);
