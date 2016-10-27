#!/usr/bin/python3

# 1 Byte cheksum code

def checksum(msg):
    total = 0
    for byte in msg:
#        byte = ord(byte)
        print(byte)
        total = total + byte

    return bytes(bytearray([255 - (total % 256)]))
#    return ord(b'\xFF') - ord(total % 256)

msg4 = b'\xf5\x11\x20\x00\x00\x00' # Answer is D9
#print("Should be D9:", bytes(bytearray([ret4])));
ret = checksum(msg4)

print(ret)
