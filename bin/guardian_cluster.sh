#!/bin/bash
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

BASE="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
LOG="$HOME/HormigasAIS-Nodo-Escuela/guardian_cluster.log"
SCRIPT="$BASE/nodo_cluster_raft_log_server.py"
CHECK_INTERVAL=20
ESTABILIZACION=35

declare -A NODOS
NODOS[9301]="9302,9303"
NODOS[9302]="9301,9303"
NODOS[9303]="9301,9302"

timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
log() { echo -e "$1"; echo "[$(timestamp)] $2" >> "$LOG"; }

nodo_vivo() {
    local http=$((${1} + 1000))
    curl -s --connect-timeout 1 http://127.0.0.1:$http/status > /dev/null 2>&1
}

lanzar_nodo() {
    local port=$1
    local peers="${NODOS[$port]}"
    local http=$((port + 1000))
    local logfile="$HOME/HormigasAIS-Nodo-Escuela/nodo_$http.log"
    log "${YELLOW}⚡ Relanzando nodo $port...${NC}" "RELAUNCH | port=$port"
    cd "$BASE"
    nohup python3 "$SCRIPT" $port $peers >> "$logfile" 2>&1 &
    disown
}

# ── ARRANQUE INTELIGENTE ──────────────────────────────
log "${GREEN}🐜 Guardian LBH v1.2 Iniciado${NC}" "START"

VIVOS=0
for port in 9301 9302 9303; do
    nodo_vivo $port && ((VIVOS++))
done

if [ "$VIVOS" -eq 3 ]; then
    log "${GREEN}✅ Cluster ya activo ($VIVOS/3). Omitiendo reset.${NC}" "SKIP_RESET"
elif [ "$VIVOS" -gt 0 ]; then
    log "${YELLOW}⚠️  Cluster parcial ($VIVOS/3). Relanzando caídos...${NC}" "PARTIAL_RESET"
    for port in 9301 9302 9303; do
        nodo_vivo $port || { lanzar_nodo $port; sleep 4; }
    done
    sleep $ESTABILIZACION
else
    log "${RED}🚨 Cluster muerto. Reinicio total...${NC}" "FULL_RESET"
    pkill -9 -f nodo_cluster_raft_log_server 2>/dev/null
    sleep 2
    for port in 9301 9302 9303; do
        lanzar_nodo $port; sleep 4
    done
    sleep $ESTABILIZACION
fi

# ── BUCLE DE VIGILANCIA ───────────────────────────────
log "${CYAN}👁  Iniciando vigilancia...${NC}" "WATCH_START"

while true; do
    sleep $CHECK_INTERVAL
    MUERTOS=()
    LIDER=""

    for port in 9301 9302 9303; do
        if ! nodo_vivo $port; then
            MUERTOS+=($port)
        else
            local_http=$((port + 1000))
            role=$(curl -s --connect-timeout 1 http://127.0.0.1:$local_http/status | jq -r '.role // empty' 2>/dev/null)
            [ "$role" = "LEADER" ] && LIDER=$local_http
        fi
    done

    if [ ${#MUERTOS[@]} -eq 0 ]; then
        log "${GREEN}💚 Cluster sano | Líder: $LIDER${NC}" "HEALTHY | lider=$LIDER"
    elif [ ${#MUERTOS[@]} -ge 2 ]; then
        log "${RED}🚨 Quórum perdido — reinicio completo${NC}" "QUORUM_LOST"
        pkill -9 -f nodo_cluster_raft_log_server 2>/dev/null
        sleep 2
        for port in 9301 9302 9303; do
            lanzar_nodo $port; sleep 4
        done
        sleep $ESTABILIZACION
    else
        for p in "${MUERTOS[@]}"; do
            lanzar_nodo $p; sleep 5
        done
    fi
done
