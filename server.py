import socket

HOST = "127.0.0.1"
PORT = 25566

# IPV4 / TCP
stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream.bind((HOST, PORT))
stream.listen()
conn, addr = stream.accept()
with conn:
    print("Connected by ", addr)
    while True:
        data = conn.recv(1024)
        if not data:
            break
        conn.sendall(data)

stream.close()