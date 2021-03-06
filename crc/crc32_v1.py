#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Reference:
# http://cn.voidcc.com/question/p-nbrlxzhd-kp.html
# 
# If just use crc32 in python internally, following modules are good options
#  * binascii.crc32
#  * zlib.crc32
#

import numpy as np
import crcmod

if __name__ == '__main__':

    d = np.array([
        0xaa, 0x44, 0x12, 0x1c, 0x2a, 0x00, 0x02, 0x20, 0x48, 0x00, 0x00, 0x00, 0x90,
        0xb4, 0x93, 0x05, 0xb0, 0xab, 0xb9, 0x12, 0x00, 0x00, 0x00, 0x00, 0x45, 0x61,
        0xbc, 0x0a, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x1b, 0x04, 0x50,
        0xb3, 0xf2, 0x8e, 0x49, 0x40, 0x16, 0xfa, 0x6b, 0xbe, 0x7c, 0x82, 0x5c, 0xc0,
        0x00, 0x60, 0x76, 0x9f, 0x44, 0x9f, 0x90, 0x40, 0xa6, 0x2a, 0x82, 0xc1, 0x3d,
        0x00, 0x00, 0x00, 0x12, 0x5a, 0xcb, 0x3f, 0xcd, 0x9e, 0x98, 0x3f, 0xdb, 0x66,
        0x40, 0x40, 0x00, 0x30, 0x30, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x0b, 0x0b, 0x00, 0x00, 0x00, 0x06, 0x00, 0x03
        ], dtype=np.uint8)

    d = np.arange(4, dtype=np.uint8) + 0x0a

    poly = 0xedb88320
    print(hex(poly) + ': ' + bin(poly))

    poly = 0x104C11DB7
    print(hex(poly) + ': ' + bin(poly))

    # 0x104C11DB7 = 0xedb88320 reverse and or 0x100000000

    crc32_func = crcmod.mkCrcFun(poly, initCrc=0x00000000, rev=True, xorOut=0x00000000)
    print('data\'s crc32: 0x%x'%crc32_func(bytes(d)))
