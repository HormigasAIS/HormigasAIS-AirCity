#!/bin/bash

NODO_ID=$1

if [ -z "$NODO_ID" ]; then
    echo "Uso: ./reiniciar_nodo.sh <numero_nodo>"
    exit 1
fi

NODE_DIR="NODO_$NODO_ID"

if [ ! -d "$NODE_DIR" ]; then
    echo "🚨 $NODE_DIR no existe."
    exit 1
fi

PORT=$((8000 + NODO_ID))

echo "🔄 Reiniciando $NODE_DIR en puerto $PORT..."

python3 -m http.server $PORT --directory "$NODE_DIR" \
    > "$NODE_DIR/nodo.log" 2>&1 &

NEW_PID=$!
echo $NEW_PID > "$NODE_DIR/pid"

echo "✅ $NODE_DIR reiniciado con PID $NEW_PID"
