#!/usr/bin/env python3

import socket
import threading
import time
import sys
import json
import random

# --- CONFIG ---
HEARTBEAT_INTERVAL = 2
ELECTION_TIMEOUT_MIN = 4
ELECTION_TIMEOUT_MAX = 7

if len(sys.argv) < 3:
    print("Uso: python nodo_cluster_raft.py <PUERTO> <peer1,peer2,...>")
    sys.exit(1)

MY_PORT = int(sys.argv[1])
PEERS = [int(p) for p in sys.argv[2].split(",") if p]

# --- ESTADO ---
role = "FOLLOWER"
current_term = 0
voted_for = None
leader_id = None
votes_received = 0

state_machine = {}

last_heartbeat = time.time()
election_timeout = random.uniform(ELECTION_TIMEOUT_MIN, ELECTION_TIMEOUT_MAX)

lock = threading.Lock()


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] ({role}) {msg}")


# --- NETWORK SEND ---
def send_message(peer, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("localhost", peer))
        s.send(json.dumps(message).encode())
        response = s.recv(4096)
        s.close()
        if response:
            return json.loads(response.decode())
    except:
        return None


# --- SERVER ---
def server():
    global current_term, voted_for, role, leader_id, last_heartbeat

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", MY_PORT))
    s.listen()

    log(f"Nodo escuchando en puerto {MY_PORT}")

    while True:
        conn, _ = s.accept()
        data = conn.recv(4096)
        if not data:
            conn.close()
            continue

        msg = json.loads(data.decode())

        with lock:

            if msg["type"] == "HEARTBEAT":
                if msg["term"] >= current_term:
                    role = "FOLLOWER"
                    current_term = msg["term"]
                    leader_id = msg["leader"]
                    last_heartbeat = time.time()
                conn.send(b"OK")

            elif msg["type"] == "VOTE_REQUEST":
                if msg["term"] > current_term:
                    current_term = msg["term"]
                    voted_for = None
                    role = "FOLLOWER"

                vote_granted = False
                if voted_for in (None, msg["candidate"]):
                    voted_for = msg["candidate"]
                    vote_granted = True

                conn.send(json.dumps({"vote": vote_granted}).encode())

            elif msg["type"] == "REPLICATE":
                state_machine.update(msg["data"])
                conn.send(b"OK")

        conn.close()


# --- HEARTBEAT LOOP ---
def heartbeat_loop():
    global role

    while True:
        time.sleep(HEARTBEAT_INTERVAL)

        with lock:
            if role == "LEADER":
                for peer in PEERS:
                    send_message(peer, {
                        "type": "HEARTBEAT",
                        "term": current_term,
                        "leader": MY_PORT
                    })


# --- ELECTION LOOP (CORREGIDO) ---
def election_loop():
    global role, current_term, voted_for, votes_received
    global last_heartbeat, election_timeout, leader_id

    while True:
        time.sleep(1)

        with lock:

            if role == "LEADER":
                continue

            if time.time() - last_heartbeat > election_timeout:

                # --- INICIAR ELECCIÓN ---
                role = "CANDIDATE"
                current_term += 1
                voted_for = MY_PORT
                votes_received = 1

                # 🔥 RESET PARA EVITAR ELECTION STORM
                last_heartbeat = time.time()
                election_timeout = random.uniform(
                    ELECTION_TIMEOUT_MIN,
                    ELECTION_TIMEOUT_MAX
                )

                log("Iniciando elección")

                for peer in PEERS:
                    response = send_message(peer, {
                        "type": "VOTE_REQUEST",
                        "term": current_term,
                        "candidate": MY_PORT
                    })

                    if response and response.get("vote"):
                        votes_received += 1

                majority = (len(PEERS) + 1) // 2 + 1

                if votes_received >= majority:
                    role = "LEADER"
                    leader_id = MY_PORT
                    log("LÍDER ELECTO")
                else:
                    role = "FOLLOWER"


# --- REPLICACIÓN ---
def replicate_state(data):
    global state_machine

    with lock:
        if role != "LEADER":
            log("No soy líder")
            return

        state_machine.update(data)

    success = 1

    for peer in PEERS:
        response = send_message(peer, {
            "type": "REPLICATE",
            "data": data
        })
        if response:
            success += 1

    majority = (len(PEERS) + 1) // 2 + 1

    if success >= majority:
        log(f"Estado replicado con éxito: {data}")
    else:
        log("Falló replicación")


# --- START THREADS ---
threading.Thread(target=server, daemon=True).start()
threading.Thread(target=heartbeat_loop, daemon=True).start()
threading.Thread(target=election_loop, daemon=True).start()

log("Cluster iniciado")
log(f"Peers: {PEERS}")

# --- CLI ---
while True:
    cmd = input()

    if cmd == "status":
        with lock:
            log(f"Term: {current_term} | Líder: {leader_id}")
            log(f"Estado: {state_machine}")

    elif cmd.startswith("set "):
        try:
            _, k, v = cmd.split()
            replicate_state({k: v})
        except:
            print("Uso: set clave valor")
