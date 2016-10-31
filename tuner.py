#!/usr/bin/env python3

import serial
import os
import sys
import time

import xtscontroller

TSTMOD = b'\x01\x02\x01\x40' # CRC is \xF7
EPREQ = b'\x00\x12\x01\x06' # CRC is \x02

READ_DATA_REQ = b'\xF5\x11'
#READ_DATA_REQ_MODEL_SERIAL = READ_DATA_REQ + b'\x20\x00\x00\x00\xD9' # D9 is the Checksum

ACK = b'\x50'

def openradio():
    device = serial.Serial("/dev/ttyUSB0")
    device.baudrate = 9600
    device.stopbits = 1
    device.parity = serial.PARITY_NONE
    device.bytesize = serial.EIGHTBITS
    device.timeout = 1 # 1 seconds seems reasonable, eh?
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

    tstmod = TSTMOD + xtscontroller._sbCRC(TSTMOD)
    
    rtsdtr_on(device)                   # Line 13-14
    device.flush()                      # Line 15

#    print("tstmod: ", tstmod)
    device.write(tstmod)        # Line 16
    b = device.read(size=5)             # Line 18
    if b != tstmod:
        print("Error 1: The device failed to return the same bits back")
        sys.exit()

    rtsdtr_off(device)                  # Line 20-21

def cmd_epreq(device):

    epreq = EPREQ + xtscontroller._sbCRC(EPREQ)

#    print("epreq: ", epreq)

    rtsdtr_on(device)                   # Line 23-24
#    device.dtr = True                   # Line 23
#    device.rts = True                   # Line 24
    device.flush()                      # Line 25
    device.write(epreq)        # Line 26
    b = device.read(size=5)             # Line 28
    if b != epreq:
        print("Error 2: The device failed to return the same bits back")
        sys.exit()
    rtsdtr_off(device)                  # Line 30-31

def get_deviceinfo(device, xts):
#    crc_ret = xtscontroller._sbCRC(READ_DATA_REQ + b'\x20\x00\x00\x00')
#    print("deviceinfo", crc_ret)
    radioinfo = get_data(device, b'\x20\x00\x00\x00') # Get 32 bytes, from 00, D9 is the checksum

    xts.serial = radioinfo[7:17].decode()
    xts.model = radioinfo[17:29].decode()

def get_softspot(device, xts):
    radioinfo = get_data(device, b'\x20\x00\x00\x60') # Get 32 byte
    xts.softspot = radioinfo[9] - 95

def get_softspot_high_1(device, xts):
    radioinfo = get_data(device, b'\x20\x00\x00\x80')
    xts.softspot_high_1 = radioinfo[18]

    radioinfo = get_data(device, b'\x20\x00\x00\xA0')
    xts.softspot_high_3 = radioinfo[10]

def get_data(device, location):
    ''' Gets serial and model number '''
#    sys.exit()
    device.flush()                      # Line 47
    combined = READ_DATA_REQ + location
#    print("Combined:", combined)
    crc_code = xtscontroller._checksum(READ_DATA_REQ + location)
#    print("CRC:", crc_code)
    msg_crc = READ_DATA_REQ + location + crc_code

#    print(msg_crc)

#    device.write(READ_DATA_REQ_MODEL_SERIAL)         # Line 48
    device.write(msg_crc) #b'\x20\x00\x00\x00\xD9')
    b = device.read(size=7)             # Line 50
    if b != msg_crc: #b'\x20\x00\x00\x00\xD9':
        print("Error 4: The device failed to return the same bits back")
        sys.exit()

    b = device.read(size=1)             # Line 53
    if b != ACK:
        print("Error 5a: ACK not received")
        sys.exit()

    b = device.read(size=2)             # Line 56
    if b != b'\xFF\x80':
        print("Error 6: READ_DATA_REPLY not received")
        sys.exit()
    b = device.read(size=2)             # Line 59
    readsize = b[1]
    radioinfo = device.read(size=readsize) # Line 62

    return radioinfo
#    xts.serial = radioinfo[7:17].decode()
#    xts.model = radioinfo[17:29].decode()

def main():

    options = options_parse()

    xts = xtscontroller.xtscontroller()

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
        print("Error 3: ACK not received")
        sys.exit()

    get_deviceinfo(device, xts)
    get_softspot(device, xts)
    get_softspot_high_1(device, xts)
#    mem = get_data(device, b'\x20\x00\x00\x00\xD9')
#    print(mem)
#    mem = get_data(device, b'\x20\x00\x00\x00\xD9')

    print("Serial Number:\t\t\t", xts.serial)
    print("Model Number:\t\t\t", xts.model)
    print()

    print("Radio Softspot:\t\t\t", xts.softspot, "This is incorrect")
    print()

    print("Tx High Protocol")
    print("Radio Softspot 136.025 MHz:\t", xts.softspot_high_1)
    print("Radio Softspot 142.123 MHz:\t", "[memory address undetermined]")
    print("Radio Softspot 154.225 MHz:\t", xts.softspot_high_3)

def options_parse():
#    interface_types = ['stdio', 'tun', 'socks5']
#    transport_types = ['tcp', 'http', 'dns', 'udp', 'icmp']
    usage = "usage: %prog [-d] [-r variable] [-w variable=value] [...]"
    version = "Currently not versioned"

    from optparse import OptionParser
    from optparse import OptionGroup

    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-d", "--device", dest="devfile", type="string", help="Device File ie. /dev/ttyUSB0", default="/dev/ttyUSB0")

    group = OptionGroup(parser, "Retrieve Device Information")
    group.add_option("-r", "--read", dest="read", type="string", help="device - Device Information | zone - Zone List", default="all")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Write to Device")
    group.add_option("-w", "--write", dest="write", type="string", help="Unimplemented")

    (options, args) = parser.parse_args()

#    parser.error("Testing")

    if not options.devfile:
        parser.error("Must specify device file with -d/--device")

    if options.write:
       parser.error("This is currently not implemented. Exiting.")

    if not options.read and not options.write:
        parser.error("Must select either --read or --write")

    print("Read value:", options.read)

    (options, args) = parser.parse_args()

    return options

if __name__ == "__main__":
    main()
