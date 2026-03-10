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
    print("Uso: python nodo_cluster_raft_log.py <PUERTO> <peer1,peer2,...>")
    sys.exit(1)

MY_PORT = int(sys.argv[1])
PEERS = [int(p) for p in sys.argv[2].split(",") if p]

# --- ESTADO ---
role = "FOLLOWER"
current_term = 0
voted_for = None
leader_id = None

log_entries = []
commit_index = -1
last_applied = -1

state_machine = {}

last_heartbeat = time.time()
election_timeout = random.uniform(ELECTION_TIMEOUT_MIN, ELECTION_TIMEOUT_MAX)

lock = threading.Lock()


def log_msg(msg):
    print(f"[{time.strftime('%H:%M:%S')}] ({role}) {msg}")


def majority():
    return (len(PEERS) + 1) // 2 + 1


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


# --- APPLY COMMITTED ENTRIES ---
def apply_entries():
    global last_applied

    while last_applied < commit_index:
        last_applied += 1
        entry = log_entries[last_applied]
        state_machine.update(entry["command"])
        log_msg(f"Aplicado index {entry['index']} -> {entry['command']}")


# --- SERVER ---
def server():
    global role, current_term, voted_for, leader_id
    global last_heartbeat, commit_index

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", MY_PORT))
    s.listen()

    log_msg(f"Nodo escuchando en puerto {MY_PORT}")

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

            elif msg["type"] == "APPEND":
                entry = msg["entry"]
                log_entries.append(entry)
                commit_index = msg["commit_index"]
                apply_entries()
                conn.send(b"OK")

        conn.close()


# --- HEARTBEAT ---
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


# --- ELECTION ---
def election_loop():
    global role, current_term, voted_for
    global last_heartbeat, election_timeout, leader_id

    while True:
        time.sleep(1)

        with lock:

            if role == "LEADER":
                continue

            if time.time() - last_heartbeat > election_timeout:

                role = "CANDIDATE"
                current_term += 1
                voted_for = MY_PORT

                last_heartbeat = time.time()
                election_timeout = random.uniform(
                    ELECTION_TIMEOUT_MIN,
                    ELECTION_TIMEOUT_MAX
                )

                votes = 1

                log_msg("Iniciando elección")

                for peer in PEERS:
                    response = send_message(peer, {
                        "type": "VOTE_REQUEST",
                        "term": current_term,
                        "candidate": MY_PORT
                    })

                    if response and response.get("vote"):
                        votes += 1

                if votes >= majority():
                    role = "LEADER"
                    leader_id = MY_PORT
                    log_msg("LÍDER ELECTO")
                else:
                    role = "FOLLOWER"


# --- CLIENT COMMAND ---
def replicate_command(command):
    global log_entries, commit_index

    with lock:
        if role != "LEADER":
            log_msg("No soy líder")
            return

        index = len(log_entries)
        entry = {
            "term": current_term,
            "index": index,
            "command": command
        }

        log_entries.append(entry)

    success = 1

    for peer in PEERS:
        response = send_message(peer, {
            "type": "APPEND",
            "entry": entry,
            "commit_index": commit_index
        })
        if response:
            success += 1

    if success >= majority():
        with lock:
            commit_index = index
            apply_entries()
            log_msg(f"Commit index {commit_index}")


# --- START ---
threading.Thread(target=server, daemon=True).start()
threading.Thread(target=heartbeat_loop, daemon=True).start()
threading.Thread(target=election_loop, daemon=True).start()

log_msg("Cluster iniciado")
log_msg(f"Peers: {PEERS}")

while True:
    cmd = input()

    if cmd == "status":
        with lock:
            log_msg(f"Term: {current_term} | Líder: {leader_id}")
            log_msg(f"Commit index: {commit_index}")
            log_msg(f"Log size: {len(log_entries)}")
            log_msg(f"State: {state_machine}")

    elif cmd.startswith("set "):
        try:
            _, k, v = cmd.split()
            replicate_command({k: v})
        except:
            print("Uso: set clave valor")
