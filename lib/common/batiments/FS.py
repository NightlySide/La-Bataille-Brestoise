from lib.common.batiments import batiment
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde, MM40

class FS(batiment.Batiment):

    def __init__(self):
        super().__init__()
        self.nom_unite = "frégate type FS"
        self.hitpoints = 20000  # hitpoints int[0:99999]
        self.vmax = 1.15 # vitesse max du batiment
        self.portee_detection = 10 # float [0:99]
        self.armes = [Canon,C50, CanonAutomatique,
                      Mistral,MM40]  # tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 3  # tier du navire de 1 à 5
        self.status = True  # etat du navire ( vie /mort)
        self.imgpath = "assets/images/batiments/patrolboat.png"