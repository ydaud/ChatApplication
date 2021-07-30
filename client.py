import socket
import threading
import logging

from defines import ADDR, HEADER, DISCONNECT_MESSAGE, FORMAT


class Client:

    def __init__(self, client_name):
        logging.basicConfig(filename='logs/client.log', level=logging.DEBUG,
                            format='%(asctime)s:%(message)s')
        self.client_name = client_name
        self.conn = None
        self.connected = False
        self.count = 0

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(ADDR)
        self.connected = True

    def disconnect(self):
        self.send_message(DISCONNECT_MESSAGE)
        self.conn.shutdown(socket.SHUT_RDWR)
        self.connected = False

    def recv_message(self, on_message):
        while self.connected:
            msg_length = self.conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    self.connected = False
                on_message(msg)

    def send_message(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)

    def start_client(self, on_message):
        logging.info('[STARTING] client is starting ...')
        threading.Thread(target=self.recv_message, args=[on_message]).start()
