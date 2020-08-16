import socket
from threading import Thread

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 5000))


def send_message():
    while True:
        message = input().encode()
        sock.send(message)



def recieve_message():
    while True:
        result = sock.recv(4096)
        print(result.decode())


t1 = Thread(target=send_message)
t2 = Thread(target=recieve_message)

t1.start()
t2.start()
