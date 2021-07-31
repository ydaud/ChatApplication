from layouts import MAIN_LAYOUT

import PySimpleGUI as sg

class View:

    def __init__(self):
        self.output = ""
        self.window = None
        self.callbacks = []

    def create_window(self):
        self.window = sg.Window("Chat App", MAIN_LAYOUT)
        self.window.read()

    def close_window(self):
        self.window.close()

    def clear_input(self):
        self.window["-INPUT-"].update('')

    def add_message(self, message):
        self.output += f'{message}\n'
        self.window["-OUTPUT-"].update(self.output)

    def get_event(self):
        while True:
            event, values = self.window.read()
            if event == "SEND":
                msg = values["-INPUT-"]
                if msg == ':q':
                    self.notify('close', None)
                    break
                self.notify('input', msg)
            elif event in ('Exit', sg.WIN_CLOSED):
                self.notify('close', None)
                break

    def register(self, callback):
        self.callbacks.append(callback)
        return callback

    def notify(self, *args, **kwargs):
        for callback in self.callbacks:
            callback(self, *args, **kwargs)