#!/bin/bash

echo "🗳 Ejecutando consenso..."

TOTAL=0
VALIDOS=0

for dir in NODO_*; do
    if [ -f "$dir/voto.txt" ]; then
        VOTO=$(cat "$dir/voto.txt")
        TOTAL=$((TOTAL+1))
        if [ "$VOTO" == "VALIDADO" ]; then
            VALIDOS=$((VALIDOS+1))
        fi
    fi
done

if [ $TOTAL -eq 0 ]; then
    echo "⚠️ No hay votos."
    exit 1
fi

MAYORIA=$((TOTAL/2 + 1))

echo "Votos totales: $TOTAL"
echo "Votos válidos: $VALIDOS"
echo "Mayoría requerida: $MAYORIA"

if [ $VALIDOS -ge $MAYORIA ]; then
    echo "✅ CONSENSO ALCANZADO"
else
    echo "❌ CONSENSO FALLIDO"
fi
