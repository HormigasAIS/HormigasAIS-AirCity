#!/data/data/com.termux/files/usr/bin/bash

echo "🐜 INCUBADORA A16: monitor iniciado"
echo "📡 Escuchando BEACON del A20..."
echo ""

while true
do
  date
  curl -s http://192.168.1.5:8080/beacon
  echo ""
  echo "-----------------------------"
  sleep 3
done
