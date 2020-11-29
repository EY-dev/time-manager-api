import json
from urllib import parse
from API.user import User


class APIHandler:
    def __init__(self, get_params, post_params=None, put_params=None):
        self.get_data = dict(parse.parse_qsl(get_params))
        self.method = self.get_data['method']
        if post_params is not None:
            self.post_data = json.loads(post_params)
        else:
            self.post_data = {}
        if put_params is not None:
            self.put_data = json.loads(put_params)
        else:
            self.put_data = {}

        self.full_data = {**self.get_data, **self.post_data, **self.put_data}

    def authentication(self):
        user = User(self.full_data)
        return user.authentication()

