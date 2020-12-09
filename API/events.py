from DBO.dbo_events import DBOEvents


class Events:
    def __init__(self, data):
        self.method = data['method']
        self.data = data
        self.dbo_instance = DBOEvents()

    def get_events(self):
        if self.dbo_instance.get_error() == {}:
            result = self.dbo_instance.get_events(self.data['id'], self.data['date'])
            if self.dbo_instance.get_error() == {}:
                return result
            else:
                return {'error': self.dbo_instance.get_error()}
        else:
            return {'error': self.dbo_instance.get_error()}
