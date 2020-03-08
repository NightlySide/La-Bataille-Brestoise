from lib.server.tcp_server import TCPServer
import asyncio


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: TCPServer(),
        '127.0.0.1', 25566)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    print("[ ] Lancement du serveur")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nFin du programme serveur")
        loop.close()
