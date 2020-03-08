import pickle
import asyncio


class TCPClient():

    def __init__(self, host, port, chunk_size=8192):
        self.addr = (host, port)
        self.chunk_size = chunk_size
        self.writer = None
        self.reader = None
        self.id = None

    async def connect(self, host=None, port=None):
        ip = host if host is not None else self.addr[0]
        p = port if port is not None else self.addr[1]
        print(f"[ ] Connexion en cours au ({ip}, {p})")
        if self.writer is not None:
            await self.close()
        try:
            self.reader, self.writer = await asyncio.open_connection(ip, p)
            print(f"[+] Connecté au serveur avec succès !")
            await self.request_client_id()
        except ConnectionRefusedError:
            print(f"[-] ERREUR : le serveur {host} n'est pas atteignable sur {port}")

    async def send(self, data):
        if self.writer is None:
            raise Exception("Le client n'est pas connecté, tentez client.connect()")
        self.writer.write(pickle.dumps(data))
        await self.writer.drain()
        return await self.recv()

    async def ping(self):
        print(await self.send({"action": "ping"}))

    async def request_client_id(self):
        print("[ ] Demande d'un id client")
        requete = {"action": "request_id"}
        self.id = await self.send(requete)
        if self.id is not None:
            print(f"[+] Reçu identifiant : {self.id}")
        else:
            print("[-] Attention pas d'identifiant reçu")

    async def recv(self):
        if self.reader is None:
            raise Exception("Le client n'est pas connecté, tentez client.connect()")
        data = await self.reader.read(self.chunk_size)
        if len(data) > 0:
            return pickle.loads(data)
        else:
            print("[-] Le client n'a pas reçu de données !")
            return

    async def close(self):
        print("[-] Fermeture du socket")
        self.writer.close()
        await self.writer.wait_closed()
        self.writer = self.reader = None