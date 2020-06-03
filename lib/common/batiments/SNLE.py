from lib.common.batiments import batiment
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde, MM40

class SNLE(batiment.Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "sous marin nucléaire lanceur d'engins"
        self.hitpoints = 30000  # hitpoints int[0:99999]
        self.vmax = 1.2 # vitesse max du batiment
        self.portee_detection = 18 # float [0:99]
        self.armes = [TorpilleLourde, MM40, TorpilleLegere]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 5  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = "assets/images/batiments/sousmarin.png"