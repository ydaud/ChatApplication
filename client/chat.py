import uuid
import sys

import PySimpleGUI as sg

from client.client import *

class ChatApp:
    
    def __init__(self):
        self.userid_prefix = "rand"
        self.userid = f'{self.userid_prefix}-{str(uuid.uuid4())}'

        self.conn = None
        self.messages = []
        self.output = ""


    def run(self):
        self.create_window()
        self.init_connection()
        self.run_loop()
        self.close_window()
        

    def on_message(self, message):
        self.messages.append(message)
        self.output += message + '\n'
        self.window["-OUTPUT-"].update(self.output)


    def run_loop(self):
        while True:
            event, values = self.window.read()
            if event == "Exit" or event == sg.WIN_CLOSED:
                self.conn.disconnect()
                break
            elif event == "SEND":
                msg = values["-INPUT-"]
                if msg == ':q':
                    self.conn.disconnect()
                    break;
                self.conn.send_message(msg)
                self.window["-INPUT-"].update('')


    def init_connection(self):
        self.conn = Client('hello')
        self.conn.connect()
        self.conn.start_client(self.on_message)
        self.conn.send_message('yahya')


    def create_window(self):
        layout = [
            [
                sg.Output(size=(110, 20), font=('Helvetica 10'), key="-OUTPUT-")
            ],
            [
                sg.Text("Send:"),
                sg.In(size=(98, 1), enable_events=True, key="-INPUT-", focus=True),
                sg.Button("SEND")
            ]
        ]

        self.window = sg.Window("Chat App", layout)
        self.window.read()


    def close_window(self):
        self.window.close()

    
if __name__ == '__main__':
    app = ChatApp()
    app.run()
