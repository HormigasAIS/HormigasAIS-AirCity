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

FIRST_LINE=$(head -1 "$LOG_FILE")
LAST_LINE=$(tail -1 "$LOG_FILE")

echo "📦 Tamaño del log: ${SIZE_MB}MB"
echo "📄 Total de eventos registrados: $LINES"
echo "------------------------------------------"
echo "🕰 Primer evento registrado:"
echo "$FIRST_LINE"
echo "------------------------------------------"
echo "🕰 Último evento registrado:"
echo "$LAST_LINE"
echo "------------------------------------------"
echo "📜 Últimos 20 eventos:"
echo "------------------------------------------"

tail -20 "$LOG_FILE"

echo "=========================================="
echo "✅ Sistema con actividad histórica continua."
echo "=========================================="
