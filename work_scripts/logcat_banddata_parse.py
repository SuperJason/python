#!/usr/bin/env python3
"""
    This scripts is created for parsing bandmode sleep data.
"""

import re
import sys
import os
import time
import numpy as np

def banddata_extract(lines):
    pattern = r'^([0-9\- :\.]{21}).*health.bg.band_sync: +bandData: +([0-9a-fA-F]*)$'
    all_data = ''
    for line in lines:
        #print(line)
        match = re.match(pattern, line)
        if match:
            #print(' -- match.groups(): ' + str(match.groups()))
            time = match.group(1)
            data = match.group(2)
            all_data = all_data + data
            #print('time: ' + time)
            #print('data: ' + data)

    #print('all_data(%d): '%(len(all_data)) + all_data)
    return all_data

def convert_4_u8_to_u32(data):
    u32 = (data[0] & 0x000000ff) | ((data[1]<<8) & 0x0000ff00) | ((data[2]<<16) & 0x00ff0000) | ((data[3]<<24) & 0xff000000)
    return u32

def parse_data(data):
    bin_data = np.zeros(len(data)>>1, dtype=np.uint8)
    #print('data: ' + data[0:2])
    #bin_data[0] = int(data[0:2], 16)
    #print('bin_data[0] = ' + str(hex(bin_data[0])))
    for i in range(len(data)>>1):
        bin_data[i] = int(data[i*2:i*2+2], 16)
        #print('bin_data[%d] = %s'%(i, hex(bin_data[i])))

    #print('data lenght: %d'%(len(data)))
    print('bin data lenght: %d'%(len(bin_data)))
    #data_u32_1 = convert_4_u8_to_u32(bin_data[0:4])
    #data_u32_2 = convert_4_u8_to_u32(bin_data[4:8])
    #print('data_u32_1: %s'%(hex(data_u32_1)))
    #print('data_u32_2: %s'%(hex(data_u32_2)))
    #print('time: %d(%s)'%(data_u32_1, hex(data_u32_1)))
    #print('steps: %d(%s)'%((data_u32_2 & 0x0003ffff), hex(data_u32_2 & 0x0003ffff)))
    #print('activity type: %d(%s)'%(((data_u32_2 & 0x00f80000) >> 19), hex((data_u32_2 & 0x00f80000) >> 19)))
    #print('heart rate: %d(%s)'%(((data_u32_2 & 0xff000000) >> 24, hex((data_u32_2 & 0xff000000) >> 24))))
    data_dict_list = []
    for i in range(len(bin_data)>>3):
        data_u32_1 = convert_4_u8_to_u32(bin_data[i*8:i*8+4])
        data_u32_2 = convert_4_u8_to_u32(bin_data[i*8+4:i*8+8])
        data_dict = {'time':0, 'step':0, 'activity':0, 'heart_rate':0}
        data_dict['time'] = data_u32_1
        data_dict['steps'] = data_u32_2 & 0x0003ffff
        data_dict['activity'] = (data_u32_2 & 0x00f80000) >> 19
        data_dict['heart_rate'] = (data_u32_2 & 0xff000000) >> 24
        data_dict_list.append(data_dict)

    print('data_dict_list lenght: %d'%(len(data_dict_list)))
    return len(data_dict_list), data_dict_list

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
    else:
        input_file_name='l'

    if not os.path.exists(input_file_name):
        print('input file: ' + input_file_name + ' doesn\'t exist!!')
        exit(1)

    print('input file: ' + input_file_name)
    input_file = open(input_file_name, 'rt')

    lines = input_file.readlines()
    input_file.close()

    data = banddata_extract(lines)
    data_points_num, data_points = parse_data(data)
    activity_dict = {
            0:'kIdle',
            1:'kWalking',
            2:'kFastWalking',
            3:'kRunning',
            4:'kInsane',
            5:'kBiking',
            6:'kStatic',
            7:'kAwake',
            8:'kREM',
            9:'kLightSleep',
            10:'kDeepSleep',
            11:'kSwimming',
            28:'kDataStepCount',
            29:'kDataOffBodyDetect',
            30:'kDataHeartRate',
            31:'kActivityUndefined'
            }
    for i in range(data_points_num):
        print_str = ' [%5.d]'%(i+1)
        print_str += ' - %s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data_points[i]['time'])))
        print_str += ' - steps: %5.d'%(data_points[i]['steps'])
        print_str += ' - heart_rate: %3.d'%(data_points[i]['heart_rate'])
        print_str += ' - activity: %s'%(activity_dict[data_points[i]['activity']])
        print(print_str)

    #print(time.time())
    #print(time.localtime(time.time()))
    #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data_points[i]['time'])))
