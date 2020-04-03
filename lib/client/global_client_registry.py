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
    tcp_thread = None # thread TCP
    loop = None # boucle des évènements
    log = None # logger
    chatbox = None # chatbox en jeu
    joueur = None # reférence au joueur
    id = None # identifiant unique du client
    # Liste des serveurs préenregistrés
    serveurs = [["Localhost", "127.0.0.1", "25566"],
                ["Evril server", "192.168.9.15", "25566"]]
    # Liste des adjectifs pour les pseudos aléatoires
    adjectifs = ["accueillant", "adorable", "alourdi", "attifé", "attrayant", "beau", "carré", "confiant", "costaud",
                 "crasseux", "désillusionné", "droit", "dynamique", "élégant", "élevé", "énervé", "gai", "gentil", "grand",
                 "habillé", "hirsute", "inquiet", "magnifique", "maigre", "maladroit", "merveilleux", "mince", "nerveux",
                 "offensé", "parfait", "plaisant", "propre", "ravissant", "réfléchi", "sauvage", "séduisant",
                 "snob", "sombre", "souriant", "splendide", "svelte", "tendu", "timide", "trompeur", "vif", "vivace"]
    animaux = ["Abeille", "Aigle", "Alligator", "Alpaga", "Anaconda", "Anguille", "Antilope", "Araignée", "Baleine",
               "Belette", "Biche", "Bison", "Boa", "Buse", "Girafe", "Hamster", "Gorille", "Guêpe", "Poisson",
               "Jaguar", "Krill", "Lion", "Requin", "Renne", "Salamandre", "Grenouille", "Python", "Loup", "Lynx",
               "Chat", "Taupe", "Tortue", "Urubu", "Triton"]
    entities = []

    @classmethod
    def getTcpClient(cls):
        """
        Retourne la référence au client tcp
        """
        if cls.tcp_client is None:
            raise Exception("Le client TCP n'a pas été définit !")
        return cls.tcp_client

    @classmethod
    def setTcpClient(cls, client):
        """
        Définit la référence au client tcp
        """
        cls.tcp_client = client

    @classmethod
    def getEventLoop(cls):
        """
        Retourne la référence au thread tcp si il existe
        """
        if cls.loop is None:
            raise Exception("La boucle d'évènement n'est pas définit !")
        return cls.loop

    @classmethod
    def setEventLoop(cls, loop):
        """
        Définit la référence au thread tcp

        Args:
            loop (asyncio.EventLoop): boucle des évènements
        """
        cls.loop = loop

    @classmethod
    def getId(cls):
        """
        Retourne l'identifiant unique du client si il existe
        """
        if cls.id is None:
            print("Le client n'a pas encore reçu d'identifiant !")
            return None
        return cls.id

    @classmethod
    def getRandomName(cls):
        """
        Retourne un nom d'utilisateur généré aléatoirement.
        """
        return random.choice(cls.animaux) + " " + random.choice(cls.adjectifs)