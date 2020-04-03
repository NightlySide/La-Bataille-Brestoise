import time
import numpy as np
from random import randint

from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget

from lib.client.global_client_registry import GCR
from lib.common.vecteur import Vecteur


class Radar(QWidget):
    """
    Radar du joueur, permet de détecter les entités aux alentours
    et de les afficher de façon compréhensible à l'écran.

    Args:
        radius (int): rayon d'affichage du radar en pixels
        speed (int): vitesse de rotation du rayon en degrés par seconde
        parent (QWidget): (OPTIONNEL) le parent auquel rattacher
            la fenêtre.
        refresh_rate (float): la vitesse de rafraîchissement de l'écran pour avoir
            un framerate constant

    Attributes:
        angle (float): angle entre la position de départ et celle du faisceau
        points_to_draw (list): points à dessiner sur le radar
        to_remove (list): points à retirer de la liste des points à dessiner
        temps_affichage (float): temps en secondes d'affichage d'un point
            au radar.
    """
    def __init__(self, radius, speed=5, parent=None, refresh_rate=1/30):
        super().__init__(parent)
        self.radius = radius
        self.angle = 0
        self.speed = speed
        self.time_counter = time.perf_counter()
        self.refresh_rate = refresh_rate
        #self.enemies = [(randint(-int(radius*0.75), int(radius*0.75)) + 400//2,
        #                 randint(-int(radius*0.75), int(radius*0.75)) + 300//2) for _ in range(20)]
        self.enemies = []
        self.points_to_draw = []
        self.to_remove = []
        self.temps_affichage = 300 / self.speed

        self.setFixedSize(400, 300)

    def update(self):
        """
        Fonction appelée pour rafraîchir le radar. C'est cette fonction
        qui va venir limiter le nombre d'appels de manière à avoir un
        taux de rafraîchissement de la surface constant.
        Cette fonction est une surcharge des fonctions implémentées par Qt.
        """
        if time.perf_counter() - self.time_counter > self.refresh_rate:
            self.time_counter = time.perf_counter()
            super().update()
            self.enemies = GCR.entities
            # On met à jour l'angle en fonction de la vitesse
            self.angle += self.refresh_rate * self.speed
            self.angle %= 360

            # on fait la liste des points à retirer
            self.to_remove = []
            for pt in self.points_to_draw:
                pt[2] -= self.refresh_rate
                if pt[2] <= 0:
                    self.to_remove.append(pt)

            # on supprime les élents en question
            for element in self.to_remove:
                self.points_to_draw.remove(element)

    def paintEvent(self, event):
        """
        Fonction dérivée de Qt, qui est appelée à chaque fois qu'on rafraîchit l'écran.
        On va venir alors peindre sur le radar.

        Args:
            event (QPaintEvent): évènement du type peinture de l'écran
        """
        qp = QPainter(self)
        # On récupère le centre du radar
        y0 = self.height() // 2
        x0 = self.width() // 2
        # On calcule l'extrémité du faisceau
        x = np.cos(self.angle * np.pi / 180) * self.radius + x0
        y = np.sin(self.angle * np.pi / 180) * self.radius + y0
        # On crée les QPoint correspondants
        origin = QPoint(x0, y0)
        dest = QPoint(x, y)
        direction = Vecteur(np.cos(self.angle * np.pi / 180), np.sin(self.angle * np.pi / 180))

        # On dessine les cercles intermédiaires (4)
        for k in range(1, 5):
            qp.drawEllipse(origin, self.radius * k/4, self.radius * k/4)
        # On dessine le + caractéristique des radars
        qp.drawLine(QPoint(x0 - self.radius, y0), QPoint(x0 + self.radius, y0))
        qp.drawLine(QPoint(x0, y0 - self.radius), QPoint(x0, y0 + self.radius))

        # On prend un nouveau pinc
        original_pen = qp.pen()
        new_pen = QPen()
        new_pen.setColor(Qt.green)
        new_pen.setWidth(2)
        qp.setPen(new_pen)
        # On trace le faisceau
        qp.drawLine(origin, dest)
        # On remet le pinceau original
        qp.setPen(original_pen)

        # Pour chaque ennemi détecté
        for e in self.enemies:
            # On fait le tour des points déjà détectés
            for ent, player_pos, tps in self.points_to_draw:
                # Si le point est déjà présent on sort de la boucle
                if ent == e:
                    break
            # Sinon on le dessine
            else:
                # On vérifie si le point est sur le faisceau
                lim_detect = GCR.joueur.position + direction * GCR.joueur.detection_radius
                diff = lim_detect - GCR.joueur.position
                print(diff)
                if Vecteur.est_entre(GCR.joueur.position, lim_detect, e.position, epsilon=10):
                    # On l'ajoute aux points à dessiner
                    self.points_to_draw.append([e, GCR.joueur.position, self.temps_affichage])

        # Pour chaque points à dessiner
        for ent, player_pos, tps in self.points_to_draw:
            original_pen = qp.pen()
            new_pen = QPen()
            # Si il reste moins de 100° avant de repasser dessus
            # On l'affiche en gris
            if tps < 100 / self.speed:
                new_pen.setColor(Qt.darkGray)
            # Sinon on le met en rouge
            else:
                new_pen.setColor(Qt.red)
            new_pen.setWidth(5)
            qp.setPen(new_pen)
            x = (ent.position.x - player_pos.x) * 8 / GCR.joueur.detection_radius + x0
            y = (ent.position.y - player_pos.y) * 8 / GCR.joueur.detection_radius + y0
            qp.drawPoint(x, y)
            qp.setPen(original_pen)
