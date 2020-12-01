import random
from Logger.handler import LoggerIt
from DBO.handler import DBOHandler


def get_new_token():
    string = 'k9OfAtPl43jQUtzZzKpuDiZbaUFZwmwx6PtkIBlfz1Un1zrD27ETe7kd5maSj'
    token = ''
    for i in range(0, 32):
        token = token + string[random.randint(0, 60)]
    return token


class User:
    def __init__(self, data):
        self.method = data['method']
        self.data = data

    def __check_pwd(self, passwords):
        if passwords[1] != '' and passwords[1] != ' ' and passwords[1] is not None:
            return passwords[0] == passwords[1]
        else:
            return False

    def __authorize(self, user):
        cookies = {
            'serial': get_new_token(),
            'token':  get_new_token(),
            'email':  user['email'],
            'name':   user['name'],
            'id':     user['id']
        }
        return cookies

    def authentication(self):
        dbo = DBOHandler()
        if dbo.get_error() == {}:
            result = dbo.get_user_with_email(self.data['user']['email'])
            if dbo.get_error() == {}:
                if len(result) > 0:
                    if self.__check_pwd((result[0]['password'], self.data['user']['pwd'])):
                        return {
                            'name':   result[0]['name'],
                            'email':  result[0]['email'],
                            'cookies': self.__authorize(result[0])
                        }
                    else:
                        return {'error': "wrong password"}
                else:
                    return {'error': "wrong email"}
            else:
                return dbo.get_error()
        else:
            return dbo.get_error()
