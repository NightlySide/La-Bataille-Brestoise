from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage

class Rafale(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme = "escadron de rafale "
        self.DPS = 7000
        self.tps_mise_en_oeuvre = 10
        self.portee = 30
        self.image = QImage("assets\images\armes\rafale.png")