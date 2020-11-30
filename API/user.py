from DBO.handler import DBOHandler


class User:
    def __init__(self, data):
        self.method = data['method']
        self.data = data

    def authentication(self):
        dbo = DBOHandler()
        if dbo.get_error() == {}:
            return dbo.get_info_server()
        else:
            return dbo.get_error()
