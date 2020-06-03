from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class CanonAutomatique(Arme):

    def __init__(self, parent):
        super().__init__(parent)
        self.nom_arme = "canon de 20mm "
        self.DPS = 2000
        self.tps_mise_en_oeuvre = 3
        self.portee = 2
        self.image = "assets\images\armes\20mm.png"
