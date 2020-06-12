# Auteur : Guillaume LEINEN

import os
import random
import time
from lib.common.armes import C50, Canon, CanonAutomatique,CanonSuperRapido,Rafale,Mistral,TorpilleLegere,TorpilleLourde, MM40
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QImage, QKeyEvent, QPaintEvent, QMouseEvent, QPen
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from lib.client.global_client_registry import GCR
from lib.common.carte import Carte
from lib.common.entite import Entite
from lib.common.joueur import Joueur
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur


class CanvasJeu(QLabel):
    """
    Canvas sur lequel on va venir dessiner toute la partie jeu, cela inclut la carte
    le joueur et les autres entités

    Args:
        parent (QWidget): (OPTIONNEL) le parent auquel rattacher
            la fenêtre.
        refresh_rate (float): la vitesse de rafraîchissement de l'écran pour avoir
            un framerate constant

    Attributes:
        time_counter (float): compteur permettant de relever le temps entre deux itérations
        refresh_rate (float): fréquence de rafraichissement de l'affichage
        last_key (PyQt5.QtCore.Qt.Key): dernière touche pressée, utile pour s'arrêter
    """

    def __init__(self, parent: QObject = None, refresh_rate: float = 1/30):
        super().__init__(parent)
        # On fixe la taille du canvas pour plus de simplicité
        self.setFixedSize(800, 600)
        # Variables nécessaires pour un rafraîchissement constant de l'image
        self.time_counter = time.perf_counter()
        self.refresh_rate = refresh_rate
        self.last_key = None
        #on ouvre le mediaplayer pour les tirs ( géré dans keypressevent)
        self.sound_player = QMediaPlayer()
        self.sound_player.setVolume(100)
        #on ouvre le mediaplayer pour le bruit de fond
        self.background_player = QMediaPlayer()
        self.background_player.setVolume(40)
        playlist = QMediaPlaylist(self.background_player)
        playlist.addMedia(QMediaContent(QUrl.fromLocalFile(os.path.join(os.getcwd(),"assets","sfx","ocean_waves.mp3"))))
        playlist.setPlaybackMode(QMediaPlaylist.Loop)
        self.background_player.setPlaylist(playlist)
        self.background_player.play()

    def keyPressEvent(self, e: QKeyEvent) -> None:
        """
        Fonction héritée de Qt qui permet de prendre en charge les évènements du type
        touche clavier.

        Args:
            e (PyQt5.QtGui.QKeyEvent): évènement de type touche de clavier
        """

        # Si on appuie sur Echap on veut fermer la fenètre de jeu
        if e.key() == Qt.Key_Escape:
            self.parent().parent().parent().close()
        # si c'est la touche espace on autorise ou non le tir
        elif e.key() == Qt.Key_Space:
            GCR.joueur.firing = not GCR.joueur.firing
            if GCR.joueur.firing:  #si tir on joue le son
                playlist = QMediaPlaylist(self.sound_player)
                url = None
                if type(GCR.joueur.current_weapon) in (CanonAutomatique, C50):
                    url = QUrl.fromLocalFile(os.path.join(os.getcwd(), "assets", "sfx", "canonauto.mp3"))
                elif type(GCR.joueur.current_weapon) in (Canon, CanonSuperRapido):
                    url = QUrl.fromLocalFile(os.path.join(os.getcwd(), "assets", "sfx", "large_gun.mp3"))
                elif type(GCR.joueur.current_weapon) in (Mistral, MM40, Rafale):
                    url = QUrl.fromLocalFile(os.path.join(os.getcwd(), "assets", "sfx", "missile.mp3"))
                elif type(GCR.joueur.current_weapon) in (TorpilleLourde, TorpilleLegere):
                    url = QUrl.fromLocalFile(os.path.join(os.getcwd(), "assets", "sfx", "sousmarin.mp3"))
                if url is not None:
                    playlist.addMedia(QMediaContent(url))
                    playlist.setPlaybackMode(QMediaPlaylist.Loop)
                    self.sound_player.setPlaylist(playlist)
                    self.sound_player.play()
            else:
                self.sound_player.stop()

            GCR.log.log(Logger.DEBUG, "Space")
        elif e.key() in [Qt.Key_Up, Qt.Key_Down, Qt.Key_Left, Qt.Key_Right]:
            # On crée un vecteur qui donnera la direction voulue par le joueur
            dir = Vecteur()
            if e.key() == Qt.Key_Left:
                GCR.log.log(Logger.DEBUG, "Flèche gauche")
                dir.x -= 1
            elif e.key() == Qt.Key_Right:
                GCR.log.log(Logger.DEBUG, "Flèche droite")
                dir.x += 1
            elif e.key() == Qt.Key_Up:
                GCR.log.log(Logger.DEBUG, "Flèche haut")
                dir.y -= 1
            elif e.key() == Qt.Key_Down:
                GCR.log.log(Logger.DEBUG, "Flèche bas")
                dir.y += 1

            # Si c'est une touche de déplacement on regarde si c'est pour arrêter le bateau
            if e.key() in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down] and e.key() == self.last_key:
                self.last_key = None
                dir = Vecteur()
            # Sinon on enregistre juste la touche
            elif e.key() in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down]:
                self.last_key = e.key()

            # On indique à l'entité joueur quelle est la direction à prendre
            GCR.joueur.direction = dir

    def paintEvent(self, e: QPaintEvent) -> None:
        """
        Fonction dérivée de Qt, qui est appelée à chaque fois qu'on rafraîchit l'écran.
        On va venir alors peindre sur le canvas.

        Args:
            e (PyQt5.QtGui.QPaintEvent): évènement du type peinture de l'écran
        """
        qp = QPainter(self)

        # On dessine la carte
        GCR.current_map.render(qp, (self.width(), self.height()))
        for entity in GCR.entities:
            # Si l'entité peut être affichée
            if GCR.current_map.can_player_see(entity, (self.width(), self.height())):
                dx = (entity.position.x - GCR.joueur.position.x) * GCR.current_map.cell_size[0] + self.width() // 2
                dy = (entity.position.y - GCR.joueur.position.y) * GCR.current_map.cell_size[1] + self.height() // 2
                entity.render(qp, dx, dy)
                # Si l'entité est la cible du joueur
                if GCR.joueur.current_target == entity.id:
                    entity.draw_target(qp, dx, dy)
                # Si l'entité est en train de tirer
                if entity.firing and entity.current_target is not None and random.randrange(0, 10) < 7:
                    pen = QPen(Qt.black)
                    pen.setStyle(Qt.DashLine)
                    qp.setPen(pen)
                    target = Entite.findById(entity.current_target, GCR.entities + [GCR.joueur])
                    tdx = (target.position.x - GCR.joueur.position.x) * GCR.current_map.cell_size[0] + self.width() // 2
                    tdy = (target.position.y - GCR.joueur.position.y) * GCR.current_map.cell_size[1] + self.height() // 2
                    qp.drawLine(dx, dy, tdx, tdy)
            else:
                # Si l'entité est hors champ alors elle n'est plus ciblée
                if GCR.joueur.current_target == entity.id:
                    GCR.joueur.current_target = None
                    GCR.joueur.firing = False
        if GCR.joueur.firing and GCR.joueur.current_target is not None and random.randrange(0, 10) < 7:
            pen = QPen(Qt.black)
            pen.setStyle(Qt.DashLine)
            qp.setPen(pen)
            target = Entite.findById(GCR.joueur.current_target, GCR.entities + [GCR.joueur])
            dx = (target.position.x - GCR.joueur.position.x) * GCR.current_map.cell_size[0] + self.width() // 2
            dy = (target.position.y - GCR.joueur.position.y) * GCR.current_map.cell_size[1] + self.height() // 2
            qp.drawLine(self.width() // 2, self.height() // 2, dx, dy)

        # On vient dessiner le joueur par dessus la carte
        GCR.joueur.render(qp, self.width() // 2, self.height() // 2)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """
        Fonction dérivée de Qt, qui est appelée à chaque fois que la souris
        est bougée sur le canvas

        Args:
            e (PyQt5.QtGui.QMouseEvent): évènement du type déplacement de souris
        """
        # On récupère la position de la souris sur l'écran
        x = e.x()
        y = e.y()
        wx, wy = mouseToWorldPosition(x, y)
        text = "Mouse x: {},  y: {} | World position x: {}, y: {}".format(x, y, wx, wy)
        self.parent().parent().parent().setWindowTitle(text)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """
        Fonction dérivée de Qt, qui est appelée à chaque fois qu'un
        bouton de la souris est pressé

        Args:
            e (PyQt5.QtGui.QMouseEvent): évènement du type souris
        """
        x, y = mouseToWorldPosition(e.x(), e.y())
        GCR.log.log(Logger.DEBUG, f"Click à la pos : ({x}, {y})")
        # On met le focus sur le canvas pour récupérer les autres évènements ici
        self.setFocus()
        for e in GCR.entities:
            # Si l'entité n'est pas le joueur on peut cibler
            if e != GCR.joueur:
                diff = Vecteur(x, y) - e.position
                distance = diff.distance()
                # Si le click est proche d'une cible
                if distance < max(e.size[0], e.size[1]) // (8*2) * 1.5:
                    GCR.joueur.ciblage(e)
                    GCR.log.log(Logger.DEBUG, f"Nouvelle cible : {e}")
                    break
        # Sinon le click est trop loin d'une cible, on déselectionne
        else:
            GCR.joueur.ciblage(None)

    def update(self) -> None:
        """
        Fonction appelée pour rafraîchir le canvas. C'est cette fonction
        qui va venir limiter le nombre d'appels de manière à avoir un
        taux de rafraîchissement de la surface constant.
        Cette fonction est une surcharge des fonctions implémentées par Qt.
        """
        # Si on peut rafraichir l'écran
        if self.time_counter - time.perf_counter() < self.refresh_rate:
            self.time_counter = time.perf_counter()
            super().update()
            GCR.getTcpClient().send({
                        "action": "update_player",
                        "user": GCR.getTcpClient().id,
                        "data": GCR.joueur})


def mouseToWorldPosition(mouse_x: int, mouse_y: int) -> (int, int):
    """
    Fonction outil permettant de transformer la position de la souris à l'écran
    en position dans le monde du jeu.

    Args:
        mouse_x (int): position en X de la souris sur l'écran
        mouse_y (int): position en Y de la souris sur l'écran

    Returns:
        world_pos (int, int): tuple contenant la position de la souris dans le monde

    """
    # On récupère la position du joueur
    x0, y0 = GCR.joueur.position.x, GCR.joueur.position.y
    dx = (mouse_x - 800 // 2) // 8
    dy = (mouse_y - 600 // 2) // 8
    # On retourne la position dans le monde
    return int(x0 + dx), int(y0 + dy)
