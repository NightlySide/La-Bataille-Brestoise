from lib.common.armes.arme import Arme


class CanonAutomatique(Arme):

    def __init__(self):
        super().__init__()
        self.nom_arme = "Canon 20 mm"
        self.DPS = 150
        self.degats_instantannée = 0
        self.tps_mise_en_oeuvre = 2
        self.tps_vol = 0
        self.portee = 2
        self.image = QImage("assets\images\armes\20mm.png")
        self.refresh_rate = 1 / 50
