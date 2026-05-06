# -*- coding: utf-8 -*-

import argparse
import re

def main(filename, selected_keys):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            line_key_list = re.split('\t+', line)
            #print(line_key_list)
            #print(f'{len(line_key_list) = }')
            data.append(line_key_list)
    max_name_len = max([len(d[0]) for d in data])
    #print(f'{max_name_len=}')
    if not selected_keys:
        selected_keys = data[0][1:]
    for d in data:
        out_str = d[0] + ' ' * (max_name_len + 1 - len(d[0]))
        for entry in enumerate(data[0]):
            entry_index = entry[0]
            entry_name = entry[1]
            if entry_name in selected_keys:
                out_str += d[entry_index] + ' '* (len(entry_name) + 1 - len(d[entry_index]))
        print(out_str)
    print(list(enumerate(data[0])))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='输入文件的路径')
    parser.add_argument('-e', '--entry', help='选择列名, None为全选')
    args = parser.parse_args()
    if args.input:
        filename = args.input
        print(f'输入文件：{filename}')
    else:
        filename = 'wakelocks.txt'
        print(f'默认输入文件：{filename}')

    if args.entry:
        entry_name = args.entry
        if entry_name == 'None':
            entry_name = None
            print(f'输出所有列名')
        else:
            print(f'输出列名：{entry_name}')
    else:
        entry_name = 'active_since'
        print(f'默认输出列名：{entry_name}')
    main(filename, entry_name)
