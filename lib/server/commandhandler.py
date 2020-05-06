from lib.server.global_server_registry import GSR


class CommandHandler:
    COMMANDS = ["help", "playerlist", "stop", "entities", "getentity"]

    def __init__(self):
        pass

    def handle_input(self, message):
        message = message.lower()
        cmd, *args = message.split(" ")

        if cmd == "help":
            print("Liste des commandes disponibles :")
            for c in self.COMMANDS:
                print("- " + c)
        elif cmd == "playerlist":
            print(f"Il y a {len(GSR.clients)} joueurs connectés :")
            for c in GSR.clients:
                print("- " + c.username)
        elif cmd == "stop":
            print("Arrêt du serveur ...")
            GSR.running = False
        elif cmd == "entities":
            print("Nombre d'entitées existantes : {}".format(len(GSR.entities)))
        elif cmd == "getentity" and len(args) == 1:
            print("{} : {}".format(args[0], GSR.entities[int(args[0])]))
        else:
            print("Commande non reconnue ... Tapez 'help' pour la liste des commandes")