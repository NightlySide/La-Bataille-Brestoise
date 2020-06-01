from PyQt5.QtCore import QRect, QPoint, Qt
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter, QColor, QBrush, QPen
from uuid import uuid4
from random import randint

from lib.client.global_client_registry import GCR
from lib.common.armes.arme import Arme
from lib.common.batiments.batiment import Batiment
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur
import time

class Entite:
    """
    Definition d'une entité du jeu.

    Attributes:
        vie (int): vie de l'entité
        vitesse (int): vitesse de déplacement de l'unité
        image (QImage): image de référence de l'entité
        position (Vecteur): position du joueur
        direction (Vecteur): direction vers lequel se dirige le joueur
        current_ship(batiment) : batiment actuellement manoeuvré par le joueur
        current_weapon(arme) : arme actuellement équipé par le joueur
        current_target(entite) : entité actuellement visée par le joueur

    """
    exp_treashold = [1000,5000,10000,40000] #pallier d'experience pour passer un niveau
    exp_win = 100000
    taux_exp_gain = 0.5
    exp_boost = 1000

    def __init__(self):
        self.vie = 20
        self.vitesse = 1
        self.image = None
        self.position = Vecteur(200, 200)
        self.direction = Vecteur()
        self.image_direction = self.direction
        self.current_ship = Batiment()
        self.current_weapon = Arme()
        self.current_target = None
        self.id = uuid4()
        self.exp = 0
        self.size = (16, 16)

    def set_image(self, img_path):
        """
        Affecte une image à l'entité.

        Args:
            img_path (str): chemin d'accès relatif à l'image
        """
        self.image = img_path

    def is_alive(self):
        """
        Vérifie si l'entité est encore en vie.
        """
        return self.vie > 0

    def render(self, qp, x, y):
        """
        Fait le rendu de l'entité sur l'écran à l'aide du painter de
        ce dernier.

        Args:
            qp (QPainter): painter de la surface sur laquelle dessiner
        """
        # Si on a définit une image on la dessine
        if self.image is not None:
            img = QPixmap(self.image)
            if self.image_direction.equal(Vecteur(0.0, 1.0)): # direction sud
                rotation = 180
            elif self.image_direction.equal(Vecteur(1.0, 0.0)): # direction est
                rotation = 90
            elif self.image_direction.equal(Vecteur(-1.0, 0.0)): # direction ouest
                rotation = 270
            else: # direction nord
                rotation = 0
            img_rotated = img.transformed(QTransform().rotate(rotation))
            #xoffset = (img_rotated.width() - img.width()) / 2
            #yoffset = (img_rotated.height() - img.height()) / 2
            #img_rotated = img_rotated.copy(xoffset, yoffset, img.width(), img.height())
            img_rot_scal = img_rotated.scaled(*self.size)
            qp.drawPixmap(QPoint(x - self.size[0] // 2, y - self.size[1] // 2), img_rot_scal)
            self.draw_life_bar(qp, x, y)

    def draw_life_bar(self, qp:QPainter, x, y):
        bar_size = (40, 4)

        # On dessine le carré rouge
        pen = QPen(Qt.black)
        qp.setPen(pen)
        qp.setBrush(QColor(125, 125, 125))
        qp.drawRect(x - bar_size[0] // 2, y - self.size[1] // 2 - 10, *bar_size)

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
        life_size = bar_size[0] * self.vie / self.current_ship.hitpoints
        qp.drawRect(1 + x - bar_size[0] // 2, 1 + y - self.size[1] // 2 - 10, life_size - 2, bar_size[1] - 2)

    def draw_target(self, qp:QPainter, x, y):
        tar_length = 10
        tar_width = 2
        pen = QPen(Qt.red)
        pen.setWidth(tar_width)
        qp.setBrush(QColor(255, 255, 255, 0))
        qp.setPen(pen)
        qp.drawRect(x - self.size[0] // 2, y - self.size[1] // 2, *self.size)

    def __str__(self):
        return f"Entité ({self.id}) : position ({self.position.x}, {self.position.y}), vie : {self.vie}"

    def update(self, delta):
        self.position += self.direction * self.vitesse
        # On retient la dernière direction prise par le bateau
        if not self.direction.equal(Vecteur(0.0, 0.0)):
            self.image_direction = self.direction
        #self.direction = Vecteur()

    def ciblage(self, entite):
        if entite is None:
            self.current_target = None
        else:
            self.current_target = entite.id

    @staticmethod
    def findById(e_id, entities):
        for e in entities:
            if e.id == e_id:
                return e
        return None

    def spawnShip(self, shipname):
        """
        permet de générer un nouveau batiment au joueur, si il meurt ou si il monte de niveau
        Args:
            shipname: chaine de caractère identifiant le navire à générer

        Returns:

        """
        self.current_ship = shipname
        self.current_weapon = self.current_ship.armes[0]
        self.vie = self.current_ship.hitpoints
        if self.vitesse >= self.current_ship.vmax:
            self.vitesse = self.current_ship.vmax

    def level_up(self):
        """
        fonction testant la montée de niveau à chaque tour. le joueur passe au niveau superieur
        si l'experience  est supérieure à des paliers de niveau (définis dans exp_treashold).
        le test est exécuté dans le gameloop.
        Returns:
            nothing

        """
        for i in range(0,4) :
            if self.exp > Entite.exp_treashold[i] and self.current_ship.tier == i+1 :
                #le joueur passe au niveau superieur
                tier = self.current_ship.tier
                taille = len(Batiment.Tierlist[tier])
                self.spawnShip(Batiment.Tierlist[tier][randint(0, taille - 1)])
#TODO : a implementer dans le gameloop

    def isDead(self):
        """
        test si le joueur à encore assez de points de vie. si les points de vie sont à 0,
        le joueur respawn dans un navire du tier inferieur, l'exp est reset au treashold du tier inferieur
        Returns:

        """
        #TODO : afficher un pop up Qwidget signifiant la mort au joueur
        if self.vie == 0 :
            if self.tier < 3 :
                self.spawnShip(Batiment.Tierlist[1][randint(0, 1)])
                self.exp = 0
            else :
                tier = self.current_ship.tier
                taille = len(Batiment.Tierlist[tier-1])
                self.spawnShip(Batiment.Tierlist[tier-1][randint(0, taille - 1)])
                self.exp = Entite.exp_treashold[self.current_ship.tier-2]

    def isWinning(self):
        """
        fonction testant si le joueur à gagné ou non, en comparant l'exp à la valeur exp_win
        Returns:
        nothing

        """
        if self.exp >= Entite.exp_win :
            return True
        else :
            return False
#TODO : à implementer dans le gameloop

    def takeDamage(self, entiteEnnemie, refresh_rate):
        """
        fonction implementant les dégats infligés à une entite. Elle test si le joueur à encore
        assez de PV, sinon elle provoque le Respawn. l'EXP gagné par le joueur ennemie est proportionnel au dégats infligés.
        le joueur obtient un boost d'XP proportionnel à son tier en cas de frag ( IE il tue un ennemi).
        Args:
            entiteEnnemie: entite ennemie qui inflige les dégats

        Returns:
            nothing
        """
        degats = entiteEnnemie.current_weapon.DPS // refresh_rate
        if self.vie - degats < 0 :
            entiteEnnemie.exp += ( Entite.taux_exp_gain * degats ) + Entite.exp_boost * entiteEnnemie.current_ship.tier
            self.vie = 0
            self.isDead()
        else :
            self.vie = self.vie - degats
            entiteEnnemie.exp += Entite.taux_exp_gain * degats

    def equiper(self):
        """
        permet à un joueur d'équiper une arme. Elle sert à attendre un délai de mise en oeuvre d'une arme avant de pouvoir tirer.
        plus l'arme est importante et plus son temps d'équipement est grand. une arme de conception plus récente aura un temps d'équipement plus court.
        Les valeurs précises sont trouvables dans le tableau d'équillibrage.

        Args:
            self: objet arme

        """
        t0 = time.perf_counter()
        t=t0
        if t > t0 + self.tps_mise_en_oeuvre :
            print("équippement de l'arme : ", self.nom_arme)
        #TODO roue d'equipmment des armes ( pie menu )