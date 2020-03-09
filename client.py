from PyQt5.QtWidgets import *
from lib.client.connexion_screen import EcranConnexion
from lib.client.game_screen import EcranJeu
import sys


if __name__=="__main__":
    app = QApplication(sys.argv)
    fen = EcranConnexion()
    fen.show()
    app.exec()