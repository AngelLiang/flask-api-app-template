# coding=utf=8
# flake8: noqa

import unittest
from tests.web.test_auth_api import AuthAPITestCase
from tests.web.test_user_api import UserAPITestCase

# from apps.web import create_app
# app = create_app('testing')

if __name__ == '__main__':
    unittest.main(verbosity=2)