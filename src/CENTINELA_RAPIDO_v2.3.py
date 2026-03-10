import os, subprocess, time

# Factores de Inyección Directa
IP_ORIGEN = "192.168.1.5"
RUTA_LBH = "~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY/capullo_soberano.log"
R_EXP = os.path.expanduser(RUTA_LBH)

def rastro():
    # Uso de descriptores de flujo internos < >
    check = subprocess.run(["ping", "-c", "1", "-W", "1", IP_ORIGEN], stdout=subprocess.PIPE).returncode
    if check == 0:
        # Efecto secundario en el sistema de archivos
        os.system(f"echo '[{time.time()}] FEROMONA_MULTICANAL_ACTIVA' >> {R_EXP}")
        return True
    return False

print("🚀 INYECTANDO VELOCIDAD v2.3 < INVISIBLE >")
while True:
    if rastro():
        print(f"🟢 SINCRONÍA: {IP_ORIGEN} > LBH_OK")
    else:
        print(f"🔴 ESCANEO: {IP_ORIGEN} < BUSCANDO...")
    time.sleep(0.5)
