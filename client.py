import socket
from threading import Thread
import sys

print('You are connected to: {}:{}'.format(sys.argv[1], sys.argv[2]))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1], int(sys.argv[2])))


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
