from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class TorpilleLegere(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme = "torpille légère "
        self.DPS = 5000
        self.tps_mise_en_oeuvre = 8
        self.portee = 20
        self.image = QImage("assets\images\armes\torpille légère.png")
