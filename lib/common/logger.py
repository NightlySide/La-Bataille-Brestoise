import datetime


def get_time():
    now = datetime.datetime.now()
    return str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)


class Logger:
    CRITIQUE = 50
    ERREUR = 40
    AVERTISSEMENT = 20
    INFORMATION = 10
    DEBUG = 5
    NONDEF = 0

    def __init__(self, seuil=NONDEF):
        self.seuil = seuil
        self.file_path = None

    def save_to_file(self, file_path):
        self.file_path = file_path

    def level_name(self, level):
        if level == self.CRITIQUE:
            return "[CRIT]"
        elif level == self.ERREUR:
            return "[ERR]"
        elif level == self.AVERTISSEMENT:
            return "[AVERT]"
        elif level == self.INFORMATION:
            return "[INFO]"
        elif level == self.DEBUG:
            return "[DEBUG]"
        else:
            return ""

    def log(self, niveau, message):
        if niveau >= self.seuil:
            date = "[{}:{}:{}]".format(*get_time())
            print(f"{date}{self.level_name(niveau)} {message}")

        if self.file_path is not None:
            with open(self.file_path, "a") as f:
                date = "[{}:{}:{}]".format(*get_time())
                f.write(f"{date}{self.level_name(niveau)} {message}\n")
