#!/bin/bash
echo "💉 [HormigasAIS] Iniciando Cirugía de Resurrección LBH..."

# 1. Limpieza Profunda
pkill -9 -f python3
rm -f ~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY/*.json
sleep 2

# 2. Lanzamiento en Cascada con Monitoreo
cd ~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY

echo "🐜 Despertando Nodo 9301..."
python3 nodo_cluster_raft_log_server.py 9301 9302,9303 > ../nodo_10301.log 2>&1 &
sleep 5

echo "🐜 Despertando Nodo 9302..."
python3 nodo_cluster_raft_log_server.py 9302 9301,9303 > ../nodo_10302.log 2>&1 &
sleep 5

echo "🐜 Despertando Nodo 9303..."
python3 nodo_cluster_raft_log_server.py 9303 9301,9302 > ../nodo_10303.log 2>&1 &

echo "⌛ Esperando Consenso de la Colonia (30 segundos)..."
sleep 30

# 3. Localización Quirúrgica del Líder
for port in 10301 10302 10303; do
    ROLE=$(curl -s http://127.0.0.1:$port/status | jq -r '.role')
    if [ "$ROLE" == "LEADER" ]; then
        echo "👑 Líder encontrado en puerto $port"
        CURRENT_LEADER=$port
        break
    fi
done

if [ -z "$CURRENT_LEADER" ]; then
    echo "❌ Fallo de Consenso: No hay líder. Intentando forzar Nodo 9301..."
    CURRENT_LEADER=10301
fi

# 4. Sello de Soberanía Final
echo "📡 Sellando Contrato en $CURRENT_LEADER..."
curl -s -X POST -H "Content-Type: application/json" \
-d '{"key": "CONTRATO_AIR_2026", "value": "SOBERANIA_TOTAL_QUIÑONEZ"}' \
http://127.0.0.1:$CURRENT_LEADER/set

echo "🔍 Estado de Persistencia:"
cat state_*.json
