import threading
import time

from lib.common.logger import Logger
from lib.server.global_server_registry import GSR


class GameLoop:

    def __init__(self, update_delta=1/60):
        GSR.log.log(Logger.INFORMATION, "Initialization du serveur")
        self.running = True
        self._time_counter = time.perf_counter()

        self._timer = RepeatingTimer(update_delta, self.update)
        self._timer.start()
        GSR.log.log(Logger.INFORMATION, "Fini d'itérer")

    def update(self):
        GSR.log.log(Logger.INFORMATION, "Updating")

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
