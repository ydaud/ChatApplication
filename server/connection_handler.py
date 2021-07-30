import logging

from server import Server
from client_info import ClientInfo
from defines import *

class ConnectionHandler(Server):

    def __init__(self):
        super().__init__()
        self.messages = []
        self.client_connections = []
    

    def run(self):
        self.start_thread(self.send_msg_to_client)
        self.start_server(self.get_msg_from_client)
    
    def add_message(self, msg):
        self.messages.append(msg)


    def get_client_info(self, conn):
        msg = self.get_message(conn)
        client = ClientInfo(msg, conn)
        return client

        
    def get_message(self, conn):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        try:
            print(msg_length)
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(msg)
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
        except socket.error as e:
            logging.error(f'socket error while sending')


    def send_msg_to_client(self):
        curr_len = len(self.messages)
        while not self.is_stopped():
            if curr_len is not len(self.messages):
                new_messages = len(self.messages) - curr_len
                for i in range(curr_len, curr_len+new_messages):
                    for client in self.client_connections:
                        msg = self.messages[i]
                        self.send_message(client.conn, msg)
                curr_len += new_messages


    def get_msg_from_client(self, conn, client_info):
        self.add_message(f'{client_info.name} has connected')
        connected = True
        while connected and not self.is_stopped():
            msg = self.get_message(conn)
            if msg is None:
                continue
            if msg == DISCONNECT_MESSAGE:
                connected = False
                self.add_message(f'[{client_info.name}] has disconnected')
            else:    
                self.add_message(f'[{client_info.name}] {msg}')

if __name__ == '__main__':
    x = ConnectionHandler()
    x.run()