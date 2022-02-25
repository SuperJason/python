#!/usr/bin/env python3
"""
    Analyze dts and dtsi file including relationship
"""

import os.path
import re
import os 

def find_file_from_path(filename, path):
    retval = None
    for dirpath, dirnames, files in os.walk(path):
        if filename in files:
            #print('dirpath: ' + str(dirpath))
            #print('dirname: ' + str(dirname))
            #print('files: ' + str(files))
            retval = dirpath + '/' + filename
            break
    return retval

def analyze_including_relationship(path, filename, level=0):

    basename = os.path.basename(filename)
    in_file = open(filename, 'rt')
    in_lines = in_file.readlines()
    in_file.close()

    for i in range(len(in_lines)):
        line = in_lines[i]
        ptn = r'#include[ \t]+\"(.*.dtsi?)\"'
        m = re.match(ptn, line)
        if m:
            #print('m: ' + str(m))
            #print('m.groups(): ' + str(m.groups()))
            sub_filename = os.path.basename(m.group(1))
            #print('sub_filename: ' + sub_filename)
            get_sub_file = find_file_from_path(sub_filename, path)
            if get_sub_file != None:
                print('\t' * level + get_sub_file[len(path) + 1:])
                analyze_including_relationship(path, get_sub_file, level + 1)
            else:
                print('\t' * level + '### file: ' + sub_filename + ' not found!')


if __name__ == '__main__':
    
    kernel_src_path = 'private/msm-mobvoi-cw'
    in_dts_file_name = 'private/msm-mobvoi-cw/devicetree/qcom/monaco-idp-v1.dts'
    #in_dts_file_name = 'private/msm-mobvoi-cw/devicetree/qcom/monaco-idp-v1-overlay.dts'
    in_dts_abspath_file_name = os.path.abspath(in_dts_file_name)
    in_dts_file_basename = os.path.basename(in_dts_abspath_file_name)
    in_dts_file_dirname = os.path.dirname(in_dts_abspath_file_name)

    #print('abspath: ' + in_dts_abspath_file_name)
    #print('basename: ' + in_dts_file_basename)
    #print('dirname: ' + in_dts_file_dirname)
    print('--------------------')
    print('kernel_src_path: ' + kernel_src_path)
    print('  core dts file: ' + find_file_from_path(in_dts_file_basename, kernel_src_path))

    in_dts_file = open(in_dts_abspath_file_name, 'rt')
    in_dts_lines = in_dts_file.readlines()
    in_dts_file.close()

    print('--------------------')
    for i in range(len(in_dts_lines)):
        line = in_dts_lines[i]
        ptn = r'[ \t]*model[ \t]*=[ \t]*\"(.*)\".*'
        m = re.match(ptn, line)
        if m:
            #print('m.groups(): ' + str(m.groups()))
            #print('m.group(0): ' + m.group(0))
            model_str = m.group(1)
            print('Machine model: ' + model_str)

    print('--------------------')
    analyze_including_relationship(kernel_src_path, in_dts_abspath_file_name)
