import time

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect

from lib.client.global_client_registry import GCR
from lib.common.carte import Carte
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur


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
        self.last_key = None

    def keyPressEvent(self, e):
        """
        Fonction héritée de Qt qui permet de prendre en charge les évènements du type
        touche clavier.

        Args:
            e (QKeyEvent): évènement de type touche de clavier
        """

        # Si on appuie sur Echap on veut fermer la fenètre de jeu
        if e.key() == Qt.Key_Escape:
            self.parent().parent().parent().close()
        elif e.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            # On crée un vecteur qui donnera la direction voulue par le joueur
            dir = Vecteur()
            if e.key() == Qt.Key_Left:
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

            # Si c'est une touche de déplacement on regarde si c'est pour arrêter le bateau
            if e.key() == self.last_key:
                self.last_key = None
                dir = Vecteur()
            # Sinon on enregistre juste la touche
            else:
                self.last_key = e.key()

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
        GCR.current_map.render(qp, (self.width(), self.height()))
        # On vient dessiner le joueur par dessus la carte
        #qp.drawImage(QRect(self.width() // 2 - 25, self.height() // 2 - 25, 50, 50), QImage(GCR.joueur.image))
        GCR.joueur.render(qp, self.width() // 2, self.height() // 2)
        for entity in GCR.entities:
            if GCR.current_map.can_player_see(entity, (self.width(), self.height())):
                dx = (entity.position.x - GCR.joueur.position.x) * GCR.current_map.cell_size[0] + self.width() // 2
                dy = (entity.position.y - GCR.joueur.position.y) * GCR.current_map.cell_size[1] + self.height() // 2
                #qp.drawImage(QRect(dx, dy, 16, 16), QImage(entity.image))
                entity.render(qp, dx, dy)
                # Si l'entité est la cible du joueur
                if GCR.joueur.current_target == entity.id:
                    entity.draw_target(qp, dx, dy)

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
        wx, wy = mouseToWorldPosition(x, y)
        text = "Mouse x: {},  y: {} | World position x: {}, y: {}".format(x, y, wx, wy)
        self.parent().parent().parent().setWindowTitle(text)

    def mousePressEvent(self, e):
        """
        Fonction dérivée de Qt, qui est appelée à chaque fois qu'un
        bouton de la souris est pressé

        Args:
            e (QMouseEvent): évènement du type souris
        """
        x, y = mouseToWorldPosition(e.x(), e.y())
        GCR.log.log(Logger.DEBUG, f"Click à la pos : ({x}, {y})")
        # On met le focus sur le canvas pour récupérer les autres évènements ici
        self.setFocus()
        for e in GCR.entities:
            # Si l'entité n'est pas le joueur on peut cibler
            if e != GCR.joueur:
                diff = Vecteur(x, y) - e.position
                distance = diff.distance()
                GCR.log.log(Logger.DEBUG, f"Distance : {distance}")
                if distance < max(e.size[0], e.size[1]) // (8*2) * 1.5:
                    GCR.joueur.ciblage(e)
                    GCR.log.log(Logger.DEBUG, f"Nouvelle cible : {e.id}")
                    break
        else:
            GCR.joueur.ciblage(None)

    def update(self):
        """
        Fonction appelée pour rafraîchir le canvas. C'est cette fonction
        qui va venir limiter le nombre d'appels de manière à avoir un
        taux de rafraîchissement de la surface constant.
        Cette fonction est une surcharge des fonctions implémentées par Qt.
        """
        if self.time_counter - time.perf_counter() < self.refresh_rate:
            self.time_counter = time.perf_counter()
            super().update()
            GCR.getTcpClient().send({
                        "action": "update_player",
                        "user": GCR.getTcpClient().id,
                        "data": GCR.joueur})


def mouseToWorldPosition(mouseX, mouseY):
    x0, y0 = GCR.joueur.position.x, GCR.joueur.position.y
    dx = (mouseX - 800 // 2) // 8
    dy = (mouseY - 600 // 2) // 8
    return int(x0 + dx), int(y0 + dy)