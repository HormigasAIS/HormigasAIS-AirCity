#!/usr/bin/env python3
import time
import os
import subprocess
import sys

# Configuración de Rutas Reales de HormigasAIS
CASTA_DIR = os.path.expanduser("~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY")
NODOS = [f"CASTA_{i}" for i in range(1, 8)]

def limpiar_sin_parpadeo():
    # En lugar de clear, movemos el cursor a la posición (0,0)
    sys.stdout.write("\033[H")
    sys.stdout.flush()

def get_battery():
    try:
        res = subprocess.run(["termux-battery-status"], capture_output=True, text=True, timeout=1)
        import json
        return json.loads(res.stdout).get("percentage", 100)
    except:
        return 100

def leer_logs():
    log_path = os.path.join(CASTA_DIR, "bus_consenso.log")
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r') as f:
                lines = f.readlines()
                return [line.strip() for line in lines[-4:]]
        except:
            return ["Error leyendo logs perimetrales..."]
    return ["Iniciando Secuencia LBH...", "Esperando Feromonas..."]

def barra_progreso(valor, total=100, largo=25):
    filled = int(largo * valor // total)
    color = "\033[92m" if valor > 25 else "\033[91m"
    reset = "\033[0m"
    return f"{color}[{'▮'*filled}{' '*(largo-filled)}]{reset} {valor}%"

def mostrar_panel():
    limpiar_sin_parpadeo()
    bat = get_battery()
    votos = 0
    
    # Renderizado del Panel
    output = []
    output.append("\033[96m╭────────────────────────────────────────────────╮")
    output.append("│ \033[1mHormigasAIS v1.2\033[0m – San Miguel, SV              │")
    output.append("│ \033[93m· · · · · · · · · · · · · · · · · · · · · · ·\033[0m  │")
    output.append("╰────────────────────────────────────────────────╯\033[0m")

    output.append("\033[95m╭─────── • • • FEROMONAS DIGITALES • • • ────────╮\033[0m")
    for nodo in NODOS:
        path = os.path.join(CASTA_DIR, nodo, "voto.tmp")
        if os.path.exists(path):
            estado = "\033[92mACTIVO\033[0m"
            icono = "🟢"
            votos += 1
        else:
            estado = "\033[91mFALLO \033[0m"
            icono = "🔴"
        output.append(f"│  🐜 {nodo:<10} {icono} {estado:<15} │")
    
    color_c = "\033[92m" if votos >= 4 else "\033[91m"
    msg = "SOBERANÍA CONFIRMADA" if votos >= 4 else "CONSENSO INSUFICIENTE"
    output.append(f"\033[95m╰─────────── {color_c}{msg} ({votos}/7)\033[95m ───────────╯\033[0m\n")

    output.append(f"\033[1mENERGÍA EDGE:\033[0m {barra_progreso(bat)}")
    output.append("\033[90m" + "─" * 50 + "\033[0m")
    output.append("\033[1mÚLTIMOS EVENTOS (LOG LBH):\033[0m")
    for log in leer_logs():
        output.append(f" \033[90m>\033[0m {log[:45]}") # Truncamos para evitar saltos de línea
    output.append("\033[90m" + "─" * 50 + "\033[0m")
    output.append("\033[93m[!] Monitor estable. Ctrl+C para salir.\033[0m")
    
    # Imprimimos todo de un solo golpe para evitar parpadeo
    sys.stdout.write("\n".join(output) + "\n")
    sys.stdout.flush()

if __name__ == "__main__":
    # Limpiamos una sola vez al inicio
    os.system('clear')
    try:
        while True:
            mostrar_panel()
            time.sleep(1) # Actualización cada segundo
    except KeyboardInterrupt:
        print("\n\033[91m[!] SOBERANÍA EN HIBERNACIÓN.\033[0m\n")
        sys.exit(0)

