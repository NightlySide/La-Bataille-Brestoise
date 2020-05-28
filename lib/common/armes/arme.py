import time

from PyQt5.QtCore import Qt, QRect
from random import randint

class Arme():

    def __init__(self,refresh_rate=1, img_path=""):
        self.nom_arme= ""
        self.DPS = 0
        self.tps_mise_en_oeuvre = 0
        self.portee = 0
        self.image = img_path


