import random

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
        self.brain.ajouter_etat("idle", Gambader(self))
        self.brain.ajouter_etat("follow", SuivreJoueur(self))

        # On programme un premier état pour le cerveau
        self.brain.prochain_etat = "idle"

    def update(self, delta):
        self.brain.update()
        self.isDead()
        self.level_up()
        self.current_weapon.update()
        self.takeDamage(self.current_target, 1 / 30)

        if GSR.carte is not None:
            new_position = (self.position + self.direction * self.vitesse)
            # Si il n'y a pas de collision avec la map
            if not GSR.carte.is_colliding(int(new_position.x), int(new_position.y)):
                self.position += self.direction * self.vitesse
            # Si il y en a
            else:
                self.direction = Vecteur()
        # On retient la dernière direction prise par le bateau
        if not self.direction.equal(Vecteur(0.0, 0.0)):
            self.image_direction = self.direction

    def __str__(self):
        return f"I.A. ({self.id}) : position ({self.position.x}, {self.position.y}), vie : {self.vie}\n" \
               f"Etats : {list(self.brain.etats.keys())}"


class Gambader(Etat):

    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        if random.random() < 1/4:
            vecteurs = [Vecteur(-1, 0), Vecteur(1, 0), Vecteur(0, -1), Vecteur(0, 1), Vecteur(0, 0)]
            self.parent.direction = random.choice(vecteurs)
            GSR.entities_to_update.append(self.parent)

        # On essaie de voir si un client n'est pas à portée
        for client in GSR.clients:
            diff = client.joueur.position - self.parent.position
            if diff.distance() < 10:
                self.parent.target = client.joueur.id
                self.parent.brain.prochain_etat = "follow"
                self.en_vie = False
                break


class SuivreJoueur(Etat):

    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        target = None
        for client in GSR.clients:
            if client.joueur.id == self.parent.target:
                target = client.joueur
                break
        if target is None:
            self.parent.target = None
            self.parent.brain.prochain_etat = "idle"
            self.en_vie = False
            return

        diff = target.position - self.parent.position
        if diff.distance() > 20:
            self.parent.target = None
            self.parent.brain.prochain_etat = "idle"
            self.en_vie = False
            return
        self.parent.direction = diff.normaliser()

