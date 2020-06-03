from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class MM40(Arme):

    def __init__(self, parent):
        super().__init__(parent)
        self.nom_arme = "missile exocet MM40"
        self.DPS = 5000
        self.tps_mise_en_oeuvre = 8
        self.portee = 15
        self.image = "assets\images\armes\exocet.png"
