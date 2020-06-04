# Auteur : Guillaume LEINEN

from lib.common.entite import Entite
from lib.client.global_client_registry import GCR
from lib.common.vecteur import Vecteur


class Joueur(Entite):
    """
    Définition d'un joueur

    Attributes:
        detection_radius(int): distance de détection en cases
    """
    def __init__(self, position: Vecteur):
        super().__init__()
        self.position = position
        self.detection_radius = 10 # en cases

    def update(self, delta: float) -> None:
        """
        Met à jour les éléments essentiels au fonctionnement de l'entité comme sa position
        ou bien sa direction.

        Args:
            delta (float): temps mis entre l'itération précédente et l'itération actuelle
        """
        self.isDead()
        self.level_up()
        self.current_weapon.update()
        self.takeDamage(self.current_target, 1 / 30)
        self.position += self.direction * self.vitesse
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

    def isDead(self) -> None:
        """
        Test si le joueur à encore assez de points de vie. si les points de vie sont à 0,
        le joueur respawn dans un navire du tier inferieur, l'exp est reset au treshold du tier inferieur
        """
        if self.vie <= 0 and GCR.chatbox is not None:
            GCR.chatbox.add_line(f"Vous êtes mort, respawn au tier inferieur")
        super().isDead()