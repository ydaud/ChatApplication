import socket
import threading
import logging

from defines import ADDR, HEADER, DISCONNECT_MESSAGE, FORMAT


class Model:

    def __init__(self):
        self.conn = None
        self.connected = False
        self.count = 0
        self.messages = []
        self.callbacks = []

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(ADDR)
        self.connected = True

    def disconnect(self):
        self.send_message(DISCONNECT_MESSAGE)
        self.conn.shutdown(socket.SHUT_RDWR)
        self.connected = False

    def recv_message(self):
        while self.connected:
            msg_length = self.conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = self.conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    self.connected = False
                self.notify('message', msg)

    def send_message(self, msg):
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' '*(HEADER - len(send_length))
        self.conn.send(send_length)
        self.conn.send(message)

    def start_receiving_thread(self, ):
        threading.Thread(target=self.recv_message).start()

    def register(self, callback):
        self.callbacks.append(callback)
        return callback

    def notify(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(self, *args, **kwargs)