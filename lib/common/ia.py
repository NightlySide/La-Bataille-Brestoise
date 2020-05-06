from random import random

from lib.common.entite import Entite
from lib.common.vecteur import Vecteur
from lib.server.FSM import FSM, Etat
from lib.server.global_server_registry import GSR


class IA(Entite):

    def __init__(self):
        super().__init__()

        self.target = None
        self.brain = FSM(self)

        # On ajoute les états au FSM
        self.brain.ajouter_etat("idle", Gambader())
        self.brain.ajouter_etat("follow", SuivreJoueur())

    def update(self, delta):
        self.brain.update()

    def __str__(self):
        return f"I.A. ({self.id}) : position ({self.position.x}, {self.position.y}), vie : {self.vie}\n" \
               f"Etats : {list(self.brain.etats.keys())}"


class Gambader(Etat):

    def __init__(self):
        super().__init__()

    def update(self):
        if random.random() < 0.005:
            vecteurs = [Vecteur(-1, 0), Vecteur(1, 0), Vecteur(0, -1), Vecteur(0, 1), Vecteur(0, 0)]
            self.parent.direction = random.choice(vecteurs)
            GSR.entities_to_update.append(self.parent)


class SuivreJoueur(Etat):

    def __init__(self):
        super().__init__()

    def update(self):
        if self.parent.target is None:
            self.en_vie = False
