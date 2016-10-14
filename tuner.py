#!/usr/bin/env python3

import serial
import os
import sys

import xts

def main():
    radio = xts.xts()
    radio.openserial('/dev/ttyUSB0')
    print(radio.radioserial)
    print("Sending initiate command")
    print("The size is: %d" % len(xts.tuner_initialize))
    radio.sendecho(xts.tuner_initialize)
    print("After initialize command")
#    radio.sendsimple(xts.tuner_first)
    radio._endlessRead()
#    radio.sendsimple(xts.tuner_second)
#    radio.sendsimple(xts.tuner_third)

if __name__ == "__main__" :
    main()
