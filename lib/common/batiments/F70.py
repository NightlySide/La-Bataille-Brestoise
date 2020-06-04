# Auteur : Guillaume LEINEN

import os

from lib.common.batiments import batiment
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde, MM40

class F70(batiment.Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "frégate type F70"
        self.hitpoints = 30000  # hitpoints int[0:99999]
        self.vmax = 1.1  # vitesse max du batiment
        self.portee_detection = 8 # float [0:99]
        self.armes = [MM40, Canon, CanonAutomatique,
                      Mistral,C50]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 3  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = os.path.join("assets", "images", "batiments", "F70.png")
        self.size = (50, 50)