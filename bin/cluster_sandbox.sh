#!/usr/bin/env bash
# ===============================================================
# 🚀 Cluster RAFT Log - Wrapper / Sandbox de prueba
# ===============================================================
# Uso:
# ./cluster_sandbox.sh
# Arranca 3 nodos limpios en puertos 9301,9302,9303
# Permite detener nodos y monitorear estado
# ===============================================================

NODES=(9301 9302 9303)
SCRIPT="nodo_cluster_raft_log.py"

# --- FUNCIONES ---
function stop_old_nodes() {
    echo "🔹 Deteniendo nodos antiguos si existen..."
    for p in "${NODES[@]}"; do
        pid=$(lsof -ti tcp:$p)
        if [ ! -z "$pid" ]; then
            kill $pid
            echo "🛑 Puerto $p detenido (PID $pid)"
        fi
    done
}

function start_nodes() {
    echo "🔹 Iniciando cluster RAFT log..."
    for i in "${!NODES[@]}"; do
        peers=("${NODES[@]}")
        unset peers[$i]
        peers_str=$(IFS=,; echo "${peers[*]}")

        # Ejecuta cada nodo en background
        python $SCRIPT "${NODES[$i]}" "$peers_str" &
        echo "✅ Nodo ${NODES[$i]} arrancado con peers: $peers_str"
        sleep 0.5
    done
}

function show_instructions() {
    echo ""
    echo "💡 Instrucciones:"
    echo "  - Usa 'lsof -i :PUERTO' para ver procesos"
    echo "  - Usa 'kill PID' para detener nodos específicos"
    echo "  - Abre terminales separadas para cada nodo si quieres CLI interactiva"
    echo "  - Todos los nodos comparten estado replicado y commit"
    echo ""
}

# --- EJECUCIÓN ---
stop_old_nodes
start_nodes
show_instructions

echo "🟢 Cluster listo. Observa los logs en esta terminal o abre otras para CLI de cada nodo."
wait
