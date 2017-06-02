from flask import Flask, request, abort, g

from .utils import json_response, error_response
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
def execute():
    data = request.json
    language = data['language']
    flavor = data.get('flavor')
    code = data['code']
    files = data.get('files')

    try:
        result = executor.execute(code, language, flavor, files)
        return json_response(result)
    except executor.InvalidLanguageFlavorException:
        return error_response('Language/flavor is invalid')
