from lib.common.armes.arme import Arme


class Canon(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme = "Canon 100 mm"
        self.DPS = 250
        self.degats_instantannée = 0
        self.tps_mise_en_oeuvre = 5
        self.tps_vol = 0
        self.portee = 5
        self.image = QImage("assets\images\armes\100mm.png")
        self.refresh_rate = 1 / 50

