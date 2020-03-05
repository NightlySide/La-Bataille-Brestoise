from lib.sockets.tcp_client import TCPClient

if __name__ == "__main__":
    client = TCPClient("127.0.0.1", 25566)
    client.send("Hello world")
    client.send(["a", 5, "Hello cutie ;)"])
    client.close()
