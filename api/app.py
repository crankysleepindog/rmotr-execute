from flask import Flask, request, abort, g

from .utils import json_response, error_response, json_parameters
from . import executor


app = Flask(__name__)
{
    'code': '...',
    'language': 'python',
    'flavor': 'python-2',
    'files': {
        'tests.py': '...',
        'data.json': '...'
    }
}


@app.route('/execute', methods=['POST'])
@json_parameters({
    'required': ['code', 'language'],
    'optional': ['flavor', 'files']
})
def execute(code, language, **kwargs):
    try:
        result = executor.execute(code, language, **kwargs)
        return json_response(result)
    except executor.exceptions.InvalidLanguageFlavorException:
        return error_response('Language/flavor is invalid')
