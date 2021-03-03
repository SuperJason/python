#!/usr/bin/env python3
"""
    Convert E3 display asset png pictures to c header file.
"""

from PIL import Image
import numpy as np
import sys
import time

def stack_png_on_bg(bg, fg, x, y):
    bg_w, bg_h = bg.size
    fg_w, fg_h = fg.size
    #bg.paste(fg, (x, y, x + fg_w, y + fg_h))
    #bg_raw_pixels = list(bg.getdata())
    #fg_raw_pixels = list(fg.getdata())
    bg_pixels = np.array(bg)
    fg_pixels = np.array(fg)
    
    white_zone = np.array(Image.new('RGB', fg.size, (255,255,255)))
    
    mask_zone = white_zone + fg_pixels
    #Image.fromarray(mask_zone).show()

    mask_zone_r = (mask_zone[:,:,0] < 200) * 255
    mask_zone_g = (mask_zone[:,:,1] < 200) * 255
    mask_zone_b = (mask_zone[:,:,2] < 200) * 255

    mask_zone[:,:,0] = mask_zone_r | mask_zone_g | mask_zone_b
    mask_zone[:,:,1] = mask_zone_r | mask_zone_g | mask_zone_b
    mask_zone[:,:,2] = mask_zone_r | mask_zone_g | mask_zone_b

    mask_zone = ~mask_zone
    #Image.fromarray(mask_zone).show()
    bg_pixels[y:y + fg_h, x:x + fg_w] = (bg_pixels[y:y + fg_h, x:x + fg_w] & mask_zone) + fg_pixels
    final_img = Image.fromarray(bg_pixels)
    
    #final_img.show()

    return final_img


if __name__ == '__main__':

    if len(sys.argv) > 1:
        background_file_name = sys.argv[1]
    else:
        background_file_name = 'background.jpg'

    background_img = Image.open(background_file_name).convert('RGB')
    #background_img.show()
    x, y = 200, 200
    bg_img = background_img.crop((x, y, x + 800, y + 600))
    #bg_img.show()

    fg_list = [ 'big_0.png', 'big_1.png', 'big_2.png', 'big_3.png', 'big_4.png',
            'big_5.png', 'big_6.png', 'big_7.png', 'big_8.png', 'big_9.png' ]
    for fg_file_name in fg_list:
        frontground_img = Image.open(fg_file_name).convert('RGB')
        #frontground_img.show()
        x = bg_img.size[0] // 2 - frontground_img.size[0] // 2
        y = bg_img.size[1] // 2 - frontground_img.size[1] // 2
        final_img = stack_png_on_bg(bg_img, frontground_img, x, y)
        final_img.show()
        time.sleep(1)
        final_img.close()

        #sys.exit(1)
