import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 5000))

while True:
    message = input().encode()
    sock.send(message)
    result = sock.recv(4096)
    print(result.decode())
