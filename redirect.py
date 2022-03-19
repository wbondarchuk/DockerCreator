import sys
import subprocess
import random
from http.server import HTTPServer, BaseHTTPRequestHandler


def port_generator():
    port = random.choice(ports)
    return port


def port_check(port, work_ports):
    if port not in work_ports:
        work_ports.append(port)
    else:
        port = port_generator()
        port_check(port, work_ports)
    return port


def docker_run(port):
    cmd = f'docker run -d --name docker_theia{port} -p {port}:{port} -v "$(pwd):/home/project:cached" elswork/theia'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0].decode("utf-8")[:-1]
    print(result)
    return result


def docker_remove(id):
    cmd = f'docker rm -f {id}'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0]
    print(result)
    return result


class Redirect(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(302)
        self.send_header('Location', sys.argv[2])
        self.end_headers()


def main():
    server = HTTPServer(("", int(sys.argv[1])), Redirect)
    docker_id = docker_run(3000)
    print("Forwarding...")
    print('||', sys.argv[0], '||', int(sys.argv[1]), '||', sys.argv[2], '||')
    print(docker_id)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        docker_remove(docker_id)
        print("Server stopped!")
        server.server_close()


if __name__ == '__main__':

    ports = [3000, 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010]
    work_ports = []

    if len(sys.argv) - 1 != 2:
        print(f"Usage: {sys.argv[0]} <port_number> <url>")
        sys.exit()

    main()
