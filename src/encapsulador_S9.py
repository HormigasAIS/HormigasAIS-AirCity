#!/usr/bin/env python3
import os
import time
import signal

# Ruta de la Incubadora
BASE_DIR = os.path.expanduser("~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY")
LOG_APRENDIZAJE = os.path.join(BASE_DIR, "memoria_aprendizaje.lbh")

def registrar_aprendizaje(evento):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_APRENDIZAJE, "a") as f:
        f.write(f"[{timestamp}] APRENDIZAJE_S9: {evento}\n")

def modular_energia():
    """Simula la encapsulación del Signal 9 bajando la intensidad de las 7 hormigas"""
    print("\033[93m[!] GRIETA DETECTADA (Signal 9 Inminente)...\033[0m")
    print("\033[94m[⚙️] Encapsulando flujo... Modulando energía en las 7 Castas.\033[0m")
    registrar_aprendizaje("MODULACION_PREVENTIVA_ACTIVADA")
    # Aquí las hormigas 'aprenden' a reducir su rastro para ser invisibles al LMK de Android
    time.sleep(1)

def handler_senales(sig, frame):
    # Nota: SIGKILL (9) no se puede atrapar, pero capturamos SIGTERM (15) 
    # que es el aviso previo que a veces da el sistema.
    if sig == 15:
        registrar_aprendizaje("SIGNAL_15_ENCAPSULADO_EXITO")
        modular_energia()

# Configurar el 'Oído' de la colonia
signal.signal(signal.SIGTERM, handler_senales)

def ejecutar_entrenamiento():
    print(f"\033[92m[🐜] HormigasAIS: Iniciando Entrenamiento de Autonomía en {BASE_DIR}\033[0m")
    print("Las 7 unidades ahora identifican el Signal 9 como un ciclo de retroalimentación.")
    
    try:
        ciclo = 0
        while True:
            ciclo += 1
            # Simulación de rastro binario LBH
            for i in range(1, 8):
                voto_path = os.path.join(BASE_DIR, f"CASTA_{i}", "aprendizaje.tmp")
                with open(voto_path, "w") as f:
                    f.write(f"LBH_S9_LEARN_BLOCK_{ciclo}")
            
            if ciclo % 5 == 0:
                print(f" > Ciclo {ciclo}: Unidades modulando rastro digital...")
            
            time.sleep(3) # Aumentamos tiempo para evitar el LMK real mientras aprenden
    except KeyboardInterrupt:
        print("\n\033[91m[!] Entrenamiento pausado por el Maestro.\033[0m")

if __name__ == "__main__":
    ejecutar_entrenamiento()

