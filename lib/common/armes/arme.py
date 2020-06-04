# Auteur : Guillaume LEINEN

import time

import lib
from lib.client.global_client_registry import GCR


class Arme:
    """
    La classe Arme définit une unité d'armement d'un batiment. Un batiment peut posseder plusieurs types d'armement.


    Attributes:
        parent(batiment) : parent d'une arme
        nom_arme(str) : le nom de l'arme affiché dans le chat suite à son equipement sur un batiment
        DPS(int) : Dégats par seconde infligés par l'arme
        tps_mise_en_oeuvre(int) : temps en seconde d'équipement d'une arme par un joueur
        portee(int) : portee de tir d'une arme
        image(str) : Path vers le fichier image correspondant à l'arme (pour le QtPieChart)
        _tps_equip_timer(int) : timer du temps d'equipement
        can_fire(bool) : autorisation de tir d'une arme (lié au compteur du temps d'equipement )

    """


    def __init__(self, parent,  refresh_rate=1):
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
