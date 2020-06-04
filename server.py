# Auteur : Alexandre FROEHLICH

from lib.common.json_loader import JsonLoader
from lib.server.commandhandler import CommandHandler
from lib.server.tcp_server import TCPServer
from lib.server.global_server_registry import GSR
from lib.common.logger import Logger
from threading import Thread
import asyncio
import socket
import colorama


def motd(port, max_players):
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    msg = f"""
    #------------------------La Bataille Brestoise SERVEUR----------------------#
    #
    #       HOST NAME : {host_name}
    #       IP = {host_ip}
    #       PORT = {port}
    #       Nb max joueurs = {max_players}
    #
    #                               Have Fun !!!
    #---------------------------------------------------------------------------#
    """
    print(msg)


if __name__ == "__main__":
    colorama.init()
    config = JsonLoader("server_config.json")
    PORT = config["port"]
    IP = config["ip"]
    MAX_PLAYERS = 10
    GSR.log = Logger(Logger.DEBUG)
    GSR.log.save_to_file("serveur.log")
    GSR.log.log(Logger.INFORMATION, f"Lancement du serveur sur {IP}:{PORT} ...")
    loop = asyncio.get_event_loop()
    GSR.setEventLoop(loop)
    server = loop.run_until_complete(TCPServer.create(IP, PORT, MAX_PLAYERS))
    motd(PORT, MAX_PLAYERS)
    cmd_h = CommandHandler()
    t = Thread(target=loop.run_forever)
    t.start()

    while GSR.running:
        user = input("> ")
        cmd_h.handle_input(user)

    GSR.getEventLoop().call_soon_threadsafe(GSR.getEventLoop().stop)
    server.close()
    GSR.game_loop.stop()
    t.join()
    GSR.log.log(Logger.INFORMATION, "Serveur fermé avec succès")

