#!/usr/bin/env python3

import serial
import os
import sys
import time

TSTMOD = b'\x01\x02\x01\x40\xF7'
EPREQ = b'\x00\x12\x01\x06\x02'

READ_DATA_REQ = b'\xF5\x11'
READ_DATA_REQ_MODEL_SERIAL = READ_DATA_REQ + b'\x20\x00\x00\x00\xD9'

ACK = b'\x50'

class xtscontroller(object):
    model = b''
    serial = b''
    codeplug = b''

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

def rtsdtr_off(device):
    device.dtr = False
    device.rts = False

def rtsdtr_on(device):
    device.dtr = True
    device.rts = True

def cmd_tstmod(device):
    rtsdtr_on(device)                   # Line 13-14
    device.flush()                      # Line 15
    device.write(TSTMOD)        # Line 16
    b = device.read(size=5)             # Line 18
    if b != TSTMOD:
        print("Error 1: The device failed to return the same bits back")
        sys.exit()

    rtsdtr_off(device)                  # Line 20-21

def cmd_epreq(device):
    rtsdtr_on(device)                   # Line 23-24
#    device.dtr = True                   # Line 23
#    device.rts = True                   # Line 24
    device.flush()                      # Line 25
    device.write(EPREQ)        # Line 26
    b = device.read(size=5)             # Line 28
    if b != EPREQ:
        print("Error 2: The device failed to return the same bits back")
        sys.exit()
    rtsdtr_off(device)                  # Line 30-31

def get_info(device, xts):
    ''' Gets serial and model number '''
    device.flush()                      # Line 47
    device.write(READ_DATA_REQ_MODEL_SERIAL)         # Line 48
    b = device.read(size=7)             # Line 50
    if b != READ_DATA_REQ_MODEL_SERIAL:
        print("Error 4: The device failed to return the same bits back")
        sys.exit()

    b = device.read(size=1)             # Line 53
    if b != ACK:
        print("Error 5: 0x50 not received")
        sys.exit()

    b = device.read(size=2)             # Line 56
    if b != b'\xFF\x80':
        print("Error 6: READ_DATA_REPLY not received")
        sys.exit()
    b = device.read(size=2)             # Line 59
    readsize = b[1]
    radioinfo = device.read(size=readsize) # Line 62

    xts.serial = radioinfo[7:17].decode()
    xts.model = radioinfo[17:29].decode()

def main():

    xts = xtscontroller()

    device = openradio()                # Lines 3-8

    device.flush()                      # Line 9
    rtsdtr_off(device)                  # Line 10-11
#    device.dtr = False                  # Line 10
#    device.rts = False                  # Line 11

    cmd_tstmod(device)
    cmd_epreq(device)

    rtsdtr_off(device)                  # Line 32-33
#    device.dtr = False                  # Line 30
#    device.rts = False                  # Line 31
#    device.dtr = False                  # Line 32
#    device.rts = False                  # Line 33
    
    device.close()                      # Line 34
    device = openradio()                # Lines 35-43

    b = device.read(size=1)             # Line 45
    if b != ACK:
        print("Error 3: 0x50 not received")
        sys.exit()

    get_info(device, xts)

    print("Serial Number:\t", xts.serial)
    print("Model Number:\t", xts.model)

if __name__ == "__main__" :
    main()
