from email import message
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MyAPI(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_header("Content-type", "application/json")
        self.end_headers()

        if self.path == '/':
            self.send_response(200)

            response = {
            "message": 'Hello from my API!'
        }

        elif self.path == '/products':
            self.send_response(200)

            response = {
            "products": ["Laptop", "Mouse", "Keyboard"]
        }

        else:
            self.send_response(404)

            response = {
                "error": "Not found"
            }

    def do_POST(self):

        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                response = {
                    'error': 'Invalid JSON'
                 }

                self.wfile.write(json.dumps(response).encode())
                return

            if 'message' not in data:
                self.send_response(400)

                response = {
                    "error": "Message is required"
                }

            else:
                message = data['message']

                self.send_response(200)

                response = {
                    "reply": f"You said: {message}"
                }

            self.send_header("Content-type", "application/json")
            self.end_headers()


            self.wfile.write(json.dumps(response).encode())

server = HTTPServer(('localhost', 8080), MyAPI)

print("API Server running on http://localhost:8080")

server.serve_forever()
