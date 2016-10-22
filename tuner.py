#!/usr/bin/env python3

import serial
import os
import sys
import time

import xts

def main():
    radio = xts.xts()
    radio.openserial('/dev/ttyUSB0')

    # Send Mode
    radio.sendecho(xts.tuner_initialize)

    # Receive Mode
    radio.recvmode()
#    radio._endlessRead()


if __name__ == "__main__" :
    main()
