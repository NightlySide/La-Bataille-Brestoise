# Auteur : Guillaume LEINEN

from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class Mistral(Arme):

    def __init__(self, parent):
        super().__init__(parent)
        self.nom_arme = "missile mistral léger "
        self.DPS = 4500
        self.tps_mise_en_oeuvre = 5
        self.portee = 5
        self.image = "assets\images\armes\mistral.png"
