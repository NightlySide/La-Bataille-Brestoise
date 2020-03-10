from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import asyncio
from lib.client.tcp_client import TCPClientProtocol
from lib.client.game_screen import EcranJeu
from lib.client.global_client_registry import GCR
from threading import Thread


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
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.game = None
        uic.loadUi('assets/ecran_connexion.ui', self)

        # On cherche les éléments
        self.logo = self.findChild(QLabel, 'logo')
        self.btn_connect = self.findChild(QPushButton, 'btn_connect')
        self.btn_local = self.findChild(QPushButton, 'btn_local')
        self.server_list = self.findChild(QListWidget, 'server_list')
        self.input_username = self.findChild(QLineEdit, 'input_username')

        # On connecte les boutons aux méthodes
        self.btn_connect.clicked.connect(self.connect_from_list)
        self.btn_local.clicked.connect(self.connect_local)

        self.setWindowTitle("La Bataille Brestoise - Alexandre F. & Guillaume L.")

        # On met l'image sur le logo
        pix = QPixmap("assets/images/logo.png")
        self.logo.setPixmap(pix)

        # On paramètre la liste des serveurs
        for k in range(len(GCR.serveurs)):
            nom, ip, port = GCR.serveurs[k]
            self.server_list.addItem(QListWidgetItem(f"{nom} | {ip} | {port}"))
        self.server_list.setCurrentRow(0)

    def connect_from_list(self):
        """
        Appelée lorsque l'utilisateur clique sur le bouton 'Connecter'
        Se connecter à partir d'un serveur enregistré
        """
        nom, ip, port = self.server_list.currentItem().text().split(" | ")
        # On se connecte
        self.connect(nom, ip, port)

    def connect_local(self):
        """
        Appelée lorsque l'utilisateur clique sur le bouton 'Connexion locale'
        Ouvre la boite de dialogue correspondante
        """
        nom, ip, port = LocalServerDialog.get_local_server_addr()
        # On se connecte
        self.connect(nom, ip, port)

    def connect(self, nom, ip, port):
        """
        Appelée finalement pour se connecter au serveur et ouvrir
        la fenêtre de jeu.

        Args:
            nom (str): le nom affiché du serveur
            ip (str): l'adresse IP (IPv4) de l'hôte
            port (int): le port de l'hôte
        """
        # On récupère la boucle des évènements
        loop = asyncio.get_event_loop()
        # On en fait la boucle principale
        GCR.setEventLoop(loop)
        t = None
        try:
            # On ouvre la connexion au serveur
            username = self.input_username.text()
            loop.run_until_complete(TCPClientProtocol.create(nom, ip, port, "Anonyme" if username == "" else username))
            self.open_game()
            # L'astuce réside ici
            # On contient les évènements réseau dans un autre Thread
            # Comme ça le thread PyQt peut continuer de tourner
            t = Thread(target=loop.run_forever)
            t.start()
        except KeyboardInterrupt:
            print("\nFin du programme client")
            t.stop()
            loop.close()

    def open_game(self):
        """
        Ouvre la fenêtre de jeu et cache la fenêtre de
        connexion jusqu'à ce que la fenêtre de jeu soit
        fermée.
        """
        print("[ ] Ouverture du jeu en cours...")
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
    def __init__(self, parent=None):
        super(LocalServerDialog, self).__init__(parent)
        uic.loadUi('assets/dialog_local_server.ui', self)

        self.nom = self.findChild(QLineEdit, "input_name")
        self.ip = self.findChild(QLineEdit, "input_ip")
        self.port = self.findChild(QLineEdit, "input_port")

    @staticmethod
    def get_local_server_addr(parent=None) -> tuple:
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
        dialog.exec_()
        return dialog.nom.text(), dialog.ip.text(), dialog.port.text()
