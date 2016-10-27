#include <stdio.h>

unsigned char sbCRC(const unsigned char *msgbuf, const int len) {
    const unsigned char table[8] = {0x00, 0x99, 0xac, 0x35, 0xc7, 0x5e, 0x6b, 0xf2};

    unsigned char a, b, n = 0;
    int i = 0;

    while (i < len) {
        n = (unsigned char)*(msgbuf + i) ^ n;
        a = ((unsigned char)((signed char)n >> 1) >> 1) ^ n;
        b = a;
        a = ((signed char)a << 1) & 0xF0;
        b = (signed char)b >> 1;
        if (b & 0x80) {
             b = ~b;
        }
        n = (a + (b & 0x0F)) ^ table[n & 0x07];
        i++;
    }

    return n;
}

int main() {

    unsigned char msg1[4] = {0x01, 0x02, 0x01, 0x40};
    unsigned char msg2[9] = {0x05, 0x03, 0x00, 0x58, 0xB7, 0x01, 0x00, 0x01, 0x1D};
    unsigned char msg3[4] = {0x00, 0x12, 0x01, 0x06};
    unsigned char msg4[6] = {0xf5, 0x11, 0x20, 0x00, 0x00, 0x40};

    unsigned char ret1;
    unsigned char ret2;
    unsigned char ret3;
    unsigned char ret4;

    ret1 = sbCRC(msg1, 4);
    ret2 = sbCRC(msg2, 9);
    ret3 = sbCRC(msg3, 4);
    ret4 = sbCRC(msg4, 6);

    printf("Should be F7: %X\n", ret1);
    printf("Should be DC: %X\n", ret2);
    printf("Should be 02: %X\n", ret3);
    printf("Should be 99: %X\n", ret4);

    return 0;
}
