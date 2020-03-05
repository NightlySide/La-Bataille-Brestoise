import asyncore
import pickle


class TPCHandler(asyncore.dispatcher_with_send):

    def __init__(self, server, sock, ip, port):
        super().__init__(sock)
        self.server = server
        self.closed = False
        self.ip = ip
        self.port = port

    def handle_read(self):
        data = self.recv(8192)
        if data:
            res = pickle.loads(data)
            print(f"({self.ip}:{self.port}) Données reçues : {res}")
            self.send(data)

    def handle_close(self):
        if not self.closed:
            self.closed = True
            print(f"({self.ip}:{self.port}) Connexion fermée ")
            self.server.remove_closed_handlers()


class TCPServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.handlers = {}
        print(f"[+] Serveur ouvert sur {host}:{port}")

    def handle_accepted(self, sock, addr):
        print(f"({addr[0]}:{addr[1]}) Connexion ouverte")
        self.handlers[addr] = TPCHandler(self, sock, *addr)

    def remove_closed_handlers(self):
        a_retirer = []
        for h in self.handlers:
            if self.handlers[h].closed:
                print(f"[-] On retire la connexion : {h}")
                a_retirer.append(h)
        for h in a_retirer:
            self.handlers.pop(h, None)


if __name__ == "__main__":
    server = TCPServer('localhost', 25566)
    asyncore.loop()