from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from lib.client.global_client_registry import GCR


class EcranJeu(QMainWindow):
    closed = pyqtSignal()

    def __init__(self,  parent=None):
        super().__init__(parent)
        uic.loadUi('assets/ecran_jeu.ui', self)

        # On cherche les éléments
        self.game_scr = self.findChild(QWidget, 'game_screen')
        self.minimap = self.findChild(QLabel, 'minimap')
        self.chatbox = self.findChild(QTextEdit, 'chatbox')
        self.input_chatbox = self.findChild(QLineEdit, 'input_chat')
        self.btn_send_chatbox = self.findChild(QPushButton, 'btn_sendchat')

        # On connecte les fonctions
        self.btn_send_chatbox.clicked.connect(self.send_chat)
        self.input_chatbox.editingFinished.connect(self.send_chat)

        minimap_background = QPixmap("assets/images/rade_brest.png")
        self.minimap.setPixmap(minimap_background)

        self.chatbox.setAcceptRichText(True)
        self.chatbox.setReadOnly(True)
        self.chatbox.setText("[+] Vous avez rejoint la partie\n[ ] Essayez de ne pas mourir ...")

        self.setWindowTitle("La Bataille Brestoise - Alexandre F. & Guillaume L.")

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def send_chat(self):
        message = self.input_chatbox.text()
        if message != "":
            self.input_chatbox.setText("")
            self.chatbox.setHtml(self.chatbox.toHtml() + "\n(Joueur 1): " + message)
            GCR.getEventLoop().run_until_complete(GCR.getTcpClient().send({
                                                        "action": "chat",
                                                        "user": GCR.getTcpClient().id,
                                                        "msg": message}))
            self.chatbox.verticalScrollBar().setValue(self.chatbox.verticalScrollBar().maximum())