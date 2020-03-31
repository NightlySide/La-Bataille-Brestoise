from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage

from lib.common.vecteur import Vecteur


class Entite:
    """
    Definition d'une entité du jeu.

    Attributes:
        vie (int): vie de l'entité
        vitesse (int): vitesse de déplacement de l'unité
        image (QImage): image de référence de l'entité
        position (Vecteur): position du joueur
    """

    def __init__(self):
        self.vie = 20
        self.vitesse = 5
        self.image = None
        self.position = Vecteur(200, 200)

    def set_image(self, img_path):
        """
        Affecte une image à l'entité.

        Args:
            img_path (str): chemin d'accès relatif à l'image
        """
        self.image = QImage(img_path)

    def is_alive(self):
        """
        Vérifie si l'entité est encore en vie.
        """
        return self.vie > 0

    def render(self, qp):
        """
        Fait le rendu de l'entité sur l'écran à l'aide du painter de
        ce dernier.

        Args:
            qp (QPainter): painter de la surface sur laquelle dessiner
        """
        # Si on a définit une image on la dessine
        if self.image is not None:
            qp.drawImage(QRect(self.position.x, self.position.y, 25, 25), self.image)
