from model import Model
from view import View

class Controller:

    def __init__(self):
        self.userid = "temp"
        self.done = False
        self.model = Model()
        self.view = View()

    def run(self):
        self.init_view()
        self.init_model()
        self.register_listeners()
        self.view.get_event()

    def init_view(self):
        self.view.create_window()

    def init_model(self):
        self.model.connect()
        self.model.start_receiving_thread()
        self.model.send_message(self.userid)

    def register_listeners(self):
        self.model.register(self.handle_message)
        self.view.register(self.handle_event)

    def handle_message(self, obj, key, message):
        self.view.add_message(message)

    def handle_event(self, obj, key, message):
        if key == 'close':
            self.model.disconnect()
            self.view.close_window()
        elif key == 'input':
            self.model.send_message(message)
            self.view.clear_input()


controller = Controller()
controller.run()