import random

class GCR:
    """
    Registre global de variables globales.
    Dans toutes structures de jeu, les variables globales sont
    nécessaire. Cette classe agit comme un registre qui permet
    de contenir ces variables

    Attributes:
        tcp_client (TCPClientProtocol): tunnel tcp vers le serveur
        loop (asyncio.EventLoop): boucle des évènements
        chatbox (ChatBox): chatbox du jeu
        id (str): identifiant unique du client (uuid)
        serveurs (list): liste des serveurs enregistrés
    """

    tcp_client = None # tunnel TCP
    tcp_thread = None
    loop = None # boucle des évènements
    log = None
    chatbox = None # chatbox en jeu
    id = None # identifiant unique du client
    # Liste des serveurs préenregistrés
    serveurs = [["Localhost", "127.0.0.1", "25566"],
                ["Evril server", "192.168.9.15", "25566"]]

    names = ["Petit lapin", "Quiche lorraine", "Choupinou", "Rutabaga"]

    @classmethod
    def getTcpClient(cls):
        if cls.tcp_client is None:
            raise Exception("Le client TCP n'a pas été définit !")
        return cls.tcp_client

    @classmethod
    def setTcpClient(cls, client):
        cls.tcp_client = client

    @classmethod
    def getEventLoop(cls):
        if cls.loop is None:
            raise Exception("La boucle d'évènement n'est pas définit !")
        return cls.loop

    @classmethod
    def setEventLoop(cls, loop):
        cls.loop = loop

    @classmethod
    def getId(cls):
        if cls.id is None:
            print("Le client n'a pas encore reçu d'identifiant !")
            return None
        return cls.id

    @classmethod
    def getRandomName(cls):
        return random.choice(cls.names)