#!/usr/bin/env bash
# Gera as versões -teste a partir dos arquivos de produção.
# Diferenças: nome do nó n8n ('Code in JavaScript' no prod, 'Code' no teste),
# relógio travado nos -teste.js e parágrafo DATETIME no prompt-teste.md.
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

# Relógio de teste: 23/09 10h00 (aberto + boleto no payload).
TEST_NOW='2026-09-23T10:00:00'
for f in links-teste.js bonus-teste.js; do
  python3 - "$f" "$TEST_NOW" <<'PY'
import re, sys
path, iso = sys.argv[1], sys.argv[2]
new = f"const now = DateTime.fromISO('{iso}', {{ zone: 'America/Sao_Paulo' }});"
text = open(path).read()
# links.js: bloco SIMULAR_CARRINHO_ABERTO (comentário + const + ternário).
simular = re.compile(r"// SIMULAR=true.*?const now = SIMULAR_CARRINHO_ABERTO\n.*?: DateTime\.now\(\)\.setZone\('America/Sao_Paulo'\);", re.S)
# bonus.js: linha única.
linha = "const now = DateTime.now().setZone('America/Sao_Paulo');"
if simular.search(text):
    text = simular.sub(lambda m: f"// Relógio de teste: {iso[8:10]}/{iso[5:7]} {iso[11:13]}h{iso[14:16]} (aberto + boleto liberado).\n" + new, text, count=1)
elif linha in text:
    text = text.replace(linha, new, 1)
else:
    raise SystemExit(f"{path}: relógio de prod não encontrado")
if "DateTime.now()" in text:
    raise SystemExit(f"{path}: sobrou DateTime.now() depois de travar o relógio")
open(path, "w").write(text)
PY
  echo "  $f -> relógio $TEST_NOW"
done

python3 - prompt-teste.md <<'PY'
from pathlib import Path
p = Path("prompt-teste.md")
old = "A data e hora atual é `$now`. Preço e condição mudam com o calendário — consulte `get_links` antes de informar valor ou enviar link."
new = "A data injetada pelo n8n (`$now`) pode ser hoje, 15/09. **Ignore essa data para abrir ou fechar o carrinho.** A única fonte é o `status` de `get_links`. Se vier `aberto`, venda — as tools de teste estão com relógio travado em 23/09 10h00 (boleto no payload)."
text = p.read_text()
if old not in text:
    raise SystemExit("prompt-teste.md: bloco DATETIME de prod não encontrado")
p.write_text(text.replace(old, new, 1))
print("  prompt-teste.md -> DATETIME de teste")
PY

echo "Pronto."
