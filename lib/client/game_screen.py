from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5 import uic
from lib.client.global_client_registry import GCR
from lib.client.chatbox import ChatBox
from lib.client.canvas_jeu import CanvasJeu


class EcranJeu(QMainWindow):
    # Signal de fermeture (par défaut il n'existe pas)
    closed = pyqtSignal()

    def __init__(self,  parent=None, update_delta=100):
        super().__init__(parent)
        uic.loadUi('assets/ecran_jeu.ui', self)

        # On cherche les éléments de l'écran
        self.game_scr_widget = self.findChild(QWidget, 'game_canvas')
        self.minimap = self.findChild(QLabel, 'minimap')
        self.chatbox_widget = self.findChild(QWidget, 'chatbox_anchor')
        self.input_chatbox = self.findChild(QLineEdit, 'input_chat')
        self.btn_send_chatbox = self.findChild(QPushButton, 'btn_sendchat')

        # On connecte les signaux/évènements
        self.btn_send_chatbox.clicked.connect(self.send_chat)
        self.input_chatbox.editingFinished.connect(self.send_chat)

        # Paramétrage de la minimap
        minimap_background = QPixmap("assets/images/rade_brest.png")
        self.minimap.setPixmap(minimap_background)

        # Création du jeu
        self.game_canvas = CanvasJeu(self.game_scr_widget)

        # Création de la chatbox
        self.chatbox = ChatBox(self.chatbox_widget)
        self.chatbox.add_line("[+] Vous avez rejoint la partie")
        self.chatbox.update()
        GCR.chatbox = self.chatbox

        # On donne un titre à la fenêtre
        self.setWindowTitle("La Bataille Brestoise - Alexandre F. & Guillaume L.")

        # On itère toutes les X secondes pour mettre à jour l'écran
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
        print("[ ] Closing client")
        if GCR.loop is not None:
            GCR.getEventLoop().call_soon_threadsafe(GCR.getEventLoop().stop)
            GCR.loop = None
            GCR.tcp_thread.join()
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