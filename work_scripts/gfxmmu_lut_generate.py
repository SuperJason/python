#!/usr/bin/env python3
"""
    Simple shapes in cartesian coordinates
"""

from PIL import Image
import numpy as np
import sys

def circle_estimate(x, y, u):
    r = 1
    if (x**2 + y**2) < r:
        return True
    else:
        return False


#    +    length(y)   +
# +--+----------------+
#    |                |
# w  |                |
# i  |                |
# d  |                |
# t  |                |
# h  |                |
#(x) |                |
#    |                |
# +--+----------------+
def general_shapes(width=400,length=400,background=[255,255,255],frontground=[0,0,255],func=circle_estimate):

    xy=np.ones((width, length, 3))
    xy[:,:,:]=background

    #x axis
    xy[width//2,:,:]=frontground
    #y axis
    xy[:,length//2,:]=frontground

    axis_unit=float(min(width, length))
    for x in range(width):
        for y in range(length):
            axis_x=float(x-width/2)/(axis_unit/2)
            axis_y=float(y-length/2)/(axis_unit/2)
            if func(axis_x, axis_y, axis_unit):
                xy[x,y,:]=frontground

    blocks=np.ones((width,length*3//16))*True
    visable_blocks_info=np.ones((width,3), np.uint32)
    visable_blocks_cnt = 0
    for x in range(width):
        last_v = v = False
        visable_blocks_info[x][1] = len(blocks[x])-1 
        for index in range(len(blocks[x])):
            v = False
            for y in range((index*16//3), ((index+1)*16+2)//3):
                if xy[x,y,0] == frontground[0] and xy[x,y,1] == frontground[1] and xy[x,y,2] == frontground[2]:
                    v = True
            if v:
                blocks[x][index] = True
                visable_blocks_cnt += 1
                for y in range((index*16//3), ((index+1)*16+2)//3):
                    xy[x,y,0] = 255
            else:
                blocks[x][index] = False

            if last_v == False and v == True:
                visable_blocks_info[x][0] = index
                last_v = True
                
            if last_v == True and v == False:
                visable_blocks_info[x][1] = index - 1
                last_v = False

        visable_blocks_info[x][2] = visable_blocks_info[x][1] - visable_blocks_info[x][0] + 1

    Image.fromarray(np.uint8(xy)).show()
 
    print('total size: %d'%(width*length*3))
    print('total blocks: %d'%(width*(length*3//16)))
    print('visable blocks: %d'%(visable_blocks_cnt))
    print('reserved present: %.4f%%'%(((visable_blocks_cnt*16)/(width*length*3))*100))
#    for i in range(len(visable_blocks_info[:,2])):
#        print('[% 4d] first: % 3d, last: % 3d, count: % 3d'%(i, visable_blocks_info[i][0], visable_blocks_info[i][1], visable_blocks_info[i][2]))

    return visable_blocks_info

if __name__ == '__main__':

    if len(sys.argv) > 1:
        h_filename = sys.argv[1]
    else:
        h_filename = 'gfxmmu_lut_24bpp.h'

    width = length = 400
    info = general_shapes(width,length,[0,0,0],[0,0xff,0xff],circle_estimate)

    h_file = open(h_filename, 'w')

    h_file.write('/* GFXMMU look-up table for RGB888 */\n')
    h_file.write('#define GFXMMU_LUT_SIZE %d\n'%(width))
    h_file.write('\nconst uint32_t gfxmmu_lut_config_rgb888[2*GFXMMU_LUT_SIZE] = {\n')
    blocks_count = 0
    for i in range(len(info[:,2])):
#        print('[% 4d] first: % 3d, last: % 3d, count: % 3d'%(i, info[i][0], info[i][1], info[i][2]))
        lut_l = (info[i][0]<<8) | (info[i][1]<<16) | 0x01
        lut_h = (blocks_count-info[i][0]) * 16
#        print('blocks_count: %d, lut_l: 0x%x, lut_h: 0x%x'%(blocks_count, lut_l, lut_h))
        if lut_h < 0:
            lut_h = 0x3ffff0 + lut_h
#            print('lut_h < 0, lut_h: 0x%x'%(lut_h))
#        print('    0x%08x, // GFXMMU_LUT%dL'%(lut_l, i))
        h_file.write('    0x%08x, // GFXMMU_LUT%dL\n'%(lut_l, i))
#        print('    0x%08x, // GFXMMU_LUT%dH'%(lut_h, i))
        h_file.write('    0x%08x, // GFXMMU_LUT%dH\n'%(lut_h, i))
        blocks_count += info[i][2]

    print('blocks_count: %d'%(blocks_count))
    h_file.write('};\n')
