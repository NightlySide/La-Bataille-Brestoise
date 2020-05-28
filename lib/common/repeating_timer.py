import threading


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