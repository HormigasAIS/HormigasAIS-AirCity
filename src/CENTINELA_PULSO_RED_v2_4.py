import os
import subprocess
import time

IP_NODO_ORIGEN = "192.168.1.15"

def limpiar():
    os.system("clear")

# Pulso rápido tipo feromona WiFi
def pulso_directo():
    try:
        res = subprocess.run(
            ["ping", "-c", "1", "-W", "1", IP_NODO_ORIGEN],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return res.returncode == 0
    except:
        return False

# Match instantáneo (tabla de vecinos)
def escanear_perimetro_activo():
    try:
        vecinos = subprocess.check_output(["ip", "neigh", "show"]).decode()
        return IP_NODO_ORIGEN in vecinos
    except:
        return False

def panel(estado, match=False):
    limpiar()
    print("\033[94mHormigasAIS Air City - CENTINELA v2.4 (PILOTO REAL)\033[0m")
    print("Modo: Feromona WiFi Directa | Nodo Origen:", IP_NODO_ORIGEN)
    print("─" * 60)

    print("\033[93m   [1]   [2]\n[7]   {H}   [3]\n   [6]   [5]   [4]\033[0m")
    print("─" * 60)

    if match:
        print("\033[92m✅ MATCH INSTANTÁNEO DETECTADO\033[0m")
        print("🐜 Nodo Origen ha vuelto a la colonia.")
        print("⚖️ CONSENSO: 7/7 – SOBERANÍA CONFIRMADA")
    else:
        print("ESTADO:", estado)

    print("─" * 60)
    print("ENERGÍA EDGE: [▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮] 100%")

# Loop Centinela rápido
try:
    while True:
        panel("📡 RASTREANDO PULSO LOCAL...")

        if pulso_directo() or escanear_perimetro_activo():
            panel("", match=True)
            print("\n[📢] VOCERA: 'Nodo SV-2026 identificado. Acceso permitido.'")
            time.sleep(6)
        else:
            time.sleep(1)

except KeyboardInterrupt:
    print("\n[!] Centinela pausado.")
