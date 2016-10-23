#!/usr/bin/env python3

import serial
import os
import sys
import time

import xts

tuner_init_one = b'\x01\x02\x01\x40\xF7'
tuner_init_two = b'\x00\x12\x01\x06\x02'

tuner_cmd_one = b'\xF5\x11\x20\x00\x00\x00\xD9'

class xtscontroller(object):
    model = b''
    serial = b''
    codeplug = b''

def monitor():
    while True:
        print("CTS:", radio.device.cts)
        print("DSR:", radio.device.dsr)
        time.sleep(0.1)

def openradio():
    device = serial.Serial("/dev/ttyUSB0")
    device.baudrate = 9600
    device.stopbits = 1
    device.parity = serial.PARITY_NONE
    device.bytesize = serial.EIGHTBITS
    device.flush()
    device.dtr = True
    device.rts = True

    return device

def main():

    device = openradio()                # Lines 3-8

    device.flush()                      # Line 9
    device.dtr = False                  # Line 10
    device.rts = False                  # Line 11

    device.dtr = True                   # Line 13
    device.rts = True                   # Line 14
    device.flush()                      # Line 15
    device.write(tuner_init_one)        # Line 16
    b = device.read(size=5)             # Line 18
    if b != tuner_init_one:
        print("Error 1: The device failed to return the same bits back")
        sys.exit()

    device.dtr = False                  # Line 20
    device.rts = False                  # Line 21
    device.dtr = True                   # Line 23
    device.rts = True                   # Line 24
    device.flush()                      # Line 25
    device.write(tuner_init_two)        # Line 26
    b = device.read(size=5)             # Line 28
    if b != tuner_init_two:
        print("Error 2: The device failed to return the same bits back")
        sys.exit()
    device.dtr = False                  # Line 30
    device.rts = False                  # Line 31
    device.dtr = False                  # Line 32
    device.rts = False                  # Line 33
    
    device.close()                      # Line 34
    device = openradio()                # Lines 35-43

    b = device.read(size=1)             # Line 45
    if b != b'\x50':
        print("Error 3: 0x50 not received")
        sys.exit()
    device.flush()                      # Line 47
    device.write(tuner_cmd_one)         # Line 48
    b = device.read(size=7)             # Line 50
    if b != tuner_cmd_one:
        print("Error 4: The device failed to return the same bits back")
        sys.exit()

    b = device.read(size=1)             # Line 53
    if b != b'\x50':
        print("Error 5: 0x50 not received")
        sys.exit()

    b = device.read(size=1)             # Line 56
    if b != b'\xFF':
        print("Error 6: 0xFF not received")
        sys.exit()
    b = device.read(size=3)             # Line 59
    if b != b'\x80\x00\x24':
        print("Failed to receive proper bits")
        sys.exit()
    radioinfo = device.read(size=36) # Line 62

    xts = xtscontroller()
    xts.serial = radioinfo[7:17]
    xts.model = radioinfo[17:29]

    print(radioinfo)
    print("Serial Number: ", xts.serial)
    print("Model Number: ", xts.model)

if __name__ == "__main__" :
    main()
