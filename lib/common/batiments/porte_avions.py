# Auteur : Guillaume LEINEN

import os

from lib.common.batiments import batiment
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde, MM40

class PA(batiment.Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "Porte avions"
        self.hitpoints = 50000  # hitpoints int[0:99999]
        self.vmax = 1.4 # vitesse max du batiment
        self.portee_detection = 23 # float [0:99]
        self.armes = [Rafale, CanonAutomatique,
                      Mistral,MM40, C50]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 5  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = os.path.join("assets", "images", "batiments", "porteavion.png")
        self.size = (70, 70)