// Code Tool n8n — get_bonus Sofia TPOC (Agosto/2026 — Beabá do Tarot)
// Retorna o bônus de agilidade ativo baseado SOMENTE na data/hora.
//
// Lançamento sem WTP: trilho único, sem split de perfil.
// A tool não conta inscrições; "primeiras 3h / 100 primeiras / 24h" são
// tratados como itens de texto do bônus do dia (igual maio fazia com
// "10 primeiras inscritas: ...").

const now = DateTime.now().setZone('America/Sao_Paulo');

const bonusPorData = [
  {
    // 12/08 (Dia 1) — abertura do carrinho
    data: DateTime.fromISO('2026-08-12T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-08-12T23:59:59', { zone: 'America/Sao_Paulo' }),
    label: 'BÔNUS DE AGILIDADE',
    itens: [
      'Inscritas nas primeiras 3h: sorteio da Caixa Mágica da Fê (itens físicos + ingresso pro Retiro)',
      '100 primeiras inscritas: deck de Tarot',
      'Inscritas nas primeiras 24h: Curso TCA - Tarot e as Chaves da Alma',
    ],
  },
  {
    // 13/08 (Dia 2)
    data: DateTime.fromISO('2026-08-13T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-08-13T23:59:59', { zone: 'America/Sao_Paulo' }),
    label: 'COMBO TAROT+',
    itens: [
      'Combo Tarot+ — aulas integrando o Tarot com outras ferramentas mágicas',
    ],
  },
  // 14/08 (Dia 3) — sem novos bônus (chamada massiva pra Imersão).
  // Não há entrada: cai no fallback tem_bonus:false com descrição própria.
  {
    // 15/08 (Imersão Degustação)
    data: DateTime.fromISO('2026-08-15T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-08-15T23:59:59', { zone: 'America/Sao_Paulo' }),
    label: 'BÔNUS DA IMERSÃO',
    itens: [
      'Reabertura do bônus Curso TCA - Tarot e as Chaves da Alma',
      'Planilha de Organização Financeira do Carlos',
      'Aula de aplicação',
    ],
  },
];

const bonusAtivo = bonusPorData.find(b => now >= b.data && now <= b.fim);

if (!bonusAtivo) {
  // Dia 3 (14/08): foco total na Imersão Degustação, sem bônus de agilidade novo.
  const fimDia3   = DateTime.fromISO('2026-08-14T23:59:59', { zone: 'America/Sao_Paulo' });
  const inicioDia3 = DateTime.fromISO('2026-08-14T00:00:00', { zone: 'America/Sao_Paulo' });
  const ehDia3 = now >= inicioDia3 && now <= fimDia3;

  return JSON.stringify({
    tem_bonus: false,
    bonus_ativos: [],
    descricao: ehDia3
      ? 'Hoje não há bônus de agilidade novo — o foco é a Imersão Degustação do TPOC.'
      : 'Não há bônus disponível no momento.',
  });
}

return JSON.stringify({
  tem_bonus: true,
  bonus_ativos: bonusAtivo.itens,
  label: bonusAtivo.label,
  descricao: bonusAtivo.itens.join('. '),
});
