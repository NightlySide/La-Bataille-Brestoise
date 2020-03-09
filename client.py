import asyncio
from lib.client.global_client_registry import GCR
from lib.client.tcp_client import TCPClientProtocol


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    GCR.setEventLoop(loop)
    try:
        loop.run_until_complete(TCPClientProtocol.create("TEST", "127.0.0.1", 25566))
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nFin du programme client")
        loop.close()