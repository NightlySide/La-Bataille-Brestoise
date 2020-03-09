class GCR:

    tcp_client = None
    loop = None

    @classmethod
    def getTcpClient(cls):
        if cls.tcp_client is None:
            raise Exception("Le client TCP n'a pas été définit !")
        return cls.tcp_client

    @classmethod
    def setTcpClient(cls, client):
        cls.tcp_client = client

    @classmethod
    def getEventLoop(cls):
        if cls.loop is None:
            raise Exception("La boucle d'évènement n'est pas définit !")
        return cls.loop

    @classmethod
    def setEventLoop(cls, loop):
        cls.loop = loop