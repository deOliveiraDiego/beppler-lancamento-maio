// Code node n8n — get_links Sofia WTP
// Retorna apenas o lote ativo com base na data/hora atual (America/Sao_Paulo)

const now = DateTime.now().setZone('America/Sao_Paulo');

const lots = [
  {
    nome: 'Zero',
    inicio: DateTime.fromISO('2026-04-01T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:    DateTime.fromISO('2026-04-21T23:59:59', { zone: 'America/Sao_Paulo' }),
    vista:  'R$37,00',
    parcelas: '3x de R$12,95',
    link:   'https://clkdmg.site/pay/lote-0-wtp',
    bonus:  'E-book "50 Mitos sobre Tarot"',
  },
  {
    nome: '1',
    inicio: DateTime.fromISO('2026-04-22T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:    DateTime.fromISO('2026-04-27T23:59:59', { zone: 'America/Sao_Paulo' }),
    vista:  'R$47,00',
    parcelas: '4x de R$12,53',
    link:   'https://clkdmg.site/pay/lote-1wtp',
    bonus:  null,
  },
  {
    nome: '2',
    inicio: DateTime.fromISO('2026-04-28T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:    DateTime.fromISO('2026-05-04T23:59:59', { zone: 'America/Sao_Paulo' }),
    vista:  'R$57,00',
    parcelas: '5x de R$12,35',
    link:   'https://clkdmg.site/pay/lote-2wtp',
    bonus:  null,
  },
  {
    nome: '3',
    inicio: DateTime.fromISO('2026-05-05T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:    DateTime.fromISO('2026-05-11T23:59:59', { zone: 'America/Sao_Paulo' }),
    vista:  'R$67,00',
    parcelas: '6x de R$12,29',
    link:   'https://clkdmg.site/pay/lote-3wtp',
    bonus:  null,
  },
  {
    nome: '4',
    inicio: DateTime.fromISO('2026-05-12T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:    DateTime.fromISO('2026-05-18T23:59:59', { zone: 'America/Sao_Paulo' }),
    vista:  'R$77,00',
    parcelas: '8x de R$10,91',
    link:   'https://clkdmg.site/pay/lote-4wtp',
    bonus:  null,
  },
  {
    nome: 'Último',
    inicio: DateTime.fromISO('2026-05-19T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:    DateTime.fromISO('2026-05-22T14:00:00', { zone: 'America/Sao_Paulo' }),
    vista:  'R$79,00',
    parcelas: '12x de R$7,90',
    link:   'https://clkdmg.site/pay/ultimolotewtp',
    bonus:  null,
  },
];

const loteAtivo = lots.find(l => now >= l.inicio && now <= l.fim);

if (!loteAtivo) {
  return JSON.stringify({
    status: 'fechado',
    mensagem: 'O carrinho do WTP está temporariamente fechado.',
  });
}

return JSON.stringify({
    status: 'aberto',
    lote: loteAtivo.nome,
    preco_vista: loteAtivo.vista,
    parcelado: loteAtivo.parcelas,
    link: loteAtivo.link,
    suporte_email: 'suporte@fernandabeppler.com.br',
    bonus: loteAtivo.bonus,
    pagina_vendas: 'https://sndflw.com/l/wtpwhats1',
    formas_pagamento: 'PIX (à vista) ou cartão de crédito (parcelado). Boleto não disponível para o WTP.'
});
