from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5 import uic

from lib.client.global_client_registry import GCR
from lib.client.chatbox import ChatBox
from lib.client.canvas_jeu import CanvasJeu
from lib.client.radar import Radar
from lib.common.joueur import Joueur
from lib.common.logger import Logger
import functools

from lib.common.vecteur import Vecteur


class EcranJeu(QMainWindow):
    """
    Fenetre Qt qui contient tout ce qui touche à l'écran de jeu.
    Cela comporte la chatbox, le canvas de jeu, les informations sur la vie du joueur,
    et son radar.

    Args:
        parent (QWidget): (OPTIONNEL) le parent auquel rattacher
            la fenêtre.
        update_delta (float): temps entre deux itérations (fixe) de rendu
            pour afficher un framerate constant. Fixé par défaut à 60fps.

    Attributes:
        closed (QSignal): signal émit par la fenêtre pour signaler quelle s'est
            fermée correctement.
        game_canvas (CanvasJeu): canvas du jeu sur lequel on retrouve la carte
            et le joueur
        radar (Radar): radar de détection du joueur
        chatbox (ChatBox): boite de chat entre les joueurs d'un même serveur
        input_chatbox (QLineEdit): boite de texte pour envoyer un message sur le chat
        btn_send_chatbox (QPushButton): bouton pour envoyer un message sur le chat
    """

    # Signal de fermeture (par défaut il n'existe pas)
    closed = pyqtSignal()

    def __init__(self, parent=None, update_delta=1/60*1000):
        super().__init__(parent)
        uic.loadUi('assets/ecran_jeu.ui', self)

        # On cherche les éléments de l'écran
        self._game_scr_widget = self.findChild(QWidget, 'game_canvas')
        self._minimap = self.findChild(QLabel, 'minimap')
        self._chatbox_widget = self.findChild(QWidget, 'chatbox_anchor')
        self.input_chatbox = self.findChild(QLineEdit, 'input_chat')
        self.btn_send_chatbox = self.findChild(QPushButton, 'btn_sendchat')

        # On connecte les signaux/évènements
        self.btn_send_chatbox.clicked.connect(self.send_chat)
        self.input_chatbox.editingFinished.connect(self.send_chat)

        # Paramétrage de la minimap
        # minimap_background = QPixmap("assets/images/rade_brest.png")
        self.radar = Radar(125, 90, self._minimap)

        # Création du jeu
        self.game_canvas = CanvasJeu(self._game_scr_widget)
        self.game_canvas.setMouseTracking(True)

        # Création de la chatbox
        self.chatbox = ChatBox(self._chatbox_widget)
        self.chatbox.add_line("[+] Vous avez rejoint la partie")
        self.chatbox.update()
        GCR.chatbox = self.chatbox

        # Création du joueur
        GCR.joueur = Joueur(Vecteur(700, 300))

        # On donne un titre à la fenêtre
        self.setWindowTitle("La Bataille Brestoise - Alexandre F. & Guillaume L.")

        # On itère toutes les X secondes pour mettre à jour l'écran
        self._timer = QTimer()
        # la fonction partial permet d'envoyer des arguments dans la fonction connect
        self._timer.timeout.connect(functools.partial(self.update, update_delta / 1000))
        self._timer.start(int(update_delta))

    def keyPressEvent(self, e):
        """
        Fonction héritée de Qt qui permet de prendre en charge les évènements du type
        touche clavier.

        Args:
            e (QKeyEvent): évènement de type touche de clavier
        """
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, event):
        """
        Fonction héritée de Qt, appelée lorsque le signal de fermeture de la
        fenêtre est emit. On ferme le thread TCP puis le thread Qt et enfin
        on émet le signal qui indique que la fermeture s'est bien déroulée.
        Args:
            event (QCloseEvent): évènement du type fermeture de fenêtre
        """

        GCR.log.log(Logger.INFORMATION, "Fermeture de la fenêtre de jeu")
        # Si le thread tcp n'est pas déjà fermé
        if GCR.loop is not None:
            # On coupe la connexion avec le serveur
            GCR.tcp_client.transport.close()
            # On stoppe le thread tcp
            GCR.getEventLoop().call_soon_threadsafe(GCR.getEventLoop().stop)
            GCR.loop = None
            # On fait rejoindre le thread tcp sur le thread courant (qt)
            GCR.tcp_thread.join()
        self.closed.emit()
        # Pour éviter que l'évènement ne fasse écho
        event.accept()

    def send_chat(self):
        """
        Permet d'envoyer le contenu de l'entrée chat au serveur pour
        le transmettre dans la chatbox.
        """
        # On récupère le message que veut envoyer le joueur
        message = self.input_chatbox.text()
        # Si le message est vide on ne fait rien
        if message != "":
            # On vide la boite de dialogue
            self.input_chatbox.setText("")
            # On transmet le message au serveur
            GCR.getTcpClient().send({
                "action": "chat",
                "user": GCR.getTcpClient().id,
                "msg": message})

    def update(self, delta):
        """
        Fonction appelée pour rafraîchir l'écran de jeu et tous ses
        composants (chatbox, joueur, canvas de jeu, radar)
        Cette fonction est une surcharge des fonctions implémentées par Qt.
        """
        super().update()
        self.chatbox.update()
        GCR.joueur.update(delta)
        self.game_canvas.update()
        self.radar.update()
