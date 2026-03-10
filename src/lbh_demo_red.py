#!/usr/bin/env python3
"""
lbh_demo_red.py - Demo de 2 nodos LBH comunicandose por TCP
Implementacion 1: Android/Termux (EMISOR A16)
Implementacion 2: Raspberry Pi / Linux (RECEPTOR A20s)

Uso:
  Nodo RECEPTOR (RPi o segunda terminal):
    python3 lbh_demo_red.py receptor

  Nodo EMISOR (Android A16):
    python3 lbh_demo_red.py emisor <IP_RECEPTOR>

Ejemplo:
    python3 lbh_demo_red.py receptor
    python3 lbh_demo_red.py emisor 192.168.1.15
"""

import sys
import socket
import time
import json
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lbh_node_v1_1 import LBHNode

# --- ADN COMPARTIDO DE LA COLONIA ---
SHARED_SECRET  = b"supersecret_shared_key_32bytes!!"
NODE_A16       = "A16-Soberano-Salvador"
NODE_A20S      = "A20s-Manager-Alpha"
PUERTO         = 9001
TIMEOUT        = 10

# --- COLORES ---
VERDE  = "\033[92m"
ROJO   = "\033[91m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

def banner(rol):
    print(f"\n{BOLD}{'='*55}{RESET}")
    print(f"{BOLD}  HormigasAIS LBH v1.1 - Demo Red TCP{RESET}")
    print(f"  Rol: {CYAN}{rol}{RESET}")
    print(f"  Puerto: {PUERTO}")
    print(f"  Protocolo: LBH HMAC-SHA256 + Anti-Replay")
    print(f"{BOLD}{'='*55}{RESET}\n")

# ============================================================
# MODO RECEPTOR — corre en Raspberry Pi o segunda terminal
# ============================================================
def modo_receptor():
    banner("RECEPTOR / A20s-Manager-Alpha")

    # Nodo A20s conoce a A16
    nodo = LBHNode(NODE_A20S, {}, {
        NODE_A16: {1: SHARED_SECRET}
    })

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(("0.0.0.0", PUERTO))
    servidor.listen(5)

    print(f"{CYAN}[RECEPTOR]{RESET} Escuchando en 0.0.0.0:{PUERTO}")
    print(f"{CYAN}[RECEPTOR]{RESET} Esperando feromona LBH...\n")

    mensajes_recibidos = 0

    while True:
        try:
            conn, addr = servidor.accept()
            datos = conn.recv(4096).decode("utf-8").strip()

            print(f"{CYAN}[RECEPTOR]{RESET} Conexion desde {addr[0]}")
            print(f"{CYAN}[RECEPTOR]{RESET} Mensaje recibido:")
            print(f"  {datos[:80]}...")

            # Validar mensaje LBH
            valido = nodo.validate_message(datos)
            mensajes_recibidos += 1

            if valido:
                # Extraer DATA del mensaje
                campos = {p.split(":",1)[0]: p.split(":",1)[1]
                         for p in datos.split("|")[1:]}
                payload = campos.get("DATA", "DESCONOCIDO")

                print(f"\n{VERDE}[RECEPTOR] FEROMONA VALIDADA{RESET}")
                print(f"  Payload: {BOLD}{payload}{RESET}")
                print(f"  Nodo emisor: {campos.get('NODE', '?')}")
                print(f"  Total recibidos: {mensajes_recibidos}\n")

                respuesta = json.dumps({
                    "status": "ACEPTADO",
                    "payload": payload,
                    "receptor": NODE_A20S,
                    "ts": int(time.time())
                })
            else:
                print(f"\n{ROJO}[RECEPTOR] FEROMONA RECHAZADA{RESET}\n")
                respuesta = json.dumps({
                    "status": "RECHAZADO",
                    "receptor": NODE_A20S,
                    "ts": int(time.time())
                })

            conn.sendall(respuesta.encode("utf-8"))
            conn.close()

        except KeyboardInterrupt:
            print(f"\n{CYAN}[RECEPTOR]{RESET} Nodo en standby.")
            break

    servidor.close()

# ============================================================
# MODO EMISOR — corre en Android A16
# ============================================================
def modo_emisor(ip_receptor):
    banner("EMISOR / A16-Soberano-Salvador")

    # Nodo A16 tiene su clave para firmar
    nodo = LBHNode(NODE_A16, {1: SHARED_SECRET}, {})

    comandos = [
        "ESTADO:OPERATIVO",
        "PATH_CLEAR:0x10",
        "LATIDO:0x01",
        "MED_PRIORITY:0x77",
        "ESTADO:SOBERANO"
    ]

    print(f"{CYAN}[EMISOR]{RESET} Conectando a {ip_receptor}:{PUERTO}")
    print(f"{CYAN}[EMISOR]{RESET} Enviando {len(comandos)} feromonas LBH...\n")

    exitosos = 0
    rechazados = 0

    for i, comando in enumerate(comandos, 1):
        try:
            # Construir mensaje LBH firmado
            mensaje = nodo.build_message(comando, key_id=1)

            print(f"{CYAN}[EMISOR]{RESET} Feromona {i}/{len(comandos)}: {comando}")

            # Enviar por TCP
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(TIMEOUT)
            cliente.connect((ip_receptor, PUERTO))
            cliente.sendall(mensaje.encode("utf-8"))

            # Recibir respuesta
            respuesta_raw = cliente.recv(4096).decode("utf-8")
            cliente.close()

            respuesta = json.loads(respuesta_raw)

            if respuesta.get("status") == "ACEPTADO":
                print(f"  {VERDE}ACEPTADO{RESET} por {respuesta.get('receptor')}")
                exitosos += 1
            else:
                print(f"  {ROJO}RECHAZADO{RESET}")
                rechazados += 1

        except Exception as e:
            print(f"  {ROJO}ERROR: {e}{RESET}")
            rechazados += 1

        time.sleep(1)

    # Resumen final
    print(f"\n{BOLD}{'='*55}{RESET}")
    print(f"{BOLD}  RESULTADO DE LA DEMO{RESET}")
    print(f"  {VERDE}Feromonas aceptadas: {exitosos}/{len(comandos)}{RESET}")
    if rechazados > 0:
        print(f"  {ROJO}Feromonas rechazadas: {rechazados}{RESET}")
    print(f"  Protocolo: LBH v1.1 HMAC-SHA256")
    print(f"  Interoperabilidad: {'CONFIRMADA' if exitosos > 0 else 'FALLIDA'}")
    print(f"{BOLD}{'='*55}{RESET}\n")

# ============================================================
# ENTRADA PRINCIPAL
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    rol = sys.argv[1].lower()

    if rol == "receptor":
        modo_receptor()
    elif rol == "emisor":
        if len(sys.argv) < 3:
            print(f"{ROJO}Error: falta IP del receptor{RESET}")
            print("Uso: python3 lbh_demo_red.py emisor <IP>")
            sys.exit(1)
        modo_emisor(sys.argv[2])
    else:
        print(f"{ROJO}Rol desconocido: {rol}{RESET}")
        print("Uso: receptor | emisor <IP>")
        sys.exit(1)
