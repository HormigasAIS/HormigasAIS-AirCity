#!/bin/bash
# 🐜 Sincronización soberana: Nodo Maestro -> Espejo Público
echo "🔄 Iniciando sincronización de feromonas..."

# 1. Empujar el estado al espejo institucional en GitHub
git push --mirror github

if [ $? -eq 0 ]; then
    echo "✅ Sincronización exitosa: El enjambre en GitHub está alineado."
else
    echo "❌ Error: Verifica tu autenticación SSH con HormigasAIS/xoxo-lbh-adapter."
fi
