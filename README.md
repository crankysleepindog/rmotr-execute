# RMOTR Execute

Execute code securely through a RESTful API using Docker containers 🤖.

`POST /execute`

Parameters:

| Parameter    |                  Second Header                        | required |
| ------------ | ----------------------------------------------------- | -------- |
| **code**     | Your Code                                             | **yes**  |
| **language** | See list of available languages                       | **yes**  |
| flavor       | Special flavor of a language                          |    no    |
| files        | Extra files to add to execution. See Language details |    no    |


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

```
CODE = """
import requests
print(requests.get('https://rmotr.com/learn-python-online')
"""
```

`POST /execute`
```{
  "code": CODE,
  "language": "python",
  "files": {
    "requirements.txt": "requests==2.17.3"
  }
}```
