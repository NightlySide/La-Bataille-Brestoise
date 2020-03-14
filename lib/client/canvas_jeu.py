import time

import numpy as np
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRect

from random import randint

from lib.client.global_client_registry import GCR
from lib.common.carte import Carte
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur
from lib.common.image_vers_tableau import img_vers_array


class CanvasJeu(QLabel):

    def __init__(self, parent=None, refresh_rate=1/30):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)
        self.time_counter = time.perf_counter()
        self.refresh_rate = refresh_rate

        rade_data = img_vers_array("assets/carte_rade_brest.jpg")
        self.carte = Carte(rade_data.shape, (8, 8), rade_data)

    def keyPressEvent(self, e):
        dir = Vecteur()
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
        GCR.joueur.direction = dir

    def paintEvent(self, e):
        qp = QPainter(self)

        # on dessine la carte
        self.carte.render(qp, (self.width(), self.height()))

        qp.drawImage(QRect(self.width() // 2, self.height() // 2, 50, 50), GCR.joueur.image)

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        text = "x: {0},  y: {1}".format(x, y)
        self.parent().parent().parent().setWindowTitle(text)

    def mousePressEvent(self, e):
        GCR.log.log(Logger.DEBUG, f"Souris à la pos : ({e.x()}, {e.y()})")
        self.setFocus()

    def update(self):
        if time.perf_counter() - self.time_counter < self.refresh_rate:
            self.time_counter = time.perf_counter()
            super().update()
