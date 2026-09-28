#!/bin/bash
# ─────────────────────────────────────────────────────────────────
# Underterra Inventory Sync
# Corre este script desde tu Mac para sincronizar maquinaria nueva
# de MachineryTrader con el sitio web.
#
# Uso: bash ~/Desktop/underterra-deploy/sync.sh
# ─────────────────────────────────────────────────────────────────

cd "$(dirname "$0")"

# Si algo falla de aquí en adelante, avisa claro y NO cierres la ventana sola
# (antes, si el push fallaba, la ventana se cerraba antes de que se viera el error).
on_error() {
  echo ""
  echo "❌ Algo falló — mira el mensaje de error arriba (en rojo o con la palabra 'error')."
  echo "   Copia todo lo que salió en esta ventana y pégaselo a Claude para revisarlo."
  read -p "Presiona Enter para cerrar esta ventana..."
  exit 1
}
trap on_error ERR
set -e

echo "🔍 Buscando maquinaria nueva en MachineryTrader..."
python3 scraper/scraper.py

echo ""
echo "📤 Subiendo cambios al sitio..."
git add index.html

# Si YA hay commits locales pendientes de subir de una corrida anterior
# (por ejemplo, porque el push de la última vez falló y no nos dimos cuenta),
# los subimos también en este paso — así no se quedan atorados sin avisar.
AHEAD=$(git rev-list --count @{u}..HEAD 2>/dev/null || echo 0)

if git diff --staged --quiet && [ "$AHEAD" -eq 0 ]; then
  echo "✅ El inventario ya está al día — no hay máquinas nuevas."
else
  if ! git diff --staged --quiet; then
    git commit -m "🤖 Sync inventario MachineryTrader [$(date +'%Y-%m-%d')]"
  else
    echo "ℹ️  Había $AHEAD commit(s) de una corrida anterior que nunca se subieron — los subimos ahora."
  fi
  git pull --rebase
  git push
  echo ""
  echo "🚀 ¡Listo! El sitio se actualizará en ~30 segundos en underterrallc.com"
fi

echo ""
read -p "Todo salió bien. Presiona Enter para cerrar esta ventana..."
