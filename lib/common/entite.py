from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage
from batiment import Batiment
from arme import Arme
from lib.common.vecteur import Vecteur


class Entite:
    """
    Definition d'une entité du jeu.

    Attributes:
        vie (int): vie de l'entité
        vitesse (int): vitesse de déplacement de l'unité
        image (QImage): image de référence de l'entité
        position (Vecteur): position du joueur
        direction (Vecteur): direction vers lequel se dirige le joueur
        current_ship(batiment) : batiment actuellement manoeuvré par le joueur
        current_weapon(arme) : arme actuellement équipé par le joueur
        current_target(entite) : entité actuellement visée par le joueur

    """

    def __init__(self):
        self.vie = 20
        self.vitesse = 1
        self.image = None
        self.position = Vecteur(200, 200)
        self.direction = Vecteur()
#TODO        self.current_player = id_joueur()  tcpclient.identifiant
        self.current_ship = batiment()
        self.current_weapon = arme()
        self.current_target = None


    def set_image(self, img_path):
        """
        Affecte une image à l'entité.

        Args:
            img_path (str): chemin d'accès relatif à l'image
        """
        self.image = img_path

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
            qp.drawImage(QRect(self.position.x, self.position.y, 25, 25), QImage(self.image))

    def update(self, delta):
        self.position += self.direction * self.vitesse
        self.direction = Vecteur()

    def ciblage(self, entite):
        self.current_target = entite()
