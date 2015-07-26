# -*- coding: utf-8 -*-
"""
CRC-16
"""

table = None
constant = 0xA001

def _initialize_table():
    global table
    table = []
    for crc in range(256):
        for j in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ constant
            else:
                crc = (crc >> 1)
        table.append(crc)
    table = tuple(table)

_initialize_table()


def crc16(string):
    crc = 0x0000
    for ch in string:
        d = ord(ch)
        tmp = crc ^ d
        rot = crc >> 8
        crc = rot ^ table[tmp & 0x00ff]
    return crc

