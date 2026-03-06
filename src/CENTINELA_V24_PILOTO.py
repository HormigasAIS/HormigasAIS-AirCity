#!/usr/bin/env python3
import os
import subprocess
import json
import time

# --- ADN DE INFRAESTRUCTURA ---
OBJETIVO_BLE = "S9-DATA-IMMUNE-2026"
IP_A20S = "192.168.1.15"
FUNDADOR = "Cristhiam Leonardo Hernandez Quiñonez"

def limpiar():
    os.system('clear')

def escanear_ble_veloz():
    try:
        # Reducimos a 1 segundo para una respuesta eléctrica
        resultado = subprocess.check_output(
            ["termux-bluetooth-scan", "-t", "1"],
            timeout=3
        )
        dispositivos = json.loads(resultado)
        for d in dispositivos:
            nombre = d.get("name", "")
            if OBJETIVO_BLE in nombre:
                return True
        return False
    except:
        return False

def panel_v24(estado_texto, validado=False):
    limpiar()
    print("HormigasAIS Air City - CENTINELA V2.4 (PILOTO REAL)")
    print("──────────────────────────────────────────────────")
    print("╭─────── • • • ESTADO DEL HEPTÁGONO • • • ───────╮")
    
    # Si está validado, mostramos el verde soberano
    indicador = "\033[92m🟢 INMUNE\033[0m" if validado else f"\033[93m🟡 {estado_texto}\033[0m"
    
    for i in range(1, 8):
        print(f"│  🐜 CASTA_{i}    {indicador}              │")
    
    footer = "─────────── SOBERANÍA CONFIRMADA (7/7) ───────────" if validado else "─────────── ESPERANDO PERSISTENCIA (0/7) ─────────"
    print(f"╰{footer}╯")
    
    print(f"\nENERGÍA: [100%] | MODO: ANTIFRÁGIL")
    if validado:
        print(f"\033[1m[📢] VOCERA: 'ADN Confirmado por persistencia doble.'\033[0m")
        print(f"ID_MAESTRO: {FUNDADOR}")
    else:
        print("[📡] ESCANEANDO ESPECTRO...")
    print("──────────────────────────────────────────────────")

# --- LOOP PRINCIPAL CON FILTRO DE PERSISTENCIA ---
MATCHES = 0

try:
    while True:
        if escanear_ble_veloz():
            MATCHES += 1
            # Necesitamos 2 detecciones seguidas para el consenso
            if MATCHES >= 2:
                panel_v24(None, True)
                time.sleep(10) # Tiempo de gloria para la foto/demo
                MATCHES = 0 # Reiniciamos tras el éxito
            else:
                panel_v24("VALIDANDO...") # Estado intermedio: ha olido algo
        else:
            MATCHES = 0 # Si se pierde un pulso, volvemos a cero
            panel_v24("ESCANEANDO...")
        
        time.sleep(0.5) # Respiro corto para el procesador del A16
except KeyboardInterrupt:
    print("\n[!] Centinela en standby.")

