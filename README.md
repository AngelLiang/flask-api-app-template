# flask api app template

Flask 搭建大型 HTTP API 后端应用的基础模板。

## 目录结构

```PowerShell
├─apps                  # APPS文件夹，存放各种APP
│  └─web                # web app，使用flask框架
│      ├─auth           # web的认证模块
│      ├─user           # web的用户模块
│      ├─utils          # web的辅助工具模块
│      ├─errors.py      # web错误处理模块
│      ├─exceptions.py  # web异常模块
│      ├─extensions.py  # web扩展模块
│      └─settings.py    # web配置
└─.flaskenv             # flask环境配置文件
```

## 快速开始

安装开发环境

```bash
# develop
pipenv install --dev
pipenv shell
flask initdata

# 启动服务器
flask run
```

## 测试

```bash
python test_app.py
```
