from lib.sockets.tcp_server import TCPServer
import asyncore

if __name__ == "__main__":
    server = TCPServer("127.0.0.1", 25566)
    asyncore.loop()