import random
import threading
import time

from lib.common.carte import Carte
from lib.common.entite import Entite
from lib.common.image_vers_tableau import img_vers_array
from lib.common.logger import Logger
from lib.common.vecteur import Vecteur
from lib.server.global_server_registry import GSR


class GameLoop:

    def __init__(self, update_delta=1/60):
        GSR.log.log(Logger.INFORMATION, "Initialisation du serveur")
        self.update_delta = update_delta
        self.setup()

        self._timer = RepeatingTimer(update_delta, self.update)
        self._timer.start()
        GSR.log.log(Logger.INFORMATION, "Initialisation terminée")

    def setup(self):
        rade_data = img_vers_array("assets/carte_rade_brest.jpg")
        GSR.carte = Carte(rade_data.shape, (8, 8), rade_data)

        for k in range(100):
            e = Entite()
            e.set_image("assets/images/plaisance.png")
            e.position = Vecteur(random.randint(0, GSR.carte.shape[0]), random.randint(0, GSR.carte.shape[1]))
            GSR.entities.append(e)

    def update(self):
        for e in GSR.entities:
            if random.random() < 0.005:
                e.direction = Vecteur(random.randrange(-1, 2), random.randrange(-1, 2))
            e.update(self.update_delta)

        if GSR.server is not None:
            GSR.server.send_all("update_entities", {"data": GSR.entities})

    def stop(self):
        self._timer.cancel()


class RepeatingTimer:

    def __init__(self, temps, fonction):
        self.temps = temps
        self.fonction = fonction
        self.thread = threading.Timer(self.temps, self.handle_function)

    def handle_function(self):
        self.fonction()
        self.thread = threading.Timer(self.temps, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()
