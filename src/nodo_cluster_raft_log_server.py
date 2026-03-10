#!/usr/bin/env python3
import socket, threading, time, sys, json, random, os
from flask import Flask, request, jsonify
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from persistencia_lbh import guardar_estado, restaurar_estado
import os

HEARTBEAT_INTERVAL = 1.5
ELECTION_TIMEOUT_MIN = 5
ELECTION_TIMEOUT_MAX = 9

if len(sys.argv) < 2:
    print("Uso: python3 nodo_cluster_raft_log_server.py <PUERTO> [peers]")
    sys.exit(1)

MY_PORT = int(sys.argv[1])
PEERS = [int(p) for p in sys.argv[2].split(",")] if len(sys.argv) > 2 else []

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
state_machine, commit_index, current_term = restaurar_estado()
last_applied = commit_index

def log_msg(msg):
    print(f"[{time.strftime('%H:%M:%S')}] ({role}) {msg}", flush=True)

def majority():
    return (len(PEERS) + 1) // 2 + 1

def send_message(peer, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect(("127.0.0.1", peer))
        s.send(json.dumps(message).encode())
        response = s.recv(4096)
        s.close()
        if not response:
            return None
        raw = response.decode().strip()
        if raw == "OK":
            return {"ok": True}
        return json.loads(raw)
    except:
        return None

def apply_entries():
    global last_applied
    while last_applied < commit_index:
        last_applied += 1
        entry = log_entries[last_applied]
        state_machine.update(entry["command"])
        log_msg(f"Aplicado index {entry['index']} -> {entry['command']}")
        guardar_estado(state_machine, commit_index, current_term)

app = Flask(__name__)

@app.route("/status", methods=["GET"])
def status():
    with lock:
        return jsonify({
            "leader": leader_id,
            "commit_index": commit_index,
            "log_size": len(log_entries),
            "state": state_machine,
            "role": role,
            "term": current_term
        })

@app.route("/set", methods=["POST"])
def set_key():
    global commit_index
    data = request.json
    key, value = data.get("key"), data.get("value")
    if not key or not value:
        return jsonify({"ok": False}), 400
    with lock:
        if role != "LEADER":
            return jsonify({"ok": False, "error": "not leader", "leader": leader_id}), 400
        index = len(log_entries)
        entry = {"term": current_term, "index": index, "command": {key: value}}
        log_entries.append(entry)
        term_snap = current_term
        peers_snap = list(PEERS)

    success = 1
    for peer in peers_snap:
        resp = send_message(peer, {
            "type": "APPEND",
            "entry": entry,
            "commit_index": index,
            "term": term_snap
        })
        if resp and resp.get("ok"):
            success += 1
            log_msg(f"APPEND OK peer {peer} | votos: {success}")

    with lock:
        if success >= majority():
            commit_index = index
            apply_entries()
            return jsonify({"ok": True, "quorum": success})
        else:
            return jsonify({"ok": False, "error": "no quorum", "votes": success}), 500

def run_http():
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(port=MY_PORT + 1000, host='127.0.0.1')

def server():
    global role, current_term, voted_for, leader_id, last_heartbeat, commit_index
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", MY_PORT))
    s.listen(10)
    log_msg(f"Nodo escuchando en puerto {MY_PORT} (RAFT)")
    while True:
        try:
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
                    vote_granted = (voted_for is None or voted_for == msg["candidate"]) \
                                   and msg["term"] >= current_term
                    if vote_granted:
                        voted_for = msg["candidate"]
                    conn.send(json.dumps({"vote": vote_granted}).encode())
                elif msg["type"] == "APPEND":
                    if msg.get("term", 0) >= current_term:
                        log_entries.append(msg["entry"])
                        commit_index = msg["commit_index"]
                        last_heartbeat = time.time()
                        apply_entries()
                    conn.send(b"OK")
            conn.close()
        except:
            continue

def election_loop():
    global role, current_term, voted_for, leader_id, last_heartbeat, election_timeout
    while True:
        time.sleep(0.5)
        with lock:
            should_elect = (role != "LEADER") and \
                           (time.time() - last_heartbeat > election_timeout)
            if not should_elect:
                continue
            role = "CANDIDATE"
            current_term += 1
            voted_for = MY_PORT
            last_heartbeat = time.time()
            term_snap = current_term
            election_timeout = random.uniform(ELECTION_TIMEOUT_MIN, ELECTION_TIMEOUT_MAX)
        votes = 1
        for peer in PEERS:
            resp = send_message(peer, {
                "type": "VOTE_REQUEST",
                "term": term_snap,
                "candidate": MY_PORT
            })
            if resp and resp.get("vote"):
                votes += 1
        with lock:
            if votes >= majority() and role == "CANDIDATE":
                role = "LEADER"
                leader_id = MY_PORT
                log_msg("LÍDER ELECTO")
            elif role == "CANDIDATE":
                role = "FOLLOWER"

def heartbeat_loop():
    while True:
        time.sleep(HEARTBEAT_INTERVAL)
        with lock:
            if role != "LEADER":
                continue
            term_snap = current_term
            peers_snap = list(PEERS)
        for peer in peers_snap:
            send_message(peer, {
                "type": "HEARTBEAT",
                "term": term_snap,
                "leader": MY_PORT
            })

threading.Thread(target=server, daemon=True).start()
threading.Thread(target=election_loop, daemon=True).start()
threading.Thread(target=heartbeat_loop, daemon=True).start()
threading.Thread(target=run_http, daemon=True).start()

log_msg("Cluster LBH Iniciado")
while True:
    time.sleep(10)
