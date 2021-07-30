import uuid

class ClientInfo:

    def __init__(self, name, conn):
        self.prefix = 'client'
        self.id = f'{self.prefix}-{str(uuid.uuid4())}'
        self.name = name
        self.conn = conn

