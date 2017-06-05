import os

from .strategies import get_strategy
from .languages import LANGUAGES_CONF
from copy import deepcopy

HOME_DIR = os.path.expanduser("~")

DEFAULT_DOCKER_OPTIONS = {
    'timeout': int(os.environ.get('EXECUTOR_OPTION_TIMEOUT', 10)),
    'mem_limit': os.environ.get('EXECUTOR_OPTION_MEM_LIMIT', '150M'),
    'cpu_period': int(os.environ.get('EXECUTOR_OPTION_CPU_PERIOD', 1000)),
    'cpu_quota': int(os.environ.get('EXECUTOR_OPTION_CPU_QUOTA', 1000)),
    'tempdir': os.environ.get('EXECUTOR_OPTION_TEMPDIR', HOME_DIR)
}


class BaseExecutorCommand(object):
    def __init__(self, language_conf=None, use_default_languages=True,
                 docker_options=None):
        self.use_default_languages = use_default_languages
        self._docker_options = docker_options or DEFAULT_DOCKER_OPTIONS

        if not language_conf and not use_default_languages:
            raise ValueError("No languages to configure executor.")

        if use_default_languages:
            self.languages = self._merge_languages(language_conf)
        else:
            self.languages = language_conf

    def _merge_languages(self, language_conf):
        language_conf = language_conf or {}
        languages = deepcopy(LANGUAGES_CONF)
        for lang, conf in language_conf.items():
            if lang in languages and 'flavors' in conf:
                languages[lang]['flavors'].update(conf['flavors'])
        return languages

    def update(self, docker_options):
        self._docker_options.update(docker_options)

    def execute(self, language, code=None, flavor=None, files=None,
                command=None, produces=None):
        strategy = get_strategy(self.languages, language, flavor)
        return strategy.execute(
            code, files, command, produces, self._docker_options)


class ExecutorCommand(BaseExecutorCommand):
    pass
