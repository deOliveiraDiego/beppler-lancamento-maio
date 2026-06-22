#!/usr/bin/env bash
# Gera as versões -teste a partir dos arquivos de produção.
# Única diferença: nome do nó n8n ('Code in JavaScript' no prod, 'Code' no agente de teste).
# Rodar sempre que mudar links.js, bonus.js ou prompt.md.

set -euo pipefail
cd "$(dirname "$0")"

for src in links.js bonus.js prompt.md; do
  base="${src%.*}"
  ext="${src##*.}"
  dest="${base}-teste.${ext}"
  sed "s/Code in JavaScript/Code/g" "$src" > "$dest"
  echo "  $src -> $dest"
done

echo "Pronto."
