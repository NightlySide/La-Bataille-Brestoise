from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class Mistral(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme = "missile mistral léger "
        self.DPS = 4500
        self.tps_mise_en_oeuvre = 5
        self.portee = 5
        self.image = QImage("assets\images\armes\mistral.png")
