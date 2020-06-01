from lib.client.global_client_registry import GCR
from lib.common.entite import Entite
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur
import random

from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter, QColor, QBrush, QPen
from uuid import uuid4
from random import randint

from lib.client.global_client_registry import GCR
from lib.common.armes.arme import Arme
from lib.common.batiments.batiment import Batiment
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur
import time

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
        self.set_image("assets/images/batiments/fremm.png")
        self.size = (50, 50)

    def update(self, delta: float) -> None:
        """
        Met à jour les éléments essentiels au fonctionnement de l'entité comme sa position
        ou bien sa direction.

        Args:
            delta (float): temps mis entre l'itération précédente et l'itération actuelle
        """
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
        if GCR.chatbox is not None:
            GCR.chatbox.add_line(f"Vous êtes mort, respawn au tier inferieur")
        if self.vie <= 0:
            if self.current_ship.tier < 3:
                self.spawnShip(Batiment.Tierlist[1][randint(0, 1)])
                self.exp = 0
            else:
                tier = self.current_ship.tier
                taille = len(Batiment.Tierlist[tier - 1])
                self.spawnShip(Batiment.Tierlist[tier - 1][randint(0, taille - 1)])
                self.exp = Entite.exp_treshold[self.current_ship.tier - 2]