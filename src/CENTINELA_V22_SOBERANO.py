import os
import time

def dibujar_heptagono(estado, adn_status):
    os.system('clear')
    color = "\033[92m" if adn_status == "INMUNE" else "\033[93m"
    reset = "\033[0m"
    
    print("HormigasAIS Air City - CENTINELA SOBERANO v2.2")
    print(f"Puente: Nube Padre | ADN: {color}{adn_status}{reset} (S9-DATA)")
    print("────────────────────────────────────────────────────────────")
    print("   [1]   [2]")
    print(f"{color}[7]   {{H}}   [3]{reset}  <-- NÚCLEO LBH")
    print("   [6]   [5]   [4]")
    print("────────────────────────────────────────────────────────────")
    print(f"ESTADO DEL SENSOR: {estado}")
    print("────────────────────────────────────────────────────────────")
    print("ENERGÍA EDGE: [▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮▮] 100%")

LOG_PATH = os.path.expanduser("~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY/capullo_soberano.log")

while True:
    try:
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                lineas = f.readlines()
                log_data = lineas[-1] if lineas else ""
            
            if "S9-DATA-IMMUNE-2026" in log_data:
                dibujar_heptagono("FEROMONA DETECTADA - ACCESO TOTAL", "INMUNE")
            else:
                dibujar_heptagono("OLFATEANDO RASTRO EN NUBE...", "BUSCANDO")
        else:
            dibujar_heptagono("NUBE NO DETECTADA - REINICIAR PADRE", "ERROR")
    except Exception as e:
        dibujar_heptagono(f"ERROR DE LECTURA: {str(e)[:20]}", "OFFLINE")
        
    time.sleep(1)

