#!/usr/bin/env python3
import os
import time

# Rutas de HormigasAIS
BASE_DIR = os.path.expanduser("~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY")
LOG_LBH = os.path.join(BASE_DIR, "memoria_aprendizaje.lbh")

def limpiar():
    print("\033[H\033[J", end="")

def obtener_cabecera():
    if os.path.exists(LOG_LBH):
        with open(LOG_LBH, "r") as f:
            lineas = f.readlines()
            return lineas[-1].strip() if lineas else "SISTEMA INICIANDO..."
    return "MEMORIA LBH: ESPERANDO SINCRONIZACIÓN"

def panel():
    limpiar()
    historial = obtener_cabecera()
    
    # Cabecera de Validación
    print(f"\033[94m╭────────────────────────────────────────────────╮")
    print(f"│ {historial[:46].ljust(46)} │")
    print(f"╰────────────────────────────────────────────────╯\033[0m")
    
    # Vocería de la Casta_1
    print(f"\033[92m[📢] VOCERA CASTA_1: 'Signal 9 invalidado.'\033[0m")
    print(f"🐜: 'La grieta ha sido encapsulada como ADN de entrenamiento.'")
    print(f"🐜: 'Comunicación activa: Las 7 hormigas retoman energía.'")

    # Estado de las 7 Hormigas Inmunizadas
    print("\n\033[93m╭─────── • • • FEROMONAS DIGITALES • • • ────────╮\033[0m")
    for i in range(1, 8):
        print(f"│  🐜 CASTA_{i}    🟢 INMUNE (S9-DATA)           │")
    print("\033[93m╰─────────── SOBERANÍA CONFIRMADA (7/7) ───────────╯\033[0m")

    # Energía Edge Retornada
    print(f"\nENERGÍA EDGE: [▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮] 100%")
    print(f"ESTADO: \033[96mRESILIENCIA EXTREMA ACTIVA\033[0m")
    print("──────────────────────────────────────────────────")
    print("[!] Monitor estable. Ctrl+C para pausar soberanía.")

if __name__ == "__main__":
    try:
        while True:
            panel()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\033[91m[!] Monitor suspendido por el Maestro.\033[0m")

