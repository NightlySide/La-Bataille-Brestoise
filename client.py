from PyQt5.QtWidgets import *
from lib.client.connexion_screen import EcranConnexion
from lib.common.logger import Logger
from lib.client.global_client_registry import GCR
import sys


if __name__=="__main__":
    GCR.log = Logger(Logger.DEBUG)
    app = QApplication(sys.argv)
    fen = EcranConnexion()
    fen.show()
    app.exec()