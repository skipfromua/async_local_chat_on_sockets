import socket
import asyncio
from time import sleep

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 5004))
sock.listen()
sock.setblocking(False)

clients = []


async def check_new_connections():
    while True:
        try:
            client, addr = sock.accept()
            client.setblocking(False)
            clients.append((client, addr))
        except socket.error:
            await asyncio.sleep(0)


async def check_new_requests():
    while True:
        if not clients:
            await asyncio.sleep(0)
        for client, addr in clients:
            try:
                result = client.recv(4096)
                client_addr = addr
            except socket.error:
                print('have clients')
                await asyncio.sleep(0)
                continue
            for answer_for_client, addr in clients:
                if client_addr != addr:
                    answer_for_client.send(result)


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(check_new_connections()), ioloop.create_task(check_new_requests())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()