# -*- coding: utf-8 -*-

import os
import subprocess

def run_cmd(cmd):
    print(' '*4 + ' '.join(cmd))
    subprocess.check_output(cmd)

def main():
    server_with_usrname = 'fuzhongxin@10.30.0.52'
    root_path = '/home/workspace_sda/fuzhongxin/p5pro/QISI13'
    audio_kernel_outpath = 'out/target/product/bengal_515tiny/obj/DLKM_OBJ/vendor/qcom/opensource/audio-kernel'
    cmd = ['scp']
    cmd.append(''.join([server_with_usrname, ':', root_path, '/', audio_kernel_outpath, '/', 'modules.order']))
    cmd.append('.')
    print('==== Download modules.order ====')
    run_cmd(cmd)

    print('==== Parse modules.order ====')
    kos = {}
    msm_kernel_outpath = 'out/target/product/bengal_515tiny/obj/DLKM_OBJ/kernel_platform/msm-kernel'
    with open('modules.order', 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            file_name = line.split('/')[-1]
            path = ''.join([root_path, '/', msm_kernel_outpath, '/', line])
            kos[file_name] = path
    print('==== Download .ko ====')
    for key in kos:
        run_cmd(['scp', ''.join([server_with_usrname, ':', kos[key]]), key])
    print('==== Push .ko to vendor_dlkm partition ====')
    run_cmd(['adb', 'wait-for-device'])
    run_cmd(['adb', 'root'])
    run_cmd(['adb', 'remount'])
    for key in kos:
        run_cmd(['adb', 'push', key, '/vendor_dlkm/lib/modules'])
    print('==== Clean .ko and modules.order ====')
    os.remove('modules.order')
    for key in kos:
        os.remove(key)

if __name__ == '__main__':
    main()
