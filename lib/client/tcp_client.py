from lib.client.global_client_registry import GCR
import pickle
import asyncio


class TCPClientProtocol(asyncio.Protocol):
    """
    Classe protocole permettant de créer un tunnel TCP bidirectionnel
    entre le serveur et le client.
    A cause des spécificités de la bibliothèque asyncio, on est
    obligé de passer par ce qu'on appelle une fonction 'usine' qui
    va instancier la connexion en utilisant cette classe comme protocole.

    Args:
        nom (str): le nom du serveur qui sera affiché
        username (str): le nom d'utilisateur du joueur

    Attributes:
        transport (asyncio.Transport): le buffer d'écriture sur le tunnel TCP
        id (str): identifiant unique du client (uuid) fourni par le serveur
        nom (str): le nom du serveur qui sera affiché
        username (str): le nom d'utilisateur du joueur
    """
    def __init__(self, nom, username):
        self.transport = None
        self.id = None
        self.nom = nom
        self.username = username

    @classmethod
    async def create(cls, nom, host, port, username):
        """
        Fonction usine qui instancie la connexion et utilise
        cette classe comme protocole.

        Args:
            nom (str): le nom du serveur qui sera affiché
            host (str): l'ip (IPv4) du serveur auquel se connecter
            port (int): le port du serveur auquel se connecter
            username (str): le nom d'utilisateur du joueur
        """
        transport, protocol = await GCR.getEventLoop().create_connection(
            lambda: TCPClientProtocol(nom, username),
            host, port)

    def connection_made(self, transport):
        """
        Appelée lorsque l'évènement 'connexion réalisée' se produit.
        On définit alors ce tunnel comme étant celui que le client
        devra utiliser.

        Args:
            transport (asyncio.Transport): le buffer d'écriture du tunnel
        """
        self.transport = transport
        # On définit ce protocole comme celui à utiliser
        GCR.setTcpClient(self)
        addr = transport.get_extra_info('peername')
        print(f'[+] Connecté au serveur : {addr}')
        # On demande au serveur de nous attribuer un identifiant
        self.request_client_id()

    def send(self, data):
        """
        Permet de transmettre les données 'data' au serveur
        en TCP en encodant les données à l'aide de pickle.

        Args:
            data (any): données à transmettre
        """
        if self.transport is None:
            raise Exception("Le client n'est pas connecté à un serveur")
        self.transport.write(pickle.dumps(data))

    def request_client_id(self):
        """
        Fait la demande au serveur d'un identifiant unique
        """
        print("[ ] Demande d'un id client")
        self.send({"action": "request_id", "username": self.username})

    def ping(self):
        """
        Envoi un ping au serveur. Ce dernier répondra 'pong'
        si le message est bien reçu.
        """
        self.send({"action": "ping"})

    def data_received(self, data):
        """
        Appelée lorsque l'évènement 'données reçues' se produit.
        Permet la reception en asynchrone de données du serveur
        et d'agir en fonction de la nature de la réponse.

        Args:
            data (any): données reçues encodées à l'aide de pickle
        """
        # On décode la réponse
        message = pickle.loads(data)
        # Si la réponse est dans le bon format
        if isinstance(message, dict):
            if message["action"] == "request_id":
                print("[+] Reçu identifiant : " + message["id"])
                self.id = message["id"]
                GCR.id = message["id"]
            elif message["action"] == "chat":
                # On met à jour la chatbox
                GCR.chatbox.add_line(f"({message['user']}): {message['msg']}")
            else:
                # Sinon on ne connait pas (encore) la demande
                print("[-] Réponse serveur non reconnue : {!r}".format(message))
        else:
            # On a reçu un autre type de données
            print("[-] Format reçu inconnu : {!r}".format(message))

    def connection_lost(self, exc):
        """
        Appelée lorsque l'évènement 'connexion perdue' se réalise.
        Ferme la connexion du côté client.

        Args:
            exc (Exception): objet exception pour lever une erreur
                si erreur il y a
        """
        print('[-] Le serveur a fermé la connexion')
        self.transport.close()
        self.transport = None
