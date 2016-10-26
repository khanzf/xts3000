#!/usr/bin/env python3

import serial
import os
import sys

class xtscontroller(object):
    model = b''
    serial = b''
    codeplug = b''

    def right_shift_as_signed(self, byte, bits):
        result  = byte >> bits
        result |= byte & 0x80
        return result

    def sbCRC(self, msg, length):
        n = 0
        table = b'\x00\x99\xac\x35\xc7\x5e\x6b\xf2'

        for i, byte in enumerate(msg):
            n = byte ^ n
            a = self.right_shift_as_signed(n, 1)
            a = (a >> 1)
            a = a ^ n
            b = a
            a = (a << 1) & 0xF0
            b = self.right_shift_as_signed(b, 1)
            if b & 0x80:
                b = ~b & 0xFF
            n = (a + (b & 0x0F)) ^ table[n & 0x07]
        return n

