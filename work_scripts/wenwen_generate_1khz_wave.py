# -*- coding: utf-8 -*-
from __future__ import print_function, division

import wave
import numpy as np

#import matplotlib.pylab as plt

def save_wave(filename, data, rate, ch):
    # open wav file
    f = wave.open(filename, "wb")

    # Config channels, bits and samplerate
    f.setnchannels(ch)
    f.setsampwidth(2)
    f.setframerate(rate)
    # transfor wav_data to binary data and write to file
    f.writeframes(data.tostring())
    f.close()

def main():
    '''
        Generate Wave
    '''
    framerate = 48000
    duration = 1 # seconds
    freq = 1000
    channels = 2

    # Generate 1kHz frequency wave
    n = round(duration * framerate)
    ts = np.arange(n) / framerate
    ts = np.asarray(ts)
    phases = 2 * np.pi * freq * ts 
    data = np.sin(phases) * 30000
    data = data.astype(np.short)

    #ch0 = data
    ch1 = data
    ch0 = np.zeros(n, dtype=np.short)

    wave_data = np.arange(n * channels, dtype=np.short)
    wave_data[0::2] = ch0
    wave_data[1::2] = ch1

    save_wave(filename='sound_1khz.wav', data=wave_data, rate=framerate, ch=channels)

    #plt.plot(ts[0:200], wave_data[0:200])
    #plt.show()
    #print(data[0:20])
    #print(wave_data[0:20])

if __name__ == '__main__':
    main()
