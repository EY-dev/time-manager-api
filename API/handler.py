import json
from urllib import parse
from API.user import User
from API.events import Events
from Logger.handler import LoggerIt


class APIHandler:
    def __init__(self, get_params, header=None, cookie=None, post_params=None, put_params=None):
        self.__get_data = dict(parse.parse_qsl(get_params))
        self.__method = self.__get_data['method']
        self.__header = header
        self.__cookie = cookie

        if post_params is not None:
            self.__post_data = json.loads(post_params)
        else:
            self.__post_data = {}
        if put_params is not None:
            self.__put_data = json.loads(put_params)
        else:
            self.__put_data = {}

        self.full_data = {**self.__get_data, **self.__post_data, **self.__put_data}

    def authentication(self):
        user = User(self.full_data)
        result = user.authentication(self.__header, self.__cookie)
        self.__header = result[0]
        return result[1]

    def add_user(self):
        new_user = User(self.full_data)
        result = new_user.add()
        if 'error' in result:
            return result
        else:
            return self.authentication()

    def logout(self):
        user = User(self.full_data)
        result = user.logout(self.__header, self.__cookie)
        self.__header = result[0]
        if result[1] is None:
            return {'status': 'OK'}
        else:
            return result[1]

    def get_header(self):
        return self.__header

    def get_method(self):
        return self.__method

    def get_events(self):
        events = Events(self.__get_data)
        return events.get_events()
