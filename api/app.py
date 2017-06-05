from flask import Flask, request, abort, g

from .utils import json_response, error_response, json_parameters
from . import executor
from .conf import LANGUAGES_CONF


app = Flask(__name__)


@app.route('/execute', methods=['POST'])
@json_parameters({
    'required': ['language'],
    'optional': ['code', 'command', 'flavor', 'files', 'produces'],
    'at_least_one_of': ['command', 'code']
})
def execute(language, **kwargs):
    try:
        command = executor.ExecutorCommand(LANGUAGES_CONF)
        result = command.execute(language, **kwargs)
        return json_response(result)
    except executor.exceptions.InvalidLanguageFlavorException:
        return error_response('Language/flavor is invalid')
