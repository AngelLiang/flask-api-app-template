# A Simple Flask API APP

This is a simple flask app template with API.

A Demo Sending Email by celery task.

## Quick Start

console 1:

```bash
# develop
pipenv install --dev
pipenv shell
flask run
```

console 2:

```bash
pipenv shell
celery worker -A apps.task.celery -l info -c 1
```

GET `http://127.0.0.1:5000/api/v1/task/send-email?email=your_email@email.com`

## Error

If you got error in celery in Windows as bellow:

```
# ...
ValueError: not enough values to unpack (expected 3, got 0)
```

You should set environment variable `FORKED_BY_MULTIPROCESSING=1`.

```PowerShell
# PowerShell
$ $env:FORKED_BY_MULTIPROCESSING=1
# check
$ $env:FORKED_BY_MULTIPROCESSING
1

# OR cmd
# set FORKED_BY_MULTIPROCESSING=1
```
