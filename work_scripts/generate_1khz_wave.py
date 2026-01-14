#
# 2026-1-14 由chatgpt生成
#

import numpy as np
from scipy.io.wavfile import write

# 设置采样率和频率
sampling_rate = 44100  # 采样率 44.1kHz
frequency = 1000       # 频率 1kHz
duration = 5           # 持续时间 5秒

# 生成时间轴
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# 生成正弦波
waveform = np.sin(2 * np.pi * frequency * t)

# 将波形转换为 16 位 PCM 格式（整数）
waveform_int16 = np.int16(waveform * 32767)

# 保存为 WAV 文件
write('sine_wave_1kHz.wav', sampling_rate, waveform_int16)

print("WAV 文件已保存为 'sine_wave_1kHz.wav'")

