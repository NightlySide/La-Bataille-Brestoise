# Auteur : Guillaume LEINEN
import pickle

from lib.common.entite import Entite
from lib.client.global_client_registry import GCR
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur
from lib.server.global_server_registry import GSR


class Joueur(Entite):
    """
    Définition d'un joueur par héritage d'une entite ( comprendre Joueur = Entité humaine)

    Attributes:
        detection_radius(int): distance de détection en cases
    """
    def __init__(self, position: Vecteur):
        super().__init__()
        self.position = position
        self.detection_radius = 10 # en cases

    def update(self, delta: float) -> None:
        """
        Met à jour les éléments essentiels au fonctionnement de l'entité comme sa position
        ou bien sa direction.

        Args:
            delta (float): temps mis entre l'itération précédente et l'itération actuelle, ce temps est cruciale dans les performances du programme
        """
        #test de mort ou du montée de niveau
        self.isDead()
        self.level_up()
        #on vérifie que l'arme est bien équipé
        self.current_weapon.update()
        #on interroge la fonction takeDamage pour effectuer ou non des dégats
        self.takeDamage(self.current_target, 1 / 30)
        #maj de la position
        self.position += self.direction * self.vitesse
        if GCR.current_map is not None:
            new_position = (self.position + self.direction * self.vitesse)
            # Si il n'y a pas de collision avec la map
            if not GCR.current_map.is_colliding(int(new_position.x), int(new_position.y)):
                self.position += self.direction * self.vitesse
            # Si il y en a
            else:
                self.direction = Vecteur()
        if not self.direction.equal(Vecteur(0.0, 0.0)):
            self.image_direction = self.direction

    def isDead(self) -> None:
        """
        Test si le joueur à encore assez de points de vie. si les points de vie sont à 0,
        le joueur respawn dans un navire du tier inferieur, l'exp est reset au threshold du tier inferieur
        """
        if self.vie <= 0 and GCR.chatbox is not None:
            #la surcharge de la fonction est nécessaire pour afficher un message dans le chat (un bot ne peut pas ecrire dans le chat car il n'est pas relié à un client)
            GCR.chatbox.add_line(f"Vous êtes mort, respawn au tier inferieur")
        super().isDead()

    def takeDamage(self, target_id: str, refresh_rate: float) -> None:
        """
        Fonction implementant les dégats infligés à une entite si la touche espace à été pressé. Elle test si le joueur à encore
        assez de PV, sinon elle provoque le Respawn. l'EXP gagné par le joueur ennemi est proportionnel au dégats infligés.
        le joueur obtient un boost d'XP proportionnel à son tier en cas de frag ( IE il tue un ennemi).

        Args:
            entite_ennemie (Entite): entite ennemie qui inflige les dégats
            refresh_rate (float): fréquence de rafraichissement du jeu
        """
        if self.firing:
            # Géré niveau client
            if GCR.joueur is not None:
                #entite_ennemie = self.findById(target_id, GCR.entities)
                GCR.tcp_client.send({"action": "damage", "attacker": self.id, "target": target_id})
            # On est bien côté serveur
            else :
                entite_ennemie = self.findById(target_id, GSR.entities + [client.joueur for client in GSR.clients])
                if entite_ennemie == None :
                    return
                degats = self.current_weapon.DPS * refresh_rate
                exp = 0
                if entite_ennemie.vie - degats < 0:
                    exp += Entite.exp_boost * self.current_ship.tier ** 2
                    entite_ennemie.vie = 0
                else:
                    entite_ennemie.vie = entite_ennemie.vie - degats
                # Si c'est un joueur
                for client in GSR.clients:
                    if client.joueur.id == self.id:
                        exp += (Entite.taux_exp_gain * degats)
                        client.transport.write(pickle.dumps({"action": "gain_exp",
                                                             "exp": exp}))
                        break
                else:
                    GSR.log.log(Logger.ERREUR, f"Joueur {self.id} non trouvé !")