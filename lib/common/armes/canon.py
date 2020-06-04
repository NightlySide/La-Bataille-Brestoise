# Auteur : Guillaume LEINEN

from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class Canon(Arme):

    def __init__(self, parent):
        super().__init__(parent)
        self.nom_arme = "canon de 100 mm "
        self.DPS = 4000
        self.tps_mise_en_oeuvre = 5
        self.portee = 8
        self.image = "assets\images\armes\100mm.png"

