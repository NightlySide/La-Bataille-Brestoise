from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import asyncio
from lib.client.tcp_client import TCPClientProtocol
from lib.client.game_screen import EcranJeu
from lib.client.global_client_registry import GCR
from threading import Thread


class EcranConnexion(QMainWindow):
    def __init__(self,  parent=None):
        super().__init__(parent)
        self.game = None
        uic.loadUi('assets/ecran_connexion.ui', self)

        # On cherche les éléments
        self.logo = self.findChild(QLabel, 'logo')
        self.btn_connect = self.findChild(QPushButton, 'btn_connect')
        self.btn_local = self.findChild(QPushButton, 'btn_local')
        self.server_list = self.findChild(QListWidget, 'server_list')

        # On connecte les boutons aux méthodes
        self.btn_connect.clicked.connect(self.connect_from_list)
        self.btn_local.clicked.connect(self.connect_local)

        self.setWindowTitle("La Bataille Brestoise - Alexandre F. & Guillaume L.")

        # On met l'image sur le logo
        pix = QPixmap("assets/images/logo.png")
        self.logo.setPixmap(pix)

        # On paramètre la liste des serveurs
        serveurs = [["Localhost", "127.0.0.1", "25566"],
                    ["Evril server", "ieta-docs.ddns.net", "25566"]]
        for k in range(len(serveurs)):
            nom, ip, port = serveurs[k]
            self.server_list.addItem(QListWidgetItem(f"{nom} | {ip} | {port}"))
        self.server_list.setCurrentRow(0)

    def connect_from_list(self):
        nom, ip, port = self.server_list.currentItem().text().split(" | ")
        self.connect(nom, ip, port)

    def connect_local(self):
        nom, ip, port = LocalServerDialog.getLocalServerAddr()
        self.connect(nom, ip, port)

    def connect(self, nom, ip, port):
        loop = asyncio.new_event_loop()
        game_loop = asyncio.new_event_loop()
        GCR.setEventLoop(loop)
        try:
            loop.run_until_complete(TCPClientProtocol.create("TEST", "127.0.0.1", 25566))
            self.open_game()
            t = Thread(target=loop.run_forever)
            t.start()

        except KeyboardInterrupt:
            print("\nFin du programme client")
            loop.close()

    def open_game(self):
        print("[ ] Ouverture du jeu en cours...")
        self.game = EcranJeu(self)

        self.game.closed.connect(self.show)
        self.game.show()
        self.hide()


class LocalServerDialog(QDialog):

    def __init__(self, parent=None):
        super(LocalServerDialog, self).__init__(parent)

        uic.loadUi('assets/dialog_local_server.ui', self)

        self.nom = self.findChild(QLineEdit, "input_name")
        self.ip = self.findChild(QLineEdit, "input_ip")
        self.port = self.findChild(QLineEdit, "input_port")

    @staticmethod
    def getLocalServerAddr(parent = None):
        dialog = LocalServerDialog(parent)
        result = dialog.exec_()
        return dialog.nom.text(), dialog.ip.text(), dialog.port.text()