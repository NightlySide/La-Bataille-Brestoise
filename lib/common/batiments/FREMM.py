from lib.common.batiments import batiment
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde, MM40

class FREMM(batiment.Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "frégate type FREMM"
        self.hitpoints = 30000  # hitpoints int[0:99999]
        self.vmax = 1.3  # vitesse max du batiment
        self.portee_detection = 30 # float [0:99]
        self.armes = [CanonSuperRapido,C50, CanonAutomatique,
                      Mistral,MM40, TorpilleLegere]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 4  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = "assets/images/batiments/Fremm.png"