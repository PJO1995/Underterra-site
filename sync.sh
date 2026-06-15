#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# Underterra Inventory Sync
# Corre este script desde tu Mac para sincronizar maquinaria nueva
# de MachineryTrader con el sitio web.
#
# Uso: bash ~/Desktop/underterra-deploy/sync.sh
# ─────────────────────────────────────────────────────────────────

set -e
cd "$(dirname "$0")"

echo "🔍 Buscando maquinaria nueva en MachineryTrader..."
python3 scraper/scraper.py

echo ""
echo "📤 Subiendo cambios al sitio..."
git add index.html
if git diff --staged --quiet; then
  echo "✅ El inventario ya está al día — no hay máquinas nuevas."
else
  git commit -m "🤖 Sync inventario MachineryTrader [$(date +'%Y-%m-%d')]"
  git push
  echo ""
  echo "🚀 ¡Listo! El sitio se actualizará en ~30 segundos en underterrallc.com"
fi
