#!/bin/bash
# =================================================================
# 🐜 PADRE AIR CITY v2.0 — PROTOCOLO CAPULLO (LBH SOBERANO)
# Fundador: Cristhiam Leonardo Hernández Quiñonez
# =================================================================

BASE_DIR="$HOME/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY"
LOG="$BASE_DIR/capullo_soberano.log"
IP_LIMON="192.168.1.2" # <-- Ajustar a la IP real de tu server Limón
MODELO=$(getprop ro.product.model)

function sello() {
  echo "────────────────────────────────────────────────────────────"
  echo "  🐜 HORMIGASAIS - MODO CAPULLO (AIR CITY DEMO) "
  echo "  INFRAESTRUCTURA DE INTELIGENCIA DISTRIBUIDA "
  echo "────────────────────────────────────────────────────────────"
  echo "FECHA: $(date)"
  echo "NODO DETECTADO: $MODELO"
  echo "SISTEMA: LBH (Lenguaje Binario HormigasAIS)"
  echo "────────────────────────────────────────────────────────────"
}

function validar_rol() {
  # Identificación automática de Soberanía
  if [[ "$MODELO" == *"A16"* ]]; then
    ROL="CENTINELA"
    IP_ASIGNADA="192.168.1.5"
    echo "[🛡️] ROL: NODO MAESTRO / VALIDADOR (A16)"
  elif [[ "$MODELO" == *"A20"* ]]; then
    ROL="CAPULLO_EMISOR"
    IP_ASIGNADA="192.168.1.15"
    echo "[🌱] ROL: NODO PERIFÉRICO / BEACON (A20s)"
  else
    echo "[?] Hardware no identificado. Entrando en modo GENÉRICO."
    ROL="OBSERVADOR"
  fi
}

function ejecutar_logistica() {
  case "$ROL" in
    "CENTINELA")
      echo "[🚀] Iniciando Panel de Control de Camiones (Heptágono)..."
      # El A16 procesa visualización y consulta a Limón
      python3 "$BASE_DIR/CENTINELA_V2.6_LIMON.py"
      ;;
    "CAPULLO_EMISOR")
      echo "[📡] Emitiendo Feromona Digital LBH: S9-DATA-IMMUNE-2026..."
      # El A20s envía el pulso de verdad a la Nube Limón
      curl -X POST -d "{\"adn\":\"S9-DATA-IMMUNE-2026\", \"origin\":\"A20s\"}" http://$IP_LIMON:8080/reporte
      python3 "$BASE_DIR/BEACON_AIR_CITY.py"
      ;;
    *)
      echo "Esperando asignación de jerarquía..."
      ;;
  esac
}

# ======== EJECUCIÓN SOBERANA ========
clear
sello | tee -a "$LOG"
validar_rol | tee -a "$LOG"
ejecutar_logistica

