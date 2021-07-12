import serial
import os
import sys
import re
import sbep

class xtscontroller(object):
    ''' XTS3000 Controller Class '''
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

    memmap = {} # from the maps file 
    memdata = {} # Stores previously read memory

    def openradio(self, devfile):
        ''' Open the Radio '''
        try:
            self.device = serial.Serial(devfile)
        except serial.serialutil.SerialException:
            print("Unable to open %s." % devfile, file=sys.stderr)
            print("This may be a permissions issue. If you are on a Unix system, " \
                  "give read/write access to %s." % devfile, file=sys.stderr)
            sys.exit(0)
        self.device.baudrate = 9600
        self.device.stopbits = 1
        self.device.parity = serial.PARITY_NONE
        self.device.bytesize = serial.EIGHTBITS
        self.device.timeout = 1 # 1 seconds seems reasonable, eh?
        self.device.flush()
        self.device.dtr = True
        self.device.rts = True

    def initialize(self, devfile):
        ''' Initialize the radio '''
        self.openradio(devfile)
        
        self.device.flush()
        self.rtsdtr_off()
        self.cmd_tstmod()
        self.cmd_epreq()
        self.rtsdtr_off()
        self.device.close()
        self.openradio(devfile)

    def rtsdtr_off(self):
        ''' Turn off rts/dtr '''
        self.device.dtr = False
        self.device.rts = False

    def rtsdtr_on(self):
        ''' Turn on rts/dtr '''
        self.device.dtr = True
        self.device.rts = True

    def cmd_tstmod(self):
        ''' Send the TSTMOD packet '''
        tstmod = sbep.TSTMOD + sbep.sbCRC(sbep.TSTMOD)

        self.rtsdtr_on()
        self.device.flush()

        self.device.write(tstmod)
        b = self.device.read(size=5)
        if b != tstmod:
            print("Error 1: The device failed to return the same bits back.", file=sys.stderr)
            print("This may be a connection issue or the device is malfunctioning. " \
                  "Try turning it off and back on.", file=sys.stderr)
            sys.exit()

        self.rtsdtr_off()

    def cmd_epreq(self):
        ''' Send the EPREQ packet '''
        epreq = sbep.EPREQ + sbep.sbCRC(sbep.EPREQ)

        self.rtsdtr_on()
        self.device.flush()
        self.device.write(epreq)
        b = self.device.read(size=5)
        if b != epreq:
            print("Error 2: The device failed to return the same bits back")
            sys.exit()
        self.rtsdtr_off()

    def get_deviceinfo(self):
        ''' Get The device serial and model number '''
        ### These Values are hard-coded, necessary to determine which map file to use 
        radioinfo = self.get_data(b'\x00\x00\x00')
        self.serial = radioinfo[7:17].decode()
        self.model = radioinfo[17:29].decode()

    def get_softspot(self):
        ''' Get the Radio Spotspot '''
        self.softspot = self._checkread('radio_softspot') - 95

    def get_softspot_high_1(self):
        ''' Get the High Tx softspots '''
        self.softspot_high_1 = self._checkread('radio_softspot_high_135.025')
        self.softspot_high_3 = self._checkread('radio_softspot_high_154.255')

    def get_zones(self):
        self.zone_1_name = self._checkread('zone_1_name')

    def _checkread(self, variable):
        ''' Private function to read from the from already saved memory or read device '''
        offset, start, end = self.memmap[variable]
        if not offset in self.memdata:
            radioinfo = self.get_data(offset)
        else:
            radioinfo = self.memmap[variable]

        if start == end:
            return radioinfo[start]
        else:
            return radioinfo[start:end]


    def memdump(self):
        ''' Dump full device memory, debugging feature '''
        for x in range(0,1048576,32):
            mem_loc = x.to_bytes(3, byteorder='big')
            data = self.get_data(mem_loc)
            print("%s: %s" % (binascii.b2a_hex(mem_loc).decode(), data))

    def get_data(self, location):
        ''' Generic function to get device data '''
        self.device.flush()
        combined = sbep.READ_DATA_REQ + b'\x20' + location
        crc_code = sbep.checksum(sbep.READ_DATA_REQ + b'\x20' + location)
        msg_crc = sbep.READ_DATA_REQ + b'\x20' + location + crc_code

        self.device.write(msg_crc)
        b = self.device.read(size=7)
        if b != msg_crc:
            print("Error 4: The device failed to return the same bits back")
            sys.exit()

        b = self.device.read(size=1)
        if b != sbep.ACK:
            print("Error 5a: ACK not received")
            sys.exit()

        b = self.device.read(size=2)
        if b != b'\xFF\x80':
            print("Error 6: READ_DATA_REPLY not received")
            sys.exit()
        b = self.device.read(size=2)
        readsize = b[1]
        radioinfo = self.device.read(size=readsize)

        return radioinfo

    def loadmemmap(self):
        ''' Load the appropriate memory map file located in $PWD/maps '''

        _start = 0

        try:
            fp = open('maps/%s.img' % self.model)
        except IOError:
            print("Unable to open maps/%s.img!", file=sys.stderr)
            print("Your XTS3000 model might not be available yet.", file=sys.stderr)
            print("Contact Farhan Khan (KM4WRZ) at khanzf@gmail.com for support.", file=sys.stderr)
            sys.exit(0)

        for line in fp:
            if _start == 0:
               _start = 1
               continue
            offset, start, end, name = line.strip().split('\t')
            self.memmap.update({name: [bytes.fromhex(offset), int(start), int(end)]})
