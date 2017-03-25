# XTS3000 CPS for Unix

Reverse-engineered Motorola XTS3000 programming software for Unix systems!

Written by Farhan (KM4WRZ) Khan - khanzf@gmail.com

## Use
Execute `./xts3000.py -h` to view a list of options.

Typically, you must specify a dev file withthe `-i` flag, such as: `-i /dev/ttyUSB0`.

## Source Files
Files explained:
* *xts3000.py* - Executed front-end program
* *xtscontroller.py* - Portable xts3000 controller code, could be used in other applications
* *maps* - Contains memory maps for various models.
* *devcode* - Code written during the reversing process

## Memory Maps
The `maps` directory contains the memory maps file specific to the XTS3000 radio models.
I am currently working on models H09KDC9PW5AN and H09KDH9PW7BN.
If you would like your device to work, please contact me at khanzf@gmail.com to arrange 
sending me a device.

## Requirements
Just needs the pySerial package. You should be able to install it with: `pip install pyserial`

## How did you write this?
Serial monitoring tools, API snoopers, IdaPro and a custom RS232 hardware tap to monitor traffic over the wire.

## License

At this stage in development, I would like to get updates and code changes back, so I am going with GPLv3. (Sorry)
Please give me your code changes! In the future, I will likely change it to a more permissive license.
