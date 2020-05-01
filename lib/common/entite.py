from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtGui import QImage, QPixmap, QTransform
from uuid import uuid4

from lib.common.armes.arme import Arme
from lib.common.batiments.batiment import Batiment
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
        self.image_direction = self.direction
#TODO        self.current_player = id_joueur()  tcpclient.identifiant
        self.current_ship = Batiment()
        self.current_weapon = Arme()
        self.current_target = None
        self.id = uuid4()

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

    def render(self, qp, x, y, sx, sy):
        """
        Fait le rendu de l'entité sur l'écran à l'aide du painter de
        ce dernier.

        Args:
            qp (QPainter): painter de la surface sur laquelle dessiner
        """
        # Si on a définit une image on la dessine
        if self.image is not None:
            img = QPixmap(self.image)
            if self.image_direction.equal(Vecteur(0.0, 1.0)): # direction sud
                rotation = 180
            elif self.image_direction.equal(Vecteur(1.0, 0.0)): # direction est
                rotation = 90
            elif self.image_direction.equal(Vecteur(-1.0, 0.0)): # direction ouest
                rotation = 270
            else: # direction nord
                rotation = 0
            img_rotated = img.transformed(QTransform().rotate(rotation))
            #xoffset = (img_rotated.width() - img.width()) / 2
            #yoffset = (img_rotated.height() - img.height()) / 2
            #img_rotated = img_rotated.copy(xoffset, yoffset, img.width(), img.height())
            img_rot_scal = img_rotated.scaled(sx, sy)
            qp.drawPixmap(QPoint(x, y), img_rot_scal)
            # qp.drawImage(QRect(self.position.x, self.position.y, 25, 25), QImage(self.image))

    def update(self, delta):
        self.position += self.direction * self.vitesse
        # On retient la dernière direction prise par le bateau
        if not self.direction.equal(Vecteur(0.0, 0.0)):
            self.image_direction = self.direction
        #self.direction = Vecteur()

    def ciblage(self, entite):
        self.current_target = entite()

    @staticmethod
    def findById(e_id, entities):
        for e in entities:
            if e.id == e_id:
                return e
        return None