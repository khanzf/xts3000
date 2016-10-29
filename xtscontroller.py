#!/usr/bin/env python3

import serial
import os
import sys

class xtscontroller(object):
    # Radio Information
    model = ''
    serial = ''
    codeplug = ''

    # Reference Oscillator
    softspot = 0

    # Transmission Alignment
    ## Tx Power High
    softspot_high_1 = 0
    softspot_high_2 = 0
    softspot_high_3 = 0

def _right_shift_as_signed(byte, bits):
    result  = byte >> bits
    result |= byte & 0x80
    return result

def _sbCRC(msg):
    n = 0
    table = b'\x00\x99\xac\x35\xc7\x5e\x6b\xf2'

    length = len(msg)

    for i, byte in enumerate(msg):
        n = byte ^ n
        a = _right_shift_as_signed(n, 1)
        a = (a >> 1)
        a = a ^ n
        b = a
        a = (a << 1) & 0xF0
        b = _right_shift_as_signed(b, 1)
        if b & 0x80:
            b = ~b & 0xFF
        n = (a + (b & 0x0F)) ^ table[n & 0x07]

    return bytes(bytearray([n]))

def _checksum(msg):
    total = 0
    for byte in msg:
#        print(byte)
        total = total + byte

    return bytes(bytearray([255 - (total % 256)]))
