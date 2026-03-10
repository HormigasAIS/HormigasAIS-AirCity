from http.server import BaseHTTPRequestHandler, HTTPServer

BEACON_ID = "S9-DATA-IMMUNE-2026"

class BeaconHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/beacon":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(BEACON_ID.encode())
        else:
            self.send_response(404)
            self.end_headers()

print("🐜 HormigasAIS BEACON ACTIVO:", BEACON_ID)
print("📡 Puerto: 8080")

server = HTTPServer(("0.0.0.0", 8080), BeaconHandler)
server.serve_forever()
