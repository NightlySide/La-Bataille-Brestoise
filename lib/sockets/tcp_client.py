import socket
import pickle
import uuid


class TCPClient:

    def __init__(self, host, port, chunk_size=8192):
        self.addr = (host, port)
        self.chunk_size = chunk_size
        self.socket = None
        self.connect()

    def connect(self, host=None, port=None):
        ip = host if host is not None else self.addr[0]
        p = port if port is not None else self.addr[1]
        print(f"[ ] Connexion en cours au ({ip}, {p})")
        if self.socket is not None:
            self.close()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, p))
            self.socket = sock
            print(f"[+] Connecté au serveur avec succès !")
        except ConnectionRefusedError:
            print(f"[-] ERREUR : le serveur {host} n'est pas atteignable sur {port}")

    def send(self, data):
        if self.socket is None:
            raise Exception("Le client n'est pas connecté, tentez client.connect()")
        self.socket.send(pickle.dumps(data))
        return self.recv()

    def recv(self):
        if self.socket is None:
            raise Exception("Le client n'est pas connecté, tentez client.connect()")
        return pickle.loads(self.socket.recv(self.chunk_size))

    def close(self):
        print("[-] Fermeture du socket")
        self.socket.close()
        self.socket = None
