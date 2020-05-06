import datetime
from colorama import Fore

def get_time():
    """
    Retourne l'heure, les minutes et les secondes actuelles
    """
    now = datetime.datetime.now()
    return str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2)


class Logger:
    """
    Classe qui permet de logger les évènements avec des niveaux de
    priorité allant du debug à l'erreur critique.

    Args:
        seuil (int): seuil de déclenchement de l'affichage des logs

    Attributes:
        file_path (str): chemin d'enregistrement des logs
    """

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
        """
        Permet de déclencher l'enregistrement des logs dans un fichier
        spécifié dans file_path

        Args:
            file_path (str): chemin relatif d'accès au fichier des logs
        """
        self.file_path = file_path

    def level_name(self, level):
        """
        Retourne une chaine de caractère correspondant au niveau de priorité
        du log. Fonction purement esthétique.

        Args:
            level (int): niveau de priorité du message
        """
        if level == self.CRITIQUE:
            return Fore.RESET + "[" + Fore.RED + "CRIT" + Fore.RESET + "]"
        elif level == self.ERREUR:
            return Fore.RESET + "[" + Fore.RED + "ERR" + Fore.RESET + "]"
        elif level == self.AVERTISSEMENT:
            return Fore.RESET + "[" + Fore.YELLOW + "AVERT" + Fore.RESET + "]"
        elif level == self.INFORMATION:
            return Fore.RESET + "[" + Fore.BLUE + "INFO" + Fore.RESET + "]"
        elif level == self.DEBUG:
            return Fore.RESET + "[" + Fore.MAGENTA + "DEBUG" + Fore.RESET + "]"
        else:
            return ""

    def log(self, niveau, message):
        """
        Affiche le log dans la console, ou l'enregistre dans le fichier
        en fonction de son niveau de priorité.
        Le log est un message formaté pour pouvoir remontrer les erreurs ou
        bugs plus facilement et de pouvoir les cacher en production.

        Args:
            niveau (int): niveau de priorité du message
            message (str): message de log à afficher
        """
        # Si le niveau du message dépasse le seuil on l'affiche
        if niveau >= self.seuil:
            # On récupère l'heure du message
            date = Fore.RESET + "[" + Fore.GREEN + "{}:{}:{}".format(*get_time()) + Fore.RESET + "]"
            # On affiche le log
            print(f"{date}{self.level_name(niveau)} {message}")

        # Si on a décidé d'enregistrer en plus les logs
        if self.file_path is not None:
            # On ouvre le fichier uniquement pour écrire la ligne
            with open(self.file_path, "a") as f:
                date = "[{}:{}:{}]".format(*get_time())
                f.write(f"{date}{self.level_name(niveau)} {message}\n")
            # On referme directement pour éviter les fuites de données
            # En cas d'erreur d'exécution du programme.
