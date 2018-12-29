#!/usr/bin/env python3
# This scripts is created for orion pa paramater file format convert. 

import re
import sys
import os

if len(sys.argv) > 1: 
    input_file_name = sys.argv[1]
else:
    #input_file_name = 'pa_param_12171401'
    #input_file_name = 'pa_param_log1218'
    input_file_name = 'pa_param_logdefault'

if not os.path.exists(input_file_name):
    print('input file: ' + input_file_name + ' doesn\'t exist!!')
    exit(1)

name = re.match(r'.*_([^_]*)', input_file_name).group(1)

if not name:
    name = 'default'

output_file_name = name + '.h'

print('input file: ' + input_file_name)
print('output file: ' + output_file_name)
pattern = r'^Time.*Address\[(0x.{2})\].*Data\[(0x.*)].*$'
input_file = open(input_file_name, 'rt')
output_file = open(output_file_name, 'wt')

output_file.write('ntp8824_param_t ntp8824_regs_' + name + '[] = {\n')

lines = input_file.readlines()
line_num = 0
for line in lines:
    match = re.match(pattern, line)
    addr = match.group(1)
    val = match.group(2)
    if match:
        if len(val) < 5:
            val_type = '0x01'
        else:
            val_type = '0x04'
        out_line = '\t{ .addr = ' + addr + ', .type = ' + val_type + ', .val = ' + val + ' },\n'
        output_file.write(out_line)
    else:
        print('No match!!')
    line_num = line_num + 1

output_file.write('};\n\n')
output_file.write('\t{\n')
output_file.write('\t\t.name = "' + name + '",\n')
output_file.write('\t\t.data = ntp8824_regs_' + name + ',\n')
output_file.write('\t\t.size = sizeof(ntp8824_regs_' + name + ') / sizeof(ntp8824_param_t),\n')
output_file.write('\t},\n')

print('\n ----- ' + str(line_num) + ' lines have been transferred. -----')

input_file.close()
output_file.close()
