#!/usr/bin/env python3
"""
    Convert E3 display asset png pictures to c header file.
"""

from PIL import Image
import numpy as np
import sys
import os

def pic_2_c_header(img_file):
    width, height = img_file.size
    raw_pixels = list(img_file.getdata())
    #print(len(raw_pixels))
    pixels = [raw_pixels[i * width:(i + 1) * width] for i in range(height)]
    #print(len(pixels))

    c_array_content = []
    line_content = ''
    array_content_col = 0
    for i in range(width * height):
        r = int(raw_pixels[i][0] / 0xff * 0x1f) & 0x1f
        g = int(raw_pixels[i][1] / 0xff * 0x3f) & 0x3f
        b = int(raw_pixels[i][2] / 0xff * 0x1f) & 0x1f
        # 16bits, lsb
        line_content += ' 0x%04x,'%((r << 3) | (g >> 3) | ((g << 13) & 0xffff) | (b << 8))
        array_content_col += 1
        if array_content_col == 16:
            array_content_col = 0
            c_array_content.append('   ' + line_content + '\n')
            line_content = ''
    if array_content_col != 0:
        c_array_content.append('    ' + line_content[:-2] + '\n')

    return c_array_content

def get_c_array_name(file_name):
    c_array_name = 'asset_'

    #print('len(file_name): %d'%(len(file_name)))
    i = 0
    while (i < len(file_name) and i < 256):
        # is alphabet
        if 'a' <= file_name[i] <= 'z' or 'A' <= file_name[i] <= 'Z':
            c_array_name += file_name[i]
        # is number or '_'
        elif '0' <= file_name[i] <= '9' or file_name[i] == '_':
            c_array_name += file_name[i]
        # is '.' or ' ' using '_' to replace
        elif file_name[i] == '.' or file_name[i] == ' ':
            c_array_name += '_'
        # special letter using ascii number to replace, include Chinese or other language
        else:
            #print('file_name[%d]: %s(0x%x)'%(i, file_name[i], ord(file_name[i])))
            c_array_name += '_0x%x'%(ord(file_name[i]))

        #print('%d[%c] c_array_name: '%(i, file_name[i]) + c_array_name)
        i += 1

    return c_array_name

if __name__ == '__main__':

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = './'

    file_list = os.listdir(file_path)
    #print(file_list)
    png_file_list = []
    for name in file_list:
        if os.path.splitext(name)[-1] == '.png' or os.path.splitext(name)[-1] == '.jpg':
            png_file_list.append(name)
    png_file_list.sort()
    print(png_file_list)

    h_filename = 'display_assets.h'
    h_file = open(h_filename, 'w')

    h_file.write('/*\n')
    h_file.write(' * Total %d png files\n'%(len(png_file_list)))
    h_file.write(' *\n')
    h_file.write(' * ' + str(png_file_list) + '\n')
    h_file.write(' *\n')
    h_file.write('*/\n\n')
    h_file.write('#ifndef %s_H\n'%(h_filename[:-2].upper()))
    h_file.write('#define %s_H\n'%(h_filename[:-2].upper()))

    total_pixels = 0
    index = 0

    total_asset_info = []

    for pic_file_name in png_file_list:
        img_file = Image.open(pic_file_name)
        width, height = img_file.size
        info_print_string = '[%d/%d] file: '%(index, len(png_file_list))
        info_print_string += pic_file_name
        info_print_string += ' (%d x %d)'%(width, height)
        #info_print_string += ', format: %s, mode: %s'%(img_file.format, img_file.mode)
        print(info_print_string)
        index += 1
        #print('info  : ' + str(img_file.info))
        #img_file.show()
        total_pixels += width * height

        c_array_content = pic_2_c_header(img_file)
        #print(c_array_content)

        c_array_name = get_c_array_name(pic_file_name)
        #print(' ' * 16 + 'c_array_name: ' + c_array_name)

        c_array_content.insert(0, 'const uint16_t ' + c_array_name + '[] = {\n')
        c_array_content.append('};\n')
        c_array_content.insert(0, '\n/* %s (%d x %x)*/\n'%(pic_file_name, width, height))

        h_file.writelines(c_array_content)
        total_asset_info.append((pic_file_name, c_array_name, width, height))

    h_file.write('/* Total size: %d bytes*/\n'%(total_pixels * 2))

    #print(total_asset_info)
    h_file.write('\n')
    h_file.write('typedef struct asset_item {\n')
    h_file.write('    uint8_t *asset;\n')
    h_file.write('    uint16_t width;\n')
    h_file.write('    uint16_t height;\n')
    h_file.write('    uint32_t flag;\n')
    h_file.write('} asset_item_t;\n')
    h_file.write('\n')

    h_file.write('const asset_item_t asset_items[] = {\n')
    index = 0
    for (pic_file_name, c_array_name, width, height) in total_asset_info:
        h_file.write('    { /* [%d] %s */\n'%(index, pic_file_name))
        h_file.write('        .asset = (uint8_t *)%s,\n'%(c_array_name))
        h_file.write('        .width = %d,\n'%(width))
        h_file.write('        .height = %d,\n'%(height))
        h_file.write('        .flag = %d,\n'%(16))
        h_file.write('    },\n')
        index += 1

    h_file.write('};\n')
    h_file.write('#endif /* %s_H */\n'%(h_filename[:-2].upper()))

    h_file.close()

