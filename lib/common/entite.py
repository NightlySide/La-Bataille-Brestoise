from PyQt5.QtCore import QRect
from PyQt5.QtGui import QImage

from lib.common.vecteur import Vecteur


class Entite:

    def __init__(self):
        self.vie = 20
        self.vitesse = 5
        self.image = None
        self.position = Vecteur(200, 200)

    def set_image(self, img_path):
        self.image = QImage(img_path)

    def is_alive(self):
        return self.vie > 0

    def render(self, qp):
        if self.image is not None:
            qp.drawImage(QRect(self.position.x, self.position.y, 25, 25), self.image)
