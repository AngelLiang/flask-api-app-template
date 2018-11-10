# coding=utf=8
# flake8: noqa

import unittest
from tests.test_api_auth import APIAuthTestCase
from tests.test_api_user import APIUserTestCase

from app import create_app

app = create_app('testing')


if __name__ == '__main__':
    unittest.main(verbosity=2)
