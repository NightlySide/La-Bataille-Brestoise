from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class CanonSuperRapido(Arme):

    def __init__(self, parent):
        super().__init__(parent)
        self.nom_arme = "canon de 76 mm super rapido"
        self.DPS = 4250
        self.tps_mise_en_oeuvre = 4
        self.portee = 5
        self.image = "assets\images\armes\76mm.png"
