#!/usr/bin/env python3

import socket
import threading
import time
import sys
import json

HEARTBEAT_INTERVAL = 2
TIMEOUT = 5

if len(sys.argv) < 3:
    print("Uso: python nodo_cluster.py <PUERTO> <peer1,peer2,...>")
    print("Ejemplo: python nodo_cluster.py 9001 9002,9003")
    sys.exit(1)

MY_PORT = int(sys.argv[1])
PEERS = [int(p) for p in sys.argv[2].split(",") if p]

last_seen = {}
active_nodes = set()
vote_lock = threading.Lock()


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", MY_PORT))
    s.listen()
    log(f"Nodo escuchando en puerto {MY_PORT}")

    while True:
        conn, addr = s.accept()
        data = conn.recv(4096).decode()
        if not data:
            conn.close()
            continue

        msg = json.loads(data)

        if msg["type"] == "HEARTBEAT":
            sender = msg["from"]
            last_seen[sender] = time.time()
            active_nodes.add(sender)
            conn.send(b"OK")

        elif msg["type"] == "VOTE_REQUEST":
            conn.send(json.dumps({"vote": True}).encode())

        conn.close()


def heartbeat_sender():
    while True:
        for peer in PEERS:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect(("localhost", peer))
                msg = {"type": "HEARTBEAT", "from": MY_PORT}
                s.send(json.dumps(msg).encode())
                s.recv(1024)
                s.close()
                last_seen[peer] = time.time()
                active_nodes.add(peer)
            except:
                pass
        time.sleep(HEARTBEAT_INTERVAL)


def peer_monitor():
    while True:
        now = time.time()
        for peer in list(active_nodes):
            if now - last_seen.get(peer, 0) > TIMEOUT:
                log(f"Peer {peer} marcado como CAÍDO")
                active_nodes.discard(peer)
        time.sleep(1)


def start_vote():
    votes = 1  # voto propio
    total = 1

    for peer in PEERS:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(("localhost", peer))
            msg = {"type": "VOTE_REQUEST", "from": MY_PORT}
            s.send(json.dumps(msg).encode())
            response = json.loads(s.recv(1024).decode())
            if response.get("vote"):
                votes += 1
            total += 1
            s.close()
        except:
            pass

    majority = total // 2 + 1

    log(f"Votos obtenidos: {votes}/{total}")
    if votes >= majority:
        log("CONSENSO ALCANZADO")
    else:
        log("CONSENSO FALLIDO")


# Lanzar hilos
threading.Thread(target=server, daemon=True).start()
threading.Thread(target=heartbeat_sender, daemon=True).start()
threading.Thread(target=peer_monitor, daemon=True).start()

log("Cluster iniciado.")
log(f"Peers configurados: {PEERS}")

# Loop principal
while True:
    cmd = input()
    if cmd == "vote":
        start_vote()
    elif cmd == "status":
        log(f"Nodos activos: {sorted(active_nodes)}")
