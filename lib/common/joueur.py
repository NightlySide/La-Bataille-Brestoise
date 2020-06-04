# Auteur : Guillaume LEINEN

from lib.common.entite import Entite
from lib.client.global_client_registry import GCR
from lib.common.vecteur import Vecteur


class Joueur(Entite):
    """
    Définition d'un joueur par héritage d'une entite ( comprendre Joueur = Entité humaine)

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
            delta (float): temps mis entre l'itération précédente et l'itération actuelle, ce temps est cruciale dans les performances du programme
        """
        #test de mort ou du montée de niveau
        self.isDead()
        self.level_up()
        #on vérifie que l'arme est bien équipé
        self.current_weapon.update()
        #on interroge la fonction takeDamage pour effectuer ou non des dégats
        self.takeDamage(self.current_target, 1 / 30)
        #maj de la position
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
        le joueur respawn dans un navire du tier inferieur, l'exp est reset au threshold du tier inferieur
        """
        if self.vie <= 0 and GCR.chatbox is not None:
            #la surcharge de la fonction est nécessaire pour afficher un message dans le chat (un bot ne peut pas ecrire dans le chat car il n'est pas relié à un client)
            GCR.chatbox.add_line(f"Vous êtes mort, respawn au tier inferieur")
        super().isDead()