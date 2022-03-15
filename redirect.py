import sys
from http.server import HTTPServer, BaseHTTPRequestHandler


class Redirect(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', sys.argv[2])
        self.end_headers()


if len(sys.argv) - 1 != 2:
    print(f"Usage: {sys.argv[0]} <port_number> <url>")
    sys.exit()

HTTPServer(("", int(sys.argv[1])), Redirect).serve_forever()
