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
        self.size = (50, 50)

    def update(self, delta):
        if GCR.current_map is not None:
            new_position = (self.position + self.direction * self.vitesse)
            # Si il n'y a pas de collision avec la map
            if not GCR.current_map.is_colliding(int(new_position.x), int(new_position.y)):
                self.position += self.direction * self.vitesse
            # Si il y en a
            else:
                self.direction = Vecteur()
        if not self.direction.equal(Vecteur(0.0, 0.0)):
            self.image_direction = self.direction