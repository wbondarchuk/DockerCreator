import sys
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler


def bash(port):
    cmd = f'docker run -d --name docker_theia{port} -p {port}:{port} -v "$(pwd):/home/project:cached" elswork/theia'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0]
    print(result)


class Redirect(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', sys.argv[2])
        self.end_headers()


def main():
    server = HTTPServer(("", int(sys.argv[1])), Redirect)
    bash(3000)
    print("Forwarding...")
    print('||',sys.argv[0], '||', int(sys.argv[1]), '||', sys.argv[2], '||')
    server.serve_forever()
    server.server_close()
    print("Server stopped!")


if __name__ == '__main__':
    if len(sys.argv) - 1 != 2:
        print(f"Usage: {sys.argv[0]} <port_number> <url>")
        sys.exit()

    main()
