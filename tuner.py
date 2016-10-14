#!/usr/bin/env python3

import serial
import os
import sys
import time

import xts

def main():
    radio = xts.xts()
    radio.openserial('/dev/ttyUSB0')
    radio.sendecho(xts.tuner_initialize)
    print("After initialize command")
    time.sleep(0.179128)
#    radio.sendsimple(xts.tuner_first)
    radio._endlessRead()
#    radio.sendsimple(xts.tuner_second)
#    radio.sendsimple(xts.tuner_third)

if __name__ == "__main__" :
    main()
