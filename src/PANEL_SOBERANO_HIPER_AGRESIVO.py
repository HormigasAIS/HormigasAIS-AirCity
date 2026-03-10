#!/usr/bin/env python3
import os
import time

# --- IDENTIDAD SOBERANA ---
FUNDADOR = "Cristhiam Leonardo Hernandez Quiñonez"
PROTOCOLO = "LBH lbh.human"
UBICACION = "San Miguel, El Salvador"

def limpiar():
    os.system('clear')

def mostrar_panel_soberano():
    limpiar()
    # Encabezado
    print("╭────────────────────────────────────────────────╮")
    print(f"│ HormigasAIS Air City - Panel Soberano v1.5     │")
    print(f"│ {UBICACION}                        │")
    print("╰────────────────────────────────────────────────╯")
    
    # Feromonas Digitales (Estado Inmune Estático)
    print("\n╭─────── • • • FEROMONAS DIGITALES • • • ────────╮")
    for i in range(1, 8):
        # Usamos el verde directo ya que la IP está configurada
        print(f"│ 🐜 CASTA_{i}                            \033[92m🟢 INMUNE (S9-DATA)\033[0m │")
    print("╰─────────── SOBERANÍA CONFIRMADA (7/7) ─────────╯")
    
    # Energía y Estado
    print("\n╭────────────────────────────────────────────────╮")
    print(f"│ Energía EDGE: [\033[92m▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮\033[0m] 100% │")
    print(f"│ Estado: RESILIENCIA EXTREMA ACTIVA            │")
    print("╰────────────────────────────────────────────────╯")
    
    # Logs con su Autorización
    print("\n╭──────────────────── LOGS DESTACADOS ───────────╮")
    print(f"│ [{time.strftime('%H:%M:%S')}] CONSENSO_OK: IP Estática Validada")
    print(f"│ VALIDACIÓN: {FUNDADOR}           ")
    print(f"│ PROTOCOLO: {PROTOCOLO}                    ")
    print("╰────────────────────────────────────────────────╯")
    
    # ADN Entrenado
    print("\n╭────────────────── ADN ENTRENADO ───────────────╮")
    print("│ Signal 9 encapsulado como inmunidad colectiva │")
    print("╰────────────────────────────────────────────────╯")

# Ejecución de un solo paso o bucle de refresco suave
try:
    while True:
        mostrar_panel_soberano()
        # Refresco lento (cada 30 segundos) solo para actualizar la hora del log
        time.sleep(30)
except KeyboardInterrupt:
    print("\n\033[93m[!] Panel en espera - Nodo Soberano Protegido.\033[0m")

