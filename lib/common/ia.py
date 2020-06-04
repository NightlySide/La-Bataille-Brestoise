# Auteur : Alexandre FROEHLICH

import random

from lib.common.entite import Entite
from lib.common.vecteur import Vecteur
from lib.server.FSM import FSM, Etat
from lib.server.global_server_registry import GSR


class IA(Entite):
    """
    Classe héritée de Entite qui a pour particularité de possèder une FSM donc d'agir
    par états. Ce que nous appelerons ici "IA".

    Attributes:
        brain (FSM): cerveau qui controle les gestes de l'entité
    """

    def __init__(self):
        super().__init__()

        self.brain = FSM(self)

        # On ajoute les états au FSM
        self.brain.ajouter_etat("idle", Gambader(self))
        self.brain.ajouter_etat("follow", SuivreJoueur(self))

        # On programme un premier état pour le cerveau
        self.brain.prochain_etat = "idle"

    def update(self, delta):
        """
        Met à jour l'entité ainsi que son cerveau

        Args:
            delta (float): temps écoulé depuis la dernière mise à jour
        """
        self.brain.update()
        self.isDead()
        self.level_up()
        self.current_weapon.update()
        self.takeDamage(self.current_target, 1 / 30)

        # Si on est sur le serveur, on ne veut pas que le client déplace les entités
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
    """
    Etat "d'attente", l'IA se déplace aléatoirement dans ce cas.
    """
    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        """
        Mise à jour de l'état
        """
        # On se déplace aléaoirement une fois sur 4
        if random.random() < 1/4:
            vecteurs = [Vecteur(-1, 0), Vecteur(1, 0), Vecteur(0, -1), Vecteur(0, 1), Vecteur(0, 0)]
            self.parent.direction = random.choice(vecteurs)
            GSR.entities_to_update.append(self.parent)

        # On essaie de voir si un client n'est pas à portée
        for client in GSR.clients:
            diff = client.joueur.position - self.parent.position
            # Si un joueur est a portée
            if diff.distance() < 10:
                self.parent.current_target = client.joueur.id
                self.parent.brain.prochain_etat = "follow"
                self.en_vie = False
                break


class SuivreJoueur(Etat):
    """
    Etat définissant le comportement de suivi de l'entité
    """
    def __init__(self, parent):
        super().__init__(parent)

    def update(self):
        """
        Met à jour l'état
        """
        # On récupère la cible
        target = None
        for client in GSR.clients:
            if client.joueur.id == self.parent.target:
                target = client.joueur
                break
        # Si on a perdu la cible (déconnexion par exemple)
        if target is None:
            # On lui dit de gambader
            self.parent.target = None
            self.parent.brain.prochain_etat = "idle"
            self.en_vie = False
            return

        # Si la cible est trop loin
        diff = target.position - self.parent.position
        if diff.distance() > 20:
            # On arrête de la suivre
            self.parent.target = None
            self.parent.brain.prochain_etat = "idle"
            self.en_vie = False
            return
        self.parent.direction = diff.normaliser()

