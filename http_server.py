from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read the content length from the headers
        content_length = int(self.headers['Content-Length'])
        # Read the body of the request
        post_data = self.rfile.read(content_length)
        print(f"Received hidden data: {post_data.decode('utf-8')}")

        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        # Send the response body
        self.wfile.write(b"hello my name is eli")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
