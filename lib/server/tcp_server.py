import asyncio
import pickle
import threading
import uuid

from lib.common.logger import Logger
from lib.server.game_loop import GameLoop
from lib.server.global_server_registry import GSR
from lib.server.client import Client


class TCPServer(asyncio.Protocol):
    """
    Classe protocole permettant de créer un serveur TCP qui
    accueille les clients.
    A cause des spécificités de la bibliothèque asyncio, on est
    obligé de passer par ce qu'on appelle une fonction 'usine' qui
    va instancier la connexion en utilisant cette classe comme protocole.

    Attributes:
        transport (asyncio.Transport): le buffer d'écriture sur le tunnel TCP
        id (str): identifiant unique du client (uuid) fourni par le serveur
        peername (list): couple IPv4, port
        client (Client): référence au client connecté
    """
    def __init__(self):
        self.transport = None
        self.peername = None
        self.client = None

    @classmethod
    async def create(cls, host, port):
        """
        Fonction usine qui instancie le serveur et utilise
        cette classe comme protocole.

        Args:
            host (str): l'ip (IPv4) du serveur
            port (int): le port du serveur
        """
        # On crée le serveur en asynchrone
        server = await GSR.getEventLoop().create_server(
            lambda: TCPServer(),
            host, port)

        # On crée le thread de la boucle du jeu et on le démarre
        GSR.game_loop = GameLoop()

        # On fait tourner le serveur
        async with server:
            GSR.log.log(Logger.INFORMATION, "Serveur lancé")
            await server.serve_forever()

    def connection_made(self, transport):
        """
        Appelée lorsque l'évènement 'connexion réalisée' se produit.
        On définit alors ce tunnel comme étant celui que le serveur
        devra utiliser.

        Args:
            transport (asyncio.Transport): le buffer d'écriture du tunnel
        """
        # On récupère les informations de connexion
        peername = transport.get_extra_info('peername')
        GSR.log.log(Logger.INFORMATION, "Connexion ouverte sur {}".format(peername))
        # On l'enregistre
        self.transport = transport
        self.peername = peername
        # On crée le client en conséquence
        self.client = Client(peername, transport)
        # On l'ajoute finalement à la liste des clients connectés au serveur
        GSR.clients.append(self.client)

    def data_received(self, data):
        """
        Appelée lorsque l'évènement 'données reçues' se produit.
        Permet la reception en asynchrone de données des clients
        et d'agir en fonction de la nature de la requête.

        Args:
            data (any): données reçues encodées à l'aide de pickle
        """
        # On récupère le message encodé
        message = pickle.loads(data)
        GSR.log.log(Logger.DEBUG, "<-- Données reçues : {!r}".format(message))

        # Si le message est dans un format que l'on connait
        if isinstance(message, dict):
            reponse = {"action": message["action"]}
            # Si c'est une requete d'identifiant
            if message["action"] == "request_id":
                self.client.username = message["username"]
                # On génère un identifiant
                self.client.uuid = str(uuid.uuid4())
                reponse["id"] = self.client.uuid
                # On envoie à tout le monde sur le chat
                # Qu'un joueur s'est connecté
                msg = self.client.username + ' a rejoint la partie'
                GSR.log.log(Logger.INFORMATION, msg)
                for client in GSR.clients:
                    if client.peername != self.peername:
                        client.transport.write(pickle.dumps({"action": "chat", "user": "Server", "msg": msg}))
            # Si c'est un ping
            elif message["action"] == "ping":
                reponse["msg"] = "pong"
            elif message["action"] == "echo":
                reponse = message
            elif message["action"] == "nb_people_online":
                reponse["length"] = len(GSR.clients)
            # Si c'est un message de chat
            elif message["action"] == "chat":
                reponse = message
                username = self.client.username
                # On remplace l'identifiant du joueur par son pseudo
                reponse["user"] = username
                # On transmet le message aux autres clients
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
        """
        Appelée lorsque l'évènement 'connexion perdue' se réalise.
        Ferme la connexion du côté serveur.

        Args:
            exc (Exception): objet exception pour lever une erreur
                si erreur il y a
        """
        # On ferme le tunnel
        self.transport.close()
        # On retire le client de la liste des clients connectés
        GSR.clients.remove(self.client)
        GSR.log.log(Logger.INFORMATION, "Connexion fermée avec {}".format(self.peername))