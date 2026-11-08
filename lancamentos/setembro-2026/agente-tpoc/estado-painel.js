// n8n: workflow 'Sofia Black — Painel do Carrinho' (btYZLmuw2xKQJ0ug), Code node 'Calcular Links e Bônus'.
// Fonte de verdade de get_links/get_bonus a partir de 08/11/2026. links.js/bonus.js ficam como legado.
// Estado do carrinho da Black Vitalícia (reabertura relâmpago 09/11/2026).
// Fonte: última linha da data table sofia_black_carrinho do ambiente pedido.
// Query: ?tool=links|bonus&ambiente=prod|teste[&agora=ISO só em teste]
const zone = 'America/Sao_Paulo';
const q = $('Webhook Sofia').first().json.query || {};
const ambiente = q.ambiente === 'teste' ? 'teste' : 'prod';
const tool = q.tool === 'bonus' ? 'bonus' : 'links';

const now = ambiente === 'teste' && q.agora
  ? DateTime.fromISO(q.agora, { zone })
  : DateTime.now().setZone(zone);

const row = $input.first() ? $input.first().json : {};
const acao = row && row.acao ? row.acao : 'aguardar';
const desde = row && row.createdAt ? DateTime.fromISO(row.createdAt).setZone(zone) : null;

const diaReabertura = DateTime.fromISO('2026-11-09T00:00:00', { zone });

let estado;
if (acao === 'abrir') estado = 'aberto';
else if (acao === 'fechar') estado = 'pos_fechamento';
else if (now < diaReabertura) estado = 'pre_reabertura';
else estado = 'aguardando_live';

// ---------- get_bonus ----------
if (tool === 'bonus') {
  if (estado !== 'aberto' || !desde) {
    return [{ json: {
      tem_bonus: false,
      bonus_ativos: [],
      descricao: 'Não há bônus de agilidade ativo neste momento.',
      instrucao_agente: 'Resposta definitiva: não há bônus de agilidade agora. NÃO chame get_bonus de novo nesta conversa e NÃO mencione bônus de agilidade.',
    } }];
  }
  const minutos = now.diff(desde, 'minutes').minutes;
  const kit = 'Primeiros 30 min: Kit Mandinguinha da Virada + frete grátis para todo o Brasil';
  const leitura = 'Primeira 1h: concorre a uma leitura de Tarot de Ano Novo com a Fê (por vídeo chamada)';
  const itens = [];
  if (minutos < 30) itens.push(kit, leitura);
  else if (minutos < 60) itens.push(leitura);
  if (!itens.length) {
    return [{ json: {
      tem_bonus: false,
      bonus_ativos: [],
      descricao: 'Os bônus de agilidade (30 min e 1h) já passaram.',
      instrucao_agente: 'Resposta definitiva: não há bônus de agilidade agora. NÃO chame get_bonus de novo nesta conversa. Os bônus da reabertura (Mentoria Caixa Rápido etc.) estão em get_conhecimento.',
    } }];
  }
  return [{ json: {
    tem_bonus: true,
    bonus_ativos: itens,
    label: 'BÔNUS DE AGILIDADE',
    descricao: itens.join('. '),
    instrucao_agente: 'Use os bônus para criar urgência. NÃO diga quantos minutos faltam e NÃO invente horário.',
  } }];
}

// ---------- get_links ----------
if (estado === 'pre_reabertura') {
  return [{ json: {
    status: 'pre_reabertura',
    reabertura_em: '09/11, na live Tarot da Semana',
    mensagem: 'A Black Vitalícia das Bruxas volta numa reabertura relâmpago no dia 09/11, na live Tarot da Semana, com todas as formas de pagamento liberadas.',
    instrucao_agente: 'NUNCA diga que a Black está encerrada, indisponível ou fechada. Diga que ela volta numa reabertura relâmpago dia 09/11, na live Tarot da Semana, e que a pessoa precisa ficar no grupo VIP para não perder. NÃO envie preço, link de página nem link de grupo. NÃO invente horário.',
  } }];
}

if (estado === 'aguardando_live') {
  return [{ json: {
    status: 'aguardando_live',
    reabertura_em: 'hoje, ao vivo na live Tarot da Semana',
    mensagem: 'A Black Vitalícia das Bruxas reabre HOJE, ao vivo, na live Tarot da Semana. A Fernanda abre as inscrições durante a live.',
    instrucao_agente: 'NUNCA diga que a Black está encerrada. Diga que reabre HOJE, ao vivo, na live Tarot da Semana, e que a pessoa precisa estar na live para garantir os bônus de quem entra primeiro. NÃO envie preço, link de página nem link de grupo. NÃO invente horário da live.',
  } }];
}

if (estado === 'pos_fechamento') {
  // PENDENTE (Diego): comportamento pós-fechamento ainda em definição.
  // Provisório: nunca dizer encerrado; verificar com a equipe e encaminhar.
  return [{ json: {
    status: 'pos_fechamento',
    mensagem: 'As inscrições da reabertura relâmpago não estão abertas neste momento.',
    instrucao_agente: 'NUNCA diga que a Black está encerrada. Diga que você vai verificar com a equipe se ainda é possível liberar a inscrição para ela e chame encaminharAtendimento. NÃO envie preço nem link.',
  } }];
}

// aberto
return [{ json: {
  status: 'aberto',
  link: 'https://sndflw.com/l/black-sofia',
  preco_aluna_vista: 'R$3.997,00',
  preco_aluna_parcelado: '18x de R$288,81',
  preco_lead_vista: 'R$4.997,00',
  preco_lead_parcelado: '18x de R$361,06',
  cartao: 'até 18x',
  boleto_parcelas: '18x',
  boleto_aluna: '18x de R$302,79 (entrada de R$302,79 + 17x de R$302,79)',
  boleto_nao_aluna: '18x de R$378,54 (entrada de R$378,54 + 17x de R$378,54)',
  link_boleto_aluna: 'https://pay.tmb.com.br/EscoladeArte/9K929006127',
  link_boleto_nao_aluna: 'https://pay.tmb.com.br/EscoladeArte/VBV285809LQ',
  formas_pagamento: 'PIX (à vista) e cartão de crédito (até 18x) na página de vendas. Boleto (18x, entrada + 17) por link próprio de aluna ou de não aluna.',
  instrucao_agente: 'Reabertura relâmpago: as inscrições podem fechar a qualquer momento. NUNCA informe data ou hora de fechamento, nem invente uma. Crie urgência. Para PIX e cartão, envie o campo link (página de vendas). Boleto: só quando a pessoa pedir boleto; se ela ainda não disse se é aluna da Fernanda, pergunte antes e envie só o link de boleto do perfil dela (link_boleto_aluna ou link_boleto_nao_aluna). NUNCA envie os dois links de boleto juntos. NÃO envie checkout GURU. NÃO cite preço Golden (R$2.997). Se a pessoa se declarar Golden, encaminharAtendimento.',
} }];
