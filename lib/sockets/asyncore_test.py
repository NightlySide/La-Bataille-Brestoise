import asyncore
import pickle


class TPCHandler(asyncore.dispatcher_with_send):

    def __init__(self, sock):
        super().__init__(sock)
        self.closed = False

    def handle_read(self):
        data = self.recv(8192)
        if data:
            res = pickle.loads(data)
            print("Received data : ", res)
            self.send(data)

    def handle_close(self):
        if not self.closed:
            self.closed = True
            print("Close connexion")


class TCPServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print(f"Réception de connexion de {addr}")
        handler = TPCHandler(sock)


if __name__ == "__main__":
    server = TCPServer('localhost', 25566)
    asyncore.loop()