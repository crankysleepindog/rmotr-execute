from flask import Flask, request, abort, g

from .utils import json_response, error_response, json_parameters
from . import executor
from .conf import LANGUAGES_CONF


app = Flask(__name__)


@app.route('/execute', methods=['POST', 'OPTIONS'])
@json_parameters({
    'required': ['language'],
    'optional': ['code', 'command', 'flavor', 'files', 'produces'],
    'at_least_one_of': ['command', 'code']
})
def execute(language, **kwargs):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'PUT, GET, POST, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    if request.method == 'OPTIONS':
        return json_response("", headers=headers)

    try:
        command = executor.ExecutorCommand(LANGUAGES_CONF)
        result = command.execute(language, **kwargs)
        return json_response(result, headers=headers)
    except executor.exceptions.InvalidLanguageFlavorException:
        return error_response('Language/flavor is invalid')
