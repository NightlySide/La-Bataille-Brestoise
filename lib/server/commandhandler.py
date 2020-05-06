from lib.server.global_server_registry import GSR


class CommandHandler:
    COMMANDS = ["help", "playerlist", "stop"]

    def __init__(self):
        pass

    def handle_input(self, message):
        message = message.lower()

        if message == "help":
            print("Liste des commandes disponibles :")
            for c in self.COMMANDS:
                print("- " + c)
        elif message == "playerlist":
            print(f"Il y a {len(GSR.clients)} joueurs connectés :")
            for c in GSR.clients:
                print("- " + c.username)
        elif message == "stop":
            print("Arrêt du serveur ...")
            GSR.running = False
        else:
            print("Commande non reconnue ... Tapez 'help' pour la liste des commandes")