from lib.common.armes.arme import Arme


class CanonSuperRapido(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme = "Canon 76 mm"
        self.DPS = 350
        self.degats_instantannée = 0
        self.tps_mise_en_oeuvre = 3
        self.tps_vol = 0
        self.portee = 7
        self.image = QImage("assets\images\armes\76mm.png")
        self.refresh_rate = 1 / 50
