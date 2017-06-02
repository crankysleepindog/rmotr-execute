import six
import docker
import tempfile

from pathlib import Path
from requests.exceptions import ReadTimeout

from .exceptions import (InvalidLanguageException, InvalidFlavorException,
                         InvalidStrategyException, TimeoutExecutorException)

KILLABLE_STATUS = {'created', 'restarting', 'running'}


def _get_strategy_for_flavor(language_map, flavor):
    flavor_data = language_map['flavors'][flavor]
    if not isinstance(flavor_data, six.string_types):
        return flavor_data

    # Image + Base Strategy for language
    return flavor_data, language_map.get('executor_strategy')


def get_strategy(languages_conf, language, flavor=None):
    if language not in languages_conf:
        raise InvalidLanguageException('{} not found'.format(language))

    language_map = languages_conf[language]
    flavor = flavor or language_map.get('default')
    if not flavor or flavor not in language_map['flavors']:
        raise InvalidFlavorException(
            '{} flavor in {} not found'.format(flavor or 'default', language))

    docker_image, StrategyClass = _get_strategy_for_flavor(
        language_map, flavor)
    if not StrategyClass:
        raise InvalidStrategyException()

    strategy = StrategyClass(docker_image)
    return strategy


class BaseCodeExecutorStrategy(object):
    def __init__(self, docker_image):
        self.docker_image = docker_image

    def execute(self, code, files=None, docker_options=None):
        raise NotImplementedError()


class PythonCodeExecutorStrategy(BaseCodeExecutorStrategy):
    ALLOWED_FILES = ['requirements.txt']

    def __init__(self, docker_image):
        super(PythonCodeExecutorStrategy, self).__init__(docker_image)

    def _write_to_file(self, path, content):
        if isinstance(content, six.text_type):
            content = content.encode('utf-8')

        with path.open('wb') as fp:
            fp.write(content)

    def _write_files(self, directory, code, files):
        main_path = directory / Path('main.py')
        self._write_to_file(main_path, code)

        for allowed_file in self.ALLOWED_FILES:
            if allowed_file in files:
                file_path = directory / Path(allowed_file)
                content = files[allowed_file]
                self._write_to_file(file_path, content)

    def _get_docker_command(self, code, files):
        commands = ['python main.py']
        if 'requirements.txt' in files:
            commands.insert(0, 'pip install -q -r requirements.txt')

        if len(commands) == 1:
            return commands[0]

        return '/bin/sh -c "{chained_commands}"'.format(
            chained_commands=" && ".join(commands))

    def execute(self, code, files=None, docker_options=None):
        files = files or {}
        docker_options = docker_options or {}

        _tempdir = docker_options.get('tempdir')
        _mem_limit = docker_options.get('mem_limit')
        _cpu_period = docker_options.get('cpu_period')
        _cpu_quota = docker_options.get('cpu_quota')
        _timeout = docker_options.get('timeout')

        client = docker.from_env()

        with tempfile.TemporaryDirectory(dir=_tempdir) as tempdir:
            temp_path = Path(tempdir)
            self._write_files(temp_path, code, files)
            docker_command = self._get_docker_command(code, files)

            container = client.containers.run(
                self.docker_image,
                docker_command,
                detach=True,
                volumes={
                    str(temp_path): {'bind': '/app'}
                },
                mem_limit=_mem_limit,
                cpu_period=_cpu_period,
                cpu_quota=_cpu_quota,
                working_dir='/app')

            result = {
                'execution_error': None
            }
            try:
                exit_status = container.wait(timeout=_timeout)
                result.update({
                    'successful': exit_status == 0
                })
            except ReadTimeout:
                result.update({
                    'successful': False,
                    'execution_error': 'timeout'
                })
                from docker.errors import APIError
                if container.status in KILLABLE_STATUS:
                    try:
                        container.kill()
                    except APIError as e:
                        raise ValueError(
                            'Invalid status: %s' % container.status)

            result.update({
                'stdout': container.logs(stdout=True, stderr=False),
                'stderr': container.logs(stdout=False, stderr=True),
            })
            container.remove()
            return result
