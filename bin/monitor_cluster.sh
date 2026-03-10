#!/bin/bash

echo "🔎 Monitoreando nodos..."

for dir in NODO_*; do
    if [ -f "$dir/pid" ]; then
        PID=$(cat "$dir/pid")
        if ps -p $PID > /dev/null; then
            echo "✅ $dir activo (PID $PID)"
        else
            echo "🚨 $dir caído"
        fi
    fi
done
