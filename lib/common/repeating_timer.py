import threading


class RepeatingTimer:
    """
    Un timer basé sur du threading qui se répète à l'infini.
    Utile pour définir les boucles de jeu.

    Attributes:
        temps (float): le temps entre deux répétitions
        fonction (builtins.function): la fonction à appeler
        thread (threading.Timer): le timer lié à la classe
    """

    def __init__(self, temps: float, fonction):
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