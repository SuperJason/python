#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import subprocess

container_name_list = ['grok-buzz', 'grok-wear', 'historian', 'bsp-nginx']

cmd = "docker container list -a"
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
#print('-------------------- stdout --------------------')
#print(stdout)
#print('-------------------- stderr --------------------')
#print(stderr)
result = str(stdout)
container_lines = result.split('\\n')

need_starting_containters_id = []
for container_line in container_lines:
    #print('-------------------- container --------------------')
    #print(container_line)
    prop = re.split(' {2,}', container_line)
    if len(prop) >= 6 and prop[4][0:6] == 'Exited':
        #print('id: ' + prop[0])
        #print('status: ' + prop[4])
        #print('name: ' + prop[5])
        name = prop[5]
        if name in container_name_list:
            need_starting_containters_id.append(prop[0])

#print('-------------------- need started containers --------------------')
#print(need_starting_containters_id)

if len(need_starting_containters_id) > 0:
    cmd = need_starting_containters_id
    cmd.insert(0, 'docker start')
    cmd = ' '.join(cmd)

    print('-------------------- cmd --------------------')
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    #print('-------------------- stdout --------------------')
    #print(stdout)
    #print('-------------------- stderr --------------------')
    #print(stderr)
    if len(stdout) > 0:
        result = str(stdout)
        result = ' '.join(result.split('\\n'))
        print('-------------------- stdout --------------------')
        print(result[2:-1])
    if len(stderr) > 0:
        result = str(stderr)
        result = ' '.join(result.split('\\n'))
        print('-------------------- stderr --------------------')
        print(result[2:-1])
else:
    print('\n### No container is needed to start! ###\n')
