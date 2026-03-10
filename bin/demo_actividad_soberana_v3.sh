#!/bin/bash

BASE_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
LOG_FILE="$BASE_DIR/capullo_soberano.log"

echo "=========================================="
echo "🐜 AIR CITY - ACTIVIDAD OPERATIVA REAL"
echo "=========================================="

if [ ! -f "$LOG_FILE" ]; then
    echo "⚠️  capullo_soberano.log no encontrado."
    exit 1
fi

SIZE_MB=$(du -m "$LOG_FILE" | awk '{print $1}')
LINES=$(wc -l < "$LOG_FILE")

FIRST_VALID=$(grep '^\[' "$LOG_FILE" | head -1)
LAST_VALID=$(grep '^\[' "$LOG_FILE" | tail -1)

echo "📦 Tamaño del log: ${SIZE_MB}MB"
echo "📄 Total de líneas registradas: $LINES"
echo "------------------------------------------"
echo "🕰 Primer evento válido:"
echo "$FIRST_VALID"
echo "------------------------------------------"
echo "🕰 Último evento válido:"
echo "$LAST_VALID"
echo "------------------------------------------"
echo "📜 Últimos 20 eventos:"
echo "------------------------------------------"

grep '^\[' "$LOG_FILE" | tail -20

echo "=========================================="
echo "✅ Sistema con actividad histórica continua."
echo "=========================================="
