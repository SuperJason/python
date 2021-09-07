#!/usr/bin/env python3
"""
    Plot dBm to Watt 
"""
import numpy as np
import matplotlib.pyplot as plt

plt.figure(num=3, figsize=(8,5))

start = -125
end = 35
length = 1600
dBm = np.linspace(start, end - (end - start)/length, length)
mW = 10**(dBm/10)

plt.plot(dBm, mW)
plt.xlim((-125, 35))
plt.ylim((0, 2000))
plt.xlabel('dBm')
plt.ylabel('mW')

for i in range(len(dBm)//10):
    print('<%3d> dBm: %11f -- mW: %18.13f'%(i, dBm[i*10], mW[i*10]))

plt.show()
