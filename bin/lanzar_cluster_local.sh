#!/bin/bash

BASE_DIR="$PWD"
NODOS=${1:-3}

echo "🚀 Lanzando cluster local con $NODOS nodos..."

for i in $(seq 1 $NODOS); do
    NODE_DIR="$BASE_DIR/NODO_$i"
    mkdir -p "$NODE_DIR"
    cp -r CASTA_* "$NODE_DIR/" 2>/dev/null

    PORT=$((8000 + i))

    echo "🧠 Iniciando nodo $i en puerto $PORT"

    python3 -m http.server $PORT --directory "$NODE_DIR" \
        > "$NODE_DIR/nodo.log" 2>&1 &

    echo $! > "$NODE_DIR/pid"
done

echo "✅ Cluster lanzado."
