# Auteur : Guillaume LEINEN

import os

from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde
from lib.common.batiments.batiment import Batiment


class AVISO(Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "AVISO"
        self.hitpoints = 15000  # hitpoints int[0:99999]
        self.vmax = 1.0  # vitesse max du batiment
        self.portee_detection = 3.0  # float [0:99]
        self.armes = [Canon,C50,CanonAutomatique,Mistral ]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 2  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = os.path.join("assets", "images", "batiments", "patrolboat.png")
        self.size = (40, 40)