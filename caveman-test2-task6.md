# Task 6: Simple HTTP Server

Write a Python file at `/home/workspace/caveman-test2/http_server.py` that:
- Uses only stdlib (http.server module)
- Creates a simple HTTP server on port 9876
- GET / returns JSON `{"status": "ok", "time": "<current UTC time>"}`
- GET /health returns JSON `{"healthy": true}`
- All other paths return 404 with JSON `{"error": "not found"}`
- Has a `if __name__ == "__main__":` block that starts the server
