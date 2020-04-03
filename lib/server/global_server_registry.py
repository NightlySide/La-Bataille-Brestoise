from lib.common.logger import Logger
import lib.server.game_loop


class GSR:
    """
    Registre global de variables globales.
    Dans toutes structures de jeu, les variables globales sont
    nécessaire. Cette classe agit comme un registre qui permet
    de contenir ces variables

    Attributes:
        clients (list): liste des clients tcp connectés au serveur
        loop (asyncio.EventLoop): boucle des évènements
        log (Logger): logger des évènements
    """

    game_loop_thread = None
    clients = []
    loop = None
    log = None
    game_loop = None

    @classmethod
    def getEventLoop(cls):
        """
        Retourne la référence au thread tcp si il existe
        """
        if cls.loop is None:
            raise Exception("La boucle d'évènement n'est pas définit !")
        return cls.loop

    @classmethod
    def setEventLoop(cls, loop):
        """
        Définit la référence au thread tcp

        Args:
            loop (asyncio.EventLoop): boucle des évènements
        """
        cls.loop = loop
