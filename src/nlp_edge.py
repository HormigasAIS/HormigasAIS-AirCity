# Procesamiento de comandos en el borde
from feromona import emitir_feromona

# Diccionario LBH v1.0 — Protocolo Air City
LBH_CODES = {
    "estatus": ("status_check", "Colonia estable. Resiliencia al 100%.", 0x01),
    "air city": ("mosquito_pulse", "Optimizando rutas de drones.", 0x10),
    "alerta clima": ("weather_alert", "Viento excesivo detectado.", 0x22),
    "emergencia medica": ("medical_priority", "Transporte de medicinas prioritario.", 0x77),
    "bloqueo": ("lock_node", "Nodo bloqueado, intervención manual requerida.", 0xFF)
}

def procesar_comando_nlp(comando):
    comando_lower = comando.lower()
    for key in LBH_CODES:
        if key in comando_lower:
            tipo, mensaje, codigo = LBH_CODES[key]
            emitir_feromona(tipo, mensaje, codigo)
            return mensaje, tipo, codigo
    # Comando desconocido
    emitir_feromona("unknown_command", comando)
    return "Comando no reconocido en el protocolo LBH.", "unknown_command", None
