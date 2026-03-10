import time
import requests

BEACON = "http://192.168.1.5:8080/beacon"

print("🐜 CENTINELA — Escuchando feromona A20...")

while True:
    try:
        r = requests.get(BEACON, timeout=2)
        print("✅ FEROMONA RECIBIDA:", r.text.strip())
    except:
        print("⚠️ BEACON perdido... buscando...")
    time.sleep(2)
