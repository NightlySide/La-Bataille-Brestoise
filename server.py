from lib.server.tcp_server import TCPServer
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


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    HOST = "127.0.0.1"
    PORT = 25566

    server = await loop.create_server(
        lambda: TCPServer(),
        HOST, PORT)

    async with server:
        print("[+] Serveur lancé")
        motd(PORT)
        await server.serve_forever()


if __name__ == "__main__":
    print("[ ] Lancement du serveur")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nFin du programme serveur")
        loop.close()
