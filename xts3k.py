#!/usr/bin/env python3

import os
import sys

import xtscontroller

def print_results(options, xts):
    ''' Print Results table '''
    if options.deviceinfo:
        print("Serial Number:\t\t\t", xts.serial)
        print("Model Number:\t\t\t", xts.model)

    if options.softspot:
        print("Radio Softspot:\t\t\t", xts.softspot, "This is incorrect")
        print("Tx High Protocol")
        print("Radio Softspot 136.025 MHz:\t", xts.softspot_high_1)
        print("Radio Softspot 142.123 MHz:\t", "[memory address undetermined]")
        print("Radio Softspot 154.225 MHz:\t", xts.softspot_high_3)

def main():
    ''' Main Function '''
    options = options_parse()

    xts = xtscontroller.xtscontroller()
    xts.initialize(options.devfile)

    b = xts.device.read(size=1)
    if b != xtscontroller.ACK:
        print("Error 3: ACK not received")
        sys.exit()

    if options.deviceinfo:
        xts.get_deviceinfo()
    xts.get_softspot()
    xts.get_softspot_high_1()

    print_results(options, xts)

def options_parse():
    ''' Parse the cmdline options '''
    usage = "usage: %prog [-d] [-z] [-s] | [-w]"
    version = "Currently not versioned"

    from optparse import OptionParser
    from optparse import OptionGroup

    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-d", "--device", dest="devfile", type="string", help="Device File ie. /dev/ttyUSB0")

    group = OptionGroup(parser, "Retrieve Device Information")
    group.add_option("-i", dest="deviceinfo", help="Device Information", action="store_true")
    group.add_option("-z", dest="zones", help="Zone Names", action="store_true")
    group.add_option("-s", dest="softspot", help="Radio Softspots", action="store_true")
    parser.add_option_group(group)

    group = OptionGroup(parser, "Write to Device")
    group.add_option("-w", "--write", dest="write", type="string", help="Unimplemented")

    (options, args) = parser.parse_args()

    if not options.devfile:
        parser.error("Must specify device file with -d/--device")
    if options.write:
       parser.error("This is currently not implemented. Exiting.")
    if not options.deviceinfo and not options.zones:
        parser.error("Did not specify any read options")

    (options, args) = parser.parse_args()
    return options

if __name__ == "__main__":
    main()
