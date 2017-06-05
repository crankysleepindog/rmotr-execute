import simplejson as json
from functools import wraps
from flask import make_response, request

JSON_MIME_TYPE = 'application/json'


def json_response(data=None, status=200, headers=None):
    data = data or {}
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    return make_response(json.dumps(data), status, headers)


def error_response(error, status=400, headers=None):
    return json_response({'error': error}, status, headers)


class JSONParametersDecorator(object):
    def __init__(self, param_definition):
        self.params = param_definition

    def __call__(self, fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            args = list(args)
            data = request.json

            for required_param_name in self.params['required']:
                param = data.get(required_param_name)
                if not param:
                    return error_response(
                        'Missing param: %s' % required_param_name)
                args.append(param)

            for optional_param_name in self.params['optional']:
                param = data.get(optional_param_name)
                if param:
                    kwargs[optional_param_name] = param

            if 'at_least_one_of' in self.params:
                at_least_one_params = [kwargs.get(v) for v in
                                       self.params['at_least_one_of']]

                if not any(at_least_one_params):
                    error = ("At least one of the following parameters "
                             "must be provided: {}").format(
                                 ' or '.join([p.upper() for p in
                                              self.params['at_least_one_of']]))

                    return error_response(error)

            return fn(*args, **kwargs)

        return decorated


json_parameters = JSONParametersDecorator
