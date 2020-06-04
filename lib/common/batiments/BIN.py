import os

from lib.common.batiments import batiment
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde

class BIN(batiment.Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "Batiment d'instruction à la navigation"
        self.hitpoints = 10000  # hitpoints int[0:99999]
        self.vmax = 1.0  # vitesse max du batiment
        self.portee_detection = 2.0 # float [0:99]
        self.armes = [C50]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 1  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = os.path.join(os.getcwd(), "assets", "images", "batiments", "BE.png")
        self.size = (25, 25)