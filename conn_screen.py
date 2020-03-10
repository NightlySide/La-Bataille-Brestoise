from PyQt5.QtWidgets import *
from lib.client.client.connexion_screen import EcranConnexion
import sys


if __name__=="__main__":
    app = QApplication(sys.argv)
    fen = EcranConnexion()
    fen.show()
    app.exec()