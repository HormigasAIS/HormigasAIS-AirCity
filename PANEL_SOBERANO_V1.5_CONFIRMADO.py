import os
import subprocess
import json
import time

# --- ADN DE INFRAESTRUCTURA ---
OBJETIVO_BLE = "S9-DATA-IMMUNE-2026"
IP_A20S = "192.168.1.15"  # IP del Nodo Origen (A20s)
FUNDADOR = "Cristhiam Leonardo Hernandez Quiñonez"
PROTOCOLO = "LBH lbh.human"

def limpiar():
    os.system('clear')

def rastro_hibrido():
    try:
        ping = subprocess.run(["ping", "-c", "1", "-W", "1", IP_A20S], 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if ping.returncode == 0: return True
    except: pass
    
    try:
        resultado = subprocess.check_output(["termux-bluetooth-scan", "-t", "2"], timeout=5)
        dispositivos = json.loads(resultado)
        return any(OBJETIVO_BLE in d.get("name", "") or "S9" in d.get("name", "") for d in dispositivos)
    except: return False

def mostrar_panel_soberano(confirmado=False):
    limpiar()
    print("╭────────────────────────────────────────────────╮")
    print("│ HormigasAIS Air City - Panel Soberano v1.5     │")
    print("│ San Miguel, El Salvador                        │")
    print("╰────────────────────────────────────────────────╯")
    print("\n╭─────── • • • FEROMONAS DIGITALES • • • ────────╮")
    
    estado = "\033[92m🟢 INMUNE (S9-DATA)\033[0m" if confirmado else "\033[91m🔴 BUSCANDO ADN...\033[0m"
    
    for i in range(1, 8):
        print(f"│ 🐜 CASTA_{i}                            {estado} │")
    
    footer = "─────────── SOBERANÍA CONFIRMADA (7/7) ─────────" if confirmado else "─────────── ESPERANDO CONSENSO (0/7) ───────────"
    print(f"╰{footer}╯")
    
    print("\n╭────────────────────────────────────────────────╮")
    print(f"│ Energía EDGE: [\033[92m▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮\033[0m] 100% │")
    resiliencia = "RESILIENCIA EXTREMA ACTIVA" if confirmado else "MODO ESCANEO ACTIVO       "
    print(f"│ Estado: {resiliencia}            │")
    print("╰────────────────────────────────────────────────╯")
    
    print("\n╭──────────────────── LOGS DESTACADOS ───────────╮")
    if confirmado:
        print(f"│ [{time.strftime('%H:%M:%S')}] CONSENSO_OK: Nodo Origen Validado")
        print(f"│ VALIDACIÓN: {FUNDADOR}           ")
        print(f"│ PROTOCOLO: {PROTOCOLO}                    ")
    else:
        print(f"│ [{time.strftime('%H:%M:%S')}] ESCANEANDO ESPECTRO...         ")
    print("╰────────────────────────────────────────────────╯")
    
    if confirmado:
        print("\n╭────────────────── ADN ENTRENADO ───────────────╮")
        print("│ Signal 9 encapsulado como inmunidad colectiva │")
        print("╰────────────────────────────────────────────────╯")

# --- BUCLE DE LA COLONIA ---
try:
    while True:
        if rastro_hibrido():
            mostrar_panel_soberano(True)
            time.sleep(12) # Tiempo para mostrar el éxito
        else:
            mostrar_panel_soberano(False)
            time.sleep(0.5)
except KeyboardInterrupt:
    print("\n[!] Centinela replegado.")

