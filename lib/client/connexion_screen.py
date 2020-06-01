from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QUrl, QObject
from PyQt5 import uic
import asyncio
from lib.client.tcp_client import TCPClientProtocol
from lib.client.game_screen import EcranJeu
from lib.client.global_client_registry import GCR
from threading import Thread

import os, sys

from lib.common.json_loader import JsonLoader
from lib.common.logger import Logger


class EcranConnexion(QMainWindow):
    """
    Fenêtre de connexion au serveur de jeu. Permet à l'utilisateur
    de choisir un pseudo pour sa partie, de sélectionner un serveur
    disponible ou d'en ajouter un.

    Args:
        parent (QWidget): (OPTIONNEL) le parent auquel rattacher
            la fenêtre.

    Attributes:
        game (QMainWindow): la fenêtre de jeu qui s'ouvrira
            une fois connecté.
        logo (QLabel): référence au logo affiché sur l'écran
        btn_connect (QPushButton): bouton de connexion au serveur
            sélectionné dans la liste
        btn_local (QPushButton): bouton pour entrer manuellement
            les informations de connexion au serveur
        server_list (QListWidget): liste des serveurs enregistrés
        input_username (QLineEdit): pseudo du joueur, devient 'Anonyme'
            si la case est laissée vide
    """
    def __init__(self,  parent: QObject = None):
        super().__init__(parent)
        self.game = None
        uic.loadUi('assets/ecran_connexion.ui', self)

        # On cherche les éléments
        self.logo = self.findChild(QLabel, 'logo')
        self.btn_connect = self.findChild(QPushButton, 'btn_connect')
        self.btn_add_server = self.findChild(QPushButton, 'btn_add_server')
        self.server_list = self.findChild(QListWidget, 'server_list')
        self.input_username = self.findChild(QLineEdit, 'input_username')

        # On connecte les boutons aux méthodes
        self.btn_connect.clicked.connect(self.connect_from_list)
        self.btn_add_server.clicked.connect(self.add_server)
        self.server_list.itemDoubleClicked.connect(self.connect_from_list)

        self.setWindowTitle("La Bataille Brestoise - Alexandre F. & Guillaume L.")

        # On créer un widget vidéo et on place notre vidéo en lecture
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget(self.logo)
        self.logo.setFixedSize(800, int(9/16 * 800))
        self.videoWidget.setFixedSize(800, int(9/16 * 800))
        app_root = os.path.abspath(os.path.dirname(sys.argv[0]))
        movie_path = os.path.join(app_root, "assets", "background_video.mp4")
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(movie_path)))
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.play()

        # On paramètre la liste des serveurs
        liste_serveurs = JsonLoader("known_servers.json")["server_list"]
        if len(liste_serveurs) == 0:
            self.add_server()
        else:
            self.refresh_server_list()

    def refresh_server_list(self) -> None:
        """
        Recupère la liste des serveurs enregistrés et l'enregistre dans la liste
        """
        self.server_list.clear()
        # On paramètre la liste des serveurs
        liste_serveurs = JsonLoader("known_servers.json")["server_list"]
        for server in liste_serveurs:
            self.server_list.addItem(QListWidgetItem(f"{server['name']} | {server['ip']} | {server['port']}"))
        self.server_list.setCurrentRow(0)

    def connect_from_list(self) -> None:
        """
        Appelée lorsque l'utilisateur clique sur le bouton 'Connecter'
        Se connecter à partir d'un serveur enregistré
        """
        nom, ip, port = self.server_list.currentItem().text().split(" | ")
        # On se connecte
        self.connect(nom, ip, port)

    def add_server(self) -> None:
        """
        Appelée lorsque l'utilisateur clique sur le bouton 'Connexion locale'
        Ouvre la boite de dialogue correspondante
        """
        reponse = LocalServerDialog.get_local_server_addr()
        # On a cliqué sur cancel
        if reponse is None:
            return
        else:
            nom, ip, port = reponse
            liste_serveurs = JsonLoader("known_servers.json")
            liste_serveurs["server_list"].append({"name": nom, "ip": ip, "port": int(port)})
            liste_serveurs.write()
            self.refresh_server_list()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Fonction héritée de Qt qui permet de prendre en charge les évènements du type
        touche clavier.

        Args:
            event (QKeyEvent): évènement de type touche de clavier
        """
        if event.key() == Qt.Key_Escape:
            self.close()

    def connect(self, nom: str, ip: str, port: int) -> None:
        """
        Appelée finalement pour se connecter au serveur et ouvrir
        la fenêtre de jeu.

        Args:
            nom (str): le nom affiché du serveur
            ip (str): l'adresse IP (IPv4) de l'hôte
            port (int): le port de l'hôte
        """
        # On arrête d'abord la lecture de la video
        self.mediaPlayer.stop()
        # On récupère la boucle des évènements
        loop = asyncio.get_event_loop()
        # On en fait la boucle principale
        GCR.setEventLoop(loop)
        try:
            # On ouvre la connexion au serveur
            username = self.input_username.text()
            if username == "":
                username = GCR.getRandomName()
            loop.run_until_complete(TCPClientProtocol.create(nom, ip, port, username))
            self.open_game()
            # L'astuce réside ici
            # On contient les évènements réseau dans un autre Thread
            # Comme ça le thread PyQt peut continuer de tourner
            GCR.tcp_thread = Thread(target=loop.run_forever)
            GCR.tcp_thread.start()
        except KeyboardInterrupt:
            GCR.log.log(Logger.INFORMATION, "Fin du programme client")

    def open_game(self) -> None:
        """
        Ouvre la fenêtre de jeu et cache la fenêtre de
        connexion jusqu'à ce que la fenêtre de jeu soit
        fermée.
        """
        GCR.log.log(Logger.INFORMATION, "Ouverture du jeu en cours ...")
        self.game = EcranJeu(self)

        # On connecte la fermeture de la fenêtre de jeu
        # A l'ouverture de la fenêtre de connexion
        self.game.closed.connect(self.show)
        self.game.show()
        self.hide()


class LocalServerDialog(QDialog):
    """
    Boite de dialogue modale qui permet de rentrer
    manuellement un serveur pour s'y connecter.

    Args:
        parent (QWidget): le parent auquel la boite de dialogue
            se rattache.

    Attributes:
        nom (str): le nom à afficher du serveur
        ip (str): l'adresse IP (IPv4) du serveur
        port (int): le port du serveur
    """
    def __init__(self, parent: QObject = None):
        super(LocalServerDialog, self).__init__(parent)
        uic.loadUi('assets/dialog_local_server.ui', self)

        self.nom = self.findChild(QLineEdit, "input_name")
        self.ip = self.findChild(QLineEdit, "input_ip")
        self.port = self.findChild(QLineEdit, "input_port")

    @staticmethod
    def get_local_server_addr(parent=None) -> (str, str, str) or None:
        """
        Fonction statique qui permet d'ouvrir la boite de dialogue
        et de retourner les information de connexion serveur
        entrées par l'utilisateur.

        Args:
            parent (QWidget): (OPTIONNEL) le parent auquel rattacher la fenêtre

        Returns:
            tuple: le nom, l'ip et le port du serveur entré manuellement
        """
        dialog = LocalServerDialog(parent)
        if dialog.exec_():
            return dialog.nom.text(), dialog.ip.text(), dialog.port.text()
        else:
            return None
