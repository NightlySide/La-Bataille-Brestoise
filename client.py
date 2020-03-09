from lib.client.tcp_client import TCPClient
import asyncio
import sys


async def main():
    await client.connect()
    print(await client.send({"action": "echo", "msg": "Hello world!"}))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    client = TCPClient("127.0.0.1", 25566)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nFin du programme client")
        loop.close()

