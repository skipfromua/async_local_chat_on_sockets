import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 5004))

message = input().encode()
sock.send(message)
result = sock.recv(4096)
print(result.decode())
