from lib.common.armes.arme import Arme
from PyQt5.QtGui import QImage


class C50(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme = "mitrailleuse calibre 50 "
        self.DPS = 1000
        self.tps_mise_en_oeuvre = 1
        self.portee = 1
        self.image = "assets\images\armes\C5O.png"



