import hmac
import hashlib
import uuid
import time
import secrets
from typing import Dict, Set

# ==========================================================
# LBH CORE v1.1 - Motor de Comunicación Soberana
# =========================
# Implementa: Anti-replay (Nonces), Time-window, UUID Auth
# ==========================================================

PROTOCOL_VERSION = 1
TIME_WINDOW_SECONDS = 300  # Ventana de validez (5 minutos)

class NonceStore:
    """Almacena nonces temporalmente para evitar ataques de repetición."""
    def __init__(self):
        self.seen: Dict[str, float] = {}

    def register(self, nonce: str) -> bool:
        now = time.time()
        # Limpieza de nonces expirados fuera de la ventana
        expired = [n for n, ts in self.seen.items() if now - ts > TIME_WINDOW_SECONDS]
        for n in expired:
            del self.seen[n]

        if nonce in self.seen:
            return False # Nonce ya usado (Replay detected)

        self.seen[nonce] = now
        return True

class LBHNode:
    def __init__(self, node_id: str, secret_keys: Dict[int, bytes], authorized_nodes: Dict[str, Dict[int, bytes]]):
        """
        node_id: Identificador único del nodo (A16/A20s)
        secret_keys: Claves locales para firmar mensajes salientes
        authorized_nodes: Diccionario de nodos conocidos y sus claves de validación
        """
        self.node_id = node_id
        self.secret_keys = secret_keys
        self.authorized_nodes = authorized_nodes
        self.nonce_store = NonceStore()

    def build_message(self, payload: str, key_id: int) -> str:
        """Construye un frame LBH v1.1 sellado."""
        if key_id not in self.secret_keys:
            raise ValueError("KEY_ID no autorizado para este nodo local")

        timestamp = int(time.time())
        nonce = secrets.token_hex(12)  # 96-bit nonce aleatorio

        # El orden del contenido es vital para la integridad de la firma
        content = f"{PROTOCOL_VERSION}|{self.node_id}|{key_id}|{timestamp}|{nonce}|{payload}"
        signature = self._sign(content, self.secret_keys[key_id])

        return (f"LBH|VER:{PROTOCOL_VERSION}|NODE:{self.node_id}|KEY:{key_id}"
                f"|TS:{timestamp}|NONCE:{nonce}|DATA:{payload}|SIG:{signature}")

    def validate_message(self, message: str) -> bool:
        """Valida integridad, procedencia y frescura del mensaje."""
        try:
            parts = message.split("|")
            if parts[0] != "LBH": return False

            fields = {p.split(":", 1)[0]: p.split(":", 1)[1] for p in parts[1:]}

            # 1. Validación de Versión
            if int(fields["VER"]) != PROTOCOL_VERSION: return False

            # 2. Validación de Identidad del Nodo
            node_id = fields["NODE"]
            if node_id not in self.authorized_nodes: return False

            # 3. Validación de Clave
            key_id = int(fields["KEY"])
            if key_id not in self.authorized_nodes[node_id]: return False

            # 4. Ventana de Tiempo (Anti-Stale)
            timestamp = int(fields["TS"])
            if abs(int(time.time()) - timestamp) > TIME_WINDOW_SECONDS: return False

            # 5. Anti-Replay (Nonce)
            if not self.nonce_store.register(fields["NONCE"]): return False

            # 6. Verificación Criptográfica (Firma)
            content = f"{fields['VER']}|{node_id}|{key_id}|{timestamp}|{fields['NONCE']}|{fields['DATA']}"
            secret = self.authorized_nodes[node_id][key_id]
            
            return hmac.compare_digest(fields["SIG"], self._sign(content, secret))

        except Exception:
            return False

    def _sign(self, content: str, secret: bytes) -> str:
        return hmac.new(secret, content.encode(), hashlib.sha256).hexdigest()

# TEST DE INTEGRIDAD
if __name__ == "__main__":
    node_a_id = "A16-Soberano-Salvador"
    node_a_keys = {1: b"supersecret_shared_key_32bytes!!"}

    # Nodo B conoce a A
    node_b = LBHNode("A20s-Manager-Alpha", {}, {node_a_id: {1: b"supersecret_shared_key_32bytes!!"}})

    node_a = LBHNode(node_a_id, node_a_keys, {})
    
    mensaje = node_a.build_message("INMUNIDAD_HONGO_ACTIVA", key_id=1)
    print(f"Mensaje LBH v1.1:\n{mensaje}")
    print(f"\n¿Mensaje Válido en Nodo Destino?: {node_b.validate_message(mensaje)}")
