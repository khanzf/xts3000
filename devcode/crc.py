#!/usr/bin/env python3

def right_shift_as_signed(byte, bits):
    result = byte >> bits

    # this is the same as below
    # if byte & 0x80:
    #     result |= 0x80

    result |= byte & 0x80
    
    return result

def sbCRC(msg, length):
    n = 0

    table = b'\x00\x99\xac\x35\xc7\x5e\x6b\xf2'
 
    for i, byte in enumerate(msg):
        print("Iteration: %s" % i)
        n = byte ^ n
        print("\tn: %s" % n)
        a = right_shift_as_signed(n, 1)
        print("\ta: %s" % a)
        a = (a >> 1)
        print("\ta: %s" % a)
        a = a ^ n
        print("\ta: %s" % a)
        b = a
        a = (a<<1) & 0xF0
        print("\ta: %s" % a)
        b = right_shift_as_signed(b, 1)
        print("\tb: %s" % b)
        if b & 0x80:
            b = ~b & 0xFF
        print("\tb: %s" % b)
        n = (a + (b& 0x0F)) ^ table[n & 0x07]
        print("\tn: %s" % n)
 
        print()

    return n
 
msg1 = b'\x01\x02\x01\x40' # Answer is F7
msg2 = b'\x05\x03\x00\x58\xB7\x01\x00\x01\x1D' # Answer is DC
msg3 = b'\x00\x12\x01\x06' # Answer is D9

ret1 = sbCRC(msg1, 4)
ret2 = sbCRC(msg2, 9)
ret3 = sbCRC(msg3, 4)

print("Should be F7:", bytes(bytearray([ret1])));
print("Should be DC:", bytes(bytearray([ret2])));
print("Should be 02:", bytes(bytearray([ret3])));

