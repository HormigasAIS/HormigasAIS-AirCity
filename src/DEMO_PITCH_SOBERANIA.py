import time
import os

def render_demo(estado_nodos, mensaje_vocera, energia="100%"):
    os.system('clear')
    print(f"\033[94mHormigasAIS Air City - DEMO DE INVERSIÓN v1.5\033[0m")
    print("─" * 50)
    print("\033[93m╭─────── • • • ESTADO DEL HEPTÁGONO • • • ───────╮\033[0m")
    for i in range(1, 8):
        status = estado_nodos
        print(f"│  🐜 CASTA_{i}    {status}              │")
    print("\033[93m╰─────────── SOBERANÍA CONFIRMADA (7/7) ───────────╯\033[0m")
    print(f"\nENERGÍA EDGE: [{energia}] | MODO: PITCH_LIVE")
    print(f"\033[92m[📢] VOCERA: {mensaje_vocera}\033[0m")
    print("─" * 50)

# SECUENCIA DE LA DEMO
try:
    # 1. Normalidad
    render_demo("🟢 ACTIVO", "'Flujo logístico SV-2026 estable.'")
    time.sleep(4)

    # 2. El Ataque (Fricción)
    render_demo("\033[91m⚠️ S9_DETECTED\033[0m", "\033[91m'¡ALERTA! Intento de terminación forzada...'\033[0m", "85%")
    time.sleep(3)

    # 3. La Inmunización (LBH en acción)
    render_demo("\033[96m🔵 MODULANDO\033[0m", "'Sincronizando rastro... Encapsulando grieta.'", "90%")
    time.sleep(3)

    # 4. Triunfo Soberano
    render_demo("🟢 INMUNE", "'Signal 9 invalidado. El error ahora es nuestro ADN.'", "100%")
    print("\n\033[1m[!] DEMO EXITOSA: Sistema Antifragil Confirmado.\033[0m")

except KeyboardInterrupt:
    print("\nDemo finalizada.")

