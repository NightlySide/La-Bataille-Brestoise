import time

from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect

from lib.client.global_client_registry import GCR
from lib.common.carte import Carte
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur
from lib.common.image_vers_tableau import img_vers_array


class CanvasJeu(QLabel):
    """
    Canvas sur lequel on va venir dessiner toute la partie jeu, cela inclut la carte
    le joueur et les autres entités

    Args:
        parent (QWidget): (OPTIONNEL) le parent auquel rattacher
            la fenêtre.
        refresh_rate (float): la vitesse de rafraîchissement de l'écran pour avoir
            un framerate constant

    Attributes:
        carte (Carte): les données de la carte de jeu, les tuiles sur lesquelles
            on peut naviguer ou non.
    """

    def __init__(self, parent=None, refresh_rate=1/30):
        super().__init__(parent)
        # On fixe la taille du canvas pour plus de simplicité
        self.setFixedSize(800, 600)
        # Variables nécessaires pour un rafraîchissement constant de l'image
        self.time_counter = time.perf_counter()
        self.refresh_rate = refresh_rate
        self.carte = None

    def set_map(self, carte):
        self.carte = carte

    def keyPressEvent(self, e):
        """
        Fonction héritée de Qt qui permet de prendre en charge les évènements du type
        touche clavier.

        Args:
            e (QKeyEvent): évènement de type touche de clavier
        """
        # On crée un vecteur qui donnera la direction voulue par le joueur
        dir = Vecteur()
        # Si on appuie sur Echap on veut fermer la fenètre de jeu
        if e.key() == Qt.Key_Escape:
            self.parent().parent().parent().close()
        elif e.key() == Qt.Key_Left:
            GCR.log.log(Logger.DEBUG, "Flèche gauche")
            dir.x -= 1
        elif e.key() == Qt.Key_Right:
            GCR.log.log(Logger.DEBUG, "Flèche droite")
            dir.x += 1
        elif e.key() == Qt.Key_Up:
            GCR.log.log(Logger.DEBUG, "Flèche haut")
            dir.y -= 1
        elif e.key() == Qt.Key_Down:
            GCR.log.log(Logger.DEBUG, "Flèche bas")
            dir.y += 1
        # Si la direction a changé
        if not dir.equal(Vecteur(0.0, 0.0)):
            # On indique à l'entité joueur quelle est la direction à prendre
            GCR.joueur.direction = dir

    def paintEvent(self, e):
        """
        Fonction dérivée de Qt, qui est appelée à chaque fois qu'on rafraîchit l'écran.
        On va venir alors peindre sur le canvas.

        Args:
            e (QPaintEvent): évènement du type peinture de l'écran
        """
        qp = QPainter(self)

        # On dessine la carte
        self.carte.render(qp, (self.width(), self.height()))
        # On vient dessiner le joueur par dessus la carte
        #qp.drawImage(QRect(self.width() // 2 - 25, self.height() // 2 - 25, 50, 50), QImage(GCR.joueur.image))
        GCR.joueur.render(qp, self.width() // 2 - 25, self.height() // 2 - 25, 50, 50)
        for entity in GCR.entities:
            if self.carte.can_player_see(entity, (self.width(), self.height())):
                dx = (entity.position.x - GCR.joueur.position.x) * self.carte.cell_size[0] + (self.width() // 2 - 16//2)
                dy = (entity.position.y - GCR.joueur.position.y) * self.carte.cell_size[1] + (self.height() // 2 - 16//2)
                #qp.drawImage(QRect(dx, dy, 16, 16), QImage(entity.image))
                entity.render(qp, dx, dy, 16, 16)

    def mouseMoveEvent(self, e):
        """
        Fonction dérivée de Qt, qui est appelée à chaque fois que la souris
        est bougée sur le canvas

        Args:
            e (QMouseEvent): évènement du type déplacement de souris
        """
        # On récupère la position de la souris sur l'écran
        x = e.x()
        y = e.y()
        text = "x: {0},  y: {1}".format(x, y)
        self.parent().parent().parent().setWindowTitle(text)

    def mousePressEvent(self, e):
        """
        Fonction dérivée de Qt, qui est appelée à chaque fois qu'un
        bouton de la souris est pressé

        Args:
            e (QMouseEvent): évènement du type souris
        """
        GCR.log.log(Logger.DEBUG, f"Souris à la pos : ({e.x()}, {e.y()})")
        # On met le focus sur le canvas pour récupérer les autres évènements ici
        self.setFocus()

    def update(self):
        """
        Fonction appelée pour rafraîchir le canvas. C'est cette fonction
        qui va venir limiter le nombre d'appels de manière à avoir un
        taux de rafraîchissement de la surface constant.
        Cette fonction est une surcharge des fonctions implémentées par Qt.
        """
        if time.perf_counter() - self.time_counter < self.refresh_rate:
            self.time_counter = time.perf_counter()
            super().update()