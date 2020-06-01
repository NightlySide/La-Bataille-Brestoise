from asyncio import Transport

from lib.common.joueur import Joueur
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

    def __init__(self, peername: str, transport: Transport):
        self.peername = peername
        self.transport = transport
        self.username = None
        self.uuid = None
        self.joueur = Joueur(Vecteur())

    def update_from_data(self, joueur: Joueur) -> None:
        self.joueur = joueur

    @staticmethod
    def find_client_by_peername(clients: list, peername: str) -> "Client" or None:
        """
        Permet de trouver un client à partir du son nom de pair

        Args:
            clients (list): liste des clients dans laquelle chercher
            peername (str): nom de pair à trouver dans la liste

        Returns:
            client (Client): le client si il est trouvé
        """
        for c in clients:
            if c.peername == peername:
                return c
        else:
            return None

    @staticmethod
    def find_client_by_uuid(clients: list, uuid: str) -> "Client" or None:
        """
        Permet de trouver un client à partir du son identifiant unique

        Args:
            clients (list): liste des clients dans laquelle chercher
            uuid (str): identifiant unique à trouver dans la liste

        Returns:
            client (Client): le client si il est trouvé
        """
        for c in clients:
            if c.uuid == uuid:
                return c
        else:
            return None