# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 19:55:13 2022

@author: JasonFu
"""

import os
import hashlib
import time
import string

def scan_folder(path, checksum_enable=False, save_to_file=False):
    file_cnt = 0
    dirpath_cnt = 0
    total_size = 0
    pre_start_time = time.time()
    file_list = []
    dirpath_list = []
    output_file_lines = []

    for dirpath,dirnames,filenames in os.walk(path):
        line = ("---- %s --"%(dirpath))
        output_file_lines.append(line + '\n')
        print(line)
        dirpath_cnt += 1
        dirpath_list.append(dirpath)
        for filename in filenames:
            full_filename = os.path.join(dirpath,filename)
            if os.path.isfile(full_filename):
                statinfo = os.stat(full_filename)
                size = statinfo.st_size
                mtime = statinfo.st_mtime
                total_size += size
                file_list.append((full_filename, size, mtime))
                file_cnt += 1
    
    pre_end_time = time.time()
    cost_secends = int(pre_end_time - pre_start_time)
    cost_time_h = cost_secends // 60 // 60
    cost_time_m = cost_secends // 60 % 60
    cost_time_s = cost_secends % 60
    line = "---- Prescan time cost: %ds -- %d:%d:%d --"%(cost_secends, cost_time_h, cost_time_m, cost_time_s)
    output_file_lines.append(line + '\n')
    print(line)
    line = "---- Prescan file count: %d(%d)"%(file_cnt, len(file_list))
    output_file_lines.append(line + '\n')
    print(line)
    line = "---- Prescan dirpath count: %d(%d)"%(dirpath_cnt, len(dirpath_list))
    output_file_lines.append(line + '\n')
    print(line)
    line = "---- Prescan total size: %d"%(total_size)
    output_file_lines.append(line + '\n')
    print(line)  

    if save_to_file == True:
        valid_chars ="-_%s%s" % (string.ascii_letters, string.digits)
        output_file_name = ''.join(c if c in valid_chars else '_' for c in path)
        if checksum_enable == True:
            output_file_name += '_disk_folder_files_with_sha256sum.txt'
        else:
            output_file_name += '_disk_folder_files_with.txt'
        f = open(output_file_name, mode='w+', encoding='utf-8')
        f.writelines(output_file_lines)

    start_time = time.time()
    accumulate_size = 0
    current_file_cnt = 0
    total_size_g = total_size / 1024 / 1024 / 1024;
    for filename, size, mtime in file_list:
        current_file_cnt += 1
        accumulate_size += size
        current_time = time.time()
        
        cost_secends = int(current_time - start_time)
        cost_time_h = cost_secends // 60 // 60
        cost_time_m = cost_secends // 60 % 60
        cost_time_s = cost_secends % 60
        
        print("-- %02d:%02d:%02d -- cnt:%d%%, %d/%d -- size:%d%%, %dG/%dG-- %d -- %s --"
              %(cost_time_h, cost_time_m, cost_time_s,
                int((current_file_cnt*100)/file_cnt),
                current_file_cnt, file_cnt,
                int((accumulate_size*100)/total_size),
                accumulate_size / 1024 / 1024 / 1024, total_size_g,
                size, filename))
        if checksum_enable == True:
            if size < 20 * 1024 * 1024 * 1024:
                sha256sum = hashlib.sha256(open(full_filename,'rb').read()).hexdigest()
            else:
                sha256sum = '[whose size bigger than 20G]'
            line = "%s,%d,%d,%s"%(filename,size,mtime,sha256sum)
        else:
            line = "%s,%d,%d"%(filename,size,mtime)
        output_file_lines.append(line + '\n')
        if save_to_file == True:
            f.write(line + '\n')
        #print(line)

    end_time = time.time()
    cost_secends = int(end_time - start_time)
    cost_time_h = cost_secends // 60 // 60
    cost_time_m = cost_secends // 60 % 60
    cost_time_s = cost_secends % 60
    line = "-- time cost: %ds -- %d:%d:%d --"%(cost_secends, cost_time_h, cost_time_m, cost_time_s)
    output_file_lines.append(line + '\n')
    if save_to_file == True:
        f.write(line + '\n')
    print(line) 
    line = "-- file count: %d(%d)"%(file_cnt, len(file_list))
    output_file_lines.append(line + '\n')
    if save_to_file == True:
        f.write(line + '\n')
    print(line)
    line = "-- total size: %d"%(total_size)
    output_file_lines.append(line + '\n')
    if save_to_file == True:
        f.write(line + '\n')
    print(line)
    line = "-- %s --"%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    output_file_lines.append(line + '\n')
    if save_to_file == True:
        f.write(line + '\n')
    print(line)

    if save_to_file == True:
        print("-- output_file_name: %s, output_lines: %d --"%(output_file_name, len(output_file_lines)))
        f.close()

if __name__ == '__main__':
    scan_folder(r"F:\\", save_to_file=True)
    scan_folder(r"F:\\", checksum_enable=True, save_to_file=True)
    #scan_folder(r"E:\\", save_to_file=True)
    #scan_folder(r"E:\\", checksum_enable=True, save_to_file=True)
    #scan_folder(r"D:\\", save_to_file=True)
    #scan_folder(r"D:\\", checksum_enable=True, save_to_file=True)

    scan_folder(r"H:\\win7DriveF3T", save_to_file=True)
    scan_folder(r"H:\\win7DriveF3T", checksum_enable=True, save_to_file=True)
