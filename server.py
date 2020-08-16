import socket
import asyncio
import sys

print('Server hosted on: {}:{}'.format(sys.argv[1], sys.argv[2]))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((sys.argv[1], int(sys.argv[2])))  # HOST and PORT
sock.listen()
sock.setblocking(False)

clients = []


async def check_new_connections():
    print('Server is up and waiting for connections...')
    while True:
        try:
            client, addr = sock.accept()
            client.setblocking(False)
            clients.append((client, addr))
        except socket.error:
            await asyncio.sleep(0)


async def check_new_requests():
    errors_cycle_offset = 0
    while True:
        if not clients:
            await asyncio.sleep(0)
        for client, addr in clients:
            try:
                result = client.recv(4096)
                client_addr = addr
            except socket.error:
                await asyncio.sleep(0)
                continue
            for answer_for_client, addr in clients:
                if client_addr != addr:
                    try:
                        answer_for_client.send(result)
                    except socket.error:
                        clients.pop(clients.index((answer_for_client, addr)))
                        errors_cycle_offset += 1
            errors_cycle_offset = send_message_to_rest_of_adresses(errors_cycle_offset, result)


def negative(x):
    return -x


def send_message_to_rest_of_adresses(errors_cycle_offset, result):
    for client_index in range(errors_cycle_offset):
        try:
            client, addr = clients[negative(client_index+1)]
            client.send(result)
        except BaseException as message:
            print(message)
    return 0


ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(check_new_connections()), ioloop.create_task(check_new_requests())]
wait_tasks = asyncio.wait(tasks)
try:
    ioloop.run_until_complete(wait_tasks)
    ioloop.close()
except KeyboardInterrupt:
    sock.close()
    print('Server is down')