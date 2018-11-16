# A Simple Flask API APP

This is a simple flask app template with API.

## Quick Start

console 1:

```bash
# develop
pipenv install --dev
pipenv shell
flask initdata
flask run
```

console 2:

```bash
pipenv shell
celery worker -A apps.task.celery --loglevel=info
```

GET `http://127.0.0.1:5000/api/v1/task/async`
