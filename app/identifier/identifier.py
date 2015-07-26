# -*- coding: utf-8 -*-
"""
Unique Identifier with Embedded Checksum

The identifier is a random number with crc-16 checksum. The random
number has 2^103 different values. Hence, there are 119 bits altogether,
or up to 20 digits in base62.

Identifiers are safe against brute-force attempts at finding a
preexisting one.

They are not resistant against birthday paradoxes, but such a
collision would not be useful to an attacker.
"""

import random

from app.identifier.base62 import b62encode, b62decode
from app.identifier.crc16 import crc16



class InvalidChecksum(Exception):
    pass


class Identifier(object):

    def __init__(self, string):
        """
        Construct a new identifier instance from a serialized identifier

        See :meth:`__str__` to serialize the identifier.
        """
        self._string = string
        number = b62decode(string)
        self._value = (number >> 16)
        self._crc = number & 0xffff
        if self._crc != crc16(str(self._value)):
            raise InvalidChecksum('Invalid checksum: {0}'.format(string))

    def __repr__(self):
        return "Identifier('{0}')".format(self._string)
        
    def __str__(self):
        return self._string

    @classmethod
    def new_random(cls):
        value = random.randint(0, 2**103)
        crc = crc16(str(value))
        identifier = cls.__new__(cls)
        identifier._value = value
        identifier._crc = crc
        identifier._string = b62encode((value << 16) + crc)
        return identifier
        
    def __eq__(self, other):
        return self._value == other._value
    

        
        
