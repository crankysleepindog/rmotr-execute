from .executor.strategies import PythonCodeExecutorStrategy


LANGUAGES_CONF = {
    'python': {
        'flavors': {
            # ========== Testing ==========
            'python-2.7-testing': 'python-2.7-testing',
            'python-3.5-testing': 'python-3.5-testing',
            'python-3.6-testing': 'python-3.6-testing',

            # ========== Django ==========
            # 2.7
            'python-2.7-django-1.10': 'python-2.7-django-1.10',
            'python-2.7-django-1.11': 'python-2.7-django-1.11',
            # 3.5
            'python-3.5-django-1.10': 'python-3.5-django-1.10',
            'python-3.5-django-1.11': 'python-3.5-django-1.11',
            # 3.6
            'python-3.6-django-1.10': 'python-3.6-django-1.10',
            'python-3.6-django-1.11': 'python-3.6-django-1.11',
        }
    }
}
