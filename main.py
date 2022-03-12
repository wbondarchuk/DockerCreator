import socket
import subprocess

HOST = "192.168.31.252"  # Standard loopback interface address (localhost)
PORT = 8080  # Port to listen on (non-privileged ports are > 1023)


def forwarding(port1):
    cmd = f"iptables -t nat -A PREROUTING -p tcp --dport 192.168.31.252:{PORT} -j DNAT --to-destination 192.168.31.252:{port1}"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0]
    print(result)


def bash(port1, port2):
    cmd = f'docker run -d --name docker_theia -p {port1}:{port2} -v "$(pwd):/home/project:cached" elswork/theia'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    result = p.communicate()[0]
    print(result)




# создаем TCP/IP сокет
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Привязываем сокет к порту
server_address = (HOST, PORT)
print('Server starts on {} port {}'.format(*server_address))
sock.bind(server_address)

# Слушаем входящие подключения
sock.listen(1)

while True:
    # ждем соединения
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    print('Подключено к:', client_address)
    print(client_address[1])
    # forwarding(client_address[1])
    bash(3000, 3000)
    # # Принимаем данные порциями и ретранслируем их
    # while True:
    #     data = connection.recv(4096)
    #     print(f'Получено: {data.decode()}')
    #     if data:
    #         print('Обработка данных...')
    #         data = data.upper()
    #         print('Отправка обратно клиенту.')
    #         connection.sendall(data)
    #     else:
    #         print('Нет данных от:', client_address)
    #         break

    # Очищаем соединение
    connection.close()
