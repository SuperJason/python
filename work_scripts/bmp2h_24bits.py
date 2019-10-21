#!/usr/bin/env python3
"""
    Simple shapes in cartesian coordinates
"""

from PIL import Image
import numpy as np
import sys

def h_data_generate(h_file, img):
    width, height = img.size
    raw_pixels = list(img.getdata())
    col = 0
    line_content_str = ''
    for i in range(width*height):
        line_content_str += '{0x%02x, 0x%02x, 0x%02x},'%(raw_pixels[i][0], raw_pixels[i][1], raw_pixels[i][2])
        col += 1
        if col == 4:
            col = 0
            h_file.write('    ' + line_content_str + '\n')
            line_content_str = ''
    if col != 0:
        h_file.write('    ' + line_content_str[:-2] + '\n')


if __name__ == '__main__':

    if len(sys.argv) > 1:
        bmpfile = sys.argv[1]
    else:
        bmpfile = 'tmp.bmp'

    h_filename = 'display_content.h'
    h_file = open(h_filename, 'w')

    bmp_img = Image.open(bmpfile)

    h_data_generate(h_file, bmp_img)

    h_file.close()
