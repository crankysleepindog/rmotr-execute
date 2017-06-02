from .strategies import PythonCodeExecutorStrategy

# ======================
# ==== Example Conf ====
# ======================
# SAMPLE_IMAGE = {
#     'python': {
#         'executor_strategy': PythonCodeExecutorStrategy,
#         'default': 'python-2.7-clean',
#         'flavors': {
#             'python-2.7-clean': ('python:2.7-alpine', OtherPythonStrategy),
#             'python-3.5-clean': 'python:3.5-alpine',
#         }
#     },
#     'javascript': {
#         'executor_strategy': JavascriptCodeExecutor,
#         'default': 'node-v8-clean',
#         'flavors': {
#             'python-2.7-clean': ('python:2.7-alpine', OtherPythonStrategy),
#             'python-3.5-clean': 'python:3.5-alpine',
#         }
#     },
# }

LANGUAGES_CONF = {
    'python': {
        'executor_strategy': PythonCodeExecutorStrategy,
        'default': 'python-2.7-clean',
        'flavors': {
            'python-2.7-clean': 'python:2.7-alpine',
            'python-3.5-clean': 'python:3.5-alpine',
            'python-3.6-clean': 'python:3.6-alpine',

            'python-2.7-django-1.10': 'images/python/django/py-2.7/dj-1.10',
            'python-2.7-django-1.11': 'images/python/django/py-2.7/dj-1.11',

            'python-3.5-django-1.10': 'images/python/django/py-3.5/dj-1.10',
            'python-3.5-django-1.11': 'images/python/django/py-3.5/dj-1.11',

            'python-3.6-django-1.10': 'images/python/django/py-3.6/dj-1.10',
            'python-3.6-django-1.11': 'images/python/django/py-3.6/dj-1.11',
        }
    }
}
