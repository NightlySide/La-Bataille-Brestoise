import time

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QImage
from random import randint

import lib
from lib.client.global_client_registry import GCR


class Arme:

    def __init__(self, parent, refresh_rate=1):
        self.parent = parent
        self.nom_arme= ""
        self.DPS = 0
        self.tps_mise_en_oeuvre = 0
        self.portee = 0
        self.image = "assets\images\armes\C5O.png"
        self._tps_equip_timer = 0
        self.can_fire = False

    def first_equip(self):
        self._tps_equip_timer = time.perf_counter()
        if isinstance(self.parent, lib.common.joueur.Joueur) and GCR.joueur.id == self.parent.id:
            GCR.chatbox.add_line(f"[+] L'arme est en cours d'équipement")

    def fire(self):
        if self.can_fire:
            pass

    def update(self):
        if not self.can_fire:
            if time.perf_counter() - self._tps_equip_timer > self.tps_mise_en_oeuvre:
                self.can_fire = True
                # On vérifie qu'on soit bien du côté client et uniquement chez le joueur actuel
                if isinstance(self.parent, lib.common.joueur.Joueur) and GCR.joueur.id == self.parent.id:
                    GCR.chatbox.add_line(f"[+] {self.nom_arme} est équipée")
