import pymysql.cursors
import json
import os


class DBOHandler:
    def __init__(self):
        self.settings = ''
        self.connection = ''
        self.error = {}
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'db.config'), 'r') as file:
            try:
                self.config_db = json.loads(file.read())
            except Exception as error:
                self.error = {'error': str(error)}

    def connect_db(self):
        try:
            self.connection = pymysql.connect(host=self.config_db["host"],
                                              user=self.config_db["user"],
                                              password=self.config_db["password"],
                                              db=self.config_db["db"],
                                              port=int(self.config_db["port"]),
                                              charset=self.config_db["charset"],
                                              cursorclass=pymysql.cursors.DictCursor)
        except Exception as error:
            self.error = {'error': str(error)}

    def get_info_server(self):
        self.connect_db()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute('SELECT VERSION()')
                return cursor.fetchone()
        finally:
            self.connection.close()

    def get_error(self):
        return self.error

    def select_data(self):
        self.connect_db()
        try:
            with self.connection.cursor() as cursor:
                sql = 'SELECT id, email  FROM users WHERE id = 1'
                cursor.execute(sql)
                result = cursor.fetchone()
        except Exception as error:
            result = {'error': str(error)}
        finally:
            self.connection.close()

        return result
