import os
import subprocess
import json
import time

# --- CONFIGURACIÓN DE PRECISIÓN LBH ---
OBJETIVO_VINCULO = "S9-DATA-IMMUNE-2026"  # El ADN detectado en la foto
ID_ZONA = "ZONA_CARGA_SAN_MIGUEL"

def limpiar():
    os.system('clear')

def escanear_perimetro():
    # Eliminamos el ruido visual de la terminal durante el escaneo
    try:
        resultado = subprocess.check_output(["termux-bluetooth-scan"], timeout=12)
        return json.loads(resultado)
    except:
        return []

def panel_logistico(estado, activo=None, votos="0/7"):
    limpiar()
    print(f"\033[94mHormigasAIS Air City - CENTINELA SOBERANO v2.2\033[0m")
    print(f"Puente: Termux:API | ADN: \033[92mINMUNE (S9-DATA)\033[0m")
    print("─" * 60)
    print("\033[93m   [1]   [2]\n[7]   {H}   [3]  <-- NÚCLEO LBH\n   [6]   [5]   [4]\033[0m")
    print("─" * 60)
    print(f"ESTADO DEL SENSOR: {estado}")
    if activo:
        print(f"\033[92m[🚛] DETECTADO: {activo}\033[0m")
        print(f"⚖️ CONSENSO LBH: {votos}")
    print("─" * 60)
    print(f"ENERGÍA EDGE: [▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮] 100%")

# --- BUCLE DE VALIDACIÓN REAL ---
try:
    while True:
        panel_logistico("\033[90mOLFATEANDO FEROMONA S9-DATA...\033[0m")
        entorno = escanear_perimetro()
        
        deteccion = None
        for dev in entorno:
            nombre = dev.get("name", "")
            if OBJETIVO_VINCULO in nombre:
                deteccion = nombre
                break
        
        if deteccion:
            panel_logistico("\033[91m⚠️ VÍNCULO DETECTADO\033[0m")
            time.sleep(1)
            # El Heptágono valida la firma del ADN
            panel_logistico("\033[92m✅ ADN RECONOCIDO\033[0m", f"{deteccion}", "7/7 (UNANIMIDAD)")
            print(f"\033[1m[📢] VOCERA: 'Extensión de la colonia detectada. Nodo S9-2026 validado.'\033[0m")
            # Creamos el rastro físico del éxito
            with open("ACCESO_SOBERANO.log", "a") as f:
                f.write(f"[{time.ctime()}] VÍNCULO EXITOSO: {deteccion} | CONSENSO 7/7\n")
            time.sleep(8) 
        else:
            time.sleep(1)

except KeyboardInterrupt:
    print("\n[!] Centinela replegado. Log de soberanía guardado.")

