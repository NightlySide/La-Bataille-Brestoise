from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class TorpilleLourde(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme = "torpille lourde "
        self.DPS = 6000
        self.tps_mise_en_oeuvre = 10
        self.portee = 30
        self.image = QImage("assets\images\armes\torpille lourde.png")