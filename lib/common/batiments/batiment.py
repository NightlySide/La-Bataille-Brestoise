class Batiment:
    Tierlist = [["BE","BIN"],["AVISO","CMT","BH"],["FS","F70"],["FREMM","FDA","SNA","PA","SNLE"]]
    def __init__(self):
        self.nom_unite = ""
        self.hitpoints = 20 #hitpoints int[0:99999]
        self.vmax = 0.0 #vitesse max du batiment
        self.portee_detection = 0.0  #float [0:99]
        self.armes = [] #tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
        self.tier = 1 #tier du navire de 1 à 5
        self.status = True #etat du navire ( vie /mort)

