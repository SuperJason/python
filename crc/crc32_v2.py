#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Make crc32 works in Python communicating with MCU C Programming Language Evironment
#
# If just use crc32 in python internally, following modules are good options
#  * binascii.crc32
#  * zlib.crc32

import numpy as np
import crcmod

if __name__ == '__main__':

    d = np.arange(4, dtype=np.uint8) + 0x0a

    poly = 0xedb88320
    print(hex(poly) + ': ' + bin(poly))

    poly = 0x104C11DB7
    print(hex(poly) + ': ' + bin(poly))
    crc32_func = crcmod.mkCrcFun(poly, initCrc=0xffffffff, rev=True, xorOut=0x00000000)
    print('data\'s crc32: 0x%x'%crc32_func(bytes(d)))
    print('  crc32 ^ 0xffffffff: 0x%x'%(crc32_func(bytes(d))^0xffffffff))

    # ! 'xorOut=0 ^ 0xffffffff' != xorOut=0xffffffff !
    crc32_func = crcmod.mkCrcFun(poly, initCrc=0xffffffff, rev=True, xorOut=0xffffffff)
    print('data\'s crc32: 0x%x'%crc32_func(bytes(d)))
