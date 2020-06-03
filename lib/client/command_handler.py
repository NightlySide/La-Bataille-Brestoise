from lib.client.global_client_registry import GCR
from lib.server.game_loop import GameState


class CommandHandler:

    COMMANDS = {"help" : "Afficher la liste des commandes",
                "start": "Démarre la partie (besoin d'être le GameMaster)",
                "exp" :  "Retourne la quantité de points d'xp du joueur"}

    @staticmethod
    def handle(message: str) -> None:
        cmd, *args = message.split(" ")
        cmd = cmd.lower()
        # Si la commande n'est pas valable
        if cmd not in CommandHandler.COMMANDS:
            GCR.chatbox.add_line("[-] Commande non reconnue, tapez '/help' pour afficher la liste des commandes.")
        else:
            if cmd == "help":
                GCR.chatbox.add_line("[+] Affichage des commandes disponibles")
                for command in CommandHandler.COMMANDS:
                    GCR.chatbox.add_line(f"->  {command}: {CommandHandler.COMMANDS[command]}")
                GCR.chatbox.add_line("[+] Fin des commandes disponibles")
            elif cmd == "start":
                # Si la partie est déjà démarrée ou terminée
                if GCR.gamestate != GameState.NOTSTARTED:
                    GCR.chatbox.add_line("[-] Partie déjà en cours ou finie. Impossible de la démarrer.")
                else:
                    GCR.chatbox.add_line("[+] Demande de démarrage de partie envoyée au serveur.")
                    GCR.tcp_client.send({"action": "start_game",
                                         "user": GCR.tcp_client.id})
            elif cmd == "exp":
                GCR.chatbox.add_line(f"[ ] Vous avez : {GCR.joueur.exp} points d'XP")
