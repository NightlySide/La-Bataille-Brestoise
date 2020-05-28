import random
import threading

from lib.common.carte import Carte
from lib.common.ia import IA
from lib.common.image_vers_tableau import img_vers_array
from lib.common.logger import Logger
from lib.common.repeating_timer import RepeatingTimer
from lib.common.vecteur import Vecteur
from lib.server.global_server_registry import GSR


class GameLoop:

    def __init__(self, update_delta=0.2):
        GSR.log.log(Logger.INFORMATION, "Initialisation du serveur")
        self.update_delta = update_delta
        self.setup()

        self._timer = RepeatingTimer(update_delta, self.update)
        self._timer.start()
        GSR.log.log(Logger.INFORMATION, "Initialisation terminée")

    def setup(self):
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

    def update(self):
        GSR.entities_to_update = []
        for e in GSR.entities:
            e.update(self.update_delta)
            if isinstance(e, IA):
                #GSR.log.log(Logger.DEBUG, e.brain.nom_etat_courant)
                pass
            GSR.entities_to_update.append(e)

        if GSR.server is not None:
            GSR.server.send_all("update_entities", {"data": GSR.entities_to_update})

    def stop(self):
        self._timer.cancel()
