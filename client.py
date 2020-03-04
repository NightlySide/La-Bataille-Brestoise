import socket

HOST = "127.0.0.1"
PORT = 25566

stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream.connect((HOST, PORT))
stream.sendall(b"Hello, world !")
data = stream.recv(1024)
stream.close()

print("Received : ", repr(data))