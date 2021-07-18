import socket
import threading

PORT = 5050
FORMAT = 'utf-8'
HEADER = 64
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "IP Address"
DISCONNECT = "bye"
c = threading.Condition()

ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

connection_list = []
ran = False


def send_to_all(msg):
    print('SENDING to all connected clients')
    if not ran:
        for c in connection_list:
            c.send(msg.encode(FORMAT))
    return


def handle_client(conn, addr):
    print('NEW CONECTION {}'.format(addr))
    connected = True
    global ran
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg:
            msg = int(msg)
            msg = conn.recv(msg).decode(FORMAT)
            if msg == DISCONNECT:
                connected = False
            print('{} says {}'.format(addr, msg))
            ran = False
            c.acquire()
            send_to_all(msg)
            ran = True
            c.release()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        connection_list.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("ACTIVE CONNECTIONS {}".format(threading.activeCount() - 1))
        print('Connection list '+ str(len(connection_list)))

print('STARTING server is starting')
start()
