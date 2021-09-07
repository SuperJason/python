#!/usr/bin/env python3
"""
    Plot Watt to dBm
"""
import numpy as np
import matplotlib.pyplot as plt

start = 0
end = 2000
length = 2000

mW = np.linspace(start, end - (end - start)/length, length)
dBm = 10*np.log10(mW)

plt.figure(num=3, figsize=(8,5))
plt.plot(mW, dBm)
plt.xlim((0, 2000))
plt.ylim((-120, 35))
plt.xlabel('mW')
plt.ylabel('dBm')

for i in range(len(mW)//10):
    print('<%3d> mW: %11f -- dBm: %11f'%(i, mW[i*10], dBm[i*10]))

plt.show()
