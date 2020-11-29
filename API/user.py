from DBO.handler import DBOHandler


class User:
    def __init__(self, data):
        self.method = data['method']
        self.data = data

    def authentication(self):
        return self.data
