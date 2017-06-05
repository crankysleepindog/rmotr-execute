import json
import unittest
from unittest.mock import patch

from api.app import app as api_app

DEFAULT_MOCK_EXEC = 'api.executor.ExecutorCommand.execute'


class ExecuteEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = api_app.test_client()
        self.base_response = ({
            'execution_error': None,
            'stderr': '',
            'stdout': 'Hello World!\n',
            'successful': True}).copy()

    def _request(self, method, *args, **kwargs):
        method = method.lower()
        if 'content_type' not in kwargs:
            kwargs['content_type'] = 'application/json'
        return getattr(self.app, method)('/execute', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self._request('post', *args, **kwargs)

    def options(self, *args, **kwargs):
        return self._request('options', *args, **kwargs)

    def test_only_code_submitted(self):
        data = json.dumps({
            'code': 'print("Hello World!")',
            'language': 'python'
        })
        expected = self.base_response
        with patch(DEFAULT_MOCK_EXEC, return_value=expected) as m:
            resp = self.post(data=data)
            self.assertEqual(resp.status_code, 200)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            m.assert_called_once_with('python', code='print("Hello World!")')

    def test_CORS_headers_for_POST(self):
        data = json.dumps({
            'code': 'print("Hello World!")',
            'language': 'python'
        })
        expected = self.base_response
        with patch(DEFAULT_MOCK_EXEC, return_value=expected) as m:
            resp = self.post(data=data)
            self.assertEqual(resp.status_code, 200)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            m.assert_called_once_with('python', code='print("Hello World!")')

            headers = resp.headers
            self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
            self.assertTrue('POST' in headers['Access-Control-Allow-Methods'])
            self.assertEqual(
                headers['Access-Control-Allow-Headers'], 'Content-Type')

    def test_CORS_headers_for_OPTIONS(self):

        expected = self.base_response
        with patch(DEFAULT_MOCK_EXEC, return_value=expected) as m:
            resp = self.app.options('/execute')
            self.assertEqual(
                resp.status_code, 200, resp.get_data())

            self.assertEqual(m.call_count, 0)

            headers = resp.headers
            self.assertTrue('Access-Control-Allow-Origin' in headers)
            self.assertTrue('Access-Control-Allow-Methods' in headers)
            self.assertTrue('Access-Control-Allow-Headers' in headers)

            self.assertEqual(headers['Access-Control-Allow-Origin'], '*')
            self.assertTrue('POST' in headers['Access-Control-Allow-Methods'])
            self.assertEqual(
                headers['Access-Control-Allow-Headers'], 'Content-Type')

    def test_code_and_flavor_submitted(self):
        data = json.dumps({
            'code': 'print("Hello World!")',
            'language': 'python',
            'flavor': 'python-3.6-django-1.11'
        })
        expected = self.base_response
        with patch(DEFAULT_MOCK_EXEC, return_value=expected) as m:
            resp = self.post(data=data)
            self.assertEqual(resp.status_code, 200)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            m.assert_called_once_with(
                'python', code='print("Hello World!")',
                flavor='python-3.6-django-1.11')

    def test_code_and_files_are_submitted(self):
        data = {
            'code': 'print("Hello World!")',
            'language': 'python',
            'files': {
                'requirements.txt': 'requests',
                'tests.py': 'assert True, "Oh no!"'
            }
        }
        expected = self.base_response
        with patch(DEFAULT_MOCK_EXEC, return_value=expected) as m:
            resp = self.post(data=json.dumps(data))
            self.assertEqual(resp.status_code, 200)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            m.assert_called_once_with(
                'python', code='print("Hello World!")',
                files=data['files'])

    def test_code_and_produces_are_submitted(self):
        data = {
            'code': 'print("Hello World!")',
            'language': 'python',
            'produces': ['report.json']
        }
        expected = self.base_response
        with patch(DEFAULT_MOCK_EXEC, return_value=expected) as m:
            resp = self.post(data=json.dumps(data))
            self.assertEqual(resp.status_code, 200)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            m.assert_called_once_with(
                'python', code='print("Hello World!")',
                produces=['report.json'])

    def test_only_command_submitted(self):
        data = json.dumps({
            'language': 'python',
            'command': 'python -c "print(\'Hello World!\')"'
        })
        expected = self.base_response
        with patch(DEFAULT_MOCK_EXEC, return_value=expected) as m:
            resp = self.post(data=data)
            self.assertEqual(resp.status_code, 200)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            m.assert_called_once_with(
                'python', command='python -c "print(\'Hello World!\')"')

    def test_no_code_or_command_is_submitted(self):
        data = json.dumps({
            'language': 'python',
        })
        expected = {
            'error': ('At least one of the following parameters must '
                      'be provided: COMMAND or CODE')
        }
        with patch(DEFAULT_MOCK_EXEC, return_value={}) as m:
            resp = self.post(data=data)
            self.assertEqual(resp.status_code, 400)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            self.assertEqual(m.call_count, 0)
