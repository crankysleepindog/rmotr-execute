import os

from .strategies import get_strategy

HOME_DIR = os.path.expanduser("~")

DEFAULT_DOCKER_OPTIONS = {
    'timeout': int(os.environ.get('EXECUTOR_OPTION_TIMEOUT', 10)),
    'mem_limit': os.environ.get('EXECUTOR_OPTION_MEM_LIMIT', '150M'),
    'cpu_period': int(os.environ.get('EXECUTOR_OPTION_CPU_PERIOD', 1000)),
    'cpu_quota': int(os.environ.get('EXECUTOR_OPTION_CPU_QUOTA', 1000)),
    'tempdir': os.environ.get('EXECUTOR_OPTION_TEMPDIR', HOME_DIR)
}


class BaseExecutorCommand(object):
    def __init__(self, language_conf, docker_options=None):
        self.language_conf = language_conf
        self._docker_options = docker_options or DEFAULT_DOCKER_OPTIONS

    def update(self, docker_options):
        self._docker_options.update(docker_options)

    def execute(self, code, language, flavor=None, files=None):
        strategy = get_strategy(self.language_conf, language, flavor)
        return strategy.execute(code, files, self._docker_options)


class ExecutorCommand(BaseExecutorCommand):
    pass
