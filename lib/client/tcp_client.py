from lib.client.global_client_registry import GCR
import pickle
import asyncio


class TCPClientProtocol(asyncio.Protocol):

    def __init__(self):
        self.transport = None
        self.id = None

    @classmethod
    async def create(cls, nom, host, port):
        transport, protocol = await GCR.getEventLoop().create_connection(
            lambda: TCPClientProtocol(),
            host, port)

    def connection_made(self, transport):
        self.transport = transport
        GCR.setTcpClient(self)
        addr = transport.get_extra_info('peername')
        print(f'[+] Connecté au serveur : {addr}')
        self.request_client_id()

    def send(self, data):
        if self.transport is None:
            raise Exception("Le client n'est pas connecté à un serveur")
        self.transport.write(pickle.dumps(data))

    def request_client_id(self):
        print("[ ] Demande d'un id client")
        self.send({"action": "request_id"})

    def ping(self):
        self.send({"action": "ping"})

    def data_received(self, data):
        message = pickle.loads(data)
        print("Data received : ", message)
        if isinstance(message, dict):
            if message["action"] == "request_id":
                print("[+] Reçu identifiant : " + message["id"])
                self.id = message["id"]
                GCR.id = message["id"]
            elif message["action"] == "chat":
                GCR.chatbox.add_line(f"({message['user']}): {message['msg']}")
            else:
                print("[-] Réponse serveur non reconnue : {!r}".format(message))
        else:
            print("[-] Format reçu inconnu : {!r}".format(message))

    def connection_lost(self, exc):
        print('[-] Le serveur a fermé la connexion')
        self.transport.close()
        self.transport = None