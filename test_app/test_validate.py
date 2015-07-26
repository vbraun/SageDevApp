

import unittest
from app.validate.email import is_valid_email


class TestEmailValidation(unittest.TestCase):

    def test_valid_email(self):
        self.assertTrue(is_valid_email('vbraun.name@gmail.com'))
        self.assertTrue(is_valid_email('foo@bar'))

    def test_invalid_email(self):
        self.assertFalse(is_valid_email('foo@bar@baz'))
