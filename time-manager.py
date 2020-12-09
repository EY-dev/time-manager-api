import os
import sys
import json

from Logger.handler import LoggerIt

from API.handler import APIHandler

sys.path.insert(0, os.path.dirname(__file__))


class Response:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.http_origin = environ['HTTP_ORIGIN']
        self.request_method = environ['REQUEST_METHOD']
        self.query_string = environ['QUERY_STRING']
        self.start_response = start_response
        self.header = [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', self.http_origin),
            ('Access-Control-Allow-Headers', 'origin, x-requested-with, content-type, X-Auth-Token, Accept'),
            ('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS'),
            ('Access-Control-Allow-Credentials', 'true')
        ]
        try:
            if 'HTTP_COOKIE' in environ:
                str_cookie = environ['HTTP_COOKIE'].replace(' ', '')
                self.cookie = dict(item.split("=") for item in str_cookie.split(";"))
            else:
                self.cookie = {}
        except Exception as err:
            self.cookie = {}

    def get_headers(self):
        return self.header

    def GET(self):
        handler = APIHandler(get_params=self.query_string, header=self.header)
        try:
            run = getattr(handler, handler.get_method())
            result = run()
            self.start_response('200 OK', self.header)
        except Exception:
            self.start_response('501 NOT OK', self.header)
            result = {}
        return [json.dumps(result, indent=4).encode()]

    def POST(self):
        content_length = int(self.environ['CONTENT_LENGTH'])
        body = (self.environ['wsgi.input'].read(content_length)).decode("utf-8")
        handler = APIHandler(get_params=self.query_string, header=self.header, cookie=self.cookie, post_params=body)
        run = getattr(handler, handler.get_method())
        result = run()
        if len(result) > 0:
            if 'error' in result:
                self.start_response('400 NOT OK', self.header)
            else:
                self.header = handler.get_header()
                self.start_response('200 OK', self.header)
            return [json.dumps(result, indent=4).encode()]
        else:
            self.start_response('500 NOT OK', self.header)
            return [json.dumps({'error': 'Something went wrong'}, indent=4).encode()]

    def OPTIONS(self):
        self.start_response('200 OK', self.header)
        return [b'OK']

    def run(self):
        return getattr(self, self.request_method)()


def run_time_manager_api(environ, start_response):
    response = Response(environ, start_response)
    return response.run()
