import socket
import threading

PORT = 5050
FORMAT = 'utf-8'
HEADER = 64
SERVER = "IP Address"
DISCONNECT = "bye"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_close = False
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def receiver():
    while True:
        msg = client.recv(4096)
        if msg and len(msg) > 0:
            print(msg)


while True:
    receiver_thread = threading.Thread(target=receiver)
    receiver_thread.start()
    inp = input()
    send(inp)
