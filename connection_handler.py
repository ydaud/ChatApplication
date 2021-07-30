import threading

from server import Server
from defines import DISCONNECT_MESSAGE

class ConnectionHandler(Server):

    def __init__(self):
        super().__init__()
        self.messages = []
        self.client_connections = []


    def run(self):
        threading.Thread(target=self.send_msg_to_client).start()
        self.start_server(self.get_msg_from_client)


    def send_msg_to_client(self):
        curr_len = len(self.messages)
        while not self.is_stopped():
            if curr_len is not len(self.messages):
                new_messages = len(self.messages) - curr_len
                for i in range(curr_len, curr_len+new_messages):
                    for client in self.connections:
                        msg = self.messages[i]
                        self.send_message(client.conn, msg)
                curr_len += new_messages


    def get_msg_from_client(self, conn, client_info):
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
