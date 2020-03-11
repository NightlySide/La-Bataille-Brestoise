import asyncio
import pickle
import uuid

from lib.common.logger import Logger
from lib.server.global_server_registry import GSR
from lib.server.player import Player


class TCPServer(asyncio.Protocol):

    def __init__(self):
        self.transport = None
        self.peername = None
        self.player = None

    @classmethod
    async def create(cls, host, port) -> None:
        server = await GSR.getEventLoop().create_server(
            lambda: TCPServer(),
            host, port)

        async with server:
            GSR.log.log(Logger.INFORMATION, "Serveur lancé")
            await server.serve_forever()

    def connection_made(self, transport) -> None:
        peername = transport.get_extra_info('peername')
        GSR.log.log(Logger.INFORMATION, "Connexion ouverte sur {}".format(peername))
        self.transport = transport
        self.peername = peername
        self.player = Player(peername, transport)
        GSR.clients.append(self.player)

    def data_received(self, data) -> None:
        message = pickle.loads(data)
        GSR.log.log(Logger.DEBUG, "<-- Données reçues : {!r}".format(message))

        if isinstance(message, dict):
            reponse = {"action": message["action"]}
            if message["action"] == "request_id":
                self.player.username = message["username"]
                self.player.uuid = str(uuid.uuid4())
                reponse["id"] = self.player.uuid
                msg = self.player.username + ' a rejoint la partie'
                GSR.log.log(Logger.INFORMATION, msg)
                for client in GSR.clients:
                    if client.peername != self.peername:
                        client.transport.write(pickle.dumps({"action": "chat", "user": "Server", "msg": msg}))
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
                        client.transport.write(pickle.dumps(message))
            else:
                reponse["msg"] = "[+] Commande non reconnue !"
            GSR.log.log(Logger.DEBUG, "--> Envoi : {!r}".format(reponse))
            self.transport.write(pickle.dumps(reponse))
        else:
            GSR.log.log(Logger.AVERTISSEMENT, "[-] Format reçu inconnu : {!r}".format(message))

    def connection_lost(self, exc) -> None:
        self.transport.close()
        GSR.clients.remove(self.player)
        GSR.log.log(Logger.INFORMATION, "Connexion fermée avec {}".format(self.peername))