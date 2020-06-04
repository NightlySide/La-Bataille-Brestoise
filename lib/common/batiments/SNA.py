import os

from lib.common.batiments import batiment
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde, MM40

class SNA(batiment.Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "sous marin nucléaire d'attaque"
        self.hitpoints = 15000  # hitpoints int[0:99999]
        self.vmax = 1.1 # vitesse max du batiment
        self.portee_detection = 15 # float [0:99]
        self.armes = [TorpilleLegere, MM40]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 4  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = os.path.join(os.getcwd(), "assets", "images", "batiments", "sousmarin.png")
        self.size = (40, 40)