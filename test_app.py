# coding=utf=8

import unittest
from tests.test_api_auth import APIAuthTestCase

from app import create_app, db
from app.models import User

app = create_app('testing')


if __name__ == '__main__':
    unittest.main(verbosity=2)
