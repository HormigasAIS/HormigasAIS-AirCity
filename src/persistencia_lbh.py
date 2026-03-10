#!/usr/bin/env python3
"""
Módulo de persistencia para nodo_cluster_raft_log_server.py
Guarda y restaura state_machine y commit_index en disco
"""
import json, os, time

PERSIST_FILE = os.path.expanduser(
    "~/HormigasAIS-Nodo-Escuela/INCUBADORA_AIR_CITY/lbh_state_persist.json"
)

def guardar_estado(state_machine, commit_index, term):
    data = {
        "state_machine": state_machine,
        "commit_index": commit_index,
        "term": term,
        "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    tmp = PERSIST_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, PERSIST_FILE)

def restaurar_estado():
    if not os.path.exists(PERSIST_FILE):
        return {}, -1, 0
    try:
        with open(PERSIST_FILE) as f:
            data = json.load(f)
        print(f"[PERSIST] Restaurado: {len(data['state_machine'])} entradas | commit={data['commit_index']}")
        return data["state_machine"], data["commit_index"], data.get("term", 0)
    except:
        return {}, -1, 0
