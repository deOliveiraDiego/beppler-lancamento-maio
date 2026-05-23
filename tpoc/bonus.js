// Code node n8n — get_bonus Sofia TPOC
// Retorna bônus ativo baseado na data/hora e perfil da lead
// Input: { perfil: "aluna_wtp" | "publica_geral" }

const input = $input.first().json;
const perfil = input.perfil || 'publica_geral';

const now = DateTime.now().setZone('America/Sao_Paulo');

const bonusPorData = [
  {
    data: DateTime.fromISO('2026-05-23T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-05-23T23:59:59', { zone: 'America/Sao_Paulo' }),
    perfil: 'aluna_wtp',
    label: 'BÔNUS DE AGILIDADE',
    itens: [
      '10 primeiras inscritas: Leitura de Tarot com a Fê',
      'Inscritas nos primeiros 30 min: sorteio da Caixa Mágica da Fê',
      '100 primeiras inscritas: deck de Tarot',
      'Inscritas até meia-noite: Curso TCA - Tarot e as Chaves da Alma',
    ],
  },
  {
    data: DateTime.fromISO('2026-05-24T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-05-24T23:59:59', { zone: 'America/Sao_Paulo' }),
    perfil: 'aluna_wtp',
    label: 'NOVOS BÔNUS REVELADOS',
    itens: [
      'Curso TCA - Tarot e as Chaves da Alma',
      'Curso Incensos de Ervas',
      'Acesso a futuras edições do WTP ao vivo + conteúdos preparatórios',
    ],
  },
  {
    data: DateTime.fromISO('2026-05-25T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-05-25T23:59:59', { zone: 'America/Sao_Paulo' }),
    perfil: 'todas',
    label: 'BÔNUS DO DIA',
    itens: [
      'Curso TCA - Tarot e as Chaves da Alma',
    ],
  },
  {
    data: DateTime.fromISO('2026-05-26T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-05-26T23:59:59', { zone: 'America/Sao_Paulo' }),
    perfil: 'todas',
    label: 'COMBO TAROT+',
    itens: [
      'Aula Como unir o Tarot com as Ervas e Cristais',
      'Aula Como Unir o Tarot com outras Terapias',
      'Aula Como usar outros oráculos com o Tarot',
      'Aula Como Unir Tarot com outras ferramentas mágicas',
      'Aula Como limpar e proteger sua energia nos atendimentos',
      'Aula Como entregar as consultas de Tarot',
    ],
  },
  {
    data: DateTime.fromISO('2026-05-27T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-05-27T23:59:59', { zone: 'America/Sao_Paulo' }),
    perfil: 'todas',
    label: 'MÉTODO MEDITANDO COM O TAROT',
    itens: [
      'Método Meditando com o Tarot',
    ],
  },
  {
    data: DateTime.fromISO('2026-05-28T00:00:00', { zone: 'America/Sao_Paulo' }),
    fim:  DateTime.fromISO('2026-05-28T23:59:59', { zone: 'America/Sao_Paulo' }),
    perfil: 'todas',
    label: 'BIBLIOTECA DE BEPPLER',
    itens: [
      'Biblioteca de Beppler — seleção de livros sobre tarot, astrologia, ervas e empreendedorismo místico',
    ],
  },
];

const bonusAtivo = bonusPorData.find(b => {
  const perfilValido = b.perfil === 'todas' || b.perfil === perfil;
  return perfilValido && now >= b.data && now <= b.fim;
});

if (!bonusAtivo) {
  return [{
    json: {
      tem_bonus: false,
      bonus_ativos: [],
      descricao: 'Não há bônus disponível no momento.',
    }
  }];
}

return [{
  json: {
    tem_bonus: true,
    bonus_ativos: bonusAtivo.itens,
    label: bonusAtivo.label,
    descricao: bonusAtivo.itens.join('. '),
  }
}];
