from email import message
from http.server import BaseHTTPRequestHandler, HTTPServer
from google import genai
import json

client = genai.Client()

products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 899.99,
        "quantity": 12
    },
    {
        "id": 2,
        "name": "Mouse",
        "price": 24.99,
        "quantity": 37
    },
    {
        "id": 3,
        "name": "Keyboard",
        "price": 49.99,
        "quantity": 21
    }
]
class MyAPI(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            self.send_response(200)

            response = {"message": "Hello from my API!"}

        elif self.path == "/products":
            self.send_response(200)

            response = {
                'products': products
            }

        else:
            self.send_response(404)

            response = {"error": "Not found"}

        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):

        if self.path == "/chat":
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)

            try:
                data = json.loads(body)

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                response = {"error": "Invalid JSON"}

                self.wfile.write(json.dumps(response).encode())
                return

            if "message" not in data:
                self.send_response(400)

                response = {"error": "Message is required"}

            else:
                message = data["message"]

                ai_response = client.models.generate_content(model="gemini-3.6-flash", contents=message)

                self.send_response(200)

                response = {
                    "reply": ai_response.text
                }

            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())


server = HTTPServer(("localhost", 8080), MyAPI)

print("API Server running on http://localhost:8080")

server.serve_forever()
