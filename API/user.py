import random
from Logger.handler import LoggerIt
from DBO.dbo_user import DBOUser
import datetime, uuid


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
        self.dbo_instance = DBOUser()

    def __check_pwd(self, passwords):
        if passwords[1] != '' and passwords[1] != ' ' and passwords[1] is not None:
            return passwords[0] == passwords[1]
        else:
            return False

    def __authorize(self, user):
        cookies = {
            'serial': get_new_token(),
            'token': get_new_token(),
            'email': user['email'],
            'name': user['name'],
            'sid': get_new_token(),
            'id': user['id']
        }
        self.dbo_instance.authorize_user(cookies)
        return cookies

    def check_auth(self, cookies):
        if self.dbo_instance.get_error() == {}:
            if 'email' in cookies and 'id' in cookies and 'name' in cookies:
                rows = self.dbo_instance.check_auth(cookies)
                return rows == 1
            else:
                return False

    def authentication(self, header, cookies):
        if self.check_auth(cookies):
            return (header, {
                'id': cookies['id'],
                'name': cookies['name'],
                'email': cookies['email'],
            })
        if self.dbo_instance.get_error() == {}:
            result = self.dbo_instance.get_user_with_email(self.data['email'])
            if self.dbo_instance.get_error() == {}:
                if len(result) > 0:
                    if self.__check_pwd((result[0]['password'], self.data['pwd'])):
                        cookies = self.__authorize(result[0])
                        tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
                        for key in cookies:
                            header.append(('Set-Cookie', '{key}={value}; expires={date}; Path=/; SameSite=none; Secure'.
                                           format(key=key, value=cookies[key],
                                                  date=tomorrow.strftime("%a, %d %b %Y %H:%M:%S GMT"))))
                        return (header, {
                            'id': cookies['id'],
                            'name': result[0]['name'],
                            'email': result[0]['email'],
                        })
                    else:
                        return {'error': "wrong password"}
                else:
                    return {'error': "wrong email"}
            else:
                return self.dbo_instance.get_error()
        else:
            return self.dbo_instance.get_error()

    def add(self):
        if self.dbo_instance.get_error() == {}:
            result = self.dbo_instance.get_user_with_email(self.data['email'])
            if len(result) > 0:
                return {'error': "email exist"}
            else:
                return self.dbo_instance.add(self.data)
        else:
            return self.dbo_instance.get_error()

    def logout(self, header, cookies):
        def clear_cookies(hr):
            yesterday = datetime.datetime.utcnow() - datetime.timedelta(days=1)
            for key in cookies:
                hr.append(('Set-Cookie', '{key}={value}; expires={date}; Path=/; SameSite=none; Secure'.
                           format(key=key, value='', date=yesterday.strftime("%a, %d %b %Y %H:%M:%S GMT"))))
            return hr

        if self.dbo_instance.get_error() == {}:
            result = self.dbo_instance.logout(cookies)
            if self.dbo_instance.get_error() == {}:
                return clear_cookies(header), result
            else:
                return self.dbo_instance.get_error()
        else:
            return self.dbo_instance.get_error()
