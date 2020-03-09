class GSR:
    clients = {}
    loop = None

    @classmethod
    def getEventLoop(cls):
        if cls.loop is None:
            raise Exception("La boucle d'évènement n'est pas définit !")
        return cls.loop

    @classmethod
    def setEventLoop(cls, loop):
        cls.loop = loop