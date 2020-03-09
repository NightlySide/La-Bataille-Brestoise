from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5 import uic
from lib.client.global_client_registry import GCR
from lib.client.chatbox import ChatBox


class EcranJeu(QMainWindow):
    closed = pyqtSignal()

    def __init__(self,  parent=None, update_delta=100):
        super().__init__(parent)
        uic.loadUi('assets/ecran_jeu.ui', self)

        # On cherche les éléments
        self.game_scr = self.findChild(QWidget, 'game_canvas')
        self.minimap = self.findChild(QLabel, 'minimap')
        self.chatbox_widget = self.findChild(QWidget, 'chatbox_anchor')
        self.chatbox = ChatBox(self.chatbox_widget)
        self.input_chatbox = self.findChild(QLineEdit, 'input_chat')
        self.btn_send_chatbox = self.findChild(QPushButton, 'btn_sendchat')

        # On connecte les fonctions
        self.btn_send_chatbox.clicked.connect(self.send_chat)
        self.input_chatbox.editingFinished.connect(self.send_chat)

        minimap_background = QPixmap("assets/images/rade_brest.png")
        self.minimap.setPixmap(minimap_background)
        self.game_scr.setMouseTracking(True)

        self.chatbox.add_line("[+] Vous avez rejoint la partie")
        self.chatbox.update()
        GCR.chatbox = self.chatbox

        self.setWindowTitle("La Bataille Brestoise - Alexandre F. & Guillaume L.")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(update_delta)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()
        text = "x: {0},  y: {1}".format(x, y)
        self.setWindowTitle(text)

    def closeEvent(self, event):
        self.closed.emit()
        event.accept()

    def send_chat(self):
        message = self.input_chatbox.text()
        if message != "":
            self.input_chatbox.setText("")
            GCR.getTcpClient().send({
                        "action": "chat",
                        "user": GCR.getTcpClient().id,
                        "msg": message})

    def update(self):
        self.chatbox.update()