#!/bin/bash

BASE_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
LOG_FILE="$BASE_DIR/capullo_soberano.log"

echo "==============================================="
echo "🐜 AIR CITY - ACTIVIDAD OPERATIVA CUANTIFICADA"
echo "==============================================="

if [ ! -f "$LOG_FILE" ]; then
    echo "⚠️  capullo_soberano.log no encontrado."
    exit 1
fi

SIZE_MB=$(du -m "$LOG_FILE" | awk '{print $1}')
LINES=$(grep -c '^\[' "$LOG_FILE")

FIRST_LINE=$(grep '^\[' "$LOG_FILE" | head -1)
LAST_LINE=$(grep '^\[' "$LOG_FILE" | tail -1)

FIRST_TS=$(echo "$FIRST_LINE" | awk -F'[][]' '{print $2}' | cut -d'.' -f1)
LAST_TS=$(echo "$LAST_LINE" | awk -F'[][]' '{print $2}' | cut -d'.' -f1)

FIRST_HUMAN=$(date -d @"$FIRST_TS" +"%Y-%m-%d %H:%M:%S")
LAST_HUMAN=$(date -d @"$LAST_TS" +"%Y-%m-%d %H:%M:%S")

DURATION_SEC=$((LAST_TS - FIRST_TS))
DURATION_HOURS=$(awk "BEGIN {printf \"%.2f\", $DURATION_SEC/3600}")
EVENT_RATE=$(awk "BEGIN {printf \"%.2f\", $LINES/$DURATION_SEC}")

echo "📦 Tamaño del log: ${SIZE_MB}MB"
echo "📄 Total de eventos válidos: $LINES"
echo "-----------------------------------------------"
echo "🕰 Primer evento:  $FIRST_HUMAN"
echo "🕰 Último evento:  $LAST_HUMAN"
echo "-----------------------------------------------"
echo "⏱ Tiempo total en operación: ${DURATION_HOURS} horas"
echo "⚡ Frecuencia promedio: ${EVENT_RATE} eventos/segundo"
echo "-----------------------------------------------"
echo "📜 Últimos 10 eventos:"
echo "-----------------------------------------------"

grep '^\[' "$LOG_FILE" | tail -10

echo "==============================================="
echo "✅ Sistema activo, medible y cuantificado."
echo "==============================================="
