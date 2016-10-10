#!/usr/bin/env python3

import serial
import os
import sys

tuner_initialize =  b'\x01\x02\x01\x40\xF7' # Tuner Init
tuner_first =       b'\x05\x03\x00\x58\xB7\x01\x00\x01\x1D\xDC'
tuner_second =      b'\x01\x03\x00\x40\xEE\x01\x00\x1D\xB5'
tuner_third =       b'\x00\x00\x12\x12\x01\x01\x06\x06\x02\x02\x50' # This is echoed back
tuner_inforequest = b'\xF5\x11\x20\x00\x00\x00\xD9'

class xts:

    def openserial(self, device):
        self.radioserial = serial.Serial(device)

    def sendecho(self, cmd):
        for byte in cmd:
            self.radioserial.write(bytes(byte))
            echobyte = self.radioserial.read() # Read one byte
            if echobyte is not byte:
                raise Exception('The radio did not echo back the command')

    def sendsimple(self, cmd):
        self.radioserial.write(cmd)
