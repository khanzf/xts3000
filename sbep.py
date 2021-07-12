TSTMOD = b'\x01\x02\x01\x40' # CRC is \xF7
EPREQ = b'\x00\x12\x01\x06' # CRC is \x02
READ_DATA_REQ = b'\xF5\x11'
ACK = b'\x50'

def _right_shift_as_signed(byte, bits):
    ''' Pythonic way to do a right bit shift with a signed variable '''
    result  = byte >> bits
    result |= byte & 0x80
    return result

def sbCRC(msg):
    ''' Compute SBEP CRC data '''
    n = 0
    table = b'\x00\x99\xac\x35\xc7\x5e\x6b\xf2'

    length = len(msg)

    for i, byte in enumerate(msg):
        n = byte ^ n
        a = _right_shift_as_signed(n, 1)
        a = (a >> 1)
        a = a ^ n
        b = a
        a = (a << 1) & 0xF0
        b = _right_shift_as_signed(b, 1)
        if b & 0x80:
            b = ~b & 0xFF
        n = (a + (b & 0x0F)) ^ table[n & 0x07]

    return bytes(bytearray([n]))

def checksum(msg):
    ''' Calculate the checksum '''
    total = 0
    for byte in msg:
        total = total + byte

    return bytes(bytearray([255 - (total % 256)]))
