# Auteur : Alexandre FROEHLICH

from lib.client.global_client_registry import GCR
from lib.server.game_loop import GameState


class CommandHandler:
    """
    Classe permettant de gérer les commandes utilisateur dans la chatbox.
    Ne possède qu'une fonction statique pour gérer les commandes.
    """

    COMMANDS = {"help" : "Afficher la liste des commandes",
                "start": "Démarre la partie (besoin d'être le GameMaster)",
                "exp" :  "Retourne la quantité de points d'xp du joueur",
                "vie": "affiche la vie et le maximum"}

    @staticmethod
    def handle(message: str) -> None:
        """
        Prend en charge les commandes utilisateur. Parse la commande et les arguments
        et agit en conséquences.

        Args:
            message (str): la commande et les arguments envoyés par le joueur
        """
        cmd, *args = message.split(" ")
        cmd = cmd.lower()
        # Si la commande n'est pas valable
        if cmd not in CommandHandler.COMMANDS:
            GCR.chatbox.add_line("[-] Commande non reconnue, tapez '/help' pour afficher la liste des commandes.")
        else:
            # On affiche la liste des commandes et leur utilisé
            if cmd == "help":
                GCR.chatbox.add_line("[+] Affichage des commandes disponibles")
                for command in CommandHandler.COMMANDS:
                    GCR.chatbox.add_line(f"->  {command}: {CommandHandler.COMMANDS[command]}")
                GCR.chatbox.add_line("[+] Fin des commandes disponibles")
            # On démarre la partie
            elif cmd == "start":
                # Si la partie est déjà démarrée ou terminée
                if GCR.gamestate != GameState.NOTSTARTED:
                    GCR.chatbox.add_line("[-] Partie déjà en cours ou finie. Impossible de la démarrer.")
                else:
                    GCR.chatbox.add_line("[+] Demande de démarrage de partie envoyée au serveur.")
                    GCR.tcp_client.send({"action": "start_game",
                                         "user": GCR.tcp_client.id})
            # On retourne la quantité d'expérience du joueur
            elif cmd == "exp":
                GCR.chatbox.add_line(f"[ ] Vous avez : {GCR.joueur.exp} points d'XP")
            # On retourne la vie du joueur
            elif cmd == "vie":
                GCR.chatbox.add_line(f"[ ] Vous avez : {GCR.joueur.vie}/{GCR.joueur.current_ship.hitpoints} PV")
