class Player:

    def __init__(self, peername, transport):
        self.peername = peername
        self.transport = transport
        self.username = None
        self.uuid = None

    @staticmethod
    def find_player_by_peername(players, peername):
        for p in players:
            if p.peername == peername:
                return p
        else:
            return None

    @staticmethod
    def find_player_by_uuid(players, uuid):
        for p in players:
            if p.uuid == uuid:
                return p
        else:
            return None