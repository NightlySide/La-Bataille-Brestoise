from lib.client.global_client_registry import GCR
from lib.common.entite import Entite
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur


class Joueur(Entite):

    def __init__(self, position):
        super().__init__()
        self.direction = Vecteur()
        self.position = position
        self.set_image("assets/images/batiments/fremm.png")

    def update(self, delta):
        self.position += self.direction
        self.direction = Vecteur()
