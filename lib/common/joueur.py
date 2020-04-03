from lib.client.global_client_registry import GCR
from lib.common.entite import Entite
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur


class Joueur(Entite):

    def __init__(self, position):
        super().__init__()
        self.position = position
        self.detection_radius = 10 # en cases
        self.set_image("assets/images/batiments/fremm.png")