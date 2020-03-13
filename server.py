from lib.server.tcp_server import TCPServer
from lib.server.global_server_registry import GSR
from lib.common.logger import Logger
import asyncio
import socket


def motd(port):
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    msg = f"""
    #------------------------La Bataille Brestoise SERVEUR----------------------#
    #
    #       HOST NAME : {host_name}
    #       IP = {host_ip}
    #       PORT = {port}
    #       Nb max joueurs = 10
    #
    #                               Have Fun !!!
    #---------------------------------------------------------------------------#
    """
    print(msg)


if __name__ == "__main__":
    PORT = 25566
    GSR.log = Logger(Logger.INFORMATION)
    GSR.log.save_to_file("serveur.log")
    GSR.log.log(Logger.INFORMATION, "Lancement du serveur ...")
    loop = asyncio.get_event_loop()
    GSR.setEventLoop(loop)
    try:
        motd(PORT)
        loop.run_until_complete(TCPServer.create('', PORT))
    except KeyboardInterrupt:
        GSR.log.log(Logger.INFORMATION, "Fin du programme serveur")
        loop.close()
