from http.server import BaseHTTPRequestHandler, HTTPServer
import json
class
MyAPI(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)

self.send_header("Content-type", "application/json")
        self.end_headers()

        response = {
            "message": 'Hello from my API!'
        }

self.wfile.write(bytes(json.dumps(response).encode()))

