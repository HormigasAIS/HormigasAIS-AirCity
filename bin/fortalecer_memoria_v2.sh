#!/bin/bash

BASE_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
TIMESTAMP=$(date -Iseconds)

echo "🐜 Iniciando fortalecimiento estructural de persistencia..."

# -------- 1. CASTAS: Crear estado persistente estructurado --------

for i in {1..7}; do
    CASTA="$BASE_DIR/CASTA_$i"
    STATE_FILE="$CASTA/state.json"
    TMP_FILE="$CASTA/voto.tmp"

    if [ ! -d "$CASTA" ]; then
        echo "⚠️  Casta $i no existe. Saltando..."
        continue
    fi

    # Si no existe state.json, crearlo
    if [ ! -f "$STATE_FILE" ]; then
        echo "📁 Creando state.json en Casta $i..."

        echo "{
    \"caste_id\": $i,
    \"ultimo_voto\": null,
    \"historial_consenso\": [],
    \"nivel_confianza\": 0.0,
    \"ultima_actualizacion\": \"$TIMESTAMP\"
}" > "$STATE_FILE"
    fi

    # Migrar contenido de voto.tmp si existe
    if [ -f "$TMP_FILE" ]; then
        echo "🔄 Migrando voto.tmp en Casta $i..."

        RAW_CONTENT=$(cat "$TMP_FILE" | sed 's/"/\\"/g')

        # Insertar contenido como evento en historial
        jq --arg ts "$TIMESTAMP" \
           --arg voto "$RAW_CONTENT" \
           '.historial_consenso += [{"timestamp": $ts, "evento_migrado": $voto}] 
            | .ultima_actualizacion = $ts' \
           "$STATE_FILE" > "$STATE_FILE.tmp" && mv "$STATE_FILE.tmp" "$STATE_FILE"

        rm "$TMP_FILE"
        echo "✅ Casta $i migrada a persistencia estructurada."
    fi
done

# -------- 2. scan.json como log append-only --------

SCAN_FILE="$BASE_DIR/scan.json"

if [ ! -f "$SCAN_FILE" ]; then
    echo "[]" > "$SCAN_FILE"
fi

if [ ! -s "$SCAN_FILE" ]; then
    echo "[]" > "$SCAN_FILE"
fi

# Agregar entrada estructurada
echo "📡 Añadiendo entrada estructurada a scan.json..."

jq --arg ts "$TIMESTAMP" \
   '. += [{
        "timestamp": $ts,
        "device_id": "TEST_NODE",
        "rssi": -50,
        "confidence": 0.75,
        "source": "bootstrap"
   }]' \
   "$SCAN_FILE" > "$SCAN_FILE.tmp" && mv "$SCAN_FILE.tmp" "$SCAN_FILE"

echo "🚀 Persistencia fortalecida correctamente."
