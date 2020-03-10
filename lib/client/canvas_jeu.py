from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class CanvasJeu(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        self.setMaximumSize(800, 600)

        pix = QPixmap("assets/images/rade_brest.png")
        self.setPixmap(pix)