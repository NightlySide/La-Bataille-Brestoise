from lib.common.vecteur import Vecteur


class Client:
    """
    Référence du coté serveur au joueur.

    Args:
        peername (list): couple IPv4 et port du client
        transport (Transport): tunnel tcp entre le client et le serveur

    Attributes:
        username (str): pseudonyme du client
        uuid (str): identifiant unique du client
    """

    def __init__(self, peername, transport):
        self.peername = peername
        self.transport = transport
        self.username = None
        self.uuid = None
        self.position = Vecteur()
        self.vie = 0

    def update_from_data(self, joueur):
        self.position = joueur.position
        self.vie = joueur.vie

    @staticmethod
    def find_client_by_peername(clients, peername):
        for c in clients:
            if c.peername == peername:
                return c
        else:
            return None

    @staticmethod
    def find_client_by_uuid(clients, uuid):
        for c in clients:
            if c.uuid == uuid:
                return c
        else:
            return None