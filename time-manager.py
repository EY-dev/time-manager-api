import os
import sys
import json

sys.path.insert(0, os.path.dirname(__file__))


def set_headers(url):
    header = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', url),
        ('Access-Control-Allow-Headers', 'origin, x-requested-with, content-type, X-Auth-Token, Accept'),
        ('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS'),
        ('Access-Control-Allow-Credentials', 'true')
    ]
    return header


def run_time_manager_api(environ, start_response):
    header = set_headers(environ['HTTP_ORIGIN'])

    if environ['REQUEST_METHOD'] == 'POST':
        content_length = int(environ['CONTENT_LENGTH'])
        start_response('200 OK', header)
        body = (environ['wsgi.input'].read(content_length)).decode("utf-8")
        return [json.dumps(body, indent=4).encode()]

    if environ['REQUEST_METHOD'] == 'GET':
        start_response('200 OK', header)
        return [json.dumps(environ['QUERY_STRING'], indent=4).encode()]

    if environ['REQUEST_METHOD'] == 'OPTIONS':
        start_response('200 OK', header)
        return [b'OK']
