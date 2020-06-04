# Auteur : Guillaume LEINEN


class Batiment:
    """
        La classe Batiment définit un navire, manoeuvré par une entité.


        Attributes:
            nom_unite(str) : nom de l'unité
            hitpoints(int) : points de vie maximum de l'unité
            vmax(float) : vitesse de déplacement du batiment
            portee_detection(float) : portée de détection d'un ennemi (non implémenté)
            armes(list(armes) : tableau des objets Armes utilisables par un navire. L'arme en première position est l'arme par défaut
            tier(int) : niveau du navire (de 1 à 5)
            status(bool) : etat de vie ou de mort d'un batiment
            imgpath(str) : Path vers l'icone representant un batiment sur la carte (Canevas_jeu)
            size(tupple) : taille par défaut de l'unité


    """
    def __init__(self):
            self.nom_unite = ""
            self.hitpoints = 20 #hitpoints int[0:99999]
            self.vmax = 0.0 #vitesse max du batiment
            self.portee_detection = 0.0  #float [0:99]
            self.armes = [] #tableau des armes equipé [str], l'arme d'indice 0 est équipé d'office
            self.tier = 1 #tier du navire de 1 à 5
            self.status = True #etat du navire ( vie /mort)
            self.imgpath = "assets/images/batiments/fremm.png"
            self.size = (50, 50)

