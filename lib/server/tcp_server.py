import asyncio
import pickle
import uuid
from lib.server.global_server_registry import GSR


class TCPServer(asyncio.Protocol):

    def __init__(self):
        print("[+] Serveur lancé !")
        self.transport = None
        self.peername = None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('[+] Connection ouverte sur {}'.format(peername))
        self.transport = transport
        self.peername = peername
        GSR.clients[peername] = self

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
            reponse = len(GSR.clients)
        elif message["action"] == "chat":
            reponse = message
            user, msg = message["user"], message["msg"]
            for peername in GSR.clients:
                if peername != self.peername:
                    print('--> Envoi : {!r}'.format(reponse))
                    GSR.clients[peername].transport.write(pickle.dumps(message))
        else:
            reponse = "[+] Commande non reconnue !"
        print('--> Envoi : {!r}'.format(reponse))
        self.transport.write(pickle.dumps(reponse))

    def connection_lost(self, exc) -> None:
        ip, port = self.peername
        self.transport.close()
        GSR.clients.pop(self.peername, None)
        print(f"({ip}:{port}) Connexion fermée ")