---
name: Fernanda Beppler · Black Vitalícia das Bruxas
description: Identidade visual da LP do Combo Black (fernandabeppler.com.br/combo-black), extraída em 09/11/2026.
colors:
  espresso: "#210E01"
  espresso-deep: "#1E0F05"
  bark: "#321B11"
  ember-rust: "#933B0E"
  candle-gold: "#CB963E"
  parchment: "#FFF7E8"
  peach-cream: "#FCE1C3"
  apricot: "#FFDDAF"
  cocoa: "#642900"
  cta-green: "#2DA723"
  mint-glow: "#8FFEBD"
  white: "#FFFFFF"
  glass-fill: "#FFFFFF08"
  glass-border: "#FFFFFF33"
typography:
  display:
    fontFamily: "Crimson Pro, Georgia, serif"
    fontSize: "4.8em"
    fontWeight: 400
    lineHeight: 1.05
    letterSpacing: "-0.22px"
  headline:
    fontFamily: "Crimson Pro, Georgia, serif"
    fontSize: "2.6em"
    fontWeight: 400
    lineHeight: 1.1
  emphasis:
    fontFamily: "Crimson Pro, Georgia, serif"
    fontWeight: 700
    fontStyle: italic
  body:
    fontFamily: "Crimson Pro, Georgia, serif"
    fontSize: "1.2em"
    fontWeight: 400
    lineHeight: 1.3
  label:
    fontFamily: "Helvetica, Arial, sans-serif"
    fontSize: "0.8em"
    fontWeight: 700
    textTransform: uppercase
rounded:
  card: "11px"
  panel: "2em"
  pill: "4em"
spacing:
  card-gap: "12px"
  section: "96px"
components:
  button-cta:
    backgroundColor: "{colors.cta-green}"
    textColor: "{colors.white}"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "18px 48px"
  card-glass:
    backgroundColor: "{colors.glass-fill}"
    textColor: "{colors.parchment}"
    rounded: "{rounded.card}"
    padding: "24px"
  panel-offer:
    backgroundColor: "{colors.ember-rust}"
    textColor: "{colors.parchment}"
    rounded: "{rounded.panel}"
    padding: "32px"
  card-price:
    backgroundColor: "{colors.white}"
    textColor: "{colors.espresso-deep}"
    rounded: "{rounded.card}"
    padding: "20px"
---

# Design System: Fernanda Beppler · Black Vitalícia das Bruxas

Fonte: LP `https://fernandabeppler.com.br/combo-black/` (Elementor, CSS `post-1530.css`), lida em 09/11/2026.
O kit global do Elementor (`post-5.css`, Roboto e azuis) é o padrão do tema e **não** é usado na página; ignore.

## Overview

**Creative North Star: "A Biblioteca à Luz de Vela"**

Fundo marrom quase preto, como madeira escura à noite, com texto creme e dourado de vela. Uma serifada clássica (Crimson Pro) carrega tudo, de título a corpo; a ênfase é sempre itálico em negrito dourado, nunca cor nova. O clima é de acervo mágico e íntimo, não de tecnologia.

A densidade é média: blocos centralizados, títulos grandes em duas linhas, e cartões discretos de vidro escuro (preenchimento branco a 3%, borda branca a 20%). O único elemento que foge da paleta quente é o botão verde de compra, de propósito: ele é o sinal de ação.

**Key Characteristics:**
- Fundo espresso (#210E01) em quase toda a página.
- Crimson Pro em tudo; itálico negrito dourado para a palavra que importa.
- Cartões translúcidos com borda fina, cantos de 11px.
- Bloco de oferta em ferrugem (#933B0E) com cartões brancos dentro.
- CTA em pílula verde, caixa alta, sem serifa.

## Colors

Paleta quente de madeira, vela e pergaminho, com um verde isolado para a ação.

### Primary
- **Candle Gold** (`candle-gold`): palavra de ênfase nos títulos ("para sempre", "Cursos Atuais:", "E ainda:"). Itálico ou negrito.

### Secondary
- **Ember Rust** (`ember-rust`): fundo do bloco de preço/oferta. Só ali.
- **CTA Green** (`cta-green`): botões de compra. Borda/brilho em **Mint Glow** (`mint-glow`).

### Neutral
- **Espresso** (`espresso`) e **Espresso Deep** (`espresso-deep`): fundo da página e faixas.
- **Bark** (`bark`): superfícies um tom acima do fundo.
- **Parchment** (`parchment`): texto principal sobre escuro.
- **Peach Cream** (`peach-cream`) e **Apricot** (`apricot`): títulos claros e cartões claros de apoio (boleto).
- **Cocoa** (`cocoa`): texto escuro sobre cartões claros.

### Named Rules
**The One Gold Word Rule.** Em cada título, só uma palavra ou expressão vai em dourado. O resto fica em creme.
**The Green Means Buy Rule.** Verde existe só em CTA de compra. Nunca em número, gráfico ou destaque.

## Typography

**Display Font:** Crimson Pro (com Georgia, serif)
**Label Font:** Helvetica (com Arial), só em botão

**Character:** Serifada literária, de livro antigo, com pesos de 200 a 900 e itálico. A sem serifa aparece só no botão, pequena e em caixa alta.

### Hierarchy
- **Display** (400, 4.8em, 1.05): título do hero.
- **Headline** (400, 2.6em a 2.8em): títulos de seção, centralizados, em duas linhas.
- **Emphasis** (700 itálico): palavra-chave em dourado dentro do título.
- **Body** (400, 1.2em a 1.4em, 1.3): parágrafos curtos, centralizados.
- **Label** (700, 0.8em, caixa alta, Helvetica): texto de botão.

## Layout

Coluna central estreita (cerca de 720px de conteúdo útil em desktop), tudo centralizado. Seções separadas por bastante respiro vertical. Grades de 2 colunas para cartões de benefício e de preço, com espaçamento curto (cerca de 12px).

## Elevation & Depth

Plano. Profundidade vem de camadas tonais (espresso, bark, vidro a 3%) e das fotos com brilho de fogueira, não de sombra. Não há `box-shadow` relevante no CSS da página.

## Shapes

Cantos suaves em cartões (11px), arredondamento grande em painéis (2em) e pílula total em botões (4em). Bordas de 1px, translúcidas.

## Components

### Buttons
- **Shape:** pílula (4em).
- **Primary:** verde `cta-green`, texto branco Helvetica em caixa alta, borda 1px `mint-glow`.

### Cards / Containers
- **Vidro escuro:** preenchimento `glass-fill`, borda 1px `glass-border`, cantos de 11px, ícone dourado à esquerda e texto creme.
- **Preço:** cartão branco dentro do painel ferrugem; número grande em Crimson Pro escuro.

## Do's and Don'ts

### Do:
- **Do** usar fundo `espresso` e texto `parchment` como base.
- **Do** destacar uma única palavra por título em `candle-gold`, em itálico ou negrito.
- **Do** usar Crimson Pro também para números grandes.

### Don't:
- **Don't** usar o kit global do Elementor (Roboto, #6EC1E4, #61CE70): não aparece na página.
- **Don't** usar azul nem cores frias; a única cor fora da paleta quente é o verde do CTA.
- **Don't** usar verde fora de botão de compra.
