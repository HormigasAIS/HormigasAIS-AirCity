import time
import os
import random

def pantalla(sensor_status, activo="", votos="0/7"):
    os.system('clear')
    print(f"\033[94mHormigasAIS Air City - CENTINELA LOGÍSTICO v2.0\033[0m")
    print(f"Ubicación: Zona de Carga, San Miguel | Soberanía: 🟢 INMUNE")
    print("─" * 60)
    
    # El Heptágono en acción
    print("\033[93m   [1]   [2] \033[0m")
    print("\033[93m[7]   {H}   [3]\033[0m  <-- NÚCLEO LBH")
    print("\033[93m   [6]   [5]   [4]\033[0m")
    
    print("\n" + "─" * 60)
    print(f"ESTADO DEL SENSOR: {sensor_status}")
    if activo:
        print(f"\033[92m[🚛] DETECTADO: {activo}\033[0m")
        print(f"⚖️ CONSENSO DE VALIDACIÓN: {votos}")
    print("─" * 60)
    print(f"ENERGÍA EDGE: [▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮] 100%")

# Lógica de la expansión logística
try:
    while True:
        # 1. Vigilancia silenciosa
        pantalla("\033[90mESCANEANDO PERÍMETRO...\033[0m")
        time.sleep(random.randint(3, 6))
        
        # 2. Detección de Movimiento
        pantalla("\033[91m⚠️ MOVIMIENTO DETECTADO EN ZONA A-1\033[0m")
        time.sleep(2)
        
        # 3. Identificación del Activo
        pantalla("\033[96m🔍 ANALIZANDO FEROMONA VISUAL...\033[0m", "Activo SV-2026")
        time.sleep(2)
        
        # 4. Anuncio de la Vocera y Consenso
        votos_finales = f"{random.randint(6, 7)}/7"
        pantalla("\033[92m✅ IDENTIFICADO\033[0m", "Activo SV-2026 detectado en zona de carga", votos_finales)
        print("\033[1m[📢] VOCERA: 'Activo validado. Acceso permitido a la colonia.'\033[0m")
        time.sleep(5)

except KeyboardInterrupt:
    print("\n[!] Centinela replegado a los cuarteles.")

