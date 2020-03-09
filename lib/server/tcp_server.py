import asyncio
import pickle
import uuid
from lib.server.global_server_registry import GSR
from lib.server.player import Player

class TCPServer(asyncio.Protocol):

    def __init__(self):
        print("[+] Serveur lancé !")
        self.transport = None
        self.peername = None
        self.player = None

    @classmethod
    async def create(cls, host, port) -> None:
        server = await GSR.getEventLoop().create_server(
            lambda: TCPServer(),
            host, port)

        async with server:
            print("[+] Serveur lancé")
            await server.serve_forever()

    def connection_made(self, transport) -> None:
        peername = transport.get_extra_info('peername')
        print('[+] Connection ouverte sur {}'.format(peername))
        self.transport = transport
        self.peername = peername
        self.player = Player(peername, transport)
        GSR.clients.append(self.player)

    def data_received(self, data) -> None:
        message = pickle.loads(data)
        print('<-- Données reçues : {!r}'.format(message))

        if isinstance(message, dict):
            reponse = {"action": message["action"]}
            if message["action"] == "request_id":
                self.player.username = message["username"]
                self.player.uuid = str(uuid.uuid4())
                reponse["id"] = self.player.uuid
            elif message["action"] == "ping":
                reponse["msg"] = "pong"
            elif message["action"] == "echo":
                reponse = message
            elif message["action"] == "nb_people_online":
                reponse["length"] = len(GSR.clients)
            elif message["action"] == "chat":
                reponse = message
                username = self.player.username
                reponse["user"] = username
                for client in GSR.clients:
                    if client.peername != self.peername:
                        print('--> Envoi : {!r}'.format(reponse))
                        client.transport.write(pickle.dumps(message))
            else:
                reponse["msg"] = "[+] Commande non reconnue !"
            print('--> Envoi : {!r}'.format(reponse))
            self.transport.write(pickle.dumps(reponse))
        else:
            print("[-] Format reçu inconnu : {!r}".format(message))

    def connection_lost(self, exc) -> None:
        self.transport.close()
        GSR.clients.remove(self.player)
        print(f"{self.peername} Connexion fermée ")