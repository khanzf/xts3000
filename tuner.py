#!/usr/bin/env python3

import serial
import os
import sys

import xts

def main():
    radio = xts.xts()
    radio.openserial('/dev/ttyUSB0')
    radio.sendecho(xts.tuner_initialize)

if __name__ == "__main__" :
    main()
