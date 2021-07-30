import socket
import threading 
import signal
import logging 

from PySimpleGUI.PySimpleGUI import MsgBox

from defines import ADDR, HEADER, FORMAT, DISCONNECT_MESSAGE
from client_info import ClientInfo

class Server:

    def __init__(self):
        self.server = None
        self.exit_event = threading.Event()

        self.init_logger()

    
    def init_logger(self):
        logging.basicConfig(filename='logs/server.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')


    def setup_exit_event(self):
        def signal_handler(signum, frame):
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
            conn, addr = self.server.accept()
            self.on_connect(conn, on_message)


    def start_thread(self, target):
        self.resp_thread = threading.Thread(target=target)
        self.resp_thread.start()
            

    def bind_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.server.listen()


    def on_connect(self, conn, on_message):
        client_info = self.get_client_info(conn)
        self.client_connections.append(client_info)
        threading.Thread(target=on_message, args=(conn, client_info)).start()

