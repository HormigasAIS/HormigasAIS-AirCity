#!/bin/bash

BASE_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
LOG_FILE="$BASE_DIR/capullo_soberano.log"

echo "=========================================="
echo "🐜 HISTORIAL OPERATIVO - AIR CITY"
echo "=========================================="

if [ ! -f "$LOG_FILE" ]; then
    echo "⚠️  capullo_soberano.log no encontrado."
    exit 1
fi

SIZE_MB=$(du -m "$LOG_FILE" | awk '{print $1}')
LINES=$(wc -l < "$LOG_FILE")

echo "📦 Tamaño del log: ${SIZE_MB}MB"
echo "📄 Total de líneas: $LINES"
echo "------------------------------------------"
echo "📜 Últimos 20 eventos:"
echo "------------------------------------------"

tail -20 "$LOG_FILE"

echo "=========================================="
echo "✅ Sistema en operación histórica verificada."
echo "=========================================="
