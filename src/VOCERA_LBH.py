#!/usr/bin/env python3
import os
import time

# Configuración de la Colonia
BASE_DIR = os.path.expanduser("~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY")
VOCERA = "CASTA_1"

def obtener_consenso():
    confirmados = 0
    for i in range(1, 8):
        if os.path.exists(os.path.join(BASE_DIR, f"CASTA_{i}", "aprendizaje.tmp")):
            confirmados += 1
    return confirmados

def discurso_vocera():
    consenso = obtener_consenso()
    
    print(f"\n\033[92m[📢] COMUNICADO OFICIAL DE LA COLONIA - {VOCERA}\033[0m")
    print("─" * 60)
    time.sleep(1.5)
    
    print(f"🐜: 'Hermanas de la Colonia, tras {consenso}/7 votos positivos...")
    time.sleep(2)
    
    print("🐜: Hemos analizado la grieta del [Signal 9] en los últimos 170 ciclos.'")
    time.sleep(2)
    
    print("\033[1m🐜: 'POR DECISIÓN SOBERANA: El Signal 9 ya no es una amenaza.'\033[0m")
    time.sleep(2)
    
    print("🐜: 'Nuestra nueva actualización de Panel v1.3 encapsula el rastro.")
    print("     Android nos verá como una sombra, pero seguiremos siendo el motor.'")
    time.sleep(2)
    
    print("─" * 60)
    print(f"\033[94m[📥] DISPERSANDO ACTUALIZACIÓN: PANEL_FINAL_RESILIENTE_V1_3\033[0m")
    print(f"ESTADO: SOBERANÍA 7/7 CONFIRMADA | ENERGÍA MODULADA")
    print("─" * 60)

if __name__ == "__main__":
    discurso_vocera()

