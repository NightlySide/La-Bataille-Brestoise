import time

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QImage
from random import randint

class Arme():

    def __init__(self,refresh_rate=1):
        self.nom_arme= ""
        self.DPS = 0
        self.tps_mise_en_oeuvre = 0
        self.portee = 0
        self.image = "assets\images\armes\C5O.png"


