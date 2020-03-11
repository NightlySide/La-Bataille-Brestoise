from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

from lib.client.global_client_registry import GCR
from lib.common.logger import Logger


class CanvasJeu(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)

        pix = QPixmap("assets/images/rade_brest.png")
        self.setPixmap(pix)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.parent().parent().parent().close()
        if e.key() == Qt.Key_Left:
            GCR.log.log(Logger.DEBUG, "Flèche gauche")
        elif e.key() == Qt.Key_Right:
            GCR.log.log(Logger.DEBUG, "Flèche droite")
        elif e.key() == Qt.Key_Up:
            GCR.log.log(Logger.DEBUG, "Flèche haut")
        elif e.key() == Qt.Key_Down:
            GCR.log.log(Logger.DEBUG, "Flèche bas")

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        text = "x: {0},  y: {1}".format(x, y)
        self.parent().parent().parent().setWindowTitle(text)

    def mousePressEvent(self, e):
        GCR.log.log(Logger.DEBUG, f"Souris à la pos : ({e.x()}, {e.y()})")
        self.setFocus()
