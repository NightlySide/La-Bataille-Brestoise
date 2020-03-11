from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from lib.client.global_client_registry import GCR
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur


class CanvasJeu(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)

    def keyPressEvent(self, e):
        dir = Vecteur()
        if e.key() == Qt.Key_Escape:
            self.parent().parent().parent().close()
        elif e.key() == Qt.Key_Left:
            GCR.log.log(Logger.DEBUG, "Flèche gauche")
            dir.y -= 1
        elif e.key() == Qt.Key_Right:
            GCR.log.log(Logger.DEBUG, "Flèche droite")
            dir.y += 1
        elif e.key() == Qt.Key_Up:
            GCR.log.log(Logger.DEBUG, "Flèche haut")
            dir.x -= 1
        elif e.key() == Qt.Key_Down:
            GCR.log.log(Logger.DEBUG, "Flèche bas")
            dir.x += 1
        GCR.joueur.direction = dir

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        GCR.joueur.render(qp)
        qp.end()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        text = "x: {0},  y: {1}".format(x, y)
        GCR.joueur.position.x = x
        GCR.joueur.position.y = y
        self.parent().parent().parent().setWindowTitle(text)

    def mousePressEvent(self, e):
        GCR.log.log(Logger.DEBUG, f"Souris à la pos : ({e.x()}, {e.y()})")
        self.setFocus()
