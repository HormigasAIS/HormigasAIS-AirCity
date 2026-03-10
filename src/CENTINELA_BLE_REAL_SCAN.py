import asyncio
from bleak import BleakScanner
import datetime

# FEROMONA OBJETIVO (Activo autorizado)
TARGET_NAME = "TruckBeacon_SV-2026"

# Log soberano
LOG_FILE = "centinela_ble.log"

def registrar(evento):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{timestamp}] {evento}"
    print(linea)
    with open(LOG_FILE, "a") as f:
        f.write(linea + "\n")

async def escanear():
    registrar("🐜 CENTINELA BLE ACTIVADO — Escaneando perímetro Air City...")

    while True:
        devices = await BleakScanner.discover(timeout=4.0)

        encontrado = False

        for d in devices:
            name = d.name or "UNKNOWN"
            rssi = d.rssi

            # Si detecta el activo autorizado
            if TARGET_NAME in name:
                encontrado = True
                registrar(f"🚛 ACTIVO DETECTADO: {name} | RSSI: {rssi} dBm")
                registrar("⚖️ CONSENSO: 7/7 — Acceso permitido a la colonia.")
                registrar("✅ SOBERANÍA CONFIRMADA\n")

        if not encontrado:
            registrar("...Perímetro limpio. Ningún activo autorizado detectado.")

        await asyncio.sleep(3)

# Ejecutar Centinela
asyncio.run(escanear())
