import asyncio
import pickle
import uuid
from lib.game_registry import GR


class TCPServer(asyncio.Protocol):

    def __init__(self):
        super().__init__()
        print("[+] Serveur lancé !")

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('[+] Connection ouverte sur {}'.format(peername))
        self.transport = transport
        self.peername = peername
        GR.clients.append(peername)

    def data_received(self, data):
        message = pickle.loads(data)
        print('<-- Données reçues : {!r}'.format(message))

        if message["action"] == "request_id":
            reponse = str(uuid.uuid4())
        elif message["action"] == "ping":
            reponse = "pong"
        elif message["action"] == "echo":
            reponse = message
        elif message["action"] == "nb_people_online":
            reponse = len(GR.clients)
        else:
            reponse = "[+] Commande non reconnue !"
        print('--> Envoi : {!r}'.format(reponse))
        self.transport.write(pickle.dumps(reponse))

    def connection_lost(self, exc) -> None:
        ip, port = self.peername
        self.transport.close()
        GR.clients.remove(self.peername)
        print(f"({ip}:{port}) Connexion fermée ")