# RMOTR Execute

Execute code securely through a RESTful API using Docker containers 🤖.

`POST /execute`

Parameters:

| Parameter    |                  Second Header                        | required |
| ------------ | ----------------------------------------------------- | -------- |
| **language** | See list of available languages                       | **yes**  |
| code         | Your Code                                             | no(\*)    |
| command      | Commandto execute                                     | no(\*)    |
| flavor       | Special flavor of a language                          |    no    |
| files        | Extra files to add to execution. See Language details |    no    |

(\*) You have to provide at least one of these parameters, either `code` or `command`. If you pass `command` you can specifically provide the command to execute and have more control. See [Advanced Examples](#examples) below.

## Languages

Available languages:

### Python 🐍

**Language:** `python` (will use `python-2.7-clean`)

**Flavors:**

* Pure Python
  * `python-2.7-clean`: Python 2.7 - Clean (**DEFAULT**)
  * `python-3.5-clean`: Python 3.5 - Clean
  * `python-3.6-clean`: Python 3.6 - Clean
* Django
  * `python-2.7-django-1.10`: Python 2.7 - Django 1.10
  * `python-2.7-django-1.11`: Python 2.7 - Django 1.11
  * `python-3.5-django-1.10`: Python 3.5 - Django 1.10
  * `python-3.5-django-1.11`: Python 3.5 - Django 1.11
  * `python-3.6-django-1.10`: Python 3.6 - Django 1.10
  * `python-3.6-django-1.11`: Python 3.6 - Django 1.11

**Files:**
If your files object contains a file `'requirements.txt'` the service will install the requirements on the container before executing your code. Please keep in mind that execution might timeout just due to the dependency installation.

Your `$CODE` as an example:

```python
import requests  # `requests` dependency required
print(requests.get('https://rmotr.com/learn-python-online')
```

```bash
$ curl -X POST /execute \
  -H 'content-type: application/json' \
  -d '{
    "code": $CODE,
    "language": "python",
    "files": {
      "requirements.txt": "requests==2.17.3"
    }'
```

# Examples

### Basics

**Print Hello World**
```bash
$ curl -X POST /execute \
  -H 'content-type: application/json' \
  -d '{
    "code": "print('Hello World')",
    "language": "python"
  }'
```

**Print Django version**
```bash
$ curl -X POST /execute \
  -H 'content-type: application/json' \
  -d '{
    "code": "import django\nprint(django.__version__)",
    "flavor": "python-3.6-django-1.11",
    "language": "python"
  }'
```


**Install Dependencies**
```bash
$ curl -X POST /execute \
  -H 'content-type: application/json' \
  -d '{
    "code": "import requests\nprint(requests.get('https://google.com').status_code)",
    "files": {
     "requirements.txt": "requests==requests==2.17.3"
    },
    "language": "python"
  }'
```

**Run python command directly**
```bash
$ curl -X POST /execute \
  -H 'content-type: application/json' \
  -d '{
    "command": "python -c \"print('hello')\"",
    "language": "python"
  }'
```



### Advanced

**Run py.test and receive a JSON report**

```python
# tests.py
def test_simple_addition():
    assert 1 + 1 == 3
```

```bash
$ curl -X POST /execute \
  -H 'content-type: application/json' \
  -d '{
    "command": "py.test --json=report.json tests.py",
    "files": {
     "tests.py": $TESTS
    },
    "produces": ["report.json"],
    "flavor": "python-3.6-testing",
    "language": "python"
  }'
```
