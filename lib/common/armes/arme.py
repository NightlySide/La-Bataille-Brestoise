import time

from PyQt5.QtCore import Qt, QRect
from random import randint

class Arme():

    def __init__(self,refresh_rate=1):
        self.nom_arme= ""
        self.DPS = 0
        self.degats_instantannee = 0
        self.tps_mise_en_oeuvre = 0
        self.tps_vol = 0
        self.portee = 0
        self.image = QImage(img_path)
        self.refresh_rate = 1/50

    def degats(self, entiteEnnemie, Degat):
        #inflige les dégats en un refresh rate
        entiteEnnemie.VIE =- Degat

    def dammage(self, entiteEnnemie, refresh_rate = self.refresh_rate):
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
        t0 = time.perf_counter()
        t=t0
        if t > t0 + self.tps_mise_en_oeuvre :


