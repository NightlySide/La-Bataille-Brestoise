import sys
import socket
import selectors
import traceback
import uuid

from lib.sockets.clientsocket import ClientMessage

sel = selectors.DefaultSelector()


def create_request(action, value):
    if action == "search":
        return dict(
            type="text/json",
            encoding="utf-8",
            content=dict(action=action, value=value),
        )
    else:
        return dict(
            type="binary/custom-client-binary-type",
            encoding="binary",
            content=bytes(action + value, encoding="utf-8"),
        )


def start_connection(host, port, request):
    addr = (host, port)
    print("Connexion à : ", addr)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = ClientMessage(sel, sock, addr, request)
    sel.register(sock, events, data=message)

HOST = "127.0.0.1"
PORT = 25566

action = "search"
value = "morpheus"
request = create_request(action, value)
start_connection(HOST, PORT, request)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            try:
                message.process_events(mask)
            except Exception:
                print(
                    "client: Erreur: exception pour",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
                message.close()
        # On vérifie bien qu'on travaille sur un socket pour continuer.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("/!\\ Attention Ctrl+C détecté, on ferme la connexion ...")
finally:
    sel.close()