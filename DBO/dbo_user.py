from DBO.handler import DBOHandler
from Logger.handler import LoggerIt


class DBOUser(DBOHandler):
    def __init__(self):
        DBOHandler.__init__(self)

    def get_user_with_email(self, email):
        sql = 'SELECT * FROM users WHERE email = "{email}"'.format(email=email)
        return self.select_data(sql)

    def authorize_user(self, data):
        self.logout(data)
        sql = 'INSERT INTO authorized_users (user_id, sid, serial, token) VALUES ({id}, "{sid}", "{serial}", "{token}")'\
            .format(id=data['id'], sid=data['sid'], serial=data['serial'], token=data['token'])
        self.insert_data(sql)

    def add(self, data):
        sql = 'INSERT INTO users (name, email, password) VALUES ("{name}", "{email}", "{password}")' \
            .format(name=data['name'], email=data['email'], password=data['pwd'])
        self.insert_data(sql)
        return {'status': 'OK'}

    def logout(self, data):
        sql = 'DELETE FROM authorized_users WHERE user_id = {id}'.format(id=data['id'])
        return self.insert_data(sql)

    def check_auth(self, cookies):
        sql = 'SELECT COUNT(user_id) as amount FROM authorized_users WHERE user_id="{id}" and sid="{sid}" and serial="{serial}" and token="{token}"'\
            .format(id=cookies['id'], sid=cookies['sid'], serial=cookies['serial'], token=cookies['token'])
        result = self.select_data(sql)
        return int(result[0]['amount'])

