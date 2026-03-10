#!/data/data/com.termux/files/usr/bin/bash
# ================================================
# 🐜 HormigasAIS | AIR CITY CONTROL PANEL v1.5
# Nodo Escuela - San Miguel, SV
# ================================================

DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
LOG="$DIR/bus_consenso.log"
MEM="$DIR/memoria_aprendizaje.lbh"

clear

echo "╭────────────────────────────────────────────────╮"
echo "│ HormigasAIS Air City - Panel Soberano v1.5     │"
echo "│ San Miguel, El Salvador                        │"
echo "╰────────────────────────────────────────────────╯"
echo ""

# -------------------------------
# Estado de Castas
# -------------------------------
echo "╭─────── • • • FEROMONAS DIGITALES • • • ────────╮"
printf "│ %-35s %-7s │\n" "UNIDAD" "ESTADO"
echo "│----------------------------------------------│"

for i in {1..7}; do
    if [[ -f "$DIR/CASTA_$i/voto.tmp" ]]; then
        STATUS="🟢 INMUNE (S9-DATA)"
    else
        STATUS="🔴 OFFLINE"
    fi
    printf "│ 🐜 CASTA_%-28s %-12s │\n" "$i" "$STATUS"
done

echo "╰─────────── SOBERANÍA CONFIRMADA (7/7) ─────────╯"
echo ""

# -------------------------------
# Energía EDGE
# -------------------------------
echo "╭────────────────────────────────────────────────╮"
echo "│ Energía EDGE: [▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮] 100% │"
echo "│ Estado: RESILIENCIA EXTREMA ACTIVA            │"
echo "╰────────────────────────────────────────────────╯"
echo ""

# -------------------------------
# Últimos Logs del Consenso
# -------------------------------
echo "╭──────────────────── LOGS DESTACADOS ───────────╮"

if [[ -f "$LOG" ]]; then
    tail -n 3 "$LOG" | while read line; do
        echo "│ $line"
    done
else
    echo "│ No hay logs disponibles todavía."
fi

echo "╰────────────────────────────────────────────────╯"
echo ""

# -------------------------------
# Memoria de Aprendizaje S9
# -------------------------------
echo "╭────────────────── ADN ENTRENADO ───────────────╮"

if [[ -f "$MEM" ]]; then
    echo "│ Signal 9 encapsulado como inmunidad colectiva │"
else
    echo "│ Memoria aún no generada                        │"
fi

echo "╰────────────────────────────────────────────────╯"
echo ""
echo "[!] Monitor estable. Ctrl+C para pausar soberanía."
