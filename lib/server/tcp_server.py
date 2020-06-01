import asyncio
import pickle
import threading
import uuid

from lib.common.logger import Logger
from lib.server.game_loop import GameLoop, GameState
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
    def __init__(self, max_players):
        self.transport = None
        self.peername = None
        self.client = None
        self.max_players = max_players

    @classmethod
    async def create(cls, host, port, max_players):
        """
        Fonction usine qui instancie le serveur et utilise
        cette classe comme protocole.

        Args:
            host (str): l'ip (IPv4) du serveur
            port (int): le port du serveur
        """
        # On crée le serveur en asynchrone
        server = await GSR.getEventLoop().create_server(
            lambda: TCPServer(max_players),
            host, port)

        # On crée le thread de la boucle du jeu et on le démarre
        GSR.game_loop = GameLoop()

        # On fait tourner le serveur
        GSR.log.log(Logger.INFORMATION, "Serveur lancé")
        return server

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
        self.transport.set_write_buffer_limits(high=self.transport.get_write_buffer_limits()[1], low=0)
        GSR.log.log(Logger.INFORMATION, "Write buffer limits : "+str(self.transport.get_write_buffer_limits()))
        # On crée le client en conséquence
        self.client = Client(peername, transport)
        # On l'ajoute finalement à la liste des clients connectés au serveur
        GSR.clients.append(self.client)
        GSR.log.log(Logger.DEBUG, f"Il y a {len(GSR.clients)} joueurs connectés !")

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
        #GSR.log.log(Logger.DEBUG, "<-- Données reçues : {!r}".format(message))

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
            # si c'est une requete d'entités
            elif message["action"] == "request_entities":
                reponse["data"] = GSR.entities
                GSR.log.log(Logger.DEBUG, "--> Envoi des entités à {}".format(self.peername))
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
                        GSR.log.log(Logger.DEBUG, "--> Envoi à {} : {!r}".format(client.peername, reponse))
                        client.transport.write(pickle.dumps(reponse))
            elif message["action"] == "update_player":
                user_id = message["user"]
                joueur = message["data"]
                client = Client.find_client_by_uuid(GSR.clients, user_id)
                if client is not None:
                    client.update_from_data(joueur)
                    #GSR.log.log(Logger.DEBUG, client.position)
                    reponse["result"] = True
                else:
                    reponse["result"] = False
            elif message["action"] == "start_game":
                username = Client.find_client_by_uuid(GSR.clients, message["user"]).username
                # Si la partie est déjà démarrée ou terminée c'est une erreur
                if GSR.gamestate != GameState.NOTSTARTED:
                    GSR.log.log(Logger.ERREUR, f"Le joueur {username}({message['user']}) essaie de lancer une partie "
                                               f"déjà lancée ou bien terminée.")
                # Sinon on lance la partie
                else:
                    GSR.log.log(Logger.INFORMATION, "Démarrage de la partie")
                    GSR.gamestate = GameState.STARTED
                    self.send_all("set_gamestate", {"gamestate": GameState.STARTED})
                    self.send_all("chat", {"user": "Server", "msg": f"{username} à lancé la partie"})
                    self.send_all("chat", {"user": "Server", "msg": f"Début de partie"})
            else:
                reponse["msg"] = "[+] Commande non reconnue !"
            #GSR.log.log(Logger.DEBUG, "--> Envoi à {} : {!r}".format(self.peername, reponse))
            # On retourne une réponse au client
            self.transport.write(pickle.dumps(reponse))
        else:
            GSR.log.log(Logger.AVERTISSEMENT, "[-] Format reçu inconnu : {!r}".format(message))

    @staticmethod
    def send_all(action, data):
        message = {"action": action}
        for key in data:
            message[key] = data[key]
        if action == "chat":
            GSR.log.log(Logger.DEBUG, f"[CHAT] Envoi à tous de : {message}")
        for client in GSR.clients:
            client.transport.write(pickle.dumps(message))

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