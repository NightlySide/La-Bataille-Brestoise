import pickle
import random

from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter, QColor, QBrush, QPen
from uuid import uuid4
from random import randint

from lib.client.global_client_registry import GCR
from lib.common.armes.arme import Arme
from lib.common.batiments import PA, AVISO, CMT, BE, BIN, BH, FS, F70, FREMM, FDA, SNA, SNLE
from lib.common.batiments import Batiment
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur
import time

from lib.server.global_server_registry import GSR


class Entite:
    """
    Definition d'une entité du jeu.

    Attributes:
        vie (int): vie de l'entité
        vitesse (int): vitesse de déplacement de l'unité
        image (str): chemin vers l'image de référence de l'entité
        position (Vecteur): position du joueur
        direction (Vecteur): direction vers lequel se dirige le joueur
        image_direction (Vecteur): direction vers laquelle l'image doit être tournée
        current_ship(batiment) : batiment actuellement manoeuvré par l'entité
        current_weapon(arme) : arme actuellement équipé par l'entité
        current_target(entite) : entité actuellement visée par l'entité
        id (str): identifiant unique attribué à l'entité
        exp (float): expérience actuelle de l'entité
        size (list): taille de l'image de l'entité
    """
    # palier d'experience pour passer au niveau suivant
    exp_treshold = [1000, 3000, 8000, 24000]
    # expérience nécessaire pour gagner
    exp_win = 50000
    # Modificateur d'expérience gagnée
    taux_exp_gain = 0.1
    exp_boost = 100
    #liste des batiments par tier
    Tierlist = [[BE, BIN], [AVISO, CMT, BH], [FS, F70], [FREMM, FDA, SNA], [PA, SNLE]]
    def __init__(self):

        self.image = None
        self.position = Vecteur(200, 200)
        self.direction = Vecteur()
        self.image_direction = self.direction
        self.current_ship = None
        self.vie = 20
        self.current_weapon = None
        self.vitesse = None
        self.current_target = None
        self.id = uuid4()
        self.exp = 0
        self.size = (16, 16)
        self.firing = False

        self.spawnShip(random.choice(Entite.Tierlist[0]))

    def set_image(self, img_path: str) -> None:
        """
        Affecte une image à l'entité.

        Args:
            img_path (str): chemin d'accès relatif à l'image
        """
        self.image = img_path

    def is_alive(self) -> bool:
        """
        Vérifie si l'entité est encore en vie.

        Returns:
            is_alive (bool): si l'entité est encore en vie
        """
        return self.vie > 0

    def render(self, qp: QPainter, x: float, y: float) -> None:
        """
        Fait le rendu de l'entité sur l'écran à l'aide du painter de
        ce dernier.

        Args:
            qp (QPainter): painter de la surface sur laquelle dessiner
            x (float): position X du milieu de l'entité par rapport au joueur
            y (float): position Y du milieu de l'entité par rapport au joueur
        """
        # Si on a définit une image on la dessine
        if self.image is not None:
            img = QPixmap(self.image)
            if self.image_direction.equal(Vecteur(0.0, 1.0)):  # direction sud
                rotation = 180
            elif self.image_direction.equal(Vecteur(1.0, 0.0)):  # direction est
                rotation = 90
            elif self.image_direction.equal(Vecteur(-1.0, 0.0)):  # direction ouest
                rotation = 270
            else:  # direction nord
                rotation = 0
            img_rotated = img.transformed(QTransform().rotate(rotation))
            # xoffset = (img_rotated.width() - img.width()) / 2
            # yoffset = (img_rotated.height() - img.height()) / 2
            # img_rotated = img_rotated.copy(xoffset, yoffset, img.width(), img.height())
            img_rot_scal = img_rotated.scaled(*self.size)
            qp.drawPixmap(QPoint(x - self.size[0] // 2, y - self.size[1] // 2), img_rot_scal)
            self.draw_life_bar(qp, x, y)

    def draw_life_bar(self, qp: QPainter, x: float, y: float) -> None:
        """
        Fait le rendu de la barre de vie de l'entité à l'aide du painter de l'écran

        Args:
            qp (QPainter): painter de la surface sur laquelle dessiner
            x (float): position X du milieu de l'entité par rapport au joueur
            y (float): position Y du milieu de l'entité par rapport au joueur
        """
        bar_size = (40, 4)
        text_size = 12

        # On dessine le carré rouge
        pen = QPen(Qt.black)
        qp.setPen(pen)
        qp.setBrush(QColor(125, 125, 125))
        qp.drawRect(x - bar_size[0] // 2 + text_size - 2,
                    y - self.size[1] // 2 - 10,
                    bar_size[0] - text_size,
                    bar_size[1])

        # On dessine le carré vert
        life_col = QColor(0, 255, 0)
        enemy_col = QColor(255, 0, 0)
        pen = None
        if self.id == GCR.joueur.id:
            qp.setBrush(life_col)
            pen = QPen(life_col)
        else:
            qp.setBrush(enemy_col)
            pen = QPen(enemy_col)
        qp.setPen(pen)
        life_size = (bar_size[0] - text_size) * self.vie / self.current_ship.hitpoints
        qp.drawRect(1 + x - bar_size[0] // 2 + text_size - 2,
                    1 + y - self.size[1] // 2 - 10,
                    life_size - 2,
                    bar_size[1] - 2)

        # On dessine le tier du bâtiment
        tier = self.current_ship.tier
        qp.setPen(QPen(Qt.white))
        qp.drawText(QRect(x - bar_size[0] // 2,
                          y - self.size[1] // 2 - 10 - text_size // 2,
                          text_size,
                          text_size), 0, str(tier))

    def draw_target(self, qp: QPainter, x: float, y: float, tar_width: int = 2) -> None:
        """
        Fait le rendu du contour lors du ciblage de l'entité à l'aide du painter
        de l'écran.

        Args:
            qp (QPainter): painter de la surface sur laquelle dessiner
            x (float): position X du milieu de l'entité par rapport au joueur
            y (float): position Y du milieu de l'entité par rapport au joueur
            tar_width (int): épaisseur du trait lors du dessin de la cible

        Returns:

        """
        pen = QPen(Qt.red)
        pen.setWidth(tar_width)
        # On cherche à avoir le fond transparent pour ne garder que le contour
        qp.setBrush(QColor(255, 255, 255, 0))
        qp.setPen(pen)
        qp.drawRect(x - self.size[0] // 2, y - self.size[1] // 2, *self.size)

    def __str__(self) -> str:
        """
        Retourne la représentation de l'entité
        """
        return f"Entité ({self.id}) : position ({self.position.x}, {self.position.y}), vie : {self.vie}"

    def update(self, delta: float) -> None:
        """
        Met à jour les éléments essentiels au fonctionnement de l'entité comme sa position
        ou bien sa direction.
        Le déplacement sera à implémenter du coté client (joueur) ou serveur (entite).

        Args:
            delta (float): temps mis entre l'itération précédente et l'itération actuelle
        """
        self.isDead()
        self.level_up()
        self.current_weapon.update()
        self.takeDamage(self.current_target, 1 / 30)
        self.position += self.direction * self.vitesse
        # On retient la dernière direction prise par le bateau
        if not self.direction.equal(Vecteur(0.0, 0.0)):
            self.image_direction = self.direction
        # self.direction = Vecteur()

    def ciblage(self, entite: "Entite") -> None:
        """
        Permet de définir une cible pour l'attaque notamment.
        La référence à la cibles est l'identifiant unique.

        Args:
            entite (Entite): l'entité à cibler, doit posséder un uuid
        """
        if entite is None:
            self.current_target = None
        else:
            self.current_target = entite.id

    @staticmethod
    def findById(e_id: str, entities: list) -> "Entite":
        """
        Methode outil pour trouver une entité à partir de son
        identifiant dans une liste donnée.

        Args:
            e_id (str): identifiant de l'entité à trouver
            entities (list): liste des entités dans laquelle chercher
        """
        for e in entities:
            if e.id == e_id:
                return e
        return None

    def spawnShip(self, ship: Batiment) -> None:
        """
        Permet de générer un nouveau batiment au joueur par exemple
        quand il meurt ou bien si il monte de niveau

        Args:
            ship (Batiment): bâtiment à générer
        """
        self.current_ship = ship()
        self.set_image(self.current_ship.imgpath)
        self.size = self.current_ship.size
        self.current_weapon = self.current_ship.armes[0](self)
        self.vie = self.current_ship.hitpoints
        self.vitesse = self.current_ship.vmax

    def level_up(self) -> None:
        """
        Fonction testant la montée de niveau à chaque tour. Le joueur passe au niveau superieur
        si l'experience est supérieure à un des paliers de niveau (définis dans exp_treshold).
        le test est exécuté dans le gameloop.
        """
        for i in range(0, 4):
            if self.exp > Entite.exp_treshold[i] and self.current_ship.tier == i + 1:
                # le joueur passe au niveau superieur
                tier = self.current_ship.tier
                self.spawnShip(random.choice(Entite.Tierlist[tier]))

                # Si on est du côté client
                if GCR.joueur is not None:
                    GCR.chatbox.add_line(f"[+] Vous avez monté au niveau {self.current_ship.tier} !")
                    GCR.chatbox.add_line(f"[+] Vous avez obtenu le bâtiment : {self.current_ship.nom_unite} !")
                break

    # TODO : a implementer dans le gameloop

    def isDead(self) -> None:
        """
        Test si le joueur à encore assez de points de vie. si les points de vie sont à 0,
        le joueur respawn dans un navire du tier inferieur, l'exp est reset au treshold du tier inferieur
        """

        if self.vie <= 0:
            if self.current_ship.tier < 3:
                self.spawnShip(random.choice(Entite.Tierlist[0]))
                self.exp = 0
            else:
                self.spawnShip(random.choice(Entite.Tierlist[self.current_ship.tier - 1]))
                self.exp = Entite.exp_treshold[self.current_ship.tier - 2]

            # L'entité ou joueur respawn dans un endroit aléatoire pour éviter le respawnkill
            carte = GCR.current_map if GCR.current_map is not None else GSR.carte
            x = y = -1
            while GSR.carte.is_colliding(x, y):
                x = random.randint(0, carte.shape[0])
                y = random.randint(0, carte.shape[1])
            self.position = Vecteur(x, y)

    def isWinning(self) -> bool:
        """
        Fonction testant si le joueur à gagné ou non, en comparant l'exp à la valeur exp_win

        Returns:
            isWinning (bool): le joueur à gagné ou non
        """
        if self.exp >= Entite.exp_win:
            return True
        else:
            return False

    # TODO : à implementer dans le gameloop

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
            if GCR.entities:
                #entite_ennemie = self.findById(target_id, GCR.entities)
                GCR.tcp_client.send({"action": "damage", "attacker": self.id, "target": target_id})
            # On est bien côté serveur
            else :
                entite_ennemie = self.findById(target_id, GSR.entities)
                if entite_ennemie == None :
                    return
                degats = self.current_weapon.DPS * refresh_rate
                exp = 0
                if entite_ennemie.vie - degats < 0:
                    exp += Entite.exp_boost * self.current_ship.tier ** 2
                    entite_ennemie.vie = 0
                else:
                    entite_ennemie.vie = entite_ennemie.vie - degats
                for client in GSR.clients:
                    if client.joueur.id == self.id:
                        exp += (Entite.taux_exp_gain * degats)
                        client.transport.write(pickle.dumps({"action": "gain_exp",
                                                             "exp": exp}))
                        break
                else:
                    GSR.log.log(Logger.ERREUR, f"Joueur {self.id} non trouvé !")




    def equiper(self, arme: Arme):
        """
        Permet à un joueur d'équiper une arme. Elle sert à attendre un délai de mise en oeuvre d'une arme avant de
        pouvoir tirer.
        Plus l'arme est importante et plus son temps d'équipement est grand. Une arme de conception plus récente
        aura un temps d'équipement plus court.
        Les valeurs précises sont disponibles dans le tableau d'équillibrage.

        Args:
            arme (Arme): l'arme à équiper

        """

        self.current_weapon = arme
        self.current_weapon.first_equip()
        # TODO roue d'equipmment des armes ( pie menu )

