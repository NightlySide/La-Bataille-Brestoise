from lib.common.armes.arme import Arme


class C50(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme= "Mitrailleuse Calibre 50"
        self.DPS = 100
        self.degats_instantannée = 0
        self.tps_mise_en_oeuvre = 1
        self.tps_vol = 0
        self.portee = 1
        self.image = QImage("assets\images\armes\C5O.png")
        self.refresh_rate = 1/50
