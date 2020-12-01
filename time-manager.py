import os
import sys
import json
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

    def get_headers(self):
        return self.header

    def is_request_method_get(self):
        return self.request_method == 'GET'

    def is_request_method_post(self):
        return self.request_method == 'POST'

    def is_request_method_options(self):
        return self.request_method == 'OPTIONS'

    def request_method_run(self):
        def request_method_get():
            self.start_response('200 OK', self.header)
            return [json.dumps(self.query_string, indent=4).encode()]

        def request_method_post():
            content_length = int(self.environ['CONTENT_LENGTH'])
            body = (self.environ['wsgi.input'].read(content_length)).decode("utf-8")
            handler = APIHandler(self.query_string, body)
            run = getattr(handler, handler.method)
            result = run()
            if len(result) > 0:
                if 'error' in result:
                    self.start_response('511 NOT OK', self.header)
                else:
                    if 'cookies' in result:
                        cookies = result.pop('cookies')
                        for key in cookies:
                            self.header.append(('Set-Cookie', '{key}={value}; /; SameSite=none; Secure'.format(key=key, value=cookies[key])))
                    self.start_response('200 OK', self.header)
                return [json.dumps(result, indent=4).encode()]
            else:
                self.start_response('500 NOT OK', self.header)
                return [json.dumps({'error': 'Something went wrong'}, indent=4).encode()]

        def request_method_options():
            self.start_response('200 OK', self.header)
            return [b'OK']

        if self.is_request_method_get():
            return request_method_get()
        elif self.is_request_method_post():
            return request_method_post()
        elif self.is_request_method_options():
            return request_method_options()

    def run(self):
        return self.request_method_run()


def run_time_manager_api(environ, start_response):
    response = Response(environ, start_response)
    return response.run()
