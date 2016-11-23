from crier.script import Script
import abc
import crier
import json
import os
import platform
import pwd
import requests
import tempfile
import unittest

__all__ = ['BaseAPITest']


class BaseAPITest(unittest.TestCase):
    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.api_host = os.environ['PTERO_SHELL_COMMAND_HOST']
        self.api_port = os.environ['PTERO_SHELL_COMMAND_PORT']

        if platform.system() == 'Darwin':
            self.job_working_directory = tempfile.mkdtemp(dir='/private/tmp')
        else:
            self.job_working_directory = tempfile.mkdtemp()

    def tearDown(self):
        os.rmdir(self.job_working_directory)

    def create_webhook_server(self, response_codes):
        scripts = [Script(status_code=rc) for rc in response_codes]
        server = crier.Webserver(scripts=scripts)
        server.start()
        return server

    @property
    def jobs_url(self):
        return 'http://%s:%s/v1/jobs' % (self.api_host, self.api_port)

    @property
    def job_user(self):
        return pwd.getpwuid(os.getuid())[0]

    def get(self, url, **kwargs):
        return _deserialize_response(requests.get(url, params=kwargs))

    def patch(self, url, data):
        return _deserialize_response(
            requests.patch(url, headers={'content-type': 'application/json'},
                           data=json.dumps(data)))

    def post(self, url, data):
        return _deserialize_response(
            requests.post(url, headers={'content-type': 'application/json'},
                          data=json.dumps(data)))

    def put(self, url, data):
        return _deserialize_response(
            requests.put(url, headers={'content-type': 'application/json'},
                         data=json.dumps(data)))

    def delete(self, url):
        return _deserialize_response(requests.delete(url))


def _deserialize_response(response):
    response.DATA = response.json()
    return response
