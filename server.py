import socketserver


class AllClientsRecieveHandler(socketserver.BaseRequestHandler):
    clients = []

    def handle(self) -> None:
        data = self.request.recv(4096).strip()
        print(self.client_address)
        self.request.sendall(data)


if __name__ == '__main__':
    with socketserver.TCPServer(('127.0.0.1', 5000), AllClientsRecieveHandler) as server:
        server.serve_forever()