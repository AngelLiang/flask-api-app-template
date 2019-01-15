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

## Error


Windows 环境下启动 Celery 前需要先设置下面的环境变量，不然后面执行任务时，Celery 后端会报错。

```
ValueError: not enough values to unpack (expected 3, got 0)
```


```PowerShell
# PowerShell
$ $env:FORKED_BY_MULTIPROCESSING=1
# check
$ $env:FORKED_BY_MULTIPROCESSING
1

# OR cmd
# set FORKED_BY_MULTIPROCESSING=1
````
