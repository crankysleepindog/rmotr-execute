import six
import tempfile
import docker
from pathlib import Path

from . import images

def language_is_valid(language, flavor=None):
    pass

def execute(code, language, flavor=None, files=None, extra_requirements=None):
    pass


def execute(code, language, flavor=None, files=None, extra_requirements=None):
    if isinstance(code, six.text_type):
        code = code.encode('utf-8')

    with tempfile.TemporaryDirectory() as tempdir:
        temp_path = Path(tempdir)
        main_path = temp_path / Path('main.py')
        with main_path.open('wb') as fp:
            fp.write(code)

        client = docker.from_env()
        docker_image = images.get_image(language, flavor)
        try:
            container = client.containers.run(
                docker_image, '/bin/bash -c "pip install -r requirements.txt && python app.py"',
                detach=False,
                stderr=True,
                volumes={
                    PWD: {'bind': WORKING_DIR}
                },
                working_dir=WORKING_DIR)
            print("Putitto")

            # print("CONTAINER: %s" % container.status)
            # import time
            # # time.sleep(5)
            #
            # print(container.logs(stdout=True, stderr=False).decode('utf-8'))
            # print("------------------------------------")
            # print(container.logs(stdout=False, stderr=True).decode('utf-8'))
        except docker.errors.ContainerError as e:


if __name__ == '__main__':
    execute("print('hello %s' % (1+1))", 'python')
