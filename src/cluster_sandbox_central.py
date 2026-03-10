#!/usr/bin/env python3
import subprocess, time, socket, json, threading

NODES = [9301, 9302, 9303]
NODE_SCRIPT = "nodo_cluster_raft_log_server.py"
PROCESSES = {}

def start_nodes():
    for port in NODES:
        proc = subprocess.Popen(["python3", NODE_SCRIPT, str(port), ",".join(str(p) for p in NODES if p != port)])
        PROCESSES[port] = proc
        print(f"✅ Nodo {port} arrancado con peers: {[p for p in NODES if p != port]}")
        time.sleep(0.5)

def send_command(port, message):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(("localhost", port))
        s.send(json.dumps(message).encode())
        response = s.recv(4096)
        s.close()
        if response:
            return json.loads(response.decode())
    except:
        return None

def monitor_loop():
    while True:
        time.sleep(2)
        for port in NODES:
            status = send_command(port, {"type": "STATUS_CHECK"})
            if status:
                print(f"[MONITOR] Nodo {port} | Líder: {status['leader']} | Commit: {status['commit_index']} | Log size: {len(status['log_entries'])}")
        print("-"*60)

def cli_loop():
    while True:
        try:
            cmd = input("CLUSTER> ")
            if cmd.startswith("set "):
                try:
                    _, k, v = cmd.split()
                    # Enviar al líder
                    leader_port = None
                    for port in NODES:
                        resp = send_command(port, {"type": "WHO_IS_LEADER"})
                        if resp and resp.get("leader"):
                            leader_port = resp["leader"]
                            break
                    if leader_port:
                        send_command(leader_port, {"type": "CLIENT_COMMAND", "command": {k:v}})
                        print(f"✅ Comando {k}:{v} enviado al líder {leader_port}")
                    else:
                        print("⚠️ No se detecta líder actualmente")
                except:
                    print("Uso: set clave valor")
            elif cmd == "status":
                for port in NODES:
                    status = send_command(port, {"type": "STATUS_CHECK"})
                    if status:
                        print(f"[{port}] Líder: {status['leader']} | Commit: {status['commit_index']} | Log size: {len(status['log_entries'])}")
            elif cmd == "exit":
                break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    print("🔹 Deteniendo nodos antiguos si existen...")
    # Opción: matamos procesos viejos si es necesario
    start_nodes()
    print("🟢 Cluster listo. Usa 'set clave valor' o 'status' para monitorear.")

    threading.Thread(target=monitor_loop, daemon=True).start()
    cli_loop()

    print("🛑 Cerrando nodos...")
    for proc in PROCESSES.values():
        proc.terminate()
