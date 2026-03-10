#!/data/data/com.termux/files/usr/bin/bash

# --- CONFIGURACIÓN DE CASTA ---
CASTA_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
LOG_CONSENSO="$CASTA_DIR/bus_consenso.log"
FEROMONA_ALERTA=$1

echo "============================================================"
echo " 🐜 HormigasAIS | PROTOCOLO HEPTÁGONO v1.0 (AIR CITY)"
echo "============================================================"
echo "[🔍] Evaluando Feromona: $FEROMONA_ALERTA"

VOTOS=0
NODOS_ACTIVOS=7

# --- SIMULACIÓN DE VOTACIÓN ---
for i in {1..7}
do
    # Cada nodo realiza una validación LBH (Simulada por velocidad)
    # En un entorno real, aquí se valida la firma criptográfica
    sleep 0.2
    
    # Simulación de fallo aleatorio (Resiliencia)
    PROBABILIDAD=$(( RANDOM % 10 ))
    if [ $PROBABILIDAD -gt 1 ]; then
        echo "[✅] Nodo CASTA_0$i: VALIDADO"
        ((VOTOS++))
    else
        echo "[🚨] Nodo CASTA_0$i: ERROR/TIMEOUT (Resiliencia Activa)"
    fi
done

# --- RESOLUCIÓN DE SOBERANÍA ---
echo "------------------------------------------------------------"
echo "RESULTADO: $VOTOS / $NODOS_ACTIVOS Votos de Casta"

if [ $VOTOS -ge 4 ]; then
    echo "[🏆] CONSENSO ALCANZADO: Acción Autorizada para Air City."
    echo "[$(date)] CONSENSO_EXITOSO | Feromona: $FEROMONA_ALERTA | Votos: $VOTOS" >> $LOG_CONSENSO
else
    echo "[❌] FALLO DE CONSENSO: Seguridad Comprometida o Error Crítico."
    echo "[$(date)] CONSENSO_FALLIDO | Feromona: $FEROMONA_ALERTA | Votos: $VOTOS" >> $LOG_CONSENSO
fi
echo "============================================================"
