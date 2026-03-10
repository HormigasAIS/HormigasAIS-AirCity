#!/bin/bash

BASE_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
LOG_FILE="$BASE_DIR/auditoria_integridad.log"
TIMESTAMP=$(date -Iseconds)

echo "==========================================" | tee -a "$LOG_FILE"
echo "🔍 Verificación iniciada: $TIMESTAMP" | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

for i in {1..7}; do
    CASTA="$BASE_DIR/CASTA_$i"
    STATE_FILE="$CASTA/state.json"

    if [ ! -f "$STATE_FILE" ]; then
        echo "⚠️  Casta $i sin state.json" | tee -a "$LOG_FILE"
        continue
    fi

    echo "🧠 Verificando Casta $i..." | tee -a "$LOG_FILE"

    HASH_STORED=$(jq -r '.checksum_integridad // empty' "$STATE_FILE")

    if [ -z "$HASH_STORED" ]; then
        echo "🚨 Casta $i sin checksum. Marcada como COMPROMETIDA." | tee -a "$LOG_FILE"
        continue
    fi

    # Crear versión temporal SIN checksum
    jq 'del(.checksum_integridad)' "$STATE_FILE" > "$STATE_FILE.verify.tmp"

    HASH_CALCULATED=$(sha256sum "$STATE_FILE.verify.tmp" | awk '{print $1}')
    rm "$STATE_FILE.verify.tmp"

    if [ "$HASH_STORED" == "$HASH_CALCULATED" ]; then
        echo "✅ Casta $i íntegra." | tee -a "$LOG_FILE"
    else
        echo "🚨 ALERTA: Casta $i COMPROMETIDA." | tee -a "$LOG_FILE"

        jq \
          --arg ts "$TIMESTAMP" \
          '.estado_actual = "COMPROMETIDA"
           | .ultima_actualizacion = $ts' \
          "$STATE_FILE" > "$STATE_FILE.tmp"

        mv "$STATE_FILE.tmp" "$STATE_FILE"
    fi
done

echo "==========================================" | tee -a "$LOG_FILE"
echo "🔒 Verificación finalizada correctamente." | tee -a "$LOG_FILE"
echo "==========================================" | tee -a "$LOG_FILE"

