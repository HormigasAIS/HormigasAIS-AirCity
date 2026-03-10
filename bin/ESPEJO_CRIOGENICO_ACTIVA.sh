#!/data/data/com.termux/files/usr/bin/bash

CASTA_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
#!/data/data/com.termux/files/usr/bin/bash

CASTA_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
FEROMONA="${1:-TEST}"

# 1. LECTURA DE HARDWARE CON TIEMPO LÍMITE (Evita que se cuelgue)
# Si en 1 segundo no responde la batería, asume 100% y sigue.
BATERIA=$(timeout 1s termux-battery-status 2>/dev/null | grep percentage | awk -F: '{print $2}' | tr -d ' ,')
BATERIA=${BATERIA:-100}

echo "============================================================"
echo " ❄️ ESPEJO CRIOGÉNICO v3.4 | RESILIENCIA TOTAL"
echo " Energía: $BATERIA% | San Miguel, SV"
echo "============================================================"

# 2. CONFIGURACIÓN DE LATENCIA
WAIT_TIME=1
[ $BATERIA -lt 25 ] && WAIT_TIME=3

# 3. LANZAMIENTO PARALELO
rm -f $CASTA_DIR/CASTA_*/voto.tmp
for i in {1..7}; do
    bash $CASTA_DIR/NODO_ESPEJO.sh $i "$FEROMONA" &
done

# 4. ESPERA DE SEGURIDAD
sleep $WAIT_TIME

# 5. CONTEO
EXITOS=$(ls $CASTA_DIR/CASTA_*/voto.tmp 2>/dev/null | wc -l)
echo "------------------------------------------------------------"
echo "CONSENSO: $EXITOS / 7"
[ $EXITOS -ge 4 ] && echo "[🏆] SOBERANÍA CONFIRMADA" || echo "[🚨] FALLO DE NODO"
echo "============================================================"
FEROMONA="${1:-ACCION_ESTANDAR}"

# 1. LECTURA DE HARDWARE (Energía Real)
BATERIA=$(termux-battery-status 2>/dev/null | grep percentage | awk -F: '{print $2}' | tr -d ' ,')
BATERIA=${BATERIA:-100} # Respaldo si no hay termux-api

echo "============================================================"
echo " ❄️ ESPEJO CRIOGÉNICO v3.3 | SOBERANÍA ENERGÉTICA"
echo " Ubicación: San Miguel, SV | Energía: $BATERIA%"
echo "============================================================"

# 2. AJUSTE DE LATENCIA SEGÚN ENERGÍA
# Si hay poca batería, el sistema "respira" más lento para no drenarla
if [ $BATERIA -lt 25 ]; then
    echo "[🪫] ALERTA: MODO HIBERNACIÓN ACTIVO (Resiliencia Extrema)"
    WAIT_TIME=4
else
    WAIT_TIME=1
fi

# 3. LANZAMIENTO DEL HEPTÁGONO
rm -f $CASTA_DIR/CASTA_*/voto.tmp
for i in {1..7}; do
    bash $CASTA_DIR/NODO_ESPEJO.sh $i "$FEROMONA" &
done

# El sistema espera según su estado energético
sleep $WAIT_TIME

# 4. CONTEO DE SOBERANÍA
EXITOS=$(ls $CASTA_DIR/CASTA_*/voto.tmp 2>/dev/null | wc -l)
echo "------------------------------------------------------------"
echo "ESTADO DEL ENJAMBRE: $EXITOS / 7"

if [ $EXITOS -ge 4 ]; then
    echo "[🏆] CONSENSO ALCANZADO | Air City Segura."
else
    echo "[🚨] FALLO DE COORDINACIÓN | Revisar Entropía."
fi
echo "============================================================"

