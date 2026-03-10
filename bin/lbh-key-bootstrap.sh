#!/data/data/com.termux/files/usr/bin/bash

echo "🐜 HormigasAIS — LBH-Key Bootstrap Installer"
echo "=========================================="
echo "Creando Nodo Maestro Portátil..."
echo ""

# Carpeta base
BASE="LBH-Key"

# Crear estructura
mkdir -p $BASE/reports

echo "📁 Estructura creada en: $BASE/"
echo ""

# -----------------------------
# lbh_menu.sh
# -----------------------------
cat > $BASE/lbh_menu.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash

clear
echo "🐜 HormigasAIS LBH-Key — Nodo Maestro Portátil"
echo "============================================"
echo "1) Auditoría Edge (Healthcheck)"
echo "2) Evidencia de Latencia (Edge vs Cloud)"
echo "3) Integridad SHA (Stack HormigasAIS)"
echo "4) Generar Reporte Completo"
echo "0) Salir"
echo "--------------------------------------------"

read -p "Selecciona una opción: " opt

case $opt in
  1) bash lbh_audit.sh ;;
  2) bash lbh_latency.sh ;;
  3) bash lbh_integrity.sh ;;
  4) bash lbh_audit.sh && bash lbh_latency.sh && bash lbh_integrity.sh ;;
  0) exit ;;
  *) echo "Opción inválida" ;;
esac
EOF

# -----------------------------
# lbh_audit.sh
# -----------------------------
cat > $BASE/lbh_audit.sh <<'EOF'
#!/bin/bash

TS=$(date "+%Y-%m-%d_%H-%M-%S")
OUT="reports/audit_$TS.txt"

mkdir -p reports

echo "🐜 HormigasAIS — Auditoría de Resiliencia Edge" > $OUT
echo "Timestamp: $TS" >> $OUT
echo "=============================================" >> $OUT

echo "" >> $OUT
echo "[Sistema]" >> $OUT
uname -a >> $OUT

echo "" >> $OUT
echo "[CPU / Memoria]" >> $OUT
free -h >> $OUT

echo "" >> $OUT
echo "[Discos]" >> $OUT
df -h >> $OUT

echo "" >> $OUT
echo "[Red básica]" >> $OUT
ip route >> $OUT

echo "" >> $OUT
echo "[GPU NVIDIA (si existe)]" >> $OUT
if command -v nvidia-smi &>/dev/null; then
  nvidia-smi >> $OUT
else
  echo "No disponible (nvidia-smi no instalado)" >> $OUT
fi

echo "" >> $OUT
echo "✅ Auditoría generada en: $OUT"
EOF

# -----------------------------
# lbh_latency.sh
# -----------------------------
cat > $BASE/lbh_latency.sh <<'EOF'
#!/bin/bash

TS=$(date "+%Y-%m-%d_%H-%M-%S")
OUT="reports/latency_$TS.txt"

mkdir -p reports

echo "🐜 HormigasAIS — Evidencia de Latencia Edge" > $OUT
echo "Timestamp: $TS" >> $OUT
echo "==========================================" >> $OUT

echo "" >> $OUT
echo "[Latencia Local Gateway]" >> $OUT
GW=$(ip route | grep default | awk '{print $3}')
ping -c 5 $GW >> $OUT

echo "" >> $OUT
echo "[Latencia Internet (Google DNS)]" >> $OUT
ping -c 5 8.8.8.8 >> $OUT

echo "" >> $OUT
echo "[Latencia Cloud Pública (Amazon)]" >> $OUT
ping -c 5 amazon.com >> $OUT

echo "" >> $OUT
echo "✅ Evidencia de latencia guardada en: $OUT"
EOF

# -----------------------------
# lbh_integrity.sh
# -----------------------------
cat > $BASE/lbh_integrity.sh <<'EOF'
#!/bin/bash

TS=$(date "+%Y-%m-%d_%H-%M-%S")
OUT="reports/integrity_$TS.txt"

mkdir -p reports

echo "🐜 HormigasAIS — Validación de Integridad SHA" > $OUT
echo "Timestamp: $TS" >> $OUT
echo "===========================================" >> $OUT

echo "" >> $OUT
echo "[Hash de Scripts LBH-Key]" >> $OUT

sha256sum lbh_menu.sh lbh_audit.sh lbh_latency.sh lbh_integrity.sh >> $OUT

echo "" >> $OUT
echo "✅ Integridad registrada en: $OUT"
EOF

# -----------------------------
# lbh_latency_map.py
# -----------------------------
cat > $BASE/lbh_latency_map.py <<'EOF'
import time

print("\n🐜 HormigasAIS — Mapa del Embudo de Latencia\n")

print("Cámara Edge → Nodo Centinela A16 → DataTrust → Cloud Internacional\n")

steps = [
    ("📷 Captura local", 5),
    ("🧠 Inferencia Edge inmediata", 8),
    ("🏢 DataTrust procesamiento interno", 15),
    ("🌍 Validación internacional (RTT)", 120),
]

for name, ms in steps:
    print(f"{name:<35} {ms} ms")
    time.sleep(0.5)

print("\n✅ Conclusión: Edge evita el embudo internacional.\n")
EOF

# -----------------------------
# Report Template
# -----------------------------
cat > $BASE/reports/README_REPORT.md <<'EOF'
# HormigasAIS Air City — Auditoría de Resiliencia Edge

## Objetivo
Demostrar continuidad operacional y reducción de dependencia cloud mediante procesamiento en el borde.

## Evidencia Generada
- Auditoría técnica del nodo Edge
- Latencia comparativa local vs internacional
- Integridad SHA del stack HormigasAIS

## Conclusión Estratégica
HormigasAIS actúa como una capa soberana de observabilidad,
permitiendo operaciones críticas incluso bajo limitaciones de conectividad externa.
EOF

# Permisos ejecutables
chmod +x $BASE/*.sh

echo ""
echo "✅ Instalación completada."
echo "=========================================="
echo "Para iniciar el Nodo Maestro Portátil:"
echo ""
echo "cd LBH-Key"
echo "./lbh_menu.sh"
echo ""
echo "🐜 HormigasAIS LBH-Key listo para Air City."
