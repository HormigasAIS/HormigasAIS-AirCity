#!/usr/bin/env python3
import os
import time

# --- ADN DE LA PURGA ---
FUNDADOR = "Cristhiam Leonardo Hernandez Quiñonez"
UBICACION = "San Miguel, El Salvador"

def limpiar():
    os.system('clear')

def mostrar_panel_purga():
    limpiar()
    print("╭────────────────────────────────────────────────╮")
    print("│ HormigasAIS Air City - Panel Soberano v1.5     │")
    print("│ San Miguel, El Salvador                        │")
    print("╰────────────────────────────────────────────────╯")
    
    print("\n╭─────── • • • FEROMONAS DIGITALES • • • ────────╮")
    # Estado de Purga: El sistema ha removido ruidos y busca ADN puro
    for i in range(1, 8):
        print(f"│ 🐜 CASTA_{i}                            \033[91m🔴 BUSCANDO ADN...\033[0m │")
    print("╰─────────── ESPERANDO CONSENSO (0/7) ───────────╯")
    
    print("\n╭────────────────────────────────────────────────╮")
    print(f"│ Energía EDGE: [\033[92m▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮\033[0m] 100% │")
    print(f"│ Estado: MODO ESCANEO ACTIVO (Puro)            │")
    print("╰────────────────────────────────────────────────╯")
    
    print("\n╭──────────────────── LOGS DESTACADOS ───────────╮")
    print(f"│ [{time.strftime('%H:%M:%S')}] ESPECTROS REMOVIDOS: Limpieza Total")
    print(f"│ [{time.strftime('%H:%M:%S')}] ESCANEANDO ADN SOBERANO...        ")
    print("╰────────────────────────────────────────────────╯")

try:
    while True:
        mostrar_panel_purga()
        time.sleep(1) # Pulso rítmico de búsqueda
except KeyboardInterrupt:
    print("\n\033[93m[!] Purga finalizada. El espectro vuelve a la normalidad.\033[0m")

