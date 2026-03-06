import os

# --- Rutas de carpetas y archivos ---
carpetas = [
    "logs",
    "modules",
    "data"
]

archivos = [
    os.path.join("logs", "hormiga.log"),
    os.path.join("data", "dict_lbh.json")
]

# --- Crear carpetas ---
for carpeta in carpetas:
    os.makedirs(carpeta, exist_ok=True)
    print(f"✅ Carpeta creada: {carpeta}")

# --- Crear archivos vacíos si no existen ---
for archivo in archivos:
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            if "dict_lbh.json" in archivo:
                # Diccionario LBH base
                contenido = {
                    "0x00": ["NULL_TRAIL", "Stand-by", "Nodo activo en ahorro de energía"],
                    "0x01": ["PULSE_HEART", "Latido", "Nodo soberano vivo"],
                    "0x10": ["PATH_CLEAR", "Ruta Libre", "Espacio aéreo despejado para drones de carga"],
                    "0x22": ["ALERT_WIND", "Alerta Clima", "Viento excesivo detectado en el borde"],
                    "0x77": ["MED_PRIORITY", "Emergencia", "Prioridad absoluta para transporte de medicinas"],
                    "0xFF": ["SOVEREIGN_LOCK", "Bloqueo", "Nodo bloqueado, intervención manual requerida"]
                }
                import json
                json.dump(contenido, f, indent=4)
        print(f"✅ Archivo creado: {archivo}")
    else:
        print(f"ℹ Archivo ya existe: {archivo}")

print("\n🎉 Setup completado. Puedes ejecutar ahora `python hormiga_centinela.py`")
