import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            body = json.dumps({
                "status": "ok",
                "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            })
            self.send_response(200)
        elif self.path == "/health":
            body = json.dumps({"healthy": True})
            self.send_response(200)
        else:
            body = json.dumps({"error": "not found"})
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9876), Handler)
    print("Server running on port 9876")
    server.serve_forever()
