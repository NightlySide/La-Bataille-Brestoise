import unittest
import sys

from lib.client.game_screen import EcranJeu
from lib.client.connexion_screen import EcranConnexion
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QListWidget, QApplication

app = QApplication(sys.argv)


class TestUi(unittest.TestCase):

    def test_game_screen(self):
        ui = EcranJeu()

        self.assertIsInstance(ui.minimap, QLabel)
        self.assertIsInstance(ui.input_chatbox, QLineEdit)
        self.assertIsInstance(ui.btn_send_chatbox, QPushButton)

    def test_connection_screen(self):
        ui = EcranConnexion()

        self.assertIsInstance(ui.logo, QLabel)
        self.assertIsInstance(ui.btn_connect, QPushButton)
        self.assertIsInstance(ui.btn_add_server, QPushButton)
        self.assertIsInstance(ui.server_list, QListWidget)
        self.assertIsInstance(ui.input_username, QLineEdit)
