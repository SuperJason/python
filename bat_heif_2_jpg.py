#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# $ sudo apt install python3-pip
# $ pip3 install pyheif
## which is successful at ubuntu 20.04
## refor to https://pypi.org/project/pyheif/
#
# date       | author | Version
# 2020-08-23 | Jason  | v1.0

import os
import datetime
from PIL import Image
import pyheif

converted_files_cnt = 0
total_heic_fils_cnt = 0

def heic2jpg(heic_file_name):
    global converted_files_cnt
    #print("heic_file_name: " + heic_file_name)
    tmp_path_name = os.path.dirname(heic_file_name)
    tmp_file_name = os.path.basename(heic_file_name)
    jpg_file_name = tmp_path_name + '/' + os.path.splitext(tmp_file_name)[0] + '.jpg'
    heif_file = pyheif.read(heic_file_name)
    image = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
        )
    image.save(jpg_file_name, "JPEG")
    converted_files_cnt = converted_files_cnt + 1
    print("[%d of %d] save file: "%(converted_files_cnt, total_heic_fils_cnt) + jpg_file_name)

def is_heic_file(file_name):
    tmp_path_name = os.path.dirname(file_name)
    tmp_file_name = os.path.basename(file_name)
    #print("tmp_path_name: " + tmp_path_name)
    #print("tmp_file_name: " + tmp_file_name)
    tmp_postfix_name = os.path.splitext(tmp_file_name)[-1]
    #print("tmp_postfix_name: " + tmp_postfix_name)
    if tmp_postfix_name == ".HEIC" or tmp_postfix_name == ".heic": 
        return True
    else:
        return False

def convert_all_files(current_dir):
    print("convert all files of dir: " + current_dir)
    dir_file_list = os.listdir(current_dir)
    #print(dir_file_list)
    for i in range(0,len(dir_file_list)):
        f = os.path.join(current_dir,dir_file_list[i])
        #print("f: " + f)
        if is_heic_file(f):
            heic2jpg(f)

if __name__ == '__main__':
    start = datetime.datetime.now()

    current_abspath = os.path.abspath(".")
    print("current_abspath: " + current_abspath) 

    value = os.popen('find ' + current_abspath + ' -iname "*.heic" -type f | wc -l')
    total_heic_fils_cnt = int(value.readlines()[0][0:-1])

    dir_file_list = os.listdir(current_abspath)
    #print("current dir file list: " + str(dir_file_list))
    root_subdir = []
    for i in range(0,len(dir_file_list)):
        path = os.path.join(current_abspath,dir_file_list[i])
        if os.path.isdir(path):
            root_subdir.append(path)

    #print("current dir subdir: " + str(root_subdir))
    convert_all_files(current_abspath)

    for i in range(0,len(root_subdir)):
        path = os.path.join(current_abspath,root_subdir[i])
        if os.path.isdir(path):
            print("deal with subdir: " + str(path))
            os.chdir(path)
            convert_all_files(path)

    print("%d .heic files convert to .jpg"%(converted_files_cnt))
    end = datetime.datetime.now()
    print("converting uses time: " + str(end - start))
    
    # find . -iname "*.heic" -type f | xargs rm -f
