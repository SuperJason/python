# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
import time

def run_cmd(cmd):
    print(' '*4 + ' '.join(cmd))
    ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, check=True)
    #ret = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    #print(ret)
    return ret.stdout

def main():
    server_with_usrname = 'jason@192.168.0.107'
    root_path = '/volume1/video/8_影视剧/雍正王朝/'
    cmd = []
    cmd.append(' '.join(['ssh', server_with_usrname, '\'find', root_path, '-name', '*CHDTV.ts\'']))
    ret = run_cmd(cmd)
    #print(ret)
    file_list = ret.decode().splitlines()
    print(f'Find {len(file_list)} *CHDTV.ts files')
    for file in file_list:
        file_name = file.replace('[', '\\\\[').replace(']', '\\\\]')
        print(f'{         file=}')
        out_file_name = re.match('.*\[lightyear.club\](Yong.Zheng.Wang.Chao.1997.E\d\d).HDTV.1080p.H264.AAC-CHDTV.ts', file).group(1) + '.1080p.aac.mp4'
        print(f'{out_file_name=}')
        # Check if out file is exist
        cmd_list = ['ssh']
        cmd_list.append(server_with_usrname)
        cmd_list.append(f'[ -f {root_path}/{out_file_name} ] && echo \"yes\" || echo \"no\"')
        cmd = []
        cmd.append(' '.join(cmd_list))
        ret = run_cmd(cmd)
        if ret.decode().startswith("yes"):
            print(f'{root_path}{out_file_name} is exist, ignore converting actions.')
            continue
        # Download file
        cmd = []
        cmd.append(''.join(['scp ', server_with_usrname, ':', file_name, ' .']))
        ret = run_cmd(cmd)
        # Convert file
        cmd_list = ['ffmpeg']
        cmd_list.append(f'-nostdin')
        cmd_list.append(f'-i {os.path.basename(file)}')
        cmd_list.append(f'-map 0:0')
        cmd_list.append(f'-map 0:1')
        cmd_list.append(f'-c:v libx264')
        cmd_list.append(f'-pix_fmt yuv420p')
        cmd_list.append(f'-c:a aac')
        cmd_list.append(f'-vf scale=1920:1080')
        cmd_list.append(f'-async 1')
        cmd_list.append(f'-b:a 192k')
        cmd_list.append(f'{out_file_name}')
        cmd = []
        cmd.append(' '.join(cmd_list))
        ret = run_cmd(cmd)
        # upload file
        cmd = []
        cmd.append(''.join(['scp ', f'{out_file_name} ', server_with_usrname, ':', root_path]))
        ret = run_cmd(cmd)
        # remove downloaded file and output file
        cmd = []
        cmd.append(''.join(['rm ', f'{out_file_name} ', f'{os.path.basename(file)}']))
        ret = run_cmd(cmd)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print('--------------------')

if __name__ == '__main__':
    main()
