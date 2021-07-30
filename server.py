import socket
import threading
import signal
import logging

from defines import ADDR, HEADER, FORMAT
from client_info import ClientInfo

class Server:

    def __init__(self):
        self.messages = []
        self.connections = []
        self.server = None
        self.exit_event = threading.Event()

        logging.basicConfig(filename='logs/server.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


    def setup_exit_event(self):
        def signal_handler(_, __):
            self.exit_event.set()
        signal.signal(signal.SIGTSTP, signal_handler)


    def is_stopped(self):
        return self.exit_event.is_set()


    def start_server(self, on_message):
        self.bind_server()
        self.setup_exit_event()
        self.accept_connections(on_message)


    def accept_connections(self, on_message):
        while True:
            conn, _ = self.server.accept()
            self.on_connect(conn, on_message)


    def bind_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.server.listen()


    def add_message(self, msg):
        self.messages.append(msg)


    def get_message(self, conn):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        try:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            return msg
        except ValueError:
            return None

    def send_message(self, conn, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER - len(send_length))
        try:
            conn.send(send_length)
            conn.send(message)
        except socket.error:
            logging.error('socket error while sending message')


    def get_client_info(self, conn):
        msg = self.get_message(conn)
        client = ClientInfo(msg, conn)
        self.add_message(f'{client.name} has connected')
        return client


    def on_connect(self, conn, on_message):
        client_info = self.get_client_info(conn)
        self.connections.append(client_info)
        threading.Thread(target=on_message, args=(conn, client_info)).start()
