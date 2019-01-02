#!/usr/bin/env python3
"""
    This scripts is created for orion pa paramater file format convert.
"""

import re
import sys
import os

def format_transfer(lines):
    pattern = r'^Time.*Address\[(0x.{2})\].*Data\[(0x.*)].*$'
    line_num = 0
    param_array = []
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
            param_array.append(out_line)
        else:
            print('No match!!')
        line_num = line_num + 1
    return line_num, param_array

def data_generate(lines, name):
    data_contents = []
    data_struct_unit = []
    data_contents.append('ntp8824_param_t ntp8824_regs_' + name + '[] = {\n')
    data_contents.extend(lines)
    data_contents.append('};\n\n')

    data_struct_unit.append('\t{\n')
    data_struct_unit.append('\t\t.name = "' + name + '",\n')
    data_struct_unit.append('\t\t.data = ntp8824_regs_' + name + ',\n')
    data_struct_unit.append('\t\t.size = sizeof(ntp8824_regs_' + name + ') / sizeof(ntp8824_param_t),\n')
    data_struct_unit.append('\t}, /* 0 */\n')
    return data_contents, data_struct_unit

def h_file_generate(input_file_name='pa_param_logdefault'):
    if not os.path.exists(input_file_name):
        print('input file: ' + input_file_name + ' doesn\'t exist!!')
        exit(1)

    name = re.match(r'.*_([^_]*)', input_file_name).group(1)

    if not name:
        name = 'default'

    output_file_name = name + '.h'

    print('input file: ' + input_file_name)
    print('output file: ' + output_file_name)
    input_file = open(input_file_name, 'rt')
    output_file = open(output_file_name, 'wt')

    lines = input_file.readlines()
    input_file.close()

    line_num, data_lines = format_transfer(lines)
    data_contents, data_struct_unit = data_generate(data_lines, name)

    output_file.writelines(data_contents)
    output_file.writelines(data_struct_unit)

    print('\n ----- ' + str(line_num) + ' lines have been transferred. -----')

    output_file.close()

def append_ntp8824_h_file(input_file_name='pa_param_logdefault', h_file_name='ntp8824.h'):
    if not os.path.exists(input_file_name):
        print('input file: ' + input_file_name + ' doesn\'t exist!!')
        exit(1)

    name = re.match(r'.*_([^_]*)', input_file_name).group(1)

    if not name:
        name = 'default'

    print('input file: ' + input_file_name)
    print('ntp8824.h file: ' + h_file_name)
    input_file = open(input_file_name, 'rt')

    lines = input_file.readlines()
    input_file.close()

    line_num, data_lines = format_transfer(lines)
    data_contents, data_struct_unit = data_generate(data_lines, name)
    print(' ----- ' + str(line_num) + ' lines have been transferred. -----')

    h_file = open(h_file_name, 'rt')
    h_lines = h_file.readlines() 
    h_file.close()

    for line in h_lines:
        match = re.match(r'ntp8824_param_t +ntp8824_regs_' + name, line)
        if match != None:
            print('\n ----- ntp8824_regs_%s exists in file %s!!! -----'%(name, h_file_name))
            exit(1)

    # insert data contents and struct unit and update default definition
    contents_line_index = 0
    struct_unit_line_index = 0
    define_default_line_index = 0
    cnt = 0
    for line in h_lines:
        match = re.match(r'^ntp8824_init_data_t +ntp8824_init_data', line)
        if match != None:
            contents_line_index = cnt
        match = re.match(r'^};', line)
        if match != None and contents_line_index:
            struct_unit_line_index = cnt
        match = re.match(r'#define NTP8824_PARAM_DEFAULT', line)
        if match != None:
            define_default_line_index = cnt
        cnt = cnt + 1;

    print("cnt: %d, indexs contents: %d, unit: %d, default: %d"%(cnt, contents_line_index, struct_unit_line_index, define_default_line_index))
    search = re.search(r'\/\* +([0-9]) +\*\/', h_lines[struct_unit_line_index - 1])
    unit_index = int(search.group(1))
    unit_index = unit_index + 1

    new_data_struct_unit = data_struct_unit[:-1]
    new_data_struct_unit = new_data_struct_unit + [data_struct_unit[-1][:-5] + str(unit_index) + data_struct_unit[-1][-4:]]

    define_defaut_line = h_lines[define_default_line_index]
    new_define_defaut_line = [ define_defaut_line[:-2] + str(unit_index) + define_defaut_line[-1:] ]

    new_h_lines = h_lines[:contents_line_index]
    # insert new data struct
    new_h_lines = new_h_lines + data_contents
    new_h_lines = new_h_lines + h_lines[contents_line_index:struct_unit_line_index]
    # append a struct 'ntp8824_init_data''s unit
    new_h_lines = new_h_lines + new_data_struct_unit
    new_h_lines = new_h_lines + h_lines[struct_unit_line_index:define_default_line_index]
    # update NTP8824_PARAM_DEFAULT
    new_h_lines = new_h_lines + new_define_defaut_line 
    new_h_lines = new_h_lines + h_lines[define_default_line_index + 1:]

    #for line in new_h_lines:
    #    print("%s"%line[:-1])
    h_file = open(h_file_name, 'w+')
    h_file.writelines(new_h_lines)
    h_file.close()

    print('\n ----------------------------------------------------------------------------------------------------')
    print(' PA. paramater ' + name + ' has been added to header file: ' + h_file_name + '.')
    print(' ----------------------------------------------------------------------------------------------------\n')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_file_name = sys.argv[1]
    else:
        input_file_name='pa_param_logdefault'

    #h_file_generate(input_file_name)

    ntp8824_h_file_name='/home/mobvoi/work/codes/orion/kernel-4.4/sound/soc/codecs/ntp8824.h'
    append_ntp8824_h_file(input_file_name, ntp8824_h_file_name)
