import random
import threading

from lib.common.carte import Carte
from lib.common.ia import IA
from lib.common.image_vers_tableau import img_vers_array
from lib.common.logger import Logger
from lib.common.repeating_timer import RepeatingTimer
from lib.common.vecteur import Vecteur
from lib.server.global_server_registry import GSR
from lib.client.global_client_registry import GCR


class GameLoop:
    """
    Boucle principale de fonctionnement du jeu

    Attributes:
        _timer (RepeatingTimer): timer qui se répète pour relancer la boucle
    """

    def __init__(self, update_delta: float = 0.2):
        GSR.log.log(Logger.INFORMATION, "Initialisation du serveur")
        self.update_delta = update_delta
        self.setup()

        self._timer = RepeatingTimer(update_delta, self.update)
        self._timer.start()
        GSR.log.log(Logger.INFORMATION, "Initialisation terminée")

    def setup(self) -> None:
        """
        Appelée une seule fois, permet de mettre en place le jeu.
        """
        rade_data = img_vers_array("assets/carte_rade_brest.jpg")
        GSR.carte = Carte(rade_data.shape, (8, 8), rade_data)

        for k in range(1):
            e = IA()
            e.set_image("assets/images/plaisance.png")
            x = y = -1
            while GSR.carte.is_colliding(x, y):
                x = random.randint(0, GSR.carte.shape[0])
                y = random.randint(0, GSR.carte.shape[1])
            x = 700
            y = 300
            e.position = Vecteur(x, y)
            GSR.entities.append(e)

    def update(self) -> None:
        """
        Est appelée à intervales réguliers. Analogue à la fonction loop en arduino.
        """
        GSR.entities_to_update = []
        #escarmouche

        # On ajoute les entités crées par le serveur
        for e in GSR.entities:
            e.update(self.update_delta)

            if e.isWinning() == True :
                GCR.chatbox.add_line(f"[+] {e.id} à gagné la partie")

            """problème : comment définir le début et la fin du jeu ?  (mettre un compteur 
             d'une minute au premier joueur réel et donner la possibilité à ce joueur de 
             forcer le début de la partie avec un message dans le chat) """
            

            e.isDead()
            if isinstance(e, IA):
                #GSR.log.log(Logger.DEBUG, e.brain.nom_etat_courant)
                pass
            GSR.entities_to_update.append(e)

        # On ajoute les joueurs
        for client in GSR.clients:
            e = client.joueur
            if e.isWinning() == True :
                GCR.chatbox.add_line(f"[+] {e.id} à gagné la partie")
            e.isDead()
            GSR.entities_to_update.append(client.joueur)
        if GSR.server is not None:
            GSR.server.send_all("update_entities", {"data": GSR.entities_to_update})

    def stop(self):
        """
        Permet d'arrêter les cycles de boucle.
        """
        self._timer.cancel()
