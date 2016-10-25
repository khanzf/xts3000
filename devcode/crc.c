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

    unsigned char msg[4] = {0x01, 0x02, 0x01, 0x40};
    unsigned char ret = sbCRC(msg, 4);

    printf("%x\n", ret);

    return 0;
}
