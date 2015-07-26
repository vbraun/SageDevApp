# -*- coding: utf-8 -*-
"""
Base 62 Encoding

Lower case letters + upper case letters + numbers = 62 distinct
characters.
"""



import sys
 
DIGITS="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
REVERSE = dict((c, i) for (i, c) in enumerate(DIGITS))
BASE=len(DIGITS)
 
 
def b62encode(num):
    if num < 0:
        raise ValueError("number must be nonnegative")
    s = []
    while True:
        num, r = divmod(num, BASE)
        s.append(DIGITS[r])
        if num == 0:
            break
    return ''.join(reversed(s))


def b62decode(string):
    n = 0
    for ch in string:
        n = n * BASE + REVERSE[ch]
    return n

 
 
 
