#!/bin/bash

BASE_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
TIMESTAMP=$(date -Iseconds)

echo "🔒 Endureciendo infraestructura de estado..."

for i in {1..7}; do
    CASTA="$BASE_DIR/CASTA_$i"
    STATE_FILE="$CASTA/state.json"

    if [ ! -f "$STATE_FILE" ]; then
        echo "⚠️  Casta $i sin state.json. Saltando..."
        continue
    fi

    echo "🧠 Procesando Casta $i..."

    # Obtener último evento del historial
    ULTIMO_EVENTO=$(jq -r '.historial_consenso[-1].evento_migrado // empty' "$STATE_FILE")

    # Determinar estado actual
    if [ -n "$ULTIMO_EVENTO" ]; then
        ESTADO_ACTUAL="$ULTIMO_EVENTO"
    else
        ESTADO_ACTUAL="INACTIVO"
    fi

    # Calcular nivel_confianza basado en historial
    VALIDACIONES=$(jq '[.historial_consenso[] | select(.evento_migrado=="VALIDADO")] | length' "$STATE_FILE")
    RECHAZOS=$(jq '[.historial_consenso[] | select(.evento_migrado=="RECHAZADO")] | length' "$STATE_FILE")

    TOTAL=$((VALIDACIONES + RECHAZOS))

    if [ "$TOTAL" -gt 0 ]; then
        NIVEL=$(awk "BEGIN {printf \"%.2f\", ($VALIDACIONES - $RECHAZOS)/$TOTAL}")
    else
        NIVEL="0.0"
    fi

    # Crear JSON temporal sin checksum
    jq \
        --arg estado "$ESTADO_ACTUAL" \
        --arg nivel "$NIVEL" \
        --arg ts "$TIMESTAMP" \
        '.estado_actual = $estado
         | .ultimo_voto = $estado
         | .nivel_confianza = ($nivel | tonumber)
         | .ultima_actualizacion = $ts
         | del(.checksum_integridad)' \
        "$STATE_FILE" > "$STATE_FILE.tmp"

    # Generar checksum SHA256
    CHECKSUM=$(sha256sum "$STATE_FILE.tmp" | awk '{print $1}')

    # Insertar checksum
    jq \
        --arg hash "$CHECKSUM" \
        '.checksum_integridad = $hash' \
        "$STATE_FILE.tmp" > "$STATE_FILE"

    rm "$STATE_FILE.tmp"

    echo "✅ Casta $i actualizada | Estado: $ESTADO_ACTUAL | Confianza: $NIVEL"
done

echo "🚀 Infraestructura de castas endurecida correctamente."
