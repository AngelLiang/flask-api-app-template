# coding=utf-8
"""
使用Apache24部署时用到
"""

import os
import sys


curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, curr_dir)

# 假设主目录下有虚拟环境 .venv
# 字符串前面加r，表示禁止反斜杠转义
activate_this = curr_dir + r"\.venv\Scripts\activate_this.py"

with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# 加载.env环境变量
from flask.cli import load_dotenv
load_dotenv()

from app import create_app

app = create_app("production")
application = app

if __name__ == '__main__':
    application.run()
