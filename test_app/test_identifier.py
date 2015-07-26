# -*- coding: utf-8 -*-


import unittest
import random

from app.identifier.base62 import DIGITS
from app.identifier import Identifier, InvalidChecksum



class TestIdentifier(unittest.TestCase):

    def test_random(self):
        for i in range(1000):
            self.check_identifier(Identifier.new_random())

    def check_identifier(self, identifier):
        string = str(identifier)
        self.assertTrue(all(ch in DIGITS for ch in string))
        self.assertTrue(len(string) <= 20, string)
        self.assertEqual(identifier, Identifier(string))

    def test_checksum(self):
        """
        Test that the checksum catches any single-digit mistake
        """
        identifier = Identifier.new_random()
        string = str(identifier)
        for i in range(len(string)):
            while True:
                ch = random.choice(DIGITS)
                if ch != string[i]:
                    break
            invalid = string[0:i] + ch + string[i+1:]
            self.assertEqual(len(string), len(invalid))
            with self.assertRaises(InvalidChecksum):
                Identifier(invalid)
