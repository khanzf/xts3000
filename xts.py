#!/usr/bin/env python3

import serial
import os
import sys

tuner_init_one =    b'\x01\x02\x01\x40\xF7' # Tuner Init
tuner_init_two =    b'\x00\x12\x01\x06\x02' # This is echoed back

tuner_inforequest = b'\xF5\x11\x20\x00\x00\x00\xD9'

class xts(object):

    def openserial(self, device):
        print("Reading: %s" % device)
        device = serial.Serial(device)
        device.stopbits = 1
        device.parity = serial.PARITY_NONE
        device.bytesize = serial.EIGHTBITS
        device.baudrate = 9600

        device.flush()
        device.dtr = True
        device.rts = True
        device.flush()
        device.dtr = False
        device.rts = False

        self.device = device

    def debug(self):
        print("\t\tDebug:\tCTS: %s\tDSR: %s\tRTS: %s" % (self.device.cts, self.device.dsr, self.device.rts))
