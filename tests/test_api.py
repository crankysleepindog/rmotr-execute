import json
import unittest
from unittest.mock import patch

from api.app import app as api_app


class ExecuteEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.app = api_app.test_client()
        self.base_response = ({
            'execution_error': None,
            'stderr': '',
            'stdout': 'Hello World!\n',
            'successful': True}).copy()

    def post(self, *args, **kwargs):
        if 'content_type' not in kwargs:
            kwargs['content_type'] = 'application/json'
        return self.app.post('/execute', *args, **kwargs)

    def test_only_code_submitted(self):
        data = json.dumps({
            'code': 'print("Hello World!")',
            'language': 'python'
        })
        expected = self.base_response
        with patch('api.executor.execute', return_value=expected) as m:
            resp = self.post(data=data)
            self.assertEqual(resp.status_code, 200)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            m.assert_called_once_with('python', code='print("Hello World!")')

    def test_code_and_flavor_submitted(self):
        data = json.dumps({
            'code': 'print("Hello World!")',
            'language': 'python',
            'flavor': 'python-3.6-django-1.11'
        })
        expected = self.base_response
        with patch('api.executor.execute', return_value=expected) as m:
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
        with patch('api.executor.execute', return_value=expected) as m:
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
        with patch('api.executor.execute', return_value=expected) as m:
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
        with patch('api.executor.execute', return_value=expected) as m:
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
        with patch('api.executor.execute', return_value={}) as m:
            resp = self.post(data=data)
            self.assertEqual(resp.status_code, 400)

            content = json.loads(resp.get_data(as_text=True))
            self.assertEqual(content, expected)

            self.assertEqual(m.call_count, 0)
