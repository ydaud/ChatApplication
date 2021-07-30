import uuid
import six

import PySimpleGUI as sg

from client import Client

class ChatApp:

    def __init__(self):
        self.userid_prefix = "rand"
        self.userid = self.getusername()
        self.messages = []
        self.output = ""
        self.window = None
        self.conn = None


    def run(self):
        self.create_window()
        self.init_connection()
        self.run_loop()
        self.close_window()


    def getusername(self):
        user_input = six.moves.input('Name: ')
        if user_input:
            return user_input
        return f'{self.userid_prefix}-{str(uuid.uuid4())}'


    def on_message(self, message):
        self.messages.append(message)
        self.output += f'{message}\n'
        self.window["-OUTPUT-"].update(self.output)


    def run_loop(self):
        while True:
            event, values = self.window.read()
            if event == "SEND":
                msg = values["-INPUT-"]
                if msg == ':q':
                    self.conn.disconnect()
                    break
                self.conn.send_message(msg)
                self.window["-INPUT-"].update('')
            elif event in ('Exit', sg.WIN_CLOSED):
                self.conn.disconnect()
                break


    def init_connection(self):
        self.conn = Client(self.userid)
        self.conn.connect()
        self.conn.start_client(self.on_message)
        self.conn.send_message(self.userid)


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
