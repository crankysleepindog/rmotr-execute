import os
import six
import docker
import tempfile

from pathlib import Path
from requests.exceptions import ReadTimeout

from .exceptions import (InvalidLanguageException, InvalidFlavorException,
                         InvalidStrategyException)


KILLABLE_STATUS = {'created', 'restarting', 'running'}
MAX_PRODUCED_FILE_SIZE_IN_BYTES = 100 * 1024  # 100K
DOCKER_SCRIPT_TEMPLATE = """
#!/bin/sh
{command}
TEST_RESULTS=$?
""" + """
chown -R {uid}:{uid} .
exit $TEST_RESULTS
""".format(uid=os.getuid())


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
            fp.write(content or b'')

    def _write_files(self, directory, code, files):
        main_path = directory / Path('main.py')
        self._write_to_file(main_path, code)

        for _file in files:
            file_path = directory / Path(_file)
            content = files[_file]
            self._write_to_file(file_path, content)

    def _get_docker_command(self, tempdir, code=None, command=None,
                            files=None):
        script_path = tempdir / Path('rmotr_execute.sh')
        commands = [command or 'python main.py']
        if 'requirements.txt' in files:
            commands.insert(0, 'pip install -q -r requirements.txt')

        command = "\n".join(commands)
        script_content = DOCKER_SCRIPT_TEMPLATE.format(command=command)
        self._write_to_file(script_path, script_content)

        return "/bin/sh rmotr_execute.sh"

    def _get_produced_files(self, temp_path, files_produced):
        produced = {}
        for file_produced in files_produced:
            produced_path = temp_path / file_produced

            if not produced_path.exists() or not produced_path.is_file():
                produced[file_produced] = None
                continue

            with produced_path.open('r') as f:
                produced_result = f.read(MAX_PRODUCED_FILE_SIZE_IN_BYTES)

            if produced_path.stat().st_size > MAX_PRODUCED_FILE_SIZE_IN_BYTES:
                produced_result += "\n\n == TRUNCATED =="
            produced[file_produced] = produced_result
        return produced

    def execute(self, code=None, files=None, command=None, produces=None,
                docker_options=None):
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
            docker_command = self._get_docker_command(
                tempdir, code, command, files)

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
                if produces:
                    result['files'] = self._get_produced_files(
                        temp_path, produces)
            except ReadTimeout:
                result.update({
                    'successful': False,
                    'execution_error': 'timeout'
                })
                from docker.errors import APIError
                if container.status in KILLABLE_STATUS:
                    try:
                        container.kill()
                    except APIError:
                        pass

            result.update({
                'stdout': container.logs(stdout=True, stderr=False),
                'stderr': container.logs(stdout=False, stderr=True),
            })
            container.remove()
            return result
