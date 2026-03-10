#!/bin/bash

REQUESTS=${1:-100}
echo "⚡ Generando $REQUESTS requests..."

for i in $(seq 1 $REQUESTS); do
    for PORT in 8001 8002 8003 8004 8005; do
        curl -s http://localhost:$PORT > /dev/null &
    done
done

wait

echo "✅ Stress test finalizado."
