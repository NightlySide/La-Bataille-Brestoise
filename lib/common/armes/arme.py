import time

from PyQt5.QtCore import Qt, QRect, QTimer
from random import randint

class Arme():

    def __init__(self,refresh_rate=1, img_path=""):
        self.nom_arme= ""
        self.DPS = 0
        self.degats_instantannee = 0
        self.tps_mise_en_oeuvre = 0
        self.tps_vol = 0
        self.portee = 0
        self.image = img_path
        self.refresh_rate = 1/50
#TODO : faut'il la rendre @privateproperty ?
    def degats(self, entiteEnnemie, degat):
        """
        est appelé par la fonction "dammage", permet d'infliger des dégats pendant un incrément de temps.
                        Args:
                            self: arme
                            entiteEnnemie: la cible qui va recevoir les dégats, objet entité
                            Degat: dégats infligés sur un incrément de temps
        """
        entiteEnnemie.Vie =- degat

    def damage(self, entiteEnnemie, refresh_rate):
        """
        permet d'infliger des dégats à une cible "EntiteEnnemie". Les dégats sont infligés différemment en fonction du type de l'arme
        arme à dégats continus: inflige les dégats en continu selon un temps de refresh refresh_rate. 
        Args:
            entiteEnnemie: la cible qui va recevoir les dégats, objet entité
            refresh_rate: segmentation des dégats continus en petits dégats instantannés sur une petite portion de temps
        les dégats sont consultables sur la tableau d'équillibrage.
        """
        self._timer = QTimer()
        if self.DPS == 0 :
            #arme à dégats instantannées
            update_delta = (self.tps_vol)*1000
            self._timer.start(update_delta)   #perf_counter eventuellement
            self._timer.timeout.connect(self.degats(entiteEnnemie, self.degats_instantannée))

        elif self.degats_instantannée == 0 :
            #arme à DPS
            update_delta = refresh_rate * 1000
            self._timer.start(update_delta)
#TODO:          while mouse == clicked :
            self._timer.timeout.connect(self.degats(entiteEnnemie, self.DPS//refresh_rate))

    def equiper(self):
        """
        permet à un joueur d'équiper une arme. Elle sert à attendre un délai de mise en oeuvre d'une arme avant de pouvoir tirer.
        plus l'arme est importante et plus son temps d'équipement est grand. une arme de conception plus récente aura un temps d'équipement plus court.
        Les valeurs précises sont trouvables dans le tableau d'équillibrage.

        Args:
            self: objet arme

        """
        t0 = time.perf_counter()
        t=t0
        if t > t0 + self.tps_mise_en_oeuvre :
            print("équippement de l'arme : ", self.nom_arme)
