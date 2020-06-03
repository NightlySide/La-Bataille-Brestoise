from lib.common.batiments import batiment
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde

class CMT(batiment.Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "Batiment école"
        self.hitpoints = 10000  # hitpoints int[0:99999]
        self.vmax = 0.9  # vitesse max du batiment
        self.portee_detection = 4 # float [0:99]
        self.armes = [CanonAutomatique, C50]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 2  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = "assets/images/batiments/BE.png"