from PyQt5.QtWidgets import *
from lib.client.connexion_screen import EcranConnexion
from lib.common.logger import Logger
from lib.client.global_client_registry import GCR
import colorama
import sys


if __name__=="__main__":
    colorama.init()
    GCR.log = Logger(Logger.DEBUG)
    app = QApplication(sys.argv)
    fen = EcranConnexion()
    fen.show()
    app.exec()